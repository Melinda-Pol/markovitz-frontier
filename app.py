import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from pandas_datareader import data as wb

#Title
st.title("Efficient Frontier")
image = Image.open('images/compass.jpg')
st.image(image,caption='Photo by AbsolutVision on Unsplash')
st.markdown("*'Diversifying sufficiently among uncorrelated risks can reduce portfolio risk toward zero.'* - Harry Markowitz")
list_stocks = ['MSFT', 'AMZN', 'TSLA', 'PG', 'SPOT']

st.subheader("First approach")
#Mathematics
st.markdown("*Formula*")
st.latex(r'''Maximize Rp = \sum_{i=1}^{n} XiRi
''')
st.text("Xi: Portfolio weights")
st.text("Ri: Market Value")

def get_stock(stocks):
    pf = pd.DataFrame()
    for element in stocks:
        pf[element] = wb.DataReader(element, data_source='yahoo', start='2018-01-01')['Adj Close']
    return pf

stocks = get_stock(list_stocks)
st.subheader("Stocks table")
st.table(stocks.tail(5))

st.subheader('Stocks visualization')
chart_data = (stocks/stocks.iloc[0]*100)
st.line_chart(chart_data)

#Return calculation
st.subheader("Calculating returns")
st.latex(r''' Rt = \left(\frac{Q_t}{Q_t-1}-1\right)
''')

#Actualization percentage day-by-day
def profit_calc(stocks):
    return stocks.pct_change()


profit = profit_calc(stocks)
profit.dropna()
st.text("Formula Stock profit")
st.write(profit.sum())

st.subheader("Formula Stock Log profit")
st.latex(r''' rlog = \left(\frac{ln(\frac{V_f}{V_i})}{t}\right)
''')

def profit_log(stocks):
    return np.log(stocks) - np.log(stocks.shift(1))

log_profit = profit_log(stocks)
log_profit.dropna()
st.write(log_profit.sum())
st.write("Mean profit:", log_profit.sum().mean())

st.subheader("Optimization for cryptocurrencies users portfolio")
st.text("Assigne random weights")
# Random weights
num_stocks = len(list_stocks)
random_array = np.random.random(num_stocks)
weights = np.random.random(num_stocks)
weights /= np.sum(weights) #stock1 = stock1/stock1+stock2+stock3
st.write(weights)

#Calculating return
calc_profit = np.sum(weights*log_profit.mean())*252 #Days of trading in 2021
st.write("Profit calculated giving random weights", calc_profit)

#Variance calculation
variance = np.dot(weights.T, np.dot(log_profit.cov()*252, weights))
st.write("Variance:",variance)
volatility = np.sqrt(variance)
st.write("Volatility:", volatility)

if st.button('Simulation'):
    pass
