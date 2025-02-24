import datetime
import numpy as np
import pandas as pd
import ccxt

exchange = ccxt.binance()

def fetchOHLCV(symbol: str, timeframe: str, start: str, limit: int):
	since = datetime.datetime.strptime(start, '%Y-%m-%d')
	df = exchange.fetch_ohlcv(symbol=f'{symbol}', timeframe=timeframe, since=int(datetime.datetime.timestamp(since) * 1000), limit=limit)
	df = pd.DataFrame(df, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
	df['Datetime'] = pd.to_datetime(df['Timestamp'] * 1000 * 1000, utc=True).dt.tz_convert('Asia/Hong_Kong')
	df = df.set_index('Datetime')
	return df

def fetchMultipleOHLCV(symbol: str, timeframe: str, period: list):
	df = pd.DataFrame([])
	for i in period:
		tmp_df = fetchOHLCV(symbol, timeframe, i, 366)
		df = pd.concat([df, tmp_df])
		df.drop_duplicates(subset='Timestamp', inplace=True)
	return df

assert len(fetchMultipleOHLCV('BTC/USDT', '1d', ['2020-01-01', '2021-01-01', '2022-01-01', '2023-01-01'])) == 1462