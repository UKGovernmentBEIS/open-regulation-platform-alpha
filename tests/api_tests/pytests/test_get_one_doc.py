
#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import requests

def test_get_one_doc_by_id(base_url,editor_jwt):
    headers = {
        'Authorization' : f'Bearer {editor_jwt}'
    }

    params = {
        'select' : "id",
    }

    resp = requests.get(
        base_url + 'document',
        params=params,
        headers=headers
    )
    resp.raise_for_status()
    id = min([r['id'] for r in resp.json()])

    headers = {
        'Authorization' : f'Bearer {editor_jwt}',
        'Accept' : 'application/vnd.pgrst.object+json'
    }

    params = {
        'select' : "document_id:id,created_on,revision_number,primary_key:pk,document_type(id,name),related_documents:document_graph!document_id_a(document_id_b,relationship_properties),reverse_related_documents:document_graph!document_id_b(document_id_a,relationship_properties),document_metadata:document_metadata_view(data,category,name,distinct_metadata_id),document_enrichments:enrichment(id,data,extent,enrichment_def(id,name),enrichment_feedback(good,notes,user_id))",
        'id' : f'eq.{id}',
        'document_metadata_view.category' : 'in.(title,longtitle,enacted,identification,classification,named_entities,html)'
    }
    resp = requests.get(
        base_url + 'document',
        params=params,
        headers=headers
    )
    resp.raise_for_status()
    test = resp.json()

def test_get_one_doc_by_pk(base_url,editor_jwt):
    headers = {
        'Authorization' : f'Bearer {editor_jwt}'
    }

    params = {
        'select' : "pk",
    }

    resp = requests.get(
        base_url + 'document',
        params=params,
        headers=headers
    )
    resp.raise_for_status()
    pk = min([r['pk'] for r in resp.json()])

    headers = {
        'Authorization' : f'Bearer {editor_jwt}',
        'Accept' : 'application/vnd.pgrst.object+json'
    }

    params = {
        'select' : "document_id:id,created_on,revision_number,primary_key:pk,document_type(id,name),related_documents:document_graph!document_id_a(document_id_b,relationship_properties),reverse_related_documents:document_graph!document_id_b(document_id_a,relationship_properties),document_metadata:document_metadata_view(data,category,name,distinct_metadata_id),document_enrichments:enrichment(id,data,extent,enrichment_def(id,name),enrichment_feedback(good,notes,user_id))",
        'pk' : f'eq.{pk}',
        'document_metadata_view.category' : 'in.(title,longtitle,enacted,identification,classification,named_entities,html)'
    }
    resp = requests.get(
        base_url + 'document',
        params=params,
        headers=headers
    )
    resp.raise_for_status()


def test_get_one_doc_by_pk_2_revs(base_url,editor_jwt,db_conn):

    # make sure second doc revision is loaded
    with db_conn:
        with db_conn.cursor() as curs:
            curs.execute("""select load_single_document(
                (select id from public_api.document_type where name = 'legislation.gov.uk'),
                '/demo_data/revisions/618_v2.xml'
            );""")

    headers = {
        'Authorization' : f'Bearer {editor_jwt}'
    }

    pk = '/uksi/2002/618'

    params = {
        'select' : "document_id:id,created_on,revision_number,primary_key:pk,document_type(id,name),related_documents:document_graph!document_id_a(document_id_b,relationship_properties),reverse_related_documents:document_graph!document_id_b(document_id_a,relationship_properties),document_metadata:document_metadata_view(data,category,name,distinct_metadata_id),document_enrichments:enrichment(id,data,extent,enrichment_def(id,name),enrichment_feedback(good,notes,user_id))",
        'pk' : f'eq.{pk}',
        'document_metadata_view.category' : 'in.(title,longtitle,enacted,identification,classification,named_entities,html)'
    }

    # first request should return both revisions
    resp = requests.get(
        base_url + 'document',
        params=params,
        headers=headers
    )
    resp.raise_for_status()

    assert len(resp.json()) == 2

    # second request only gets the latest revision

    headers = {
        'Authorization' : f'Bearer {editor_jwt}',
        'Accept' : 'application/vnd.pgrst.object+json'
    }


    params = {
        'select' : "document_id:id,created_on,revision_number,primary_key:pk,document_type(id,name),related_documents:document_graph!document_id_a(document_id_b,relationship_properties),reverse_related_documents:document_graph!document_id_b(document_id_a,relationship_properties),document_metadata:document_metadata_view(data,category,name,distinct_metadata_id),document_enrichments:enrichment(id,data,extent,enrichment_def(id,name),enrichment_feedback(good,notes,user_id))",
        'pk' : f'eq.{pk}',
        'latest' : 'eq.true',
        'document_metadata_view.category' : 'in.(title,longtitle,enacted,identification,classification,named_entities,html)'
    }

    # first request should return both revisions
    resp = requests.get(
        base_url + 'document',
        params=params,
        headers=headers
    )
    resp.raise_for_status()





