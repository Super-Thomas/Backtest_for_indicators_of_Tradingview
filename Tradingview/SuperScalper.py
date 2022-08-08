import time
import datetime
import math
import sys
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import talib as ta
from Tradingview import Indicators

# https://www.tradingview.com/script/4ORGCiTh-Super-Scalper-5-Min-15-Min/
def SuperScalper(df):
    atrlen = 14 #input.int(14, "ATR Period")
    mult = 1 #input.float(1, "ATR Multi", step=0.1)

    ss_df = df.copy()

    ss_df['TR'] = ta.TRANGE(df['high'], df['low'], df['close'])
    ss_df['atr_slen'] = Indicators.ma_function(ss_df['TR'], atrlen)
    ss_df['upper_band'] = ss_df['atr_slen'] * mult + ss_df['close']
    ss_df['lower_band'] = ss_df['close'] - ss_df['atr_slen'] * mult

    #// Create Indicator's
    ShortEMAlen = 21 #input.int(21, "Fast EMA")
    LongEMAlen = 65 #input.int(65, "Slow EMA")
    ss_df['shortSMA'] = ta.EMA(ss_df['close'], ShortEMAlen)
    ss_df['longSMA'] = ta.EMA(ss_df['close'], LongEMAlen)
    RSILen1 = 25 #input.int(25, "Fast RSI Length")
    RSILen2 = 100 #input.int(100, "Slow RSI Length")
    ss_df['rsi1'] = ta.RSI(ss_df['close'], RSILen1)
    ss_df['rsi2'] = ta.RSI(ss_df['close'], RSILen2)
    ss_df['atr'] = ta.ATR(ss_df['high'], ss_df['low'], ss_df['close'], timeperiod=atrlen)

    #//RSI Cross condition
    ss_df['RSILong'] = 0
    ss_df['RSIShort'] = 0
    #// Specify conditions
    ss_df['longCondition'] = 0
    ss_df['shortCondition'] = 0
    ss_df['GoldenLong'] = Indicators.crossover_series(ss_df['shortSMA'], ss_df['longSMA'])
    ss_df['Goldenshort'] = Indicators.crossover_series(ss_df['longSMA'], ss_df['shortSMA'])

    ss_df['result'] = ''

    ss_df['stopLoss'] = ''
    ss_df['takeProfit'] = ''

    last_signal = 0

    for i in range(0, len(ss_df)):
        if ss_df['rsi1'].iloc[i] > ss_df['rsi2'].iloc[i]:
            ss_df['RSILong'].iloc[i] = 1
        if ss_df['rsi1'].iloc[i] < ss_df['rsi2'].iloc[i]:
            ss_df['RSIShort'].iloc[i] = 1

        if ss_df['open'].iloc[i] < ss_df['lower_band'].iloc[i]:
            ss_df['longCondition'].iloc[i] = 1

        if ss_df['open'].iloc[i] > ss_df['upper_band'].iloc[i]:
            ss_df['shortCondition'].iloc[i] = 1

        if ss_df['RSILong'].iloc[i] == 1 and ss_df['longCondition'].iloc[i] == 1:
            if last_signal != 1:
                ss_df['result'].iloc[i] = 1
                ss_df['stopLoss'].iloc[i] = ss_df['low'].iloc[i] - ss_df['atr'].iloc[i] * 2
                ss_df['takeProfit'].iloc[i] = ss_df['high'].iloc[i] + ss_df['atr'].iloc[i] * 5
                last_signal = 1
        if ss_df['RSIShort'].iloc[i] == 1 and ss_df['shortCondition'].iloc[i] == 1:
            if last_signal != 2:
                ss_df['result'].iloc[i] = 2
                last_signal = 2

    return ss_df
