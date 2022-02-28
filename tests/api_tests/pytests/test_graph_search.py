#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import requests


def test_graph_search_metadata_names(base_url,editor_jwt):
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
        }],
        "relationship_names" : ['guidance_references_legislation'],
        "metadata_categories" : ['title']
    }
    resp = requests.post(
        base_url + 'rpc/graph_search',
        json=json,
        headers=headers
    )
    resp.raise_for_status()

    assert len(resp.json()['edges']) == 2
    assert len(resp.json()['nodes']) == 4


def test_graph_search_metadata_categories(base_url,editor_jwt):
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
        }],
        "relationship_names" : ['guidance_references_legislation'],
        "metadata_categories" : ['title']
    }
    resp = requests.post(
        base_url + 'rpc/graph_search',
        json=json,
        headers=headers
    )
    resp.raise_for_status()

    assert len(resp.json()['edges']) == 2
    assert len(resp.json()['nodes']) == 4
