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

st.text('Project Build for hackthon')

choice  = st.sidebar.selectbox('Select from dropdown',options=['HDFC','ONGC','RELIANCE','TCS'])
df = pd.read_csv('{}.csv'.format(choice),index_col='Date')
st.write('my name is Harish')

closing_checkbox = st.sidebar.checkbox('Closing Price')
user_selectd_stock = st.sidebar.checkbox('Select Stock you want to plot')
multi_stock = st.sidebar.checkbox('Select Multi Stock  plot')
ma_checkbox = st.sidebar.checkbox('MA')
rsi_check_box = st.sidebar.checkbox('RSI')
macd_check_box = st.sidebar.checkbox('MACD')
stochastic_check_box = st.sidebar.checkbox('Stochastic')

if any([closing_checkbox,user_selectd_stock,multi_stock,ma_checkbox,rsi_check_box,macd_check_box,stochastic_check_box]) is False:

    st.write('Welcome to Stock Market Analysis ')
    
    st.text('For Now HDFC,ONGC,RELIANCE,TCS is avaliable')
    st.text('Or you can upload your own Csv file and analyze ')
    st.image('home_page_img.jpeg')
    st.text_area('If you have any suggestion What to add Next Please Sumbit Hear')
    if st.button('Submit'):
        st.balloons()

    
    





def closing_stock_chart():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'],
                    mode='lines',
                    name='Close'))

    fig.update_layout(title=' Can you See Me.',
                   xaxis_title='Date',
                   yaxis_title='Price')

    st.plotly_chart(fig)

def user_selectd_stock_chart():
    selected_stock = st.selectbox('Select the Stock that you want to plot',list(df.columns))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df[selected_stock],
                    mode='lines',
                    name=selected_stock))
    fig.update_layout(title=' {} Market Data for 1 Year'.format(selected_stock),
                   xaxis_title='Date',
                   yaxis_title='Price')

    st.plotly_chart(fig)


def multi_selected_stock_chart():
    multi_selected_stock = st.multiselect('Select Multipul Stocks  that you want to plot',list(df.columns))
    fig = go.Figure()
    for i in multi_selected_stock:
        fig.add_trace(go.Scatter(x=df.index, y=df[i],
                    mode='lines',
                    name=i))
    
    st.plotly_chart(fig)


def ma_select_stock():


    small_ma = st.sidebar.number_input('Enter Small Ma number',max_value=100,step=5)
    big_ma = st.sidebar.number_input('Chose Big Moving Average',min_value=small_ma + 10,max_value=100,step=5)
    # st.sidebar.number_input('Enter a number',max_value=100,step=5)
    

    fig = go.Figure()

    # Moving Averages
    df['EMA_9'] = df['Close'].ewm(5).mean().shift()
    df['small_ma'] = df['Close'].rolling(small_ma).mean().shift()
    df['big_ma'] = df['Close'].rolling(big_ma).mean().shift()
    # df['SMA_200'] = df['Close'].rolling(200).mean().shift()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df.EMA_9, name='EMA 9'))
    fig.add_trace(go.Scatter(x=df.index, y=df.small_ma, name='Small Ma'))
    fig.add_trace(go.Scatter(x=df.index, y=df.big_ma, name='Big Ma'))
    # fig.add_trace(go.Scatter(x=df.index, y=df.SMA_200, name='SMA 200'))
    fig.add_trace(go.Scatter(x=df.index, y=df.Close, name='Close', line_color='dimgray', opacity=0.3))
    fig.update_layout(title='Moving Avearage of Stocks ',
                    xaxis_title='Date',
                    yaxis_title='Moving Avearage ')
    st.plotly_chart(fig)


def rsi_selectd_stock():
    num_days = st.sidebar.slider('Select Number of Days ',max_value=365,min_value=1)
    # num_days = 365
    df['RSI'] = RSI().fillna(0)
    fig = go.Figure(go.Scatter(x=df.reset_index().Date.tail(num_days), y=df.RSI.tail(num_days)))
    fig.update_layout(title='RSI  of Stocks ',
                    xaxis_title='Date',
                    yaxis_title='RSI ')
    st.plotly_chart(fig)

# RSI
def RSI(n=14):
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

# MACD
def macd_selected_chart():
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



def stochastic_selected_chart():
    k = st.sidebar.slider('Enter k')
    d = st.sidebar.slider('Enter d')
    stochs = stochastic(k, d)


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.reset_index().Date.tail(365), y=stochs.stoch_k.tail(365), name='K stochastic'))
    fig.add_trace(go.Scatter(x=df.reset_index().Date.tail(365), y=stochs.stoch_d.tail(365), name='D stochastic'))
    fig.update_layout(title='stochastic of STOCKS ',
                    xaxis_title='Date',
                    yaxis_title='stochastic ')
    st.plotly_chart(fig)



def stochastic(k=12, d=3):
    df_copy = df.copy()
    low_min  = df_copy['Low'].rolling(window=k).min()
    high_max = df_copy['High'].rolling( window=k).max()
    df_copy['stoch_k'] = 100 * (df_copy['Close'] - low_min)/(high_max - low_min)
    df_copy['stoch_d'] = df_copy['stoch_k'].rolling(window=d).mean()
    return df_copy









if closing_checkbox:
    st.write('closing_checkbox is selcted')
    closing_stock_chart()
if user_selectd_stock:
    st.write('user_selectd_stock is  selected')
    user_selectd_stock_chart()
if multi_stock:
    st.write('multi_stock is  selected')
    multi_selected_stock_chart()
if ma_checkbox:
    st.write('ma_checkbox is  selected')
    ma_select_stock()
if rsi_check_box:
    st.write('rsi_check_box is  selected')
    rsi_selectd_stock()
if macd_check_box:
    macd_selected_chart()
if stochastic_check_box:
    stochastic_selected_chart()

# st.write(closing_checkbox)









 










# fig = go.Figure([go.Ohlc(x=df.index,
#                          open=df.Open,
#                          high=df.High,
#                          low=df.Low,
#                          close=df.Close)])
# fig.update_layout(title='Ohcl Open High Close Low',
#                    xaxis_title='Date',
#                    yaxis_title='High & Low')
# fig.update(layout_xaxis_rangeslider_visible=False)
# st.plotly_chart(fig)


# fig = go.Figure(go.Bar(x=df.index, y=df.Volume, name='Volume', marker_color='red'))

# fig.update_layout(title='Volume of Stock',
#                    xaxis_title='Date',
#                    yaxis_title='Volume ')
# st.plotly_chart(fig)








