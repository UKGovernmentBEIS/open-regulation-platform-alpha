
#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import requests


def test_enrichment_feedback(base_url,editor_jwt):
    headers = {
        'Authorization' : f'Bearer {editor_jwt}',
        'Range-Unit' : 'items',
        'Range' :  '0-9'
    }
    params = {
        'select' : "document_id:id,document_type(id,name),related_documents:document_graph!document_id_a(document_id_b,relationship_properties),reverse_related_documents:document_graph!document_id_b(document_id_a,relationship_properties),document_metadata:document_metadata_view(data,category,name,distinct_metadata_id),document_enrichments:enrichment(id,data,extent,enrichment_def(id,name),enrichment_feedback(good,notes,user_id))",
        'document_metadata_view.category' : 'in.(title,longtitle,enacted,identification,classification,named_entities)',
        'document_enrichments.data' : 'neq.NULL'

    }
    resp = requests.get(
        base_url + 'document',
        params=params,
        headers=headers
    )
    resp.raise_for_status()

    docs_with_enrichments = [r for r in resp.json() if len(r['document_enrichments']) > 0]

    if docs_with_enrichments:
        enrichment_id = docs_with_enrichments[0]['document_enrichments'][0]['id']
        requests.post(
            base_url + 'enrichment_feedback',
            json={
                "enrichment_id" : enrichment_id,
                "good" : True,
                "notes" : "some feedback notes"
            }
        )
        resp.raise_for_status()
        return
    raise Exception()



