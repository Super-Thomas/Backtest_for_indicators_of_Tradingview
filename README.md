# Backtest_for_indicators_of_Tradingview

## Overview
This project can backtest for indicators of [Tradingview](https://www.tradingview.com/). I converted indicators in Pine script to Python script and then simulated it on the past OHLC data from Upbit. Backtest results will output to excel file.

## You need install this modules
1. pyupbit
```python
pip install pyupbit
```
2. ta-lib
```python
pip install ta-lib
```

## How to run
```python
python Backtest.py
```
You can check excel file for backtest result in Ouput folder after this command.

## Supported indicators
1. [AlphaTrend](https://www.tradingview.com/script/o50NYLAZ-AlphaTrend/)
2. [Super Scalper - 5 Min 15 Min](https://www.tradingview.com/script/4ORGCiTh-Super-Scalper-5-Min-15-Min/)
