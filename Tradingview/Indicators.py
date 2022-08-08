import time
import datetime
import math
import sys
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import talib as ta

def MFI(df, length=14):
    typical_price = (df['close'] + df['high'] + df['low'])
    money_flow = typical_price + df['volume']
    positive_flow = []
    negative_flow = []

    for i in range(1, len(typical_price)):
        if typical_price[i] > typical_price[i - 1]:
            positive_flow.append(money_flow[i - 1])
            negative_flow.append(0)
        elif typical_price[i] < typical_price[i - 1]:
            negative_flow.append(money_flow[i - 1])
            positive_flow.append(0)
        else:
            positive_flow.append(0)
            negative_flow.append(0)

    positive_mf = []
    negative_mf = []

    for i in range(0, length):
        positive_mf.append(0)
        negative_mf.append(0)

    for i in range(length-1, len(positive_flow)):
        positive_mf.append(sum(positive_flow[i + 1 - length : i + 1]))
    for i in range(length-1, len(negative_flow)):
        negative_mf.append(sum(negative_flow[i + 1 - length : i + 1]))

    mfi = 100 * (np.array(positive_mf) / (np.array(positive_mf) + np.array(negative_mf)))

    return mfi

def crossover_series(x: pd.Series, y: pd.Series, cross_distance: int = None) -> pd.Series:
    shift_value = 1 if not cross_distance else cross_distance
    return (x > y) & (x.shift(shift_value) < y.shift(shift_value))

def crossunder_series(x: pd.Series, y: pd.Series, cross_distance: int = None) -> pd.Series:
    shift_value = 1 if not cross_distance else cross_distance
    return (x < y) & (x.shift(shift_value) > y.shift(shift_value))

def ma_function(source, atrlen):
    return ta.WMA(source, atrlen)
