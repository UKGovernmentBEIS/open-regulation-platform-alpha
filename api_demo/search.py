#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
import requests
import streamlit_bd_cytoscapejs

from common import login,init_state,base_url,format_request,summarise_docs,local_css


init_state(['jwt','docs_list','document_titles','graph1','guidance_search','guidance_search_summary','guidance_search_request'])

local_css("colorful.css")


def search(text,names,state,category=False):
    login()
    r = requests.post(
        base_url + 'api/1.0/search/',
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {st.session_state.jwt}"
        },
        json = {
            "filters" : [{
                "operator" : "and",
                "filter_elements" : [{
                    "document_metadata_category" if category else "document_metadata_name": n,
                    "websearch_tsquery" : text
                } for n in names]
            }]
        }
    )
    r.raise_for_status()
    st.session_state[state] = r.json()
    st.session_state[f"{state}_summary"] = summarise_docs(r.json())
    st.session_state[f"{state}_request"] = format_request(r)

st.markdown("""
# Search
## As a business person working in Asbestos/Net-Zero domain, I would like to understand quickly what guidance I need to adhere to.
""")

st.markdown("""
## Guidance Only Search
""")

# def testing(*args, **kwargs):
#     st.write(args)
#     st.write(kwargs)

metadata_names = st.multiselect("Metadata Names",["orpml_title","orpml_classification"])
guidance_only_search_text = st.text_input("search text","asbestos")

st.button('Click to Make Request to Search Guidance Only',on_click=lambda: search(guidance_only_search_text,metadata_names,'guidance_search'))

st.write("Search HTTP Request will appear below on click")
st.markdown(st.session_state.guidance_search_request,unsafe_allow_html=True)

st.write("Summary Of First 10 Ten Documents Below:")
st.dataframe(st.session_state.guidance_search_summary)


with st.expander('View Complete Guidance Search Results'):
    st.write(st.session_state.guidance_search)


