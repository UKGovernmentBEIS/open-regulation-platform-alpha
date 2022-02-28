#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import pytest
import requests
import psycopg2

@pytest.fixture
def editor_jwt():
    r = requests.post(
        'http://127.0.0.1:3001/rpc/login',
        json={
            "email" : "editor@beis.gov.uk",
            "password" : "Password1!"
        }
    )
    return r.json()['signed_jwt']

@pytest.fixture
def base_url():
    return 'http://127.0.0.1:3001/'

@pytest.fixture
def db_conn():
    conn = psycopg2.connect(dbname="orp_alpha", user="postgres", password="admin", port=5435, host="127.0.0.1")
    return conn