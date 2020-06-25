'''ccxt data_handler
# Created by steven on 8/10/19.
#	Reads in data from any exchange
	Returns as datafeed for use as input in backtrader
'''
import ccxt
import pandas as pd

'''
More resources
https://github.com/EliteQuant/EliteQuant/blob/master/README.md#quantitative-model
'''
def ccxt_datahandler(pair, exchange, timeframe):
	
	try:
		exchange = getattr (ccxt, exchange) ()
	except AttributeError:
		print('-'*36,' ERROR ','-'*35)
		print('Exchange "{}" not found. Please check the exchange is supported.'.format(exchange))
		print('-'*80)
		quit()
	 
	# Check if fetching of OHLC Data is supported
	if exchange.has["fetchOHLCV"] != True:
		print('-'*36,' ERROR ','-'*35)
		print('{} does not support fetching OHLC data. Please use another exchange'.format(exchange))
		print('-'*80)
		quit()
	 
	# Check requested timeframe is available. If not return a helpful error.
	if (not hasattr(exchange, 'timeframes')) or (timeframe not in exchange.timeframes):
		print('-'*36,' ERROR ','-'*35)
		print('The requested timeframe ({}) is not available from {}\n'.format(timeframe,exchange))
		print('Available timeframes are:')
		for key in exchange.timeframes.keys():
			print('  - ' + key)
		print('-'*80)
		quit()
	 
	# Check if the symbol is available on the Exchange
	exchange.load_markets()
	if pair not in exchange.symbols:
		print('-'*36,' ERROR ','-'*35)
		print('The requested symbol ({}) is not available from {}\n'.format(pair,exchange))
		print('Available symbols are:')
		for key in exchange.symbols:
			print('  - ' + key)
		print('-'*80)
		quit()

	# Get data and convert df to usable format
	data = exchange.fetch_ohlcv(pair, timeframe, since=0)
	header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
	df = pd.DataFrame(data, columns=header).set_index('Timestamp')

	df.index = pd.to_datetime(df.index,unit='ms')
	if pair.split('/')[1]=='BTC':
		df['Open'] = df['Open'].apply(lambda x: x*100000000)
		df['High'] = df['High'].apply(lambda x: x*100000000)
		df['Low'] = df['Low'].apply(lambda x: x*100000000)
		df['Close'] = df['Close'].apply(lambda x: x*100000000)
	return df