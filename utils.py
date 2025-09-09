import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def format_currency(value, currency_symbol="$"):
    """
    Format currency values with appropriate suffix (K, M, B)
    
    Args:
        value (float): Currency value
        currency_symbol (str): Currency symbol
        
    Returns:
        str: Formatted currency string
    """
    if pd.isna(value) or value is None:
        return "N/A"
    
    abs_value = abs(value)
    
    if abs_value >= 1e12:
        return f"{currency_symbol}{value/1e12:.2f}T"
    elif abs_value >= 1e9:
        return f"{currency_symbol}{value/1e9:.2f}B"
    elif abs_value >= 1e6:
        return f"{currency_symbol}{value/1e6:.2f}M"
    elif abs_value >= 1e3:
        return f"{currency_symbol}{value/1e3:.2f}K"
    else:
        return f"{currency_symbol}{value:.2f}"

def format_percentage(value, decimal_places=2):
    """
    Format percentage values
    
    Args:
        value (float): Percentage value
        decimal_places (int): Number of decimal places
        
    Returns:
        str: Formatted percentage string
    """
    if pd.isna(value) or value is None:
        return "N/A"
    
    return f"{value:.{decimal_places}f}"

def calculate_percentage_change(old_value, new_value):
    """
    Calculate percentage change between two values
    
    Args:
        old_value (float): Original value
        new_value (float): New value
        
    Returns:
        float: Percentage change
    """
    if pd.isna(old_value) or pd.isna(new_value) or old_value == 0:
        return 0
    
    return ((new_value - old_value) / old_value) * 100

def calculate_volatility(price_data, window=30):
    """
    Calculate price volatility (standard deviation of returns)
    
    Args:
        price_data (pandas.Series): Price data
        window (int): Rolling window for calculation
        
    Returns:
        pandas.Series: Volatility values
    """
    returns = price_data.pct_change()
    volatility = returns.rolling(window=window).std() * np.sqrt(365)  # Annualized
    return volatility

def calculate_sharpe_ratio(price_data, risk_free_rate=0.02):
    """
    Calculate Sharpe ratio for the given price data
    
    Args:
        price_data (pandas.Series): Price data
        risk_free_rate (float): Risk-free rate (annual)
        
    Returns:
        float: Sharpe ratio
    """
    returns = price_data.pct_change().dropna()
    
    if len(returns) == 0:
        return 0
    
    # Annualized return and volatility
    annual_return = (1 + returns.mean()) ** 365 - 1
    annual_volatility = returns.std() * np.sqrt(365)
    
    if annual_volatility == 0:
        return 0
    
    sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
    return sharpe_ratio

def calculate_max_drawdown(price_data):
    """
    Calculate maximum drawdown
    
    Args:
        price_data (pandas.Series): Price data
        
    Returns:
        float: Maximum drawdown percentage
    """
    # Calculate running maximum
    running_max = price_data.expanding().max()
    
    # Calculate drawdown
    drawdown = (price_data - running_max) / running_max
    
    # Return maximum drawdown (most negative value)
    max_drawdown = drawdown.min()
    
    return max_drawdown * 100  # Convert to percentage

def get_price_targets(current_price, support_resistance_levels=None):
    """
    Calculate potential price targets based on technical analysis
    
    Args:
        current_price (float): Current price
        support_resistance_levels (list): List of support/resistance levels
        
    Returns:
        dict: Price targets and levels
    """
    targets = {
        'current': current_price,
        'support_levels': [],
        'resistance_levels': []
    }
    
    if support_resistance_levels:
        for level in support_resistance_levels:
            if level < current_price:
                targets['support_levels'].append(level)
            else:
                targets['resistance_levels'].append(level)
    else:
        # Simple percentage-based targets
        targets['support_levels'] = [
            current_price * 0.95,  # 5% below
            current_price * 0.90,  # 10% below
            current_price * 0.85   # 15% below
        ]
        targets['resistance_levels'] = [
            current_price * 1.05,  # 5% above
            current_price * 1.10,  # 10% above
            current_price * 1.15   # 15% above
        ]
    
    return targets

def validate_dataframe(df, required_columns=None):
    """
    Validate DataFrame structure and data quality
    
    Args:
        df (pandas.DataFrame): DataFrame to validate
        required_columns (list): List of required columns
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if df is None or df.empty:
        return False, "DataFrame is empty or None"
    
    if required_columns:
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return False, f"Missing required columns: {missing_columns}"
    
    # Check for excessive NaN values
    nan_percentage = (df.isnull().sum() / len(df)) * 100
    high_nan_columns = nan_percentage[nan_percentage > 50].index.tolist()
    
    if high_nan_columns:
        return False, f"Columns with >50% NaN values: {high_nan_columns}"
    
    return True, "DataFrame is valid"

def clean_data(df, fill_method='forward'):
    """
    Clean and preprocess cryptocurrency data
    
    Args:
        df (pandas.DataFrame): Raw data
        fill_method (str): Method to fill NaN values ('forward', 'backward', 'interpolate')
        
    Returns:
        pandas.DataFrame: Cleaned data
    """
    df_clean = df.copy()
    
    # Remove duplicate indices
    df_clean = df_clean[~df_clean.index.duplicated(keep='first')]
    
    # Sort by index (timestamp)
    df_clean = df_clean.sort_index()
    
    # Handle NaN values
    if fill_method == 'forward':
        df_clean = df_clean.fillna(method='ffill')
    elif fill_method == 'backward':
        df_clean = df_clean.fillna(method='bfill')
    elif fill_method == 'interpolate':
        df_clean = df_clean.interpolate()
    
    # Remove any remaining NaN values
    df_clean = df_clean.dropna()
    
    # Ensure positive values for price columns
    price_columns = ['open', 'high', 'low', 'close', 'price']
    for col in price_columns:
        if col in df_clean.columns:
            df_clean = df_clean[df_clean[col] > 0]
    
    return df_clean

def get_market_session():
    """
    Determine current market session (useful for global markets)
    
    Returns:
        str: Current market session
    """
    current_hour = datetime.now().hour
    
    if 0 <= current_hour < 8:
        return "Asian Session"
    elif 8 <= current_hour < 16:
        return "European Session"
    elif 16 <= current_hour < 24:
        return "American Session"
    else:
        return "Global Session"

def calculate_fear_greed_index(rsi, volatility, volume_change, price_change):
    """
    Calculate a simplified Fear & Greed Index
    
    Args:
        rsi (float): RSI value
        volatility (float): Volatility percentage
        volume_change (float): Volume change percentage
        price_change (float): Price change percentage
        
    Returns:
        tuple: (index_value, sentiment)
    """
    # Normalize inputs to 0-100 scale
    rsi_score = rsi if 0 <= rsi <= 100 else 50
    
    # Volatility score (lower volatility = higher score)
    vol_score = max(0, min(100, 100 - (volatility * 2)))
    
    # Volume score (higher volume = higher score for trending)
    volume_score = max(0, min(100, 50 + volume_change))
    
    # Price momentum score
    price_score = max(0, min(100, 50 + price_change))
    
    # Weighted average
    fear_greed_index = (rsi_score * 0.3 + vol_score * 0.25 + 
                       volume_score * 0.25 + price_score * 0.2)
    
    # Determine sentiment
    if fear_greed_index >= 75:
        sentiment = "Extreme Greed"
    elif fear_greed_index >= 55:
        sentiment = "Greed"
    elif fear_greed_index >= 45:
        sentiment = "Neutral"
    elif fear_greed_index >= 25:
        sentiment = "Fear"
    else:
        sentiment = "Extreme Fear"
    
    return round(fear_greed_index, 1), sentiment

def format_timestamp(timestamp, format_str="%Y-%m-%d %H:%M:%S"):
    """
    Format timestamp for display
    
    Args:
        timestamp: Timestamp to format
        format_str (str): Format string
        
    Returns:
        str: Formatted timestamp
    """
    if isinstance(timestamp, str):
        return timestamp
    
    try:
        return timestamp.strftime(format_str)
    except:
        return str(timestamp)
