import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Streamlit Matplotlib Graphs")

values = np.random.randn(1000)

fig, ax = plt.subplots(2)

ax[0].hist(values, color="red")

ax[1].plot(values, color="green")
ax[1].axhline(y=np.nanmean(values), color="red", linestyle="--")

st.pyplot(fig)

values = np.random.randn(1000, 2)

fig, ax = plt.subplots()
ax.scatter(values[:, 0], values[:, 1])

st.pyplot(fig)
