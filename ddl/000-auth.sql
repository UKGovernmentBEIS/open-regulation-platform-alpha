
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--

create role orp_postgrest_authenticator;
create role orp_postgrest_anon;
create role orp_postgrest_web;

alter role orp_postgrest_authenticator with password :'AUTH_PASS';
alter role orp_postgrest_authenticator with login;

grant orp_postgrest_anon to orp_postgrest_authenticator,orp_postgrest_web;
grant orp_postgrest_web to orp_postgrest_authenticator;

create schema if not exists public_api;

comment on schema public_api is 'ORP Alpha Public API';

grant usage on schema public_api to orp_postgrest_anon;
grant usage on schema public_api to orp_postgrest_web;

alter database :POSTGRES_DB set log_min_messages to notice;


create table jwt_secret (
    id boolean primary key default true,
    secret text not null,
    constraint one_row check (id)
);

insert into jwt_secret (secret) values ('2db2fc88ff5b094cf0c4a5b6815ce19a');

grant select on jwt_secret to orp_postgrest_anon;

create table users (
    id bigint generated always as identity primary key,
    password text not null,
    first_name text not null,
    last_name text not null,
    email text not null unique check (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'),
    active boolean default true,
    created_on timestamp not null default now()
);

alter table users enable row level security;
grant select on table users to orp_postgrest_web;

create policy users_s_web ON users for select to orp_postgrest_web using (
    (id=current_setting('request.jwt.claim.user_id', true)::bigint)
);

create view public_api.user_info with (security_barrier) as
select id,
    first_name,
    last_name,
    email,
    created_on
from users;

alter view public_api.user_info owner to orp_postgrest_web;
grant select on public_api.user_info to orp_postgrest_web;


create extension pgcrypto;

create or replace function encrypt_pass() returns trigger as
$$
begin

    if not ((char_length(new.password) > 7) and new.password ~* '[!@#$%^&*]' and new.password ~* '[0-9]') then
        raise exception using message = 'password requirements not met';
    end if;

    if TG_OP = 'INSERT' or new.password <> old.password then
        select crypt(new.password,gen_salt('bf')) into new.password;
    end if;
    return new;
end;
$$ language plpgsql;

grant execute on function gen_salt(text) to orp_postgrest_anon;


create trigger user_password_encrypt before insert or update on users
for each row
execute procedure encrypt_pass();

create table login_attempt (
    id bigint generated always as identity primary key,
    user_id bigint,
    succeeded boolean not null,
    message text,
    created_on timestamp not null default now(),
    foreign key (user_id) references users(id) on update cascade on delete cascade
);

create table role (
    id bigint generated always as identity primary key,
    name text not null unique,
    created_on timestamp not null default now()

);

create table user_role (
    user_id bigint not null,
    role_id bigint not null,
    foreign key (user_id) references users(id) on update cascade on delete cascade,
    foreign key (role_id) references role(id) on update cascade on delete cascade,
    constraint user_role_unique unique(user_id, role_id)
);

create extension pgjwt;

create or replace function public_api.login(email text, password text) returns json as
$$
declare
_user_id bigint;
_authenticated boolean;
jwt_object json;
signed_jwt text;
begin
    select id,
        crypt(login.password,u.password) = u.password
    into _user_id,_authenticated
    from users u
    where u.email = login.email
    and u.active;

    if _user_id is null then
        insert into login_attempt (succeeded,message) values (false,format('failed login for user %s',login.email));
        perform set_config('response.status', '403', true);
        return json_build_object(
            'message','login failed'
        );
    end if;

    if _authenticated is false or _authenticated is null then
        insert into login_attempt (user_id,succeeded,message) values (_user_id,false,format('failed login for user %s',login.email));
        perform set_config('response.status', '403', true);
        return json_build_object(
            'message','login failed'
        );
    end if;

    if _user_id is not null and _authenticated is true then
        insert into login_attempt (user_id,succeeded) values (_user_id,true);

        select json_build_object(
            'role','orp_postgrest_web',
            'app_roles',(select array_agg(r.name) from user_role ur inner join role r on ur.role_id = r.id where ur.user_id = _user_id),
            'user_id',_user_id,
            'exp',(select extract(epoch from now())::integer + 60*60)
        ) into jwt_object;

        raise notice '%',jwt_object;

        select sign(jwt_object,(select secret from jwt_secret)) into signed_jwt;

        raise notice '%',signed_jwt;

        return json_build_object(
            'signed_jwt',signed_jwt
        );
    end if;

    raise exception using message = 'unknown login error';
end;
$$ language plpgsql security definer;

create table role_actions (
    id bigint not null generated always as identity primary key,
    action_name text not null,
    role_id bigint not null,
    foreign key (role_id) references role(id) on update cascade on delete cascade,
    constraint unique_role_action unique(action_name,role_id)
);

grant select on role_actions to orp_postgrest_web;

create or replace function user_has_role_for_action(action_name text) returns boolean as
$$
    select exists(
        select 1
        from role_actions
        where action_name = user_has_role_for_action.action_name
        and role_id in (
            select role_id
            from user_role
            where user_id = current_setting('request.jwt.claim.user_id')::bigint
        )
    );
$$ language sql;

grant execute on function user_has_role_for_action(text) to orp_postgrest_web;

-- grant insert on login_attempt to orp_postgrest_anon;
-- grant execute on function public_api.login(email text, password text) to orp_postgrest_anon;
-- grant select on table users to orp_postgrest_anon;
grant select on table role to orp_postgrest_web;
grant select on table user_role to orp_postgrest_web;



