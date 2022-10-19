import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

t1, t2 = st.tabs(["Matplotlib", "Streamlit"])
with t1:
    st.title("Streamlit Matplotlib Graphs")
    st.write("""
        You can always use st.write() to render markdown here.
        
        st.code can render code right in the document!
    """)
    st.code("""
        print("Hello there!")
        """, language="python")
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

with t2:
    st.title("Streamlit Graphs")

    values = np.random.randn(1000)

    st.line_chart(values)
    st.area_chart(values)
    st.bar_chart(values)

    values = np.random.randn(1000, 2)
    st.table(values[0:25])
