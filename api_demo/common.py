#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#

import requests
base_url = "http://127.0.0.1:8000/"
internal_url = "http://127.0.0.1:3001/"
import streamlit as st


import textwrap
import requests
import pandas as pd
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
import json
import arrow
from bs4 import BeautifulSoup

def local_css(fn):
    with open(fn) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def format_graph_response(r):
    data = {}

    nodes = [n for n in r['nodes']]
    edges = []


    for e in r['edges']:
        if e['data']['relationship_confirmation']['confirmation_status'] == 'reconfirmed':
            e['data']['tooltip'] = f"""
                Previously stale relationship reconfirmed by user {e['data']['relationship_confirmation']['user_id']}
                {arrow.get(e['data']['relationship_confirmation']['confirmed_on']).humanize()}
            """
        elif e['data']['stale'] == 'True':
            e['data']['tooltip'] = f"Stale relationship"

        if e['data']['property_key'] == 'same_named_entity':
            e['data']['tooltip'] = f"{e['data']['properties'][e['data']['property_key']]}"

        e['data']['edge_label'] = f"{e['data']['property_key']} - {e['data']['properties'][e['data']['property_key']]}"

        edges.append(e)


    data['nodes'] = nodes
    data['edges'] = edges

    return data

def format_edges(r):
    return pd.DataFrame.from_records([
        {
            "source" : e['data']['source'],
            "target" : e['data']['target'],
            "property_key" : e['data']['property_key'],
            "property_value" : e['data']['properties'][e['data']['property_key']]
        }
        for e in r.json()['edges']
    ])


from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from bs4 import BeautifulSoup
def format_request(response):
    if response.request.body:
        json_body = json.loads(response.request.body.decode())
        formatted_body = json.dumps(json_body,indent=4)
        highlighted = highlight(formatted_body,JsonLexer(),HtmlFormatter())
    else:
        highlighted = highlight('',JsonLexer(),HtmlFormatter())
    headers = "\n".join([f'<span class="k">{k}:</span> <span class="nd">{v}</span>' for k,v in response.request.headers.items()])

    soup = BeautifulSoup(highlighted,features="lxml")
    pre = f"""
        <span class="nc">{response.request.method}</span> <span class="no">{response.request.url}</span>
        {headers}
        <span></span>
    """

    soup.html.body.div.pre.insert(0,BeautifulSoup(pre,'html.parser'))
    return str(soup)

def init_state(state_vars):
    for v in state_vars:
        if v not in st.session_state:
            st.session_state[v] = None

def summarise_docs(results):
    doc_titles = []
    for result in results:
        title = next(dm['data'] for dm in result['document_metadata'] if dm['name'] in ('legislation_title','orpml_title'))
        doc_titles.append({"title" : title , "document_id" : result["document_id"], "primary_key" : result['primary_key'], "revision_number" : result['revision_number']})
    return pd.DataFrame.from_records(doc_titles)

def login(u = 'editor@beis.gov.uk',p = 'Password1!'):
    r = requests.post(
        base_url + 'auth/login/',
        json={
            "email" : u,
            "password" : p
        }
    )
    r.raise_for_status()
    st.session_state.jwt = r.json()['signed_jwt']
    st.session_state.login_request = format_request(r)


def get_db_conn():
    import psycopg2
    db_conn = psycopg2.connect(dbname="orp_alpha", user="postgres", password="admin", port=5435, host="127.0.0.1")
    return db_conn

graph_style = [
    {
        "selector" : 'node',
        "style" : {
            'label': 'data(title)',
            'font-size': '8px',
            "height":40,
            "width":40
        }
    },
    {
        "selector" : 'node[document_type_name=\"legislation.gov.uk\"]',
        "style" : {
            "background-color":"#30c9bc"
        }
    },
    {
        "selector" : 'node[document_type_name=\"orpml\"]',
        "style" : {
            "background-color":"#11479e"
        }
    },
    {
        "selector" : 'edge',
        "style" : {
            'font-size': '8px'
        }
    },
    {
        "selector" : 'edge[stale=\"False\"]',
        "style" : {
            "opacity": "1"
        }
    },
    {
        "selector" : 'edge[stale=\"True\"]',
        "style" : {
            "opacity": "0.5"
        }
    },
    {
        "selector" : 'edge[property_key=\"guidance_references_legislation\"]',
        "style" : {
            "label": "References Legislation",
            "line-color": "#d0b7d5"
        }
    },
    {
        "selector" : 'edge[property_key=\"same_named_entity\"]',
        "style" : {
            "label": "Same Named Entity",
            "line-color": "blue"
        }
    },
    {
        "selector" : 'edge[property_key=\"cited_in\"]',
        "style" : {
            "label": "Cited In",
            "line-color": "red"
        }
    },
    {
        "selector" : 'edge[property_key=\"same_classification\"]',
        "style" : {
            "label": "Same Classification",
            "line-color": "green"
        }
    }
]

graph_layout = {
    'name': 'circle',
    'nodeSpacing' : '150',
    'edgeLengthVal' : '45'
}