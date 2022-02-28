#
# Copyright (C) Analytics Engines 2021
# Alastair McKinley (a.mckinley@analyticsengines.com)
#
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
import requests
import streamlit_bd_cytoscapejs

from common import login,init_state,base_url,format_request,local_css

init_state(['jwt','login_request'])


local_css("colorful.css")

st.markdown("""
# Login
""")

user_name = st.text_input('Username','editor@beis.gov.uk')
password = st.text_input('Password','Password1!',type='password')

jwt_output = st.empty()


st.button('Click To Login',on_click=lambda: login(user_name,password))

st.write("Login HTTP Request will appear below on click")
st.markdown(st.session_state.login_request,unsafe_allow_html=True)

st.write({"jwt" : st.session_state.jwt})