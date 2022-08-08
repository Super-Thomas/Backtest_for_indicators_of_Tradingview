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

# https://www.tradingview.com/script/o50NYLAZ-AlphaTrend/
def AlphaTrend(df):
    at_df = df.copy()
    coeff = 1 #input.float(1, 'Multiplier', step=0.1)
    AP = 14 #input(14, 'Common Period')
    at_df['TR'] = ta.TRANGE(df['high'], df['low'], df['close'])
    at_df['ATR'] = ta.SMA(at_df['TR'], AP)
    novolumedata = False #input(title='Change calculation (no volume data)?', defval=false)

    at_df['upT'] = 0
    at_df['downT'] = 0
    at_df['rsi'] = ta.RSI(df['close'], AP)
    at_df['mfi'] = Indicators.MFI(df, AP)
    at_df['AlphaTrend'] = 0.0

    for i in range(0, len(at_df)):
        at_df['upT'].iloc[i] = at_df['low'].iloc[i] - at_df['ATR'].iloc[i] * coeff
        at_df['downT'].iloc[i] = at_df['high'].iloc[i] + at_df['ATR'].iloc[i] * coeff

    for i in range(1, len(at_df)):
        if novolumedata == True:
            if at_df['rsi'].iloc[i] >= 50:
                at_df['AlphaTrend'].iloc[i] = 1
            else:
                at_df['AlphaTrend'].iloc[i] = 0
        else:
            if at_df['mfi'].iloc[i] >= 50:
                if at_df['upT'].iloc[i] < at_df['AlphaTrend'].iloc[i - 1]:
                    at_df['AlphaTrend'].iloc[i] = at_df['AlphaTrend'].iloc[i - 1]
                else:
                    at_df['AlphaTrend'].iloc[i] = at_df['upT'].iloc[i]
            else:
                if at_df['downT'].iloc[i] > at_df['AlphaTrend'].iloc[i - 1]:
                    at_df['AlphaTrend'].iloc[i] = at_df['AlphaTrend'].iloc[i - 1]
                else:
                    at_df['AlphaTrend'].iloc[i] = at_df['downT'].iloc[i]

    at_df['buySignalk'] = ''
    at_df['sellSignalk'] = ''
    last_signal = 0
    for i in range(3, len(at_df)):
        if at_df['AlphaTrend'].iloc[i] > at_df['AlphaTrend'].iloc[i - 2]:
            if last_signal != 1:
                at_df['buySignalk'].iloc[i] = 1
                last_signal = 1
        if at_df['AlphaTrend'].iloc[i] < at_df['AlphaTrend'].iloc[i - 2]:
            if last_signal != 2:
                at_df['sellSignalk'].iloc[i] = 1
                last_signal = 2

    return at_df
