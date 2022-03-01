
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--





create or replace function deontic_language(xml_doc text) returns table (
    data text,
    extent document_extent,
    error jsonb
) as
$$
    import json
    from orp.content_enrichment import extract_obligations_from_string
    try:
        return [(e[0],e[1],None) for e in extract_obligations_from_string(xml_doc, by_section=False)]
    except Exception as e:
        return [(None,None,json.dumps({"exception" : str(e)}))]
$$ language plpython3u;




