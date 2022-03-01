
#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import requests

def test_login(base_url):
    r = requests.post(
        base_url + 'rpc/login',
        json={
            "email" : "editor@beis.gov.uk",
            "password" : "Password1!"
        }
    )
    r.raise_for_status()
    assert 'signed_jwt' in r.json()


