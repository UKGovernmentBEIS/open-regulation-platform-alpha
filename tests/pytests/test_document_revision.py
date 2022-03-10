
#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import requests
import subprocess
import arrow

def test_document_revision_subscription(db_conn,editor_jwt,anon_jwt,base_url):

    headers = {
        'Authorization' : f'Bearer {editor_jwt}',
        'Content-Type' : 'application/json',
        'Accept' : 'application/vnd.pgrst.object+json'
    }

    resp = requests.get(
        base_url + 'event_type',
        headers=headers,
        params={
            "event_name" : "eq.new_document_revision"
        }
    )

    resp.raise_for_status()

    event_type_id = resp.json()['id']

    headers = {
        'Authorization' : f'Bearer {editor_jwt}',
        'Content-Type' : 'application/json',
        'Prefer': 'resolution=merge-duplicates'
    }

    resp = requests.post(
        base_url + 'event_subscription',
        headers=headers,
        json = {
            "event_type_id" : event_type_id,
            "event_filters" : [
                {
                    "event_key" : "document_pk",
                    "event_filter" : "/uksi/2002/618"
                }
            ],
            "deliver_async" : True
        },
        params = {
            "on_conflict" : "event_type_id,event_filters,user_id"
        }
    )

    resp.raise_for_status()


    event_time = arrow.utcnow()
    with db_conn:
        with db_conn.cursor() as curs:
            curs.execute("""
                delete from public_api.document where pk = '/uksi/2002/618' and latest is true and revision_number = 1;
                delete from public_api.event;
                delete from public_api.event_stream;
            """)
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
                );""")

                do_logs_check = True

    if do_logs_check:
        logs = subprocess.getoutput('docker logs -t $(docker ps -q --filter name=orp-alpha_emailer) | grep received')
        lines = [line for line in logs.split('\n') if '/uksi/2002/618' in line and arrow.get(line.split(' ')[0]) > event_time]
        assert len(lines) == 1


    # check the event stream, there should be one total event for the editor
    headers = {
        'Authorization' : f'Bearer {editor_jwt}',
        'Content-Type' : 'application/json'
    }

    resp = requests.get(
        base_url + 'event_subscription_stream',
        headers=headers
    )

    resp.raise_for_status()

    assert len(resp.json()) == 1

    # check the event stream, there should be zero events with a time filter for last year
    headers = {
        'Authorization' : f'Bearer {editor_jwt}',
        'Content-Type' : 'application/json'
    }

    resp = requests.get(
        base_url + 'event_subscription_stream',
        headers=headers,
        params={
            "created_on" : "lt.2020-01-01"
        }
    )

    resp.raise_for_status()

    assert len(resp.json()) == 0

    # check the event stream, there should be zero events for anon
    headers = {
        'Authorization' : f'Bearer {anon_jwt}',
        'Content-Type' : 'application/json'
    }

    resp = requests.get(
        base_url + 'event_subscription_stream',
        headers=headers
    )

    resp.raise_for_status()

    assert len(resp.json()) == 0

    # clean up the db by deleting the new revision for further tests
    with db_conn:
        with db_conn.cursor() as curs:
            curs.execute("""
                delete from public_api.document where pk = '/uksi/2002/618' and latest is true and revision_number = 1;
                delete from public_api.event;
                delete from public_api.event_stream;
            """)
    db_conn.close()