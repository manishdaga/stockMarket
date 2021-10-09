# importing important liabiary
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import nsepy
import datetime

import plotly
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.offline import init_notebook_mode
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st

st.write('Enter The Stock Name ')
st.text('For Now HDFC,ONGC,RELIANCE,TCS is avaliable')
choice  = st.selectbox('Select from dropdown',options=['HDFC','ONGC','RELIANCE','TCS'])
df = pd.read_csv('{}.csv'.format(choice),index_col='Date')

init_notebook_mode(connected=True)
 
fig  = px.line(x=df.index,y=df['Close'],labels='Closing Price',title='Closing Price')

st.plotly_chart(fig, use_container_width=True)

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Close'],
                    mode='lines',
                    name='Close'))
fig.add_trace(go.Scatter(x=df.index, y=df['Open'],
                    mode='lines',
                    name='Open'))
fig.add_trace(go.Scatter(x=df.index, y=df['High'],
                    mode='lines',
                    name='High'))
fig.add_trace(go.Scatter(x=df.index, y=df['Low'],
                    mode='lines+markers',
                    name='LOW'))

fig.update_layout(title='Share Market Data for 1 Year',
                   xaxis_title='Date',
                   yaxis_title='Price')

st.plotly_chart(fig)



fig = go.Figure([go.Ohlc(x=df.index,
                         open=df.Open,
                         high=df.High,
                         low=df.Low,
                         close=df.Close)])
fig.update_layout(title='Ohcl Open High Close Low',
                   xaxis_title='Date',
                   yaxis_title='High & Low')
fig.update(layout_xaxis_rangeslider_visible=False)
st.plotly_chart(fig)


fig = go.Figure(go.Bar(x=df.index, y=df.Volume, name='Volume', marker_color='red'))

fig.update_layout(title='Volume of Stock',
                   xaxis_title='Date',
                   yaxis_title='Volume ')
st.plotly_chart(fig)



# Moving Averages
df['EMA_9'] = df['Close'].ewm(5).mean().shift()
df['SMA_50'] = df['Close'].rolling(50).mean().shift()
df['SMA_100'] = df['Close'].rolling(100).mean().shift()
df['SMA_200'] = df['Close'].rolling(200).mean().shift()

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df.EMA_9, name='EMA 9'))
fig.add_trace(go.Scatter(x=df.index, y=df.SMA_50, name='SMA 50'))
fig.add_trace(go.Scatter(x=df.index, y=df.SMA_100, name='SMA 100'))
fig.add_trace(go.Scatter(x=df.index, y=df.SMA_200, name='SMA 200'))
fig.add_trace(go.Scatter(x=df.index, y=df.Close, name='Close', line_color='dimgray', opacity=0.3))
fig.update_layout(title='Moving Avearage of Stocks ',
                   xaxis_title='Date',
                   yaxis_title='Moving Avearage ')
st.plotly_chart(fig)

# RSI
def RSI(df, n=14):
    close = df['Close']
    delta = close.diff()
    delta = delta[1:]
    pricesUp = delta.copy()
    pricesDown = delta.copy()
    pricesUp[pricesUp < 0] = 0
    pricesDown[pricesDown > 0] = 0
    rollUp = pricesUp.rolling(n).mean()
    rollDown = pricesDown.abs().rolling(n).mean()
    rs = rollUp / rollDown
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi

num_days = 365
df['RSI'] = RSI(df).fillna(0)
fig = go.Figure(go.Scatter(x=df.reset_index().Date.tail(num_days), y=df.RSI.tail(num_days)))
fig.update_layout(title='RSI  of Stocks ',
                   xaxis_title='Date',
                   yaxis_title='RSI ')
st.plotly_chart(fig)

# MACD
EMA_12 = pd.Series(df['Close'].ewm(span=12, min_periods=12).mean())
EMA_26 = pd.Series(df['Close'].ewm(span=26, min_periods=26).mean())
MACD = pd.Series(EMA_12 - EMA_26)
MACD_signal = pd.Series(MACD.ewm(span=9, min_periods=9).mean())

fig = make_subplots(rows=2, cols=1)
fig.add_trace(go.Scatter(x=df.index, y=df.Close, name='Close'), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=EMA_12, name='EMA 12'), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=EMA_26, name='EMA 26'), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=MACD, name='MACD'), row=2, col=1)
fig.add_trace(go.Scatter(x=df.index, y=MACD_signal, name='Signal line'), row=2, col=1)
fig.update_layout(title='MACD ',
                   xaxis_title='Date',
                   yaxis_title='MACD ')
st.plotly_chart(fig)


def stochastic(df, k, d):
    df = df.copy()
    low_min  = df['Low'].rolling(window=k).min()
    high_max = df['High'].rolling( window=k).max()
    df['stoch_k'] = 100 * (df['Close'] - low_min)/(high_max - low_min)
    df['stoch_d'] = df['stoch_k'].rolling(window=d).mean()
    return df

stochs = stochastic(df, k=14, d=3)

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.reset_index().Date.tail(365), y=stochs.stoch_k.tail(365), name='K stochastic'))
fig.add_trace(go.Scatter(x=df.reset_index().Date.tail(365), y=stochs.stoch_d.tail(365), name='D stochastic'))
fig.update_layout(title='stochastic of STOCKS ',
                   xaxis_title='Date',
                   yaxis_title='stochastic ')
st.plotly_chart(fig)

