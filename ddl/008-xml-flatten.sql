
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--


-- create or replace function xml_flatten returns table (

-- ) as
-- $$

-- $$ language plpython3u;


create or replace function xml_flatten(xml_doc text) returns table (
    full_path text,
    is_array_element boolean,
    text text,
    tag text,
    attrib text
) as
$$
    from orp.xmltools import recursive_walk
    return recursive_walk(xml_doc)
$$ language plpython3u;

create or replace function akomantoso_to_html(akn text) returns table (
    data text,
    extent document_extent,
    error jsonb
) as
$$
    import orp
    import os
    from orp.xmltools import xslt3_transform
    xslt_path = os.path.join(orp.__path__[0],'xmltools/test/akn2html.sef.json')

    if 'xslt_cache' not in GD:
        GD['xslt_cache'] = open(xslt_path,'r').read()

    try:
        success,data = xslt3_transform(GD['xslt_cache'],akn)
        if success:
            return [(data,None,None)]
        else:
            return [(None,None,data)]
    except Exception as e:
        return [(None,None,str(e))]

$$ language plpython3u;

-- only needed to speed up testing
create or replace function akomantoso_to_html_dummy(akn text) returns table (
    data text,
    extent document_extent,
    error jsonb
) as
$$
    return [('',None,None)]
$$ language plpython3u;


-- create or replace function deontic_language(xml_doc text) returns table (
--     data text,
--     extent document_extent,
--     error jsonb
-- ) as
-- $$
--     select _deontic_language() from akomaNtoso_to_html(xml_doc) akn;
-- $$ language sql;





create or replace function xml_text(xml_doc text) returns table (
    data text,
    extent document_extent,
    error jsonb
) as
$$
    from lxml import etree as ET
    root = ET.fromstring(xml_doc)
    try:
        return [(' '.join((''.join(element.itertext()) for element in root.iter() if element.text)),None,None)]
    except ValueError as e:
        return [('',None,None)]
$$ language plpython3u immutable parallel safe cost 999999999999;

-- create or replace function lxml_xpath(xpath text,xml_doc text, ns jsonb) returns setof text as
-- $$
--     from lxml import etree as ET
--     root = ET.fromstring(xml_doc)
--     return root.xpath(xpath,namespaces= {
--         "dcns" : "http://purl.org/dc/elements/1.1/",
--         "ans" : "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
--     })
-- $$ language plpython3u immutable parallel safe cost 999999999999;

-- create or replace function ts_vector_from_xml(data text) returns tsvector as
-- $$
--     select to_tsvector('simple',xml_text(data));
-- $$ language sql immutable parallel safe;