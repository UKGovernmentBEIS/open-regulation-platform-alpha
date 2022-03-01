
#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#


import requests


def test_enrichment_feedback_status(base_url,editor_jwt):
    headers = {
        'Authorization' : f'Bearer {editor_jwt}',
        'Range-Unit' : 'items',
        'Range' :  '0-9'
    }
    params = {
        'select' : "document_id:id,document_type(id,name),related_documents:document_graph!document_id_a(document_id_b,relationship_properties),reverse_related_documents:document_graph!document_id_b(document_id_a,relationship_properties),document_metadata:document_metadata_view(data,category,name,distinct_metadata_id),document_enrichments:enrichment(id,data,extent,enrichment_def(id,name),enrichment_feedback(good,notes,user_id))",
        'document_metadata_view.category' : 'in.(title,longtitle,enacted,identification,classification,named_entities)'

    }
    resp = requests.get(
        base_url + 'document',
        params=params,
        headers=headers
    )
    resp.raise_for_status()

    docs_with_enrichments = [r for r in resp.json() if len(r['document_enrichments']) > 0]

    if docs_with_enrichments:
        doc_to_feedback = docs_with_enrichments[0]
        headers = {
            'Authorization' : f'Bearer {editor_jwt}',
            'Content-Type' : 'application/json',
            'Accept' : 'application/json'
        }

        # this should fail as enrichments do not all have feedback
        try:
            resp = requests.post(
                base_url + 'document_enrichment_feedback_status',
                json= {
                    "document_id" : doc_to_feedback['document_id'],
                    "feedback_status" : "review_complete"
                },
                headers=headers
            )
            resp.raise_for_status()
        except Exception as e:
            assert resp.json()['message'] == 'Not all enrichments for document have had feedback'

        # give feedback for all enrichments
        for ed in doc_to_feedback['document_enrichments']:
            resp = requests.post(
                base_url + 'enrichment_feedback',
                json={
                    "enrichment_id" : ed['id'],
                    "good" : True,
                    "notes" : "some feedback notes"
                },
                headers=headers
            )
            resp.raise_for_status()

        # this document id should still be in docs_with_outstanding_feedback

        resp = requests.get(
            base_url + 'docs_with_outstanding_feedback',
            params = {
                'id' : f"eq.{doc_to_feedback['document_id']}"
            },
            headers=headers
        )
        resp.raise_for_status()

        assert doc_to_feedback['document_id'] in [d['id'] for d in resp.json()]

        # this should now suceed
        resp = requests.post(
            base_url + 'document_enrichment_feedback_status',
            json= {
                "document_id" : doc_to_feedback['document_id'],
                "feedback_status" : "review_complete"
            },
            headers=headers
        )
        resp.raise_for_status()


        # this doc should now also be present in docs_with_completed_feedback
        resp = requests.get(
            base_url + 'docs_with_completed_feedback',
            headers=headers
        )
        resp.raise_for_status()

        assert doc_to_feedback['document_id'] in [d['id'] for d in resp.json()]


        # check that docs_with_outstanding_feedback doesn't return any documents without enrichments

        # resp = requests.get(
        #     base_url + 'docs_with_outstanding_feedback',
        #     params = {
        #         'document_enrichments.data' : 'neq.NULL'
        #     },
        #     headers=headers
        # )
        # resp.raise_for_status()

        # test = [d for d in resp.json()]

        return

    raise Exception()



