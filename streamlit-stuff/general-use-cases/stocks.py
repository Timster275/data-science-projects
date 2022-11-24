import requests
# import streamlit as st
import numpy as np
## print current python version


# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=AMZN&apikey=EIH134XGYME5E6N8'
r = requests.get(url)
import pandas as pd
df = pd.DataFrame(np.flip(r.json()['Time Series (Daily)'])).T
# st.dataframe(df)
df.reset_index(inplace=True)
df.drop('index', axis=1, inplace=True)
df = df.astype(float)
df.drop('6. volume', axis=1, inplace=True)
df.drop('7. dividend amount', axis=1, inplace=True)
df = df.reindex(index=df.index[::-1])
df.reset_index(inplace=True)
df.drop('index', axis=1, inplace=True)


# st.dataframe(df)

data = r.json()
d = []
for element in data['Time Series (Daily)']:
    d.append(float(data['Time Series (Daily)'][element]['5. adjusted close']))

# st.line_chart(df)
# predict the next 500 entries of 5. adjusted close
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
X = np.array([i for i in range(len(df))]).reshape(-1,1)
Y = np.array(df['5. adjusted close'])
model = LinearRegression()
model.fit(X, Y)
X_future = np.array([i for i in range(len(df)+500)]).reshape(-1,1)
Y_future = model.predict(X_future)
plt.plot(Y_future)
plt.plot(Y)
plt.show()