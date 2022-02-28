# Standard
import json


def test_base_api(client):
    """Test if the index view is rendered."""
    response = client.get('/api/1.0/')
    assert response.status_code == 200
    assert list(response.data.keys()) == [
        'api-taxonomies',
        'api-documents',
        'api-documents-with-outstanding-feedback',
        'api-documents-with-completed-feedback',
        'api-entities',
        'api-document-search',
        'api-search-graph'
    ]


def test_document_detail(client, mocker):
    mock_request = mocker.Mock(spec=['status_code', 'data', 'url'])
    mock_request.status_code = 200
    mock_request.url = ''
    mock_request.json = mocker.Mock(return_value=[{'raw_text': '<content>'}])
    mocker.patch(
        'orp_apps.orp_api.views.mixins.ApiQueryMixin.get',
        return_value=mock_request
    )
    response = client.get('/api/1.0/documents/1/')
    assert response.status_code == 200
    assert response.data == {'raw_text': '<content>', 'entities': []}


def test_document_detail_not_found(client, mocker):
    mock_request = mocker.Mock(spec=['status_code', 'data', 'url'])
    mock_request.status_code = 200
    mock_request.url = ''
    mock_request.json = mocker.Mock(return_value=[])
    mocker.patch(
        'orp_apps.orp_api.views.mixins.ApiQueryMixin.get',
        return_value=mock_request
    )
    response = client.get('/api/1.0/documents/1/')
    assert response.status_code == 404


def test_jwt_expired(client, mocker):
    mock_request = mocker.Mock(spec=['status_code', 'data', 'url', 'version'])
    mock_request.status_code = 200
    mock_request.data = []
    mock_request.url = ''
    mock_request.version = '1.0'
    mock_request.json = mocker.Mock(return_value={'message': 'JWT expired'})
    mocker.patch(
        'orp_apps.orp_api.views.mixins.ApiQueryMixin.get',
        return_value=mock_request
    )
    response = client.get('/api/1.0/documents/')
    assert response.status_code == 401


def test_document_list(client, mocker):
    return_value = [
        {'document_id': 1},
        {
            'document_id': 2,
            'related_documents': [{'document_id_b': 7}]
        },
        {
            'document_id': 3,
            'reverse_related_documents': [{'document_id_a': 19}]
        }
    ]
    mock_request = mocker.Mock(spec=['status_code', 'data', 'url', 'version'])
    mock_request.status_code = 200
    mock_request.data = []
    mock_request.url = ''
    mock_request.version = '1.0'
    mock_request.json = mocker.Mock(return_value=return_value)
    mocker.patch(
        'orp_apps.orp_api.views.mixins.ApiQueryMixin.get',
        return_value=mock_request
    )
    response = client.get('/api/1.0/documents/')
    assert response.status_code == 200
    assert response.data['results'] == [
        {
            'document_id': 1,
            'entities': [],
            'url': 'http://testserver/api/1.0/documents/1/'
        },
        {
            'document_id': 2,
            'related_documents': [
                {
                    'document_id_b': 7,
                    'url': 'http://testserver/api/1.0/documents/7/'
                }
            ],
            'entities': [],
            'url': 'http://testserver/api/1.0/documents/2/'
        },
        {
            'document_id': 3,
            'reverse_related_documents': [
                {
                    'document_id_a': 19,
                    'url': 'http://testserver/api/1.0/documents/19/'
                }
            ],
            'entities': [],
            'url': 'http://testserver/api/1.0/documents/3/'
        },
    ]


def test_entity_list(client, mocker):
    return_value = [{'id': 1}, {'id': 2}, {'id': 3}]
    mock_request = mocker.Mock(spec=['status_code', 'data', 'url', 'version'])
    mock_request.status_code = 200
    mock_request.data = []
    mock_request.url = ''
    mock_request.version = '1.0'
    mock_request.json = mocker.Mock(return_value=return_value)
    mocker.patch(
        'orp_apps.orp_api.views.mixins.ApiQueryMixin.get',
        return_value=mock_request
    )
    response = client.get('/api/1.0/entities/')
    assert response.status_code == 200
    assert response.data['results'] == [
        {
            'id': 1,
            'url': 'http://testserver/api/1.0/entities/1/',
            'documents': 'http://testserver/api/1.0/entities/1/documents/',
        },
        {
            'id': 2,
            'url': 'http://testserver/api/1.0/entities/2/',
            'documents': 'http://testserver/api/1.0/entities/2/documents/',
        },
        {
            'id': 3,
            'url': 'http://testserver/api/1.0/entities/3/',
            'documents': 'http://testserver/api/1.0/entities/3/documents/',
        },
    ]


def test_taxonomy_list(client, mocker):
    return_value = [{'id': 1}, {'id': 2}, {'id': 3}]
    mock_request = mocker.Mock(spec=['status_code', 'data', 'url', 'version'])
    mock_request.status_code = 200
    mock_request.data = []
    mock_request.url = ''
    mock_request.version = '1.0'
    mock_request.json = mocker.Mock(return_value=return_value)
    mocker.patch(
        'orp_apps.orp_api.views.mixins.ApiQueryMixin.get',
        return_value=mock_request
    )
    response = client.get('/api/1.0/taxonomies/')
    assert response.status_code == 200
    assert response.data['results'] == [
        {
            'id': 1,
            'url': 'http://testserver/api/1.0/taxonomies/1/',
            'categories': 'http://testserver/api/1.0/taxonomies/1/categories/',
        },
        {
            'id': 2,
            'url': 'http://testserver/api/1.0/taxonomies/2/',
            'categories': 'http://testserver/api/1.0/taxonomies/2/categories/',
        },
        {
            'id': 3,
            'url': 'http://testserver/api/1.0/taxonomies/3/',
            'categories': 'http://testserver/api/1.0/taxonomies/3/categories/',
        },
    ]


def test_category_list(client, mocker):
    return_value = [{'id': 1}, {'id': 2}, {'id': 3}]
    mock_request = mocker.Mock(spec=['status_code', 'data', 'url', 'version'])
    mock_request.status_code = 200
    mock_request.data = []
    mock_request.url = ''
    mock_request.version = '1.0'
    mock_request.json = mocker.Mock(return_value=return_value)
    mocker.patch(
        'orp_apps.orp_api.views.mixins.ApiQueryMixin.get',
        return_value=mock_request
    )
    response = client.get('/api/1.0/taxonomies/1/categories/')
    assert response.status_code == 200
    assert response.data['results'] == [
        {
            'id': 1,
            'url': 'http://testserver/api/1.0/taxonomies/1/categories/1/',
        },
        {
            'id': 2,
            'url': 'http://testserver/api/1.0/taxonomies/1/categories/2/',
        },
        {
            'id': 3,
            'url': 'http://testserver/api/1.0/taxonomies/1/categories/3/',
        },
    ]


def test_search_post(client, mocker):
    mock_request = mocker.Mock(spec=['status_code', 'data', 'url', 'version'])
    mock_request.status_code = 200
    mock_request.data = []
    mock_request.url = ''
    mock_request.version = '1.0'
    mock_request.json = mocker.Mock(return_value=[113, 117])
    mocker.patch(
        'orp_apps.orp_api.views.mixins.ApiQueryMixin.post',
        return_value=mock_request
    )
    filter_value = {'filters': [
        {
            'operator': 'and',
            'filter_elements': [
                {
                    'document_metadata_category': 'title',
                    'websearch_tsquery': 'asbestos'
                }
            ]
        }
    ]}
    response = client.post(
        '/api/1.0/search/',
        data=json.dumps(filter_value),
        content_type='application/json'
    )
    assert response.status_code == 302
    assert response.url == '/api/1.0/documents/search/113,117/'


def test_graph_post(client, mocker):
    mock_request = mocker.Mock(spec=['status_code', 'data', 'url', 'version'])
    mock_request.status_code = 200
    mock_request.data = []
    mock_request.url = ''
    mock_request.version = '1.0'
    mock_request.json = mocker.Mock(return_value={})
    mocker.patch(
        'orp_apps.orp_api.views.mixins.ApiQueryMixin.post',
        return_value=mock_request
    )
    filter_value = {
        'filters': [
            {
                'operator': 'and',
                'filter_elements': [
                    {
                        'document_metadata_category': 'title',
                        'websearch_tsquery': 'asbestos'
                    }
                ]
            }
        ],
        'relationship_names': ['guidance_references_legislation'],
        'metadata_categories': ['title', 'classification']
    }
    response = client.post(
        '/api/1.0/graph/',
        data=json.dumps(filter_value),
        content_type='application/json'
    )
    assert response.status_code == 200
