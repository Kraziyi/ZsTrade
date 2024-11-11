import requests
import pandas as pd
from src.logger import logger

class AlphaVantageLoader:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://www.alphavantage.co/query'

    def fetch_data(self, function: str, symbol: str, output_size: str = None, interval: str = None):
        try:
            url = f'{self.base_url}?function={function}&symbol={symbol}&apikey={self.api_key}'
            if output_size:
                url += f'&outputsize={output_size}'
            if interval:
                url += f'&interval={interval}'
            r = requests.get(url)
            data = r.json()
            return data

        except Exception as e:
            logger.error(f'Error fetching data from Alpha Vantage: {e}')
            return None

    def get_quote_data(self, symbol: str):
        """
        Get quote data for a given symbol

        Args:
        symbol (str): The stock symbol, e.g. 'NVDA'

        Returns:
        pd.DataFrame: A DataFrame containing the quote data.
        e.g.
        | symbol | open   | high   | low    | price  | volume | latest trading day | previous close | change | change percent |
        |--------|--------|--------|--------|--------|--------|--------------------|----------------|--------|----------------|
        | NVDA   | 100.00 | 105.00 | 99.00  | 102.00 | 10000  | 2024-01-01         | 101.00         | 1.00   | 0.01           |
        """
        data =  self.fetch_data('GLOBAL_QUOTE', symbol)

        if data is None or 'Global Quote' not in data:
            return None
        
        df = pd.DataFrame.from_dict(data['Global Quote'], orient='index').T
        df = self.format_df(df)
        return df


    def get_daily_data(self, symbol: str, output_size: str = 'compact'):
        """
        Get daily data for a given symbol

        Args:
        symbol (str): The stock symbol, e.g. 'NVDA'
        output_size (str): The size of the data to return. Either 'compact' or 'full'

        Returns:
        pd.DataFrame: A DataFrame containing the daily data. 
        e.g.
        |   index    | open   | high   | low    | close  | volume |
        |------------|--------|--------|--------|--------|--------|
        | 2024-01-01 | 100.00 | 105.00 | 99.00  | 102.00 | 10000  |
        | 2024-01-02 | 102.00 | 108.00 | 101.00 | 105.00 | 12000  |
        """
        data =  self.fetch_data('TIME_SERIES_DAILY', symbol, output_size)

        if data is None or 'Time Series (Daily)' not in data:
            return None
        
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        df = self.format_df(df)
        return df

    def get_intraday_data(self, symbol: str, interval: str = '5min', output_size: str = 'compact'):
        data =  self.fetch_data('TIME_SERIES_INTRADAY', symbol, output_size, interval)

        if data is None or f'Time Series ({interval})' not in data:
            return None
        
        df = pd.DataFrame.from_dict(data[f'Time Series ({interval})'], orient='index')
        df = self.format_df(df)
        return df


    def get_weekly_data(self, symbol: str):
        data =  self.fetch_data('TIME_SERIES_WEEKLY', symbol)

        if data is None or 'Weekly Time Series' not in data:
            return None
        
        df = pd.DataFrame.from_dict(data['Weekly Time Series'], orient='index')
        df = self.format_df(df)
        return df
    
    def get_monthly_data(self, symbol: str):
        data =  self.fetch_data('TIME_SERIES_MONTHLY', symbol)

        if data is None or 'Monthly Time Series' not in data:
            return None
        
        df = pd.DataFrame.from_dict(data['Monthly Time Series'], orient='index')
        df = self.format_df(df)
        return df
    
    def get_weekly_adjusted_data(self, symbol: str):
        data =  self.fetch_data('TIME_SERIES_WEEKLY_ADJUSTED', symbol)

        if data is None or 'Weekly Adjusted Time Series' not in data:
            return None
        
        df = pd.DataFrame.from_dict(data['Weekly Adjusted Time Series'], orient='index')
        df = self.format_df(df)
        return df


    def format_df(self, df: pd.DataFrame):
        # Convert the index to datetime
        df.index = pd.to_datetime(df.index)
        # Sort by index
        df = df.sort_index()

        df.columns = [col.split(' ')[-1] for col in df.columns]

        # Convert columns to numeric
        df = df.apply(pd.to_numeric)
        return df