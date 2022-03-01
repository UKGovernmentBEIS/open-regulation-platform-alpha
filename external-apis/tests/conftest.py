# Third Party
import pytest

# Project
from orp_apps.orp_api.models import Category, Taxonomy


@pytest.fixture(autouse=True)
def auth_user(django_user_model):
    return django_user_model.objects.create_user(username='test_user_1', password='letmein')


@pytest.fixture
def authenticated_client(client, db, auth_user):
    """An authenticated Django test client."""
    client.post(
        '/auth/login/',
        data={'username': auth_user.username, 'password': auth_user.password}
    )
    return client


@pytest.fixture(scope='function')
def category_1(db):
    category = Category(name='Building Materials')
    category.save()
    return category


@pytest.fixture(scope='function')
def taxonomy(db, category_1):
    taxonomy = Taxonomy(name='Construction')
    taxonomy.save()
    taxonomy.categories.add(category_1)
    taxonomy.save()
    return taxonomy
