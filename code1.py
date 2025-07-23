import pandas as pd
import streamlit as st

st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country wise analysis','Athlete wise analysis')
)
