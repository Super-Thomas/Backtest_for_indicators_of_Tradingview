import time
import datetime
import math
import sys
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import pyupbit
from Tradingview import Alphatrend as at

########################################################################################################################
# Setting values

# You can change market here.
# For example "KRW-XRP" for Ripple, "KRW-SOL" for Solana, "KRW-DOT" for Polkadot.
MARKET = 'KRW-BTC'
# You can change timeframe here.
# For example "minute30" for 30minute, "minute60" for 1hour, "minute240" for 4hour.
TIMEFRAME = 'minute15'
# Candle count in 1 Day
# This value should be reset according to timeframe value you set.
# For example,
# If your timeframe is "minute60", this value should be 24.
# If your timeframe is "minute30", this value should be 48.
# If your timeframe is "minute240", this value should be 6.
DAY_LIMIT = 96

# Enter the number for test days you want.
TEST_DAYS = 30
# Last date of backtest.
# Until this value.
TO_DATE = '2022-08-08 09:00' # 테스트 기간의 마지막 기간

# First starting seed money
SEED_MONEY = 100000 # KRW(Won)

DELAY = 0.5
########################################################################################################################

def Backtest(ticker):
    positionFlag = 0
    orderPrice = 0
    orderSize = 0
    orderAmount = 0
    winCount = 0
    lossCount = 0
    balance = SEED_MONEY
    winrate = 0

    print(f"[1] Start for get OHLC data from Upbit: {datetime.datetime.now()}")

    ohlcCount = DAY_LIMIT * TEST_DAYS
    df_tz = pyupbit.get_ohlcv(ticker, interval=TIMEFRAME, count=ohlcCount, to=TO_DATE)
    df = df_tz.tz_localize(None)
    time.sleep(DELAY)
    del df['value']

    print(f"[1] End for get OHLC data from Upbit: {datetime.datetime.now()}")

    df['orderPrice'] = ''
    df['orderSize'] = ''
    df['orderAmount'] = ''
    df['result'] = ''
    df['percent'] = ''
    df['resultAmount'] = ''
    df['balance'] = ''
    df['winCount'] = ''
    df['lossCount'] = ''
    df['winrate'] = ''

    print(f"[2] Start for get data from AlphaTrend: {datetime.datetime.now()}")

    at_df = at.AlphaTrend(df)
    df['alphaTrend'] = at_df['AlphaTrend']
    df['buySignalk'] = at_df['buySignalk']
    df['sellSignalk'] = at_df['sellSignalk']

    print(f"[2] End for get data from AlphaTrend: {datetime.datetime.now()}")

    tradeNumber = []
    signal = []
    date = []
    price = []
    size = []
    profitAmount = []
    profitPer = []
    totalAmount = []

    print(f"[3] Start for simulation: {datetime.datetime.now()}")

    tradeNumberCount = 1

    for i in range(1, len(df)):
        if df['buySignalk'].iloc[i - 1] == 1:
            if positionFlag == 0:
                if balance > 0:
                    tradeNumber.append(tradeNumberCount)
                    signal.append('BUY')
                    date.append(df.index[i])
                    df['orderPrice'].iloc[i] = orderPrice = df['open'].iloc[i]
                    price.append(format(orderPrice, ','))
                    df['orderSize'].iloc[i] = orderSize = round(balance / orderPrice, 4)
                    size.append(orderSize)
                    orderAmount = int(balance)
                    df['orderAmount'].iloc[i] = format(orderAmount, ',')
                    profitAmount.append('')
                    profitPer.append('')
                    totalAmount.append('')
                    positionFlag = 1

        elif df['sellSignalk'].iloc[i - 1] == 1:
            if positionFlag == 1:
                tradeNumber.append(tradeNumberCount)
                signal.append('SELL')
                date.append(df.index[i])

                if df['open'].iloc[i] > orderPrice:
                    df['result'].iloc[i] = "WIN"
                    winCount += 1
                else:
                    df['result'].iloc[i] = "LOSE"
                    lossCount += 1

                df['winCount'].iloc[i] = winCount
                df['lossCount'].iloc[i] = lossCount
                if winCount > 0:
                    winrate = (winCount / (winCount + lossCount)) * 100
                else:
                    winrate = 0
                winrate = round(winrate, 2)
                df['winrate'].iloc[i] = f"{winrate}%"

                price.append(format(df['open'].iloc[i], ','))
                size.append(orderSize)
                percent = round((abs(df['open'].iloc[i] - orderPrice) / orderPrice) * 100, 2)
                resultAmount = int((balance * (percent / 100)))

                if df['open'].iloc[i] > orderPrice:
                    balance = balance + resultAmount
                    df['percent'].iloc[i] = f"{percent}%"
                    df['resultAmount'].iloc[i] = format(resultAmount, ',')

                    profitAmount.append(format(resultAmount, ','))
                    profitPer.append(f'{percent}%')
                else:
                    balance = balance - resultAmount
                    df['percent'].iloc[i] = f"-{percent}%"
                    df['resultAmount'].iloc[i] = format(-resultAmount, ',')

                    profitAmount.append(format(-resultAmount, ','))
                    profitPer.append(f'-{percent}%')

                balance = int(balance)
                df['balance'].iloc[i] = format(balance, ',')
                totalAmount.append(format(balance, ','))
                positionFlag = 0

                tradeNumberCount += 1

    print(f"[3] End for simulation: {datetime.datetime.now()}")

    print(f"[4] Start for make excel file for result: {datetime.datetime.now()}")

    output_df = pd.DataFrame()
    output_df['#'] = tradeNumber
    output_df['Signal'] = signal
    output_df['Date'] = date
    output_df['Order Price (KRW)'] = price
    output_df['Order Size'] = size
    output_df['Profit or Loss (KRW)'] = profitAmount
    output_df['Profit or Loss (%)'] = profitPer
    output_df['Balance'] = totalAmount

    title = ticker
    output_df.to_excel(f'Output/{title}_Backtest_Result.xlsx')

    print(f"[4] End for make excel file for result: {datetime.datetime.now()}")

########################################################################################################################
print(f"Backtest: {MARKET}")
Backtest(ticker=MARKET)
