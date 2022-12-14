import streamlit as st
import random
import numpy as np
from numpy.fft import fft, ifft
import pandas as pd
st.set_page_config(layout="wide")


st.title("FFT Example")


rdata = np.random.normal(0, 2, 100)
st.line_chart(rdata)
randomwave = np.sin(np.linspace(0, 10, 100))
st.write("The random wave looks like this:")
st.line_chart(randomwave)

st.write("The sum of the data multiplied by the wave is:")
st.area_chart(rdata * randomwave)

st.write("This would sum up to: ")
st.write(np.sum(rdata * randomwave))


num_waves = st.slider("Number of waves", 1, 10, 5)

# Create some random data
freqs = [random.randint(1, 20) for _ in range(num_waves)]
amps = [random.randint(1, 15) for _ in range(num_waves)]

# create the waves as lists 
x = np.linspace(0, 10, 1000)
waves = [amps[i] * np.sin(freqs[i] * x) for i in range(num_waves)]

# waves as dataframe with index as column name
waves_df = pd.DataFrame(waves).T

st.line_chart(waves_df)
# add them together
inp_signal = np.sum(waves, axis=0)
st.line_chart(inp_signal)

## Transform the added data into frequency domain
X = fft(inp_signal)
N = len(X)
n = np.arange(N)
T = N/1000
freq = n/T 

# plot each frequency of the fft 

# st.line_chart(freq)
data = ifft(X)
st.line_chart(data.real)
st.line_chart(np.abs(X))

new_waves = [amps[i] * np.sin(freq[i] * x) for i in range(num_waves)]
new_waves_df = pd.DataFrame(new_waves).T
st.line_chart(new_waves_df)
inp_signal1 = np.sum(new_waves_df.T, axis=0)
st.line_chart(inp_signal1)