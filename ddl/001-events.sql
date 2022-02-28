--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--


create table if not exists public_api.event_type (
    id bigint generated by default as identity primary key,
    can_async boolean default true,
    event_name text not null unique,
    event_keys text[] not null,
    created_on timestamp not null default now()
);

grant select on public_api.event_type to orp_postgrest_web;

create or replace function register_event_type(
    _event_name text,
    _event_keys text[]
) returns void as
$$
begin
    insert into public_api.event_type (event_name,event_keys) values (_event_name,_event_keys) on conflict (event_name) do nothing;
end;
$$ language plpgsql;


create table if not exists public_api.event (
    id bigint generated by default as identity primary key,
    event_type_id bigint not null,
    event_parameters jsonb not null,
    created_on timestamp not null default now(),
    foreign key (event_type_id) references public_api.event_type(id) on delete cascade on update cascade
);

do $$
begin
    create type event_filter as (
        event_key text,
        event_filter text
    );
    exception when duplicate_object then null;
end $$;

create table if not exists public_api.event_subscription (
    id bigint generated by default as identity primary key,
    event_type_id bigint not null,
    deliver_async boolean default false,
    event_filters event_filter[] not null,
    user_id bigint default current_setting('request.jwt.claim.user_id',true)::bigint,
    created_on timestamp not null default now(),
    foreign key (user_id) references users(id) on update cascade on delete cascade,
    foreign key (event_type_id) references public_api.event_type(id) on delete cascade on update cascade,
    constraint unique_es unique(event_type_id,event_filters,user_id)
);

alter table public_api.event_subscription enable row level security;
grant select,insert,update(event_type_id,event_filters,user_id,deliver_async),delete on public_api.event_subscription to orp_postgrest_web;

create policy event_subscription_s ON public_api.event_subscription for select to orp_postgrest_web using (
    (user_id=current_setting('request.jwt.claim.user_id', true)::bigint)
);

create policy event_subscription_user_u ON public_api.event_subscription for update to orp_postgrest_web using (
    user_id=current_setting('request.jwt.claim.user_id', true)::bigint
);

create policy event_subscription_user_d ON public_api.event_subscription for delete to orp_postgrest_web using (
    user_id=current_setting('request.jwt.claim.user_id', true)::bigint
);

create policy event_subscription_user_i ON public_api.event_subscription for insert to orp_postgrest_web with check (
    user_id=current_setting('request.jwt.claim.user_id', true)::bigint
);

create table if not exists public_api.event_stream (
    id bigint generated by default as identity primary key,
    event_subscription_id bigint not null,
    event_description jsonb not null,
    user_id bigint not null,
    created_on timestamp not null default now(),
    foreign key (user_id) references users (id) on update cascade on delete cascade,
    foreign key (event_subscription_id) references public_api.event_subscription (id) on update cascade on delete cascade
);

create index on public_api.event_stream (user_id,created_on);

alter table public_api.event_stream enable row level security;
grant select on public_api.event_stream to orp_postgrest_web;

create policy public_api_s ON public_api.event_stream for select to orp_postgrest_web using (
    (user_id=current_setting('request.jwt.claim.user_id', true)::bigint)
);

create view public_api.event_subscription_stream as
select es.event_description,et.event_name,es.created_on
from public_api.event_stream es
inner join public_api.event_subscription esub on es.event_subscription_id = esub.id
inner join public_api.event_type et on esub.event_type_id = et.id;

alter view public_api.event_subscription_stream owner to orp_postgrest_web;
grant select on public_api.event_subscription_stream to orp_postgrest_web;

comment on view public_api.event_subscription_stream is 'A view that enables polling based retrieval of events created for a particular user';


create or replace function event_after_insert_trigger_f() returns trigger as
$$
declare
et public_api.event_type;
event_sub public_api.event_subscription;
user_email text;
event_desc jsonb;
begin
    select * into et from public_api.event_type where id = new.event_type_id;
    for event_sub in (
        select es.*
        from public_api.event_subscription es
        inner join lateral (
            select bool_and((new.event_parameters->>ef.event_key) ~* ef.event_filter)
            from unnest(es.event_filters) ef
        ) s on bool_and = true
        where es.event_type_id = new.event_type_id
    ) loop
        raise notice 'new event % matches event sub %',row_to_json(new.*),row_to_json(event_sub.*);
        select email into user_email from users where id = event_sub.user_id;
        select jsonb_build_object(
            'action','send_mail',
            'email',user_email,
            'body',new.event_parameters
        ) into event_desc;
        if et.can_async is true and event_sub.deliver_async is true then
            perform pg_notify('main_exchange','q1|' || event_desc::text);
        end if;
        insert into public_api.event_stream (
            event_subscription_id,
            event_description,
            user_id
        )
        values (event_sub.id,event_desc,event_sub.user_id);
    end loop;
    return new;
end;
$$ language plpgsql;

drop trigger if exists after_insert_trigger on public_api.event;
create trigger after_insert_trigger after insert on public_api.event
for each row
execute procedure event_after_insert_trigger_f();

create or replace function publish_event(
    event_type_name text,
    event_parameters jsonb
) returns void as
$$
begin
    insert into public_api.event (event_type_id,event_parameters) values ((select id from public_api.event_type where event_name = publish_event.event_type_name),publish_event.event_parameters);
end;
$$ language plpgsql;


