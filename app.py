import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import os
from data_fetcher import DataFetcher
from technical_indicators import TechnicalIndicators
from visualizations import ChartVisualizer
from utils import format_currency, format_percentage, calculate_percentage_change

# Configure page
st.set_page_config(
    page_title="Bitcoin Data Analysis Dashboard",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'btc_data' not in st.session_state:
    st.session_state.btc_data = None
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = None

# Initialize classes
data_fetcher = DataFetcher()
tech_indicators = TechnicalIndicators()
chart_viz = ChartVisualizer()

# Title and header
st.title("₿ Bitcoin Data Analysis Dashboard")
st.markdown("Real-time Bitcoin price tracking, technical indicators, and market analysis")

# Sidebar controls
st.sidebar.header("Dashboard Controls")

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("Auto-refresh (every 5 minutes)", value=True)

# Manual refresh button
if st.sidebar.button("Refresh Data Now"):
    st.session_state.last_update = None

# Time period selection for historical data
time_period = st.sidebar.selectbox(
    "Historical Data Period",
    ["7", "30", "90", "365"],
    index=1,
    format_func=lambda x: f"{x} days"
)

# Cryptocurrency comparison
compare_cryptos = st.sidebar.multiselect(
    "Compare with other cryptocurrencies",
    ["ethereum", "cardano", "solana", "polygon", "chainlink"],
    default=["ethereum"]
)

# Technical indicators selection
selected_indicators = st.sidebar.multiselect(
    "Technical Indicators",
    ["SMA_20", "SMA_50", "EMA_12", "EMA_26", "RSI", "MACD", "Bollinger_Bands"],
    default=["SMA_20", "SMA_50", "RSI"]
)

# Data fetching logic
def fetch_data():
    """Fetch and cache data"""
    current_time = datetime.now()
    
    # Check if we need to update data (5 minutes interval for auto-refresh)
    if (st.session_state.last_update is None or 
        (current_time - st.session_state.last_update).total_seconds() > 300):
        
        with st.spinner("Fetching latest Bitcoin data..."):
            try:
                # Fetch current Bitcoin data
                btc_data = data_fetcher.get_current_price("bitcoin")
                
                # Fetch historical data
                historical_data = data_fetcher.get_historical_data("bitcoin", time_period)
                
                # Fetch comparison data
                comparison_data = {}
                for crypto in compare_cryptos:
                    comparison_data[crypto] = data_fetcher.get_historical_data(crypto, time_period)
                
                # Update session state
                st.session_state.btc_data = btc_data
                st.session_state.historical_data = historical_data
                st.session_state.comparison_data = comparison_data
                st.session_state.last_update = current_time
                
                st.sidebar.success(f"Data updated at {current_time.strftime('%H:%M:%S')}")
                
            except Exception as e:
                st.sidebar.error(f"Error fetching data: {str(e)}")
                return False
    
    return True

# Fetch data
if fetch_data():
    btc_data = st.session_state.btc_data
    historical_data = st.session_state.historical_data
    comparison_data = st.session_state.comparison_data
    
    if btc_data and historical_data is not None:
        # Key metrics section
        st.header("📊 Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Current Price",
                format_currency(btc_data['current_price']),
                delta=f"{format_percentage(btc_data['price_change_percentage_24h'])}%"
            )
        
        with col2:
            st.metric(
                "Market Cap",
                format_currency(btc_data['market_cap']),
                delta=f"{format_percentage(btc_data['market_cap_change_percentage_24h'])}%"
            )
        
        with col3:
            st.metric(
                "24h Volume",
                format_currency(btc_data['total_volume'])
            )
        
        with col4:
            st.metric(
                "24h High/Low",
                f"{format_currency(btc_data['high_24h'])} / {format_currency(btc_data['low_24h'])}"
            )
        
        # Additional metrics
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            st.metric(
                "Circulating Supply",
                f"{btc_data['circulating_supply']:,.0f} BTC"
            )
        
        with col6:
            st.metric(
                "Total Supply",
                f"{btc_data.get('total_supply', 21000000):,.0f} BTC"
            )
        
        with col7:
            st.metric(
                "Market Cap Rank",
                f"#{btc_data['market_cap_rank']}"
            )
        
        with col8:
            ath_change = ((btc_data['current_price'] - btc_data['ath']) / btc_data['ath']) * 100
            st.metric(
                "All-Time High",
                format_currency(btc_data['ath']),
                delta=f"{ath_change:.1f}%"
            )
        
        # Price chart section
        st.header("📈 Price Chart & Technical Analysis")
        
        # Calculate technical indicators
        df_with_indicators = tech_indicators.calculate_all_indicators(
            historical_data, 
            selected_indicators
        )
        
        # Create main price chart
        fig = chart_viz.create_price_chart(df_with_indicators, selected_indicators)
        st.plotly_chart(fig, use_container_width=True)
        
        # Technical indicators dashboard
        if any(indicator in selected_indicators for indicator in ["RSI", "MACD"]):
            st.header("🔍 Technical Indicators Dashboard")
            
            indicator_cols = st.columns(len([i for i in selected_indicators if i in ["RSI", "MACD"]]))
            
            col_idx = 0
            if "RSI" in selected_indicators:
                with indicator_cols[col_idx]:
                    rsi_fig = chart_viz.create_rsi_chart(df_with_indicators)
                    st.plotly_chart(rsi_fig, use_container_width=True)
                    col_idx += 1
            
            if "MACD" in selected_indicators:
                with indicator_cols[col_idx]:
                    macd_fig = chart_viz.create_macd_chart(df_with_indicators)
                    st.plotly_chart(macd_fig, use_container_width=True)
        
        # Correlation analysis
        if compare_cryptos and comparison_data:
            st.header("🔗 Cryptocurrency Correlation Analysis")
            
            # Create correlation matrix
            correlation_df = pd.DataFrame()
            correlation_df['Bitcoin'] = historical_data['price']
            
            for crypto in compare_cryptos:
                if crypto in comparison_data and comparison_data[crypto] is not None:
                    crypto_data = comparison_data[crypto]
                    if len(crypto_data) == len(historical_data):
                        correlation_df[crypto.title()] = crypto_data['price']
            
            if len(correlation_df.columns) > 1:
                # Calculate correlation matrix
                corr_matrix = correlation_df.corr()
                
                # Create heatmap
                fig_corr = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    aspect="auto",
                    title="Cryptocurrency Price Correlation Matrix",
                    color_continuous_scale="RdBu_r"
                )
                st.plotly_chart(fig_corr, use_container_width=True)
                
                # Price comparison chart
                fig_comparison = go.Figure()
                
                for column in correlation_df.columns:
                    # Normalize prices to percentage change
                    normalized_prices = ((correlation_df[column] / correlation_df[column].iloc[0]) - 1) * 100
                    fig_comparison.add_trace(
                        go.Scatter(
                            x=historical_data.index,
                            y=normalized_prices,
                            mode='lines',
                            name=column,
                            line=dict(width=2)
                        )
                    )
                
                fig_comparison.update_layout(
                    title="Normalized Price Comparison (% Change)",
                    xaxis_title="Date",
                    yaxis_title="Percentage Change (%)",
                    hovermode='x unified',
                    height=400
                )
                
                st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Data export section
        st.header("💾 Export Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Export historical data
            csv_historical = historical_data.to_csv()
            st.download_button(
                label="Download Historical Data (CSV)",
                data=csv_historical,
                file_name=f"bitcoin_historical_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Export technical indicators
            csv_indicators = df_with_indicators.to_csv()
            st.download_button(
                label="Download Technical Indicators (CSV)",
                data=csv_indicators,
                file_name=f"bitcoin_technical_indicators_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col3:
            # Export current metrics
            metrics_dict = {
                'metric': ['Current Price', 'Market Cap', '24h Volume', '24h Change %', 'Market Cap Rank'],
                'value': [
                    btc_data['current_price'],
                    btc_data['market_cap'],
                    btc_data['total_volume'],
                    btc_data['price_change_percentage_24h'],
                    btc_data['market_cap_rank']
                ]
            }
            metrics_df = pd.DataFrame(metrics_dict)
            csv_metrics = metrics_df.to_csv(index=False)
            st.download_button(
                label="Download Current Metrics (CSV)",
                data=csv_metrics,
                file_name=f"bitcoin_current_metrics_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        # Market sentiment and additional info
        st.header("📰 Market Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Price Statistics")
            stats_data = {
                "Metric": [
                    "Current Price",
                    "24h Change",
                    "7d Change",
                    "30d Change",
                    "All-Time High",
                    "All-Time Low",
                    "Market Cap Rank"
                ],
                "Value": [
                    format_currency(btc_data['current_price']),
                    f"{btc_data['price_change_percentage_24h']:.2f}%",
                    f"{btc_data.get('price_change_percentage_7d', 0):.2f}%",
                    f"{btc_data.get('price_change_percentage_30d', 0):.2f}%",
                    format_currency(btc_data['ath']),
                    format_currency(btc_data['atl']),
                    f"#{btc_data['market_cap_rank']}"
                ]
            }
            stats_df = pd.DataFrame(stats_data)
            st.table(stats_df)
        
        with col2:
            st.subheader("Technical Summary")
            
            latest_data = df_with_indicators.iloc[-1]
            current_price = latest_data['close']
            
            summary_items = []
            
            if 'SMA_20' in df_with_indicators.columns:
                sma_20 = latest_data['SMA_20']
                sma_trend = "Above" if current_price > sma_20 else "Below"
                summary_items.append(f"Price is {sma_trend} 20-day SMA")
            
            if 'SMA_50' in df_with_indicators.columns:
                sma_50 = latest_data['SMA_50']
                sma_trend = "Above" if current_price > sma_50 else "Below"
                summary_items.append(f"Price is {sma_trend} 50-day SMA")
            
            if 'RSI' in df_with_indicators.columns:
                rsi = latest_data['RSI']
                if rsi > 70:
                    rsi_status = "Overbought"
                elif rsi < 30:
                    rsi_status = "Oversold"
                else:
                    rsi_status = "Neutral"
                summary_items.append(f"RSI: {rsi:.1f} ({rsi_status})")
            
            for item in summary_items:
                st.write(f"• {item}")
    
    else:
        st.error("Failed to load Bitcoin data. Please check your internet connection and try again.")

# Auto-refresh logic
if auto_refresh:
    time.sleep(1)  # Small delay to prevent excessive API calls
    st.rerun()

# Footer
st.markdown("---")
st.markdown("**Data provided by CoinGecko API** | **Built with Streamlit**")
if st.session_state.last_update:
    st.caption(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
