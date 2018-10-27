import pandas_datareader.data as web
import pandas as pd
import numpy as np
from talib import RSI, BBANDS
import matplotlib.pyplot as plt

# Input Data
start = '2007-04-22'
end = '2017-04-22'
symbol = 'AAPL'
max_holding = 100
api_key = 's6BYSXJXU2S-nYzdpPUg'

# Define bollinger bands in percentage
def bbp(price):
    up, mid, low = BBANDS(close, timeperiod=200, nbdevup=2, nbdevdn=2, matype=0)
    bbp = (price['AdjClose'] - low) / (up - low)
    return bbp

# Create a DataFrame with quandl
price = web.DataReader(name=symbol, data_source='quandl', start=start, end=end, access_key=api_key)

# Reverse the price DataFrame
price = price.iloc[::-1]

# Removes rows that have NaN values
price = price.dropna()

# Retrieve an array of all 'AdjClose" value
close = price['AdjClose'].values

rsi = RSI(close, timeperiod=150)
bbp = bbp(price)

price['RSI'] = rsi
price['BBP'] = bbp
trend = np.zeros(price.shape[0])
price['Trend'] = trend

days = 100

for i in range(price.shape[0]-days):
    if price.AdjClose[i] > price.AdjClose[i+days]:
        price.Trend[i] = -1
    else:
        price.Trend[i] = 1

# overlap = 0
# peak = False
# for i in range(price.shape[0]-days):
#     original = price['Trend'][i]
#     if overlap == days:
#         peak = False
#     if (peak is True) and (overlap < days):
#         overlap += 1
#         continue
#
#     for d in range(1, days):
#         if price.AdjClose[i+d] > price.AdjClose[i]:
#             price['Trend'][i] = original
#             break
#         # Marking the top
#         peak = True
#         overlap = 0
#         price['Trend'][i] = -1
#
# overlap = 0
# peak = False
# for i in range(price.shape[0]-days):
#     original = price['Trend'][i]
#     if overlap == days:
#         peak = False
#     if (peak is True) and (overlap < days):
#         overlap += 1
#         continue
#
#     for d in range(1, days):
#         if price.AdjClose[i+d] < price.AdjClose[i]:
#             price['Trend'][i] = original
#             break
#         # Marking the top
#         peak = True
#         overlap = 0
#         price['Trend'][i] = 1


# for i in price.iloc[:price.shape[0]-10].AdjClose:
#     largest = 0.0
#     print(i)
#     for d in range(10):
#         print(price.loc[i].AdjClose)
#         if price.loc[i].AdjClose > largest:
#             largest = price.loc[i].AdjClose
#         if d == 9:
#             price['Trend'] = 1
#         else:
#             price['Trend'] = 0
#             break


# Plot graph
fig, (ax0, ax1, ax2) = plt.subplots(3, 1, figsize=(12, 8))
ax0.plot(price.index, price['AdjClose'])
ax0.set_xlabel('Date')
ax0.set_ylabel('AdjClose')
ax0.set_title('McDonalds Plot')
ax0.grid()

for i in range(price.shape[0]):
    if price.Trend[i] == 1:
        ax1.scatter(x=price.RSI[i], y=price.BBP[i], color='green', alpha=0.5)
    if price.Trend[i] == -1:
        ax1.scatter(x=price.RSI[i], y=price.BBP[i], color='red', alpha=0.5)


ax2.plot(price.index, price['RSI'])
ax2.fill_between(x=price.index, y1=70, y2=30, color='#adccff', alpha=0.5)
ax2.grid()
#
# ax2.plot(price.index, price['BBP'])
# ax2.grid()

for i in range(price.shape[0]):
    if price.Trend[i] == 1:
        ax0.scatter(x=price.index[i], y=price.AdjClose[i], color='green')
        # ax1.scatter(x=price.index[i], y=price.RSI[i], color='green')
        # ax2.scatter(x=price.index[i], y=price.BBP[i], color='green')
    if price.Trend[i] == -1:
        ax0.scatter(x=price.index[i], y=price.AdjClose[i], color='red')
        # ax1.scatter(x=price.index[i], y=price.RSI[i], color='red')
        # ax2.scatter(x=price.index[i], y=price.BBP[i], color='red')

fig.tight_layout()
plt.show()

