#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
import requests
import streamlit_bd_cytoscapejs

from common import login,init_state,base_url,format_request,summarise_docs,local_css,format_graph_response,graph_layout,graph_style,format_edges


init_state(['jwt','graph','graph_edges'])

local_css("colorful.css")


def get_graph():
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
                    "document_metadata_category": mn,
                    "websearch_tsquery" : search_text
                } for mn in md_filters]
            }],
            "relationship_names" : [f for f in rel_filters],
            "metadata_categories" : ['title']
        }
    )
    r.raise_for_status()
    st.session_state.graph = format_graph_response(r.json())
    st.session_state.graph_edges = format_edges(r)

st.markdown("""
# Explore
""")

rel_names = [
    'legislation_cited_in',
    'guidance_references_legislation',
    'same_named_entity',
    'same_classification'
]

metadata_categories = [
    'title',
    'classification',
    'longtitle',
    'html',
    'raw_text',
    'named_entities',
    'identification',
    'enacted',
    'legislation_cited'
]

rel_filters = st.multiselect("Relationship Names",rel_names)
md_filters = st.multiselect("Metadata Categories",metadata_categories)
search_text = st.text_input("search text","lands tribunal")


st.button('Click To Execute The Document Graph Search',on_click=lambda: get_graph())

col1, col2 = st.columns(2)

with col1:
    node_id = streamlit_bd_cytoscapejs.st_bd_cytoscape(
        st.session_state.graph,
        layout=graph_layout,
        stylesheet=graph_style,
        key='test'
    )
    st.write(node_id)

with col2:
    st.write(st.session_state.graph_edges)
