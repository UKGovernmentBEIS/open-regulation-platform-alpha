[REQUEST]
POST http://3.9.176.141:8000/auth/login/
{
    "email" : "admin@beis.gov.uk",
    "password" : "Password1!"
}

[RESPONSE]
200 OK
{
    "signed_jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIiA6ICJvcnBfcG9zdGdyZXN0X3dlYiIsICJhcHBfcm9sZXMiIDogWyJhZG1pbiJdLCAidXNlcl9pZCIgOiAxLCAiZXhwIiA6IDE2MzY3MTQ0Mjl9.VNAuX4ruvlm8JMbkrS5rg7yDNzb-0J7dUIpGFs8ZQUM"
}

[REQUEST]
GET http://3.9.176.141:8000/api/1.0/

[RESPONSE]
200 OK
{
    "api-taxonomies": "http://3.9.176.141:8000/api/1.0/taxonomies/",
    "api-documents": "http://3.9.176.141:8000/api/1.0/documents/",
    "api-documents-with-outstanding-feedback": "http://3.9.176.141:8000/api/1.0/documents_with_outstanding_feedback/",
    "api-documents-with-completed-feedback": "http://3.9.176.141:8000/api/1.0/documents_with_completed_feedback/",
    "api-entities": "http://3.9.176.141:8000/api/1.0/entities/",
    "api-document-search": "http://3.9.176.141:8000/api/1.0/search/",
    "api-search-graph": "http://3.9.176.141:8000/api/1.0/graph/"
}

[REQUEST]
GET http://3.9.176.141:8000/api/1.0/taxonomies/

[RESPONSE]
400 BAD_REQUEST
[
    {
        "id": 1,
        "name": "Sample taxonomy 1"
    },
    {
        "id": 2,
        "name": "Sample taxonomy 2"
    },
    {
        "id": 3,
        "name": "Sample taxonomy 3"
    },
    {
        "message": "No ID value can be found for metadata definition"
    },
    {
        "message": "No ID value can be found for metadata definition"
    },
    {
        "message": "No ID value can be found for metadata definition"
    }
]

[REQUEST]
GET http://3.9.176.141:8000/api/1.0/taxonomies/1/

[RESPONSE]
400 BAD_REQUEST
[
    {
        "message": "No ID value can be found for metadata definition"
    }
]

[REQUEST]
GET http://3.9.176.141:8000/api/1.0/documents/

[RESPONSE]
200 OK
{
    "count": 53,
    "next": "http://3.9.176.141:8000/api/1.0/documents/?page=2",
    "previous": null,
    "results": [
        {
            "document_id": 1,
            "document_metadata": [
                {
                    "id": 1,
                    "data": "",
                    "name": "legislation_html",
                    "document_metadata_definition_id": 1,
                    "distinct_metadata_id": null
                }
            ],
            "document_enrichments": [
                {
                    "id": 1,
                    "data": "Any reference to the London Transport Board, the London Transport Executive or London Regional Transport in any of the provisions incorporated with this Act shall be construed as a reference to the Company .",
                    "extent": {
                        "type": "xml",
                        "sections": [
                            {
                                "extent_start": "body/article/div[4]/section[1]/section[2]/section[2]/div/p",
                                "extent_end": "body/article/div[4]/section[1]/section[2]/section[2]/div/p",
                                "extent_char_start": null,
                                "extent_char_end": null
                            }
                        ]
                    },
                    "enrichment_def": {
                        "id": 2,
                        "name": "deontic_language",
                        "type": "text"
                    },
                    "enrichment_feedback": []
                }
            ],
            "entities": [
                {
                    "id": 437,
                    "data": "the Royal Commission",
                    "name": "legislation_named_entities",
                    "document_metadata_definition_id": 8,
                    "distinct_metadata_id": 123,
                    "url": "http://3.9.176.141:8000/api/1.0/entities/123/"
                }
            ],
            "url": "http://3.9.176.141:8000/api/1.0/documents/1/"
        }
    ]
}

[REQUEST]
GET http://3.9.176.141:8000/api/1.0/documents/1/

[RESPONSE]
200 OK
{
    "document_id": 1,
    "document_type": {
        "id": 1,
        "name": "legislation.gov.uk"
    },
    "document_metadata": [
        {
            "id": 51,
            "data": "London Docklands Railway (Lewisham) Act 1993",
            "name": "legislation_title",
            "document_metadata_definition_id": 2,
            "distinct_metadata_id": null
        }   
    ],
    "related_documents": [
        {
            "document_id_b": 75,
            "relationship_properties": {
                "same_named_entity": "the London Docklands Development Corporation"
            },
            "url": "http://3.9.176.141:8000/api/1.0/documents/75/"
        }
    ],
    "reverse_related_documents": [
        {
            "document_id_a": 12,
            "relationship_properties": {
                "cited_in": "London Docklands Railway (Lewisham) Act 1993"
            },
            "url": "http://3.9.176.141:8000/api/1.0/documents/12/"
        }
    ],
    "raw_text": "<akomaNtoso xmlns:xsi...",
    "document_enrichments": [
        {
            "id": 1,
            "data": "Any reference to the London Transport Board, the London Transport Executive or London Regional Transport in any of the provisions incorporated with this Act shall be construed as a reference to the Company .",
            "extent": {
                "type": "xml",
                "sections": [
                    {
                        "extent_start": "body/article/div[4]/section[1]/section[2]/section[2]/div/p",
                        "extent_end": "body/article/div[4]/section[1]/section[2]/section[2]/div/p",
                        "extent_char_start": null,
                        "extent_char_end": null
                    }
                ]
            },
            "enrichment_def": {
                "id": 2,
                "name": "deontic_language",
                "type": "text"
            },
            "enrichment_feedback": []
        },
        {
            "id": 3045,
            "data": "the British Railways Board",
            "extent": {
                "type": "html",
                "sections": [
                    {
                        "extent_start": "body/article/div[3]/ol/li[1]/p",
                        "extent_end": "body/article/div[3]/ol/li[1]/p",
                        "extent_char_start": 369,
                        "extent_char_end": 395
                    },
                    {
                        "extent_start": "body/article/div[4]/section[1]/section[2]/section[1]/div/ul/li[17]/p",
                        "extent_end": "body/article/div[4]/section[1]/section[2]/section[1]/div/ul/li[17]/p",
                        "extent_char_start": 27,
                        "extent_char_end": 53
                    }
                ]
            },
            "enrichment_def": {
                "id": 3,
                "name": "named_entity_extraction",
                "type": "text"
            },
            "enrichment_feedback": []
        }
    ],
    "entities": [
        {
            "id": 437,
            "data": "the Royal Commission",
            "name": "legislation_named_entities",
            "document_metadata_definition_id": 8,
            "distinct_metadata_id": 123,
            "url": "http://3.9.176.141:8000/api/1.0/entities/123/"
        }
    ]
}

[REQUEST]
GET http://3.9.176.141:8000/api/1.0/entities/

[RESPONSE]
200 OK
{
    "count": 89,
    "next": "http://3.9.176.141:8000/api/1.0/entities/?page=2",
    "previous": null,
    "results": [
        {
            "id": 112,
            "data": "the London Docklands Development Corporation",
            "documents": "http://3.9.176.141:8000/api/1.0/entities/112/documents/",
            "url": "http://3.9.176.141:8000/api/1.0/entities/112/"
        },
    ]
}

[REQUEST]
GET http://3.9.176.141:8000/api/1.0/entities/112/

[RESPONSE]
{
    "id": 112,
    "data": "the London Docklands Development Corporation",
    "document_metadata_definition_id": 8,
    "tsvec": "'corporation':5 'development':4 'docklands':3 'london':2 'the':1",
    "_hash": "3221061563876166087",
    "documents": "http://3.9.176.141:8000/api/1.0/entities/112/documents/"
}