#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
import requests
import streamlit_bd_cytoscapejs

from common import login,init_state,base_url,internal_url,format_request,summarise_docs,local_css

init_state(['docs_list','jwt','docs_list_request','docs_list1','docs_list_request1','ner_list_request','ner_list','ner_search_request','ner_search'])

local_css("colorful.css")


def get_enriched_doc():
    login()
    pk = '/uksi/2012/632'
    headers = {
        'Authorization' : f'Bearer {st.session_state.jwt}',
        'Accept' : 'application/vnd.pgrst.object+json'
    }


    params = {
        'select' : "document_id:id,created_on,revision_number,primary_key:pk,document_type(id,name),related_documents:document_graph!document_id_a(document_id_b,relationship_properties),reverse_related_documents:document_graph!document_id_b(document_id_a,relationship_properties),document_metadata:document_metadata_view(data,category,name,distinct_metadata_id),document_enrichments:enrichment(id,data,extent,enrichment_def(id,name),enrichment_feedback(good,notes,user_id))",
        'pk' : f'eq.{pk}',
        'latest' : 'eq.true',
        'document_metadata_view.category' : 'in.(title)'
    }

    # first request should return both revisions
    resp = requests.get(
        internal_url + 'document',
        params=params,
        headers=headers
    )
    resp.raise_for_status()

    enrichments = [{"id" : de['id'], "data" : de['data'], "extents" : ",".join([e['extent_start'] for e in de['extent']['sections']]) } for de in resp.json()['document_enrichments']]

    df = pd.DataFrame.from_records(enrichments[0:20])

    st.session_state.docs_list = df
    st.session_state.docs_list_request = format_request(resp)

def get_enriched_doc1():
    login()
    pk = '/uksi/2002/618'
    headers = {
        'Authorization' : f'Bearer {st.session_state.jwt}',
        'Accept' : 'application/json'
    }


    params = {
        'select' : "id,pk,data,extent",
        'pk' : f'eq.{pk}',
        'latest' : 'eq.true',
        'document_metadata_definition_id' : 'eq.8'
    }

    # first request should return both revisions
    resp = requests.get(
        internal_url + 'document_metadata',
        params=params,
        headers=headers
    )
    resp.raise_for_status()

    # print(resp.json())

    enrichments = [{"id" : de['id'], "pk" : de['pk'], "data" : de['data'], "extents" : ",".join([e['extent_start'] for e in de['extent']['sections']]) } for de in resp.json()]
    # enrichments = [{"id" : de['id'], "pk" : de['pk'], "data" : de['data'] } for de in resp.json()]

    df = pd.DataFrame.from_records(enrichments)

    st.session_state.docs_list1 = df
    st.session_state.docs_list_request1 = format_request(resp)

def get_ner_list():
    login()
    # pk = '/uksi/2002/618'
    headers = {
        'Authorization' : f'Bearer {st.session_state.jwt}',
        'Accept' : 'application/json'
    }


    params = {
        'select' : "id,named_entity:data",
        'document_metadata_definition_id' : 'eq.8'
    }

    # first request should return both revisions
    resp = requests.get(
        internal_url + 'distinct_document_metadata',
        params=params,
        headers=headers
    )
    resp.raise_for_status()

    print(resp.json())

    # enrichments = [{"id" : de['id'], "pk" : de['pk'], "data" : de['data'], "extents" : ",".join([e['extent_start'] for e in de['extent']['sections']]) } for de in resp.json()]
    # enrichments = [{"id" : de['id'], "pk" : de['pk'], "data" : de['data'] } for de in resp.json()]

    df = pd.DataFrame.from_records(resp.json())

    st.session_state.ner_list = df
    st.session_state.ner_list_request = format_request(resp)

def ner_search():
    login()
    # pk = '/uksi/2002/618'
    headers = {
        'Authorization' : f'Bearer {st.session_state.jwt}',
        'Accept' : 'application/json'
    }


    params = {
        'select' : "data,distinct_document_metadata_document(id,distinct_document_metadata_id),document(pk)",
        'data' : f'ilike.%{search_text}%',
        'document_metadata_definition_id' : 'eq.8'
    }

    # first request should return both revisions
    resp = requests.get(
        internal_url + 'distinct_document_metadata',
        params=params,
        headers=headers
    )
    resp.raise_for_status()

    print(resp.json())

    # enrichments = [{"id" : de['id'], "pk" : de['pk'], "data" : de['data'], "extents" : ",".join([e['extent_start'] for e in de['extent']['sections']]) } for de in resp.json()]
    # enrichments = [{"id" : de['id'], "pk" : de['pk'], "data" : de['data'] } for de in resp.json()]

    filtered = [{"data" : ner['data'], "document_identifier" : ner['document'][0]['pk']} for ner in resp.json()]

    df = pd.DataFrame.from_records(filtered)

    st.session_state.ner_search = df
    st.session_state.ner_search_request = format_request(resp)



st.markdown("""
# Enrich

## Access the document enrichments, in this case deontic lanugage to quickly understand obligations and derogations

""")

st.write("")

# with st.expander('Show Request Code'):

# st.write("## Request Code")
st.button('Click To Execute Enrichment Request For Deontic Language for document "The Control of Asbestos Regulations 2012" - /uksi/2012/632"',on_click=lambda: get_enriched_doc())

st.write("Browse HTTP Request will appear below on click")
st.markdown(st.session_state.docs_list_request,unsafe_allow_html=True)


# with st.expander('Full Document List (Warning Slow to Render)'):
st.table(st.session_state.docs_list)


st.markdown("""
## View all of the Named Entities in a Document generated automatically by the NER algorithm
""")

st.write("")

# with st.expander('Show Request Code'):

# st.write("## Request Code")
st.button('Click To Execute Enrichment Request For Named Entities for document "The Medical Devices Regulations 2002 - /uksi/2002/618"',on_click=lambda: get_enriched_doc1())
st.markdown(st.session_state.docs_list_request1,unsafe_allow_html=True)


# with st.expander('Full Document List (Warning Slow to Render)'):
st.table(st.session_state.docs_list1)

st.markdown("""
## View all of the Named Entities in the Document Corpus
""")

st.button('Click To Execute Enrichment Request For All Named Entities In the Document Corpus',on_click=lambda: get_ner_list())
st.write("Named Entity HTTP Request will appear below on click")
st.markdown(st.session_state.ner_list_request,unsafe_allow_html=True)


# with st.expander('Full Document List (Warning Slow to Render)'):
st.table(st.session_state.ner_list)

st.markdown("""
## Search by Named Entity in the Document Corpus
""")

search_text = st.text_input("search text","child support")

st.button('Click To Search By Named Entity',on_click=lambda: ner_search())
st.write("Named Entity HTTP Request will appear below on click")
st.markdown(st.session_state.ner_search_request,unsafe_allow_html=True)


# with st.expander('Full Document List (Warning Slow to Render)'):
st.table(st.session_state.ner_search)