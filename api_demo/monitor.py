#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
import requests
import streamlit_bd_cytoscapejs

from common import login,init_state,base_url,internal_url,format_request,summarise_docs,local_css,graph_layout,graph_style,get_db_conn,format_graph_response,format_edges

init_state(['jwt','graph1','graph1_request','graph2','graph2_request','graph2_edges','sub1_request','sub2_request','event_stream_req','event_stream_resp','attest_request','graph3','graph3_request','graph3_edges'])

local_css("colorful.css")

def check_event_subscriptions():
    login()
    headers = {
        'Authorization' : f'Bearer {st.session_state.jwt}',
        'Content-Type' : 'application/json'
    }

    resp = requests.get(
        internal_url + 'event_subscription_stream',
        headers=headers
    )

    st.session_state.event_stream_req = format_request(resp)
    st.session_state.event_stream_resp = resp.json()

    resp.raise_for_status()

def subscribe_to_events():
    login()
    headers = {
        'Authorization' : f'Bearer {st.session_state.jwt}',
        'Content-Type' : 'application/json',
        'Accept' : 'application/vnd.pgrst.object+json'
    }

    resp = requests.get(
        internal_url + 'event_type',
        headers=headers,
        params={
            "event_name" : "eq.new_document_revision"
        }
    )

    resp.raise_for_status()

    event_type_id = resp.json()['id']

    headers = {
        'Authorization' : f'Bearer {st.session_state.jwt}',
        'Content-Type' : 'application/json',
        'Prefer': 'resolution=merge-duplicates'
    }

    resp = requests.post(
        internal_url + 'event_subscription',
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

    st.session_state.sub1_request = format_request(resp)

    resp.raise_for_status()

    headers = {
        'Authorization' : f'Bearer {st.session_state.jwt}',
        'Content-Type' : 'application/json',
        'Accept' : 'application/vnd.pgrst.object+json'
    }

    resp = requests.get(
        internal_url + 'event_type',
        headers=headers,
        params={
            "event_name" : "eq.stale_document_relationship"
        }
    )

    headers = {
        'Authorization' : f'Bearer {st.session_state.jwt}',
        'Content-Type' : 'application/json',
        'Prefer': 'resolution=merge-duplicates'
    }

    event_type_id = resp.json()['id']

    resp = requests.post(
        internal_url + 'event_subscription',
        headers=headers,
        json = {
            "event_type_id" : event_type_id,
            "event_filters" : [
                {
                    "event_key" : "changed_document_pk",
                    "event_filter" : "/uksi/2002/618"
                }
            ],
            "deliver_async" : True
        },
        params = {
            "on_conflict" : "event_type_id,event_filters,user_id"
        }
    )

    st.session_state.sub2_request = format_request(resp)

    resp.raise_for_status()

def do_document_cleanup():
    with st.spinner('Rolling Back Document Update'):
        db_conn = get_db_conn()
        with db_conn:
            with db_conn.cursor() as curs:
                curs.execute("""
                    delete from public_api.document where pk = '/uksi/2002/618' and latest is true and revision_number = 1;
                    delete from public_api.event;
                    delete from public_api.event_stream;
                """)
        db_conn.close()

def do_document_update():
    do_document_cleanup()
    with st.spinner('Simulating Document Update'):
        db_conn = get_db_conn()
        with db_conn:
            with db_conn.cursor() as curs:
                curs.execute("""
                    select count(*) from public_api.document where pk = '/uksi/2002/618'
                """)

                res = curs.fetchone()

                if res[0] == 2:
                    print("skipping update as event already created")
                else:
                    curs.execute("""select load_single_document(
                        (select id from public_api.document_type where name = 'legislation.gov.uk'),
                        '/demo_data/revisions/618_v2.xml'
                    );

                    select update_document_metadata(id) from public_api.document_metadata_definition;

                    select update_document_graph_relationship_definition((select id from public_api.document_graph_relationship_definition where name = 'guidance_references_legislation'));
                    """)
        db_conn.close()
    # st.success('Document Update Successfully Simulated')


def get_graph2():
    login()
    r = requests.post(
        base_url + 'api/1.0/graph/',
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {st.session_state.jwt}"
        },
        json = {
            "filters" : [{
                "operator" : "and",
                "filter_elements" : [{
                    "document_metadata_category": "title",
                    "websearch_tsquery" : "medical"
                }]
            }],
            "relationship_names" : ['guidance_references_legislation'],
            "metadata_categories" : ['title']
        }
    )
    r.raise_for_status()
    st.session_state.graph2 = format_graph_response(r.json())
    st.session_state.graph2_request = format_request(r)
    st.session_state.graph2_edges = format_edges(r)

def get_graph3():
    login()
    r = requests.post(
        base_url + 'api/1.0/graph/',
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {st.session_state.jwt}"
        },
        json = {
            "filters" : [{
                "operator" : "and",
                "filter_elements" : [{
                    "document_metadata_category": "title",
                    "websearch_tsquery" : "medical"
                }]
            }],
            "relationship_names" : ['guidance_references_legislation'],
            "metadata_categories" : ['title']
        }
    )
    r.raise_for_status()
    st.session_state.graph3 = format_graph_response(r.json())
    st.session_state.graph3_request = format_request(r)
    st.session_state.graph3_edges = format_edges(r)



def reconfirm_edge():
    # mark the edge as reconfirmed

    document_graph_id = st.session_state.graph2['edges'][0]['data']['id']

    headers = {
        'Authorization' : f'Bearer {st.session_state.jwt}',
        'Content-Type' : 'application/json'
    }

    r = requests.post(
        internal_url + 'document_graph_relationship_confirmation',
        headers=headers,
        json = {
            "document_graph_id" : document_graph_id,
            "confirmation_status" : "reconfirmed"
        }
    )

    r.raise_for_status()

    st.session_state.attest_request = format_request(r)

# do_document_cleanup()

st.markdown("""
# Monitor
## As a regulator, I need to understand when any legislation that my guidance links to is updated to check if amendments are required or that I can attest that the changes do not require me to produce a new revision
""")

st.button('Click To Subscribe to Document Revisions and potentially stale relationships of "The Medical Devices Regulations 2002"',on_click=lambda:subscribe_to_events())
st.write("New Document Revision Subscription HTTP Request will appear below on click")
st.markdown(st.session_state.sub1_request,unsafe_allow_html=True)
st.write("Stale Relationship Subscription HTTP Request will appear below on click")
st.markdown(st.session_state.sub2_request,unsafe_allow_html=True)

st.button('Click To Simulate a New Revision of Document and Citation Graph Update',on_click=lambda: do_document_update())

st.button('Click To Check your Subscriptions',on_click=lambda: check_event_subscriptions())
st.write("Subscriptions HTTP Request will appear below on click")
st.markdown(st.session_state.event_stream_req,unsafe_allow_html=True)
st.write('')
st.write("Subscriptions HTTP Response will appear below on click")
st.write(st.session_state.event_stream_resp)
st.write('')

st.button('Click To View The Document Graph Around The Updated Document',on_click=lambda: get_graph2())
st.write("Graph HTTP Request will appear below on click")
st.markdown(st.session_state.graph2_request,unsafe_allow_html=True)
st.write('')
st.write("Graph HTTP Response will appear below on click")
st.write(st.session_state.graph2)
st.write('')

col1, col2 = st.columns(2)

with col1:
    st.markdown('Faded relationship illustrates the potentially stale relationship')
    node_id = streamlit_bd_cytoscapejs.st_bd_cytoscape(
        st.session_state.graph2,
        layout=graph_layout,
        stylesheet=graph_style,
        key='test'
    )
    st.write(node_id)
with col2:
    st.write(st.session_state.graph2_edges)

st.markdown(f"""
# Attestation
As a owner of the guidance document I will attest to the current version being applicable to the new legislation revision
""")

st.button('Click To Attest that this guidance is still valid',on_click=lambda: reconfirm_edge())
st.write("Attestation HTTP Request will appear below on click")
st.markdown(st.session_state.attest_request,unsafe_allow_html=True)

st.button('Click To View The Document Graph Around The Updated Document after Attestation',on_click=lambda: get_graph3())
st.write("Graph HTTP Response will appear below on click")
st.write(st.session_state.graph3)
st.write('')

col1, col2 = st.columns(2)

with col1:
    st.markdown('Solid relationship illustrates the potentially stale relationship')
    node_id = streamlit_bd_cytoscapejs.st_bd_cytoscape(
        st.session_state.graph3,
        layout=graph_layout,
        stylesheet=graph_style,
        key='test2'
    )
    st.write(node_id)
with col2:
    st.write(st.session_state.graph3_edges)

# with st.expander('View First Graph Data'):
#     st.write(st.session_state.graph1)

# st.markdown("Graph Below shows all document search results that match the filter and the first hop of related documents")
# # with st.expander('View First Graph'):
# node_id = streamlit_bd_cytoscapejs.st_bd_cytoscape(
#     st.session_state.graph1,
#     layout=graph_layout,
#     stylesheet=graph_style,
#     key='test'
# )
# st.write(node_id)

# st.markdown("""
# # Contextual Understanding Continued
# Now filter graph using only legislation that is connected to regulation
# """)

# st.button('Click To Excecute New Graph Search',on_click=lambda: get_graph2())
# st.write("Graph HTTP Request will appear below on click")
# st.markdown(st.session_state.graph2_request,unsafe_allow_html=True)
# st.write('')

# st.markdown("Graph below shows the search results and documents related only the the ```guidance_reference_legilsation``` relationship")
# node_id2 = streamlit_bd_cytoscapejs.st_bd_cytoscape(
#     st.session_state.graph2,
#     layout=graph_layout,
#     stylesheet=graph_style,
#     key='test2'
# )
# st.write(node_id2)

