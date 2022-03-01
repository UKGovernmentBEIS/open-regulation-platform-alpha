
#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import requests
import subprocess
import arrow

def do_graph_query(editor_jwt,base_url):
    headers = {
        'Authorization' : f'Bearer {editor_jwt}'
    }

    # graph query before new revision should have no stale edges
    json = {
        "filters" : [{
            "operator" : "and",
            "filter_elements" : [{
                "document_metadata_name": "orpml_title",
                "websearch_tsquery" : "medical"
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
    return resp

def do_stale_rel_setup(db_conn):
    with db_conn:
        with db_conn.cursor() as curs:
            curs.execute("""
                select count(*) from public_api.document where pk = '/uksi/2002/618'
            """)

            res = curs.fetchone()

            if res[0] == 2:
                print("skipping test as event already created")
                do_logs_check = False
            else:
                curs.execute("""select load_single_document(
                    (select id from public_api.document_type where name = 'legislation.gov.uk'),
                    '/demo_data/revisions/618_v2.xml'
                );

                select update_document_metadata(id) from public_api.document_metadata_definition;

                select update_document_graph_relationship_definition((select id from public_api.document_graph_relationship_definition where name = 'guidance_references_legislation'));
                """)

def do_reset(db_conn):
    with db_conn:
        with db_conn.cursor() as curs:
            curs.execute("delete from public_api.document where pk = '/uksi/2002/618' and latest is true and revision_number = 1;")

def test_stale_graph_edge(db_conn,editor_jwt,anon_jwt,base_url):
    # do graph query with no stale edges
    do_reset(db_conn)
    resp = do_graph_query(editor_jwt,base_url)
    assert resp.json()['edges'][0]['data']['stale'] == 'False'

    # create a new document revision and state edge
    do_stale_rel_setup(db_conn)

    # check that the edge is now stale
    resp = do_graph_query(editor_jwt,base_url)
    assert resp.json()['edges'][0]['data']['stale'] == 'True'

    document_graph_id = resp.json()['edges'][0]['data']['id']


    # mark the edge as reconfirmed
    headers = {
        'Authorization' : f'Bearer {editor_jwt}',
        'Content-Type' : 'application/json'
    }

    resp = requests.post(
        base_url + 'document_graph_relationship_confirmation',
        headers=headers,
        json = {
            "document_graph_id" : document_graph_id,
            "confirmation_status" : "reconfirmed"
        }
    )

    resp.raise_for_status()

    # check that the edge is now reconfirmed as not stale
    resp = do_graph_query(editor_jwt,base_url)
    assert resp.json()['edges'][0]['data']['stale'] == 'False'


    # clean up the db by deleting the new revision for further tests
    with db_conn:
        with db_conn.cursor() as curs:
            curs.execute("""
                delete from public_api.document where pk = '/uksi/2002/618' and latest is true;
            """)
    db_conn.close()