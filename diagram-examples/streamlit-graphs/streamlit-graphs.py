import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Streamlit Graphs")

values = np.random.randn(1000)

st.line_chart(values)
st.area_chart(values)
st.bar_chart(values)

values = np.random.randn(1000, 2)
st.table(values[0:25])