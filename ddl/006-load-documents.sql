
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--

create extension if not exists plpython3u;

create or replace function path_join(variadic path_elems text[]) returns text as
$$
    import os
    return os.path.join(*path_elems)
$$ language plpython3u;


create or replace function recursive_ls_dir(directory text, file_exts text[] default array['xml']) returns setof text as
$$
    with recursive curr_dir as (
        select fn,directory as directory,st.isdir
        from pg_ls_dir(directory) fn,
        lateral pg_stat_file(directory || fn) st
        union all
        select new_fn,path_join(directory,cd.fn) as directory,st.isdir
        from curr_dir cd,
        lateral pg_ls_dir(path_join(cd.directory,cd.fn)) new_fn,
        lateral pg_stat_file(path_join(cd.directory,cd.fn,new_fn)) st
        where cd.isdir = true
    )
    select path_join(directory,fn)
    from curr_dir
    where isdir is false and fn ~* (select string_agg(u || '$','|') from unnest(file_exts) u);
$$ language sql;


create or replace function load_single_document(
    _document_type_id bigint,
    fn text
) returns boolean
as
$$
declare
_new_rows bigint;
err_obj jsonb;
_error_sqlstate text;
_error_column_name text;
_error_constraint_name text;
_error_pg_datatype_name text;
_error_message_text text;
_error_table_name text;
_error_schema_name text;
_error_pg_exception_detail text;
_error_pg_exception_hint text;
_error_pg_exception_context text;
begin
    begin
        insert into public_api.document (document_type_id,raw_text,file_name) values (_document_type_id,pg_read_file(fn),fn) on conflict (_hash) do nothing;
        get diagnostics _new_rows = ROW_COUNT;
        if _new_rows > 0 then
            return true;
        end if;
        return false;
    exception when unique_violation then
        raise warning 'unique violation';
        select jsonb_build_object(
            'SQLERRM',SQLERRM,
            'SQLSTATE',SQLSTATE
        ) into err_obj;
        raise debug '%',jsonb_pretty(err_obj);
        return false;
    when data_exception then
        raise warning 'invalid document';
        select jsonb_build_object(
            'SQLERRM',SQLERRM,
            'SQLSTATE',SQLSTATE
        ) into err_obj;

        get stacked diagnostics
            _error_sqlstate=RETURNED_SQLSTATE,
            _error_column_name=COLUMN_NAME,
            _error_constraint_name=CONSTRAINT_NAME,
            _error_pg_datatype_name=PG_DATATYPE_NAME,
            _error_message_text=MESSAGE_TEXT,
            _error_table_name=TABLE_NAME,
            _error_schema_name=SCHEMA_NAME,
            _error_pg_exception_detail=PG_EXCEPTION_DETAIL,
            _error_pg_exception_hint=PG_EXCEPTION_HINT,
            _error_pg_exception_context=PG_EXCEPTION_CONTEXT;

        select jsonb_build_object(
            '_error_sqlstate',_error_sqlstate,
            '_error_column_name',_error_column_name,
            '_error_constraint_name',_error_constraint_name,
            '_error_pg_datatype_name',_error_pg_datatype_name,
            '_error_message_text',_error_message_text,
            '_error_table_name',_error_table_name,
            '_error_schema_name',_error_schema_name,
            '_error_pg_exception_detail',_error_pg_exception_detail,
            '_error_pg_exception_hint',_error_pg_exception_hint,
            '_error_pg_exception_context',_error_pg_exception_context
        ) || err_obj into err_obj;
        raise debug '%',jsonb_pretty(err_obj);
        return false;
    end;
end;
$$ language plpgsql;

create or replace function load_all_documents(
    _document_type_id bigint,
    directory text,
    progress_interval bigint default 10,
    max_docs bigint default null
) returns void as
$$
declare
fn text;
new_row boolean;
total_rows bigint := 0;
last_total bigint := 0;
start_time timestamp := clock_timestamp();
elapsed numeric;
begin
    for fn in (select _fn from recursive_ls_dir(directory) _fn) loop
        select load_single_document(_document_type_id,fn) into new_row;
        select total_rows + ((new_row)::int)::bigint into total_rows;
        select extract(epoch from (clock_timestamp() - start_time)) into elapsed;
        if elapsed > progress_interval::numeric then
            raise notice 'loaded % rows in % seconds',(total_rows - last_total),elapsed;
            select clock_timestamp() into start_time;
            select total_rows into last_total;
        end if;
        if (total_rows >= max_docs) then
            raise notice 'loaded % docs and stopping',total_rows;
            exit;
        end if;
        -- raise notice '% rows loaded',_new_rows;
    end loop;
end;
$$ language plpgsql;