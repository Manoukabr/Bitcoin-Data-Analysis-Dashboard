import pandas as pd
import numpy as np

class TechnicalIndicators:
    """Class to calculate various technical indicators for cryptocurrency data"""
    
    def __init__(self):
        pass
    
    def simple_moving_average(self, data, window):
        """
        Calculate Simple Moving Average (SMA)
        
        Args:
            data (pandas.Series): Price data
            window (int): Period for moving average
            
        Returns:
            pandas.Series: SMA values
        """
        return data.rolling(window=window, min_periods=1).mean()
    
    def exponential_moving_average(self, data, window):
        """
        Calculate Exponential Moving Average (EMA)
        
        Args:
            data (pandas.Series): Price data
            window (int): Period for moving average
            
        Returns:
            pandas.Series: EMA values
        """
        return data.ewm(span=window, adjust=False).mean()
    
    def relative_strength_index(self, data, window=14):
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            data (pandas.Series): Price data
            window (int): Period for RSI calculation
            
        Returns:
            pandas.Series: RSI values
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def macd(self, data, fast=12, slow=26, signal=9):
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            data (pandas.Series): Price data
            fast (int): Fast EMA period
            slow (int): Slow EMA period
            signal (int): Signal line EMA period
            
        Returns:
            tuple: (MACD line, Signal line, MACD histogram)
        """
        ema_fast = self.exponential_moving_average(data, fast)
        ema_slow = self.exponential_moving_average(data, slow)
        
        macd_line = ema_fast - ema_slow
        signal_line = self.exponential_moving_average(macd_line, signal)
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    def bollinger_bands(self, data, window=20, num_std=2):
        """
        Calculate Bollinger Bands
        
        Args:
            data (pandas.Series): Price data
            window (int): Period for moving average
            num_std (int): Number of standard deviations
            
        Returns:
            tuple: (Upper band, Middle band, Lower band)
        """
        sma = self.simple_moving_average(data, window)
        std = data.rolling(window=window).std()
        
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        
        return upper_band, sma, lower_band
    
    def stochastic_oscillator(self, high, low, close, k_period=14, d_period=3):
        """
        Calculate Stochastic Oscillator
        
        Args:
            high (pandas.Series): High price data
            low (pandas.Series): Low price data
            close (pandas.Series): Close price data
            k_period (int): %K period
            d_period (int): %D period
            
        Returns:
            tuple: (%K, %D)
        """
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_period).mean()
        
        return k_percent, d_percent
    
    def williams_r(self, high, low, close, period=14):
        """
        Calculate Williams %R
        
        Args:
            high (pandas.Series): High price data
            low (pandas.Series): Low price data
            close (pandas.Series): Close price data
            period (int): Calculation period
            
        Returns:
            pandas.Series: Williams %R values
        """
        highest_high = high.rolling(window=period).max()
        lowest_low = low.rolling(window=period).min()
        
        williams_r = -100 * ((highest_high - close) / (highest_high - lowest_low))
        
        return williams_r
    
    def average_true_range(self, high, low, close, period=14):
        """
        Calculate Average True Range (ATR)
        
        Args:
            high (pandas.Series): High price data
            low (pandas.Series): Low price data
            close (pandas.Series): Close price data
            period (int): Calculation period
            
        Returns:
            pandas.Series: ATR values
        """
        # True Range calculation
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()
        
        return atr
    
    def calculate_all_indicators(self, df, selected_indicators):
        """
        Calculate selected technical indicators for the given DataFrame
        
        Args:
            df (pandas.DataFrame): OHLCV data
            selected_indicators (list): List of indicators to calculate
            
        Returns:
            pandas.DataFrame: DataFrame with added technical indicators
        """
        result_df = df.copy()
        
        # Ensure we have the required columns
        if 'close' not in result_df.columns:
            if 'price' in result_df.columns:
                result_df['close'] = result_df['price']
            else:
                raise ValueError("DataFrame must contain 'close' or 'price' column")
        
        # Fill missing OHLC columns if not present
        if 'open' not in result_df.columns:
            result_df['open'] = result_df['close']
        if 'high' not in result_df.columns:
            result_df['high'] = result_df['close']
        if 'low' not in result_df.columns:
            result_df['low'] = result_df['close']
        
        # Calculate selected indicators
        for indicator in selected_indicators:
            if indicator == "SMA_20":
                result_df['SMA_20'] = self.simple_moving_average(result_df['close'], 20)
            elif indicator == "SMA_50":
                result_df['SMA_50'] = self.simple_moving_average(result_df['close'], 50)
            elif indicator == "EMA_12":
                result_df['EMA_12'] = self.exponential_moving_average(result_df['close'], 12)
            elif indicator == "EMA_26":
                result_df['EMA_26'] = self.exponential_moving_average(result_df['close'], 26)
            elif indicator == "RSI":
                result_df['RSI'] = self.relative_strength_index(result_df['close'])
            elif indicator == "MACD":
                macd_line, signal_line, histogram = self.macd(result_df['close'])
                result_df['MACD'] = macd_line
                result_df['MACD_Signal'] = signal_line
                result_df['MACD_Histogram'] = histogram
            elif indicator == "Bollinger_Bands":
                upper, middle, lower = self.bollinger_bands(result_df['close'])
                result_df['BB_Upper'] = upper
                result_df['BB_Middle'] = middle
                result_df['BB_Lower'] = lower
            elif indicator == "Stochastic":
                k_percent, d_percent = self.stochastic_oscillator(
                    result_df['high'], result_df['low'], result_df['close']
                )
                result_df['Stoch_K'] = k_percent
                result_df['Stoch_D'] = d_percent
            elif indicator == "Williams_R":
                result_df['Williams_R'] = self.williams_r(
                    result_df['high'], result_df['low'], result_df['close']
                )
            elif indicator == "ATR":
                result_df['ATR'] = self.average_true_range(
                    result_df['high'], result_df['low'], result_df['close']
                )
        
        return result_df
    
    def get_trend_analysis(self, df):
        """
        Analyze trend based on calculated indicators
        
        Args:
            df (pandas.DataFrame): DataFrame with technical indicators
            
        Returns:
            dict: Trend analysis summary
        """
        analysis = {}
        latest = df.iloc[-1]
        
        # Moving average trend
        if 'SMA_20' in df.columns and 'SMA_50' in df.columns:
            if latest['SMA_20'] > latest['SMA_50']:
                analysis['ma_trend'] = 'Bullish'
            else:
                analysis['ma_trend'] = 'Bearish'
        
        # RSI analysis
        if 'RSI' in df.columns:
            rsi = latest['RSI']
            if rsi > 70:
                analysis['rsi_signal'] = 'Overbought'
            elif rsi < 30:
                analysis['rsi_signal'] = 'Oversold'
            else:
                analysis['rsi_signal'] = 'Neutral'
        
        # MACD analysis
        if 'MACD' in df.columns and 'MACD_Signal' in df.columns:
            if latest['MACD'] > latest['MACD_Signal']:
                analysis['macd_signal'] = 'Bullish'
            else:
                analysis['macd_signal'] = 'Bearish'
        
        return analysis
