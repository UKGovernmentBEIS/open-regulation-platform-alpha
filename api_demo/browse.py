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

init_state(['docs_list','document_titles','docs_list_request','graph1','guidance_search','guidance_search_summary'])

local_css("colorful.css")


def get_docs():
    login()
    r = requests.get(
        base_url + 'api/1.0/documents/',
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {st.session_state.jwt}"
        }
    )
    r.raise_for_status()
    st.session_state.docs_list = r.json()
    st.session_state.document_titles = summarise_docs(r.json()['results'])
    st.session_state.docs_list_request = format_request(r)
    # st.session_state.docs_list_request = "stuff"
    # print(st.session_state.doc_list_request)


st.markdown("""
# Browse

## As a new user of the ORP Platform, I would like to understand what data is present in the platform and it's structure

""")

st.write("")

# with st.expander('Show Request Code'):

# st.write("## Request Code")
st.button('Click To Execute Browse Request',on_click=lambda: get_docs())

st.write("Browse HTTP Request will appear below on click")
st.markdown(st.session_state.docs_list_request,unsafe_allow_html=True)

# st.write(st.session_state.docs_list_request)

st.write("Summary Of First 10 Ten Documents Below:")
st.dataframe(st.session_state.document_titles)

with st.expander('Full Document List (Warning Slow to Render)'):
    st.write(st.session_state.docs_list)

