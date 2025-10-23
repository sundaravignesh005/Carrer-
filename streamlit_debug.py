"""
Debug version to check what's happening
"""

import streamlit as st

st.title("🔍 Debug Version")
st.write("If you can see this, the app is working!")

# Test tabs
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

with tab1:
    st.write("This is Tab 1")

with tab2:
    st.write("This is Tab 2")

with tab3:
    st.write("This is Tab 3")

st.write("Tabs should be visible above!")
