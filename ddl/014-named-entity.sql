
--
-- Copyright (C) Analytics Engines
-- 2021 Lauren Stephens (l.stephens@analyticsengines.com)
--


create or replace function named_entity_extraction(html_doc text) returns table (
    data text,
    extent document_extent,
    error jsonb
) as
$$
    import json
    from orp.authority_ner import extract_entities_from_string
    patterns = {"departments": r"the (Department|Ministry|Office) of(\sthe)? ([A-Z][a-z]+(?=(,)?(\s([A-Z]|and|[a-z]))))(?:(((,\s)|(\s)|(\sand\s))([A-Z][a-z]+)+)+)?",
                "authorities": r"the ([A-Z][a-z]+(?=\s[A-Z])((?:\s[A-Z][a-z]+)?)+) (Administration|Agency|Assembly|Authority|Board|Commission|Committee|Corporation|Council|Court|Executive|Institute|Office|Ombudsman|Parliament|Registry|Regulator|Service|Tribunal|Trust)(?=\sfor ([A-Z][a-z]+))?(?:\sfor(\s[A-Z][a-z]+)+)?"}

    try:
        return [(entity[0],entity[1],None) for entity in extract_entities_from_string(html_doc, patterns)]
    except Exception as e:
        return [(None,None,json.dumps({"exception" : str(e)}))]
$$ language plpython3u;
