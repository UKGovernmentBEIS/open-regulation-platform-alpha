#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import requests


def test_doc_search_names(base_url,editor_jwt):
    headers = {
        'Authorization' : f'Bearer {editor_jwt}'
    }
    json = {
        "filters" : [{
            "operator" : "and",
            "filter_elements" : [{
                "document_metadata_name": "orpml_title",
                "websearch_tsquery" : "asbestos"
            },
            {
                "document_metadata_name": "orpml_classification",
                "websearch_tsquery" : "asbestos"
            }]
        }]
    }
    resp = requests.post(
        base_url + 'rpc/document_search',
        json=json,
        headers=headers
    )
    resp.raise_for_status()

    assert len(resp.json()) == 2

def test_doc_search_cats(base_url,editor_jwt):
    headers = {
        'Authorization' : f'Bearer {editor_jwt}'
    }
    json = {
        "filters" : [{
            "operator" : "and",
            "filter_elements" : [{
                "document_metadata_category": "title",
                "websearch_tsquery" : "asbestos"
            },
            {
                "document_metadata_category": "classification",
                "websearch_tsquery" : "asbestos"
            }]
        }]
    }
    resp = requests.post(
        base_url + 'rpc/document_search',
        json=json,
        headers=headers
    )
    resp.raise_for_status()

    assert len(resp.json()) == 2


    params = {
        'select' : "document_id:id,document_type(id,name),related_documents:document_graph!document_id_a(document_id_b,relationship_properties),reverse_related_documents:document_graph!document_id_b(document_id_a,relationship_properties),document_metadata:document_metadata_view(data,category,name,distinct_metadata_id),document_enrichments:enrichment(id,data,extent,enrichment_def(id,name),enrichment_feedback(good,notes,user_id))",
        'id' : f'in.({",".join([str(d) for d in resp.json()])})',
        'document_metadata_view.category' : 'in.(title,longtitle,enacted,identification,classification,named_entities,html)'
    }
    resp = requests.get(
        base_url + 'document',
        params=params,
        headers=headers
    )
    resp.raise_for_status()

    assert len(resp.json()) == 2


def test_doc_search_single(base_url,editor_jwt):
    headers = {
        'Authorization' : f'Bearer {editor_jwt}'
    }
    json = {
        "filters" : [{
            "operator" : "and",
            "filter_elements" : [{
                "document_metadata_category": "title",
                "websearch_tsquery" : "asbestos"
            }]
        }]
    }
    resp = requests.post(
        base_url + 'rpc/document_search',
        json=json,
        headers=headers
    )
    resp.raise_for_status()

    assert len(resp.json()) == 4


    params = {
        'select' : "document_id:id,document_type(id,name),related_documents:document_graph!document_id_a(document_id_b,relationship_properties),reverse_related_documents:document_graph!document_id_b(document_id_a,relationship_properties),document_metadata:document_metadata_view(data,category,name,distinct_metadata_id),document_enrichments:enrichment(id,data,extent,enrichment_def(id,name),enrichment_feedback(good,notes,user_id))",
        'id' : f'in.({",".join([str(d) for d in resp.json()])})',
        'document_metadata_view.category' : 'in.(title,longtitle,enacted,identification,classification,named_entities,html)'
    }
    resp = requests.get(
        base_url + 'document',
        params=params,
        headers=headers
    )
    resp.raise_for_status()

    assert len(resp.json()) == 4


