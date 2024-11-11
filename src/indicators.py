import pandas as pd
import pandas_ta as ta

class Indicators:
    @staticmethod
    def calculate_moving_average(data, window=50):
        ma = ta.sma(data['close'], length=window)
        return pd.concat([data, ma.rename(f'MA_{window}')], axis=1)

    @staticmethod
    def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
        macd = ta.macd(data['close'], fast=short_window, slow=long_window, signal=signal_window)
        return pd.concat([data, macd], axis=1)

    @staticmethod
    def calculate_rsi(data, window=14):
        rsi = ta.rsi(data['close'], length=window)
        return pd.concat([data, rsi.rename('RSI')], axis=1)

    @staticmethod
    def calculate_bollinger_bands(data, window=20, num_std_dev=2):
        bbands = ta.bbands(data['close'], length=window, std=num_std_dev)
        return pd.concat([data, bbands], axis=1)

    @staticmethod
    def calculate_all_indicators(data):
        """
        Add Moving Average, MACD, RSI, and Bollinger Bands to the data
        
        Args:
        data: pd.DataFrame

        Returns:
        pd.DataFrame
        """
        data = Indicators.calculate_moving_average(data)
        data = Indicators.calculate_macd(data)
        data = Indicators.calculate_rsi(data)
        data = Indicators.calculate_bollinger_bands(data)
        return data
