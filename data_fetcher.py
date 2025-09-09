import requests
import pandas as pd
import os
from datetime import datetime, timedelta
import time

class DataFetcher:
    """Class to handle cryptocurrency data fetching from CoinGecko API"""
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Bitcoin-Analysis-App/1.0'
        })
        
    def get_current_price(self, coin_id="bitcoin"):
        """
        Fetch current price and market data for a cryptocurrency
        
        Args:
            coin_id (str): CoinGecko coin ID
            
        Returns:
            dict: Current price and market data
        """
        try:
            url = f"{self.base_url}/coins/{coin_id}"
            params = {
                'localization': 'false',
                'tickers': 'false',
                'community_data': 'false',
                'developer_data': 'false',
                'sparkline': 'false'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant market data
            market_data = data['market_data']
            
            return {
                'current_price': market_data['current_price']['usd'],
                'market_cap': market_data['market_cap']['usd'],
                'market_cap_rank': data['market_cap_rank'],
                'total_volume': market_data['total_volume']['usd'],
                'high_24h': market_data['high_24h']['usd'],
                'low_24h': market_data['low_24h']['usd'],
                'price_change_24h': market_data['price_change_24h'],
                'price_change_percentage_24h': market_data['price_change_percentage_24h'],
                'price_change_percentage_7d': market_data.get('price_change_percentage_7d', 0),
                'price_change_percentage_30d': market_data.get('price_change_percentage_30d', 0),
                'market_cap_change_24h': market_data['market_cap_change_24h'],
                'market_cap_change_percentage_24h': market_data['market_cap_change_percentage_24h'],
                'circulating_supply': market_data['circulating_supply'],
                'total_supply': market_data.get('total_supply'),
                'max_supply': market_data.get('max_supply'),
                'ath': market_data['ath']['usd'],
                'ath_change_percentage': market_data['ath_change_percentage']['usd'],
                'ath_date': market_data['ath_date']['usd'],
                'atl': market_data['atl']['usd'],
                'atl_change_percentage': market_data['atl_change_percentage']['usd'],
                'atl_date': market_data['atl_date']['usd'],
                'last_updated': data['last_updated']
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching current price data: {str(e)}")
    
    def get_historical_data(self, coin_id="bitcoin", days="30"):
        """
        Fetch historical price data for a cryptocurrency
        
        Args:
            coin_id (str): CoinGecko coin ID
            days (str): Number of days of historical data
            
        Returns:
            pandas.DataFrame: Historical price data with OHLCV
        """
        try:
            url = f"{self.base_url}/coins/{coin_id}/ohlc"
            params = {
                'vs_currency': 'usd',
                'days': days
            }
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            if not data:
                raise Exception("No historical data returned from API")
            
            # Convert to DataFrame
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            # Ensure all price columns are numeric
            price_columns = ['open', 'high', 'low', 'close']
            for col in price_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Add a price column (using close price)
            df['price'] = df['close']
            
            # Forward fill any NaN values
            df.fillna(method='ffill', inplace=True)
            
            return df
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching historical data: {str(e)}")
    
    def get_simple_price(self, coin_ids, vs_currency="usd"):
        """
        Fetch simple price data for multiple cryptocurrencies
        
        Args:
            coin_ids (list): List of CoinGecko coin IDs
            vs_currency (str): Currency to get prices in
            
        Returns:
            dict: Simple price data
        """
        try:
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': ','.join(coin_ids),
                'vs_currencies': vs_currency,
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true',
                'include_market_cap': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching simple price data: {str(e)}")
    
    def get_market_data(self, coin_id="bitcoin", days="7"):
        """
        Fetch market chart data (price, market cap, volume)
        
        Args:
            coin_id (str): CoinGecko coin ID
            days (str): Number of days of data
            
        Returns:
            dict: Market chart data
        """
        try:
            url = f"{self.base_url}/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily' if int(days) > 90 else 'hourly'
            }
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            # Convert to more usable format
            prices_df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
            market_caps_df = pd.DataFrame(data['market_caps'], columns=['timestamp', 'market_cap'])
            volumes_df = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'volume'])
            
            # Convert timestamps
            for df in [prices_df, market_caps_df, volumes_df]:
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.set_index('timestamp', inplace=True)
            
            # Combine into single DataFrame
            combined_df = prices_df.join(market_caps_df).join(volumes_df)
            
            return combined_df
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching market chart data: {str(e)}")
