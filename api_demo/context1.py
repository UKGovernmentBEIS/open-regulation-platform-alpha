#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
import requests
import streamlit_bd_cytoscapejs

from common import login,init_state,base_url,format_request,summarise_docs,local_css,graph_layout,graph_style,format_graph_response,format_edges

init_state(['jwt','graph1','graph1_request','graph1_edges','graph2','graph2_request','graph2_edges'])

local_css("colorful.css")

def get_graph1():
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
                    "websearch_tsquery" : "asbestos"
                }]
            }],
            "relationship_names" : [],
            "metadata_categories" : ['title']
        }
    )
    r.raise_for_status()
    st.session_state.graph1 = format_graph_response(r.json())
    st.session_state.graph1_request = format_request(r)
    st.session_state.graph1_edges = format_edges(r)

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
                    "websearch_tsquery" : "asbestos"
                }]
            }],
            "relationship_names" : ['guidance_references_legislation'],
            "metadata_categories" : ['title']
        }
    )
    r.raise_for_status()
    st.session_state.graph2 = r.json()
    st.session_state.graph2_request = format_request(r)
    st.session_state.graph2_edges = format_edges(r)


st.markdown("""
# Contextual Understanding
## As a compliance officer, I would like to horizon-scan the legislative and regulatory document corpus in specific of
interest so that I can visualise how these documents are related
""")

st.button('Click To Excecute Graph Search',on_click=lambda: get_graph1())
st.write("Graph HTTP Request will appear below on click")
st.markdown(st.session_state.graph1_request,unsafe_allow_html=True)
st.write('')

with st.expander('View First Graph Data'):
    st.write(st.session_state.graph1)

col1, col2 = st.columns(2)

with col1:
    st.markdown("Graph Below shows all document search results that match the filter and the first hop of related documents")
    # with st.expander('View First Graph'):
    node_id = streamlit_bd_cytoscapejs.st_bd_cytoscape(
        st.session_state.graph1,
        layout=graph_layout,
        stylesheet=graph_style,
        key='test'
    )
    st.write(node_id)
with col2:
    st.write(st.session_state.graph1_edges)




st.markdown("""
# Contextual Understanding Continued
Now filter graph using only legislation that is connected to regulation
""")

st.button('Click To Excecute New Graph Search',on_click=lambda: get_graph2())
st.write("Graph HTTP Request will appear below on click")
st.markdown(st.session_state.graph2_request,unsafe_allow_html=True)
st.write('')


col1, col2 = st.columns(2)

with col1:
    st.markdown("Graph below shows the search results and documents related only the the ```guidance_reference_legilsation``` relationship")
    node_id2 = streamlit_bd_cytoscapejs.st_bd_cytoscape(
        st.session_state.graph2,
        layout=graph_layout,
        stylesheet=graph_style,
        key='test2'
    )
    st.write(node_id2)
with col2:
    st.write(st.session_state.graph2_edges)

