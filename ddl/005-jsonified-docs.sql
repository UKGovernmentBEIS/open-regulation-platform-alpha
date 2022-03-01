
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--

create or replace function jsonify_xml(xml_string text) returns jsonb as
$$
    from xmljson import badgerfish as bf
    from xml.etree.ElementTree import fromstring

    import json
    try:
        return json.dumps(bf.data(fromstring(xml_string)))
    except Exception as e:
        return '{}'
$$ language plpython3u strict immutable parallel safe cost 9999999999;


create or replace function jsonify_xml2(xml_string text) returns jsonb as
$$
    import xmltodict

    import json
    try:
        return json.dumps(xmltodict.parse(xml_string,process_namespaces=False))
    except Exception as e:
        return '{}'
$$ language plpython3u strict immutable parallel safe cost 9999999999;


create or replace function jsonify_xml3(xml_string text) returns jsonb as
$$
    import untangle
    import json
    try:
        return json.dumps(untangle.parse(xml_string))
    except Exception as e:
        plpy.notice(f"{e}")
        return '{}'
$$ language plpython3u strict immutable parallel safe cost 9999999999;

-- insert into enrichment_def (name,type,function_name) values ('jsonified_docs','jsonb','jsonify_xml');


-- insert

-- insert into enrichment_types (type) values ('jsonb');

-- create or replace enrich