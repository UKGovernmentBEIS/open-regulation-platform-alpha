#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#
import argparse
import streamlit as st

def args_handler():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', default="127.0.0.1")
    return parser.parse_args()

st.set_page_config(layout="wide")

args = args_handler()

st.markdown("""
# ORP Alpha API Walkthrough Demo
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
### [Login](http://{args.address}:8502/login)
Login to obtain access token (JWT)
### [Browse](http://{args.address}:8503/browse)
Browse the documents in the ORP system
### [Search](http://{args.address}:8504/search)
Search for documents by type and keyword
    """)

with col2:
        st.markdown(f"""
### [Contextual Understanding](http://{args.address}:8505/context1)
Visualise the Document Graph for Contextual Knowledge of Related Documents
### [Monitor](http://{args.address}:8506/monitor)
Subscribe to change relative to me in the Document Graph
### [Explore](http://{args.address}:8507/explore)
Interactively explore the Document Graph
### [Enrich](http://{args.address}:8508/enrich)
Use the document enrichments automatically created by platform AI algorithms
    """)