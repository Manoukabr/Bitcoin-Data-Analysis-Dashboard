import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class ChartVisualizer:
    """Class to create interactive charts for cryptocurrency data analysis"""
    
    def __init__(self):
        self.color_palette = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff9800',
            'info': '#17a2b8',
            'background': '#f8f9fa'
        }
    
    def create_price_chart(self, df, selected_indicators=None):
        """
        Create main price chart with candlesticks and technical indicators
        
        Args:
            df (pandas.DataFrame): OHLCV data with technical indicators
            selected_indicators (list): List of indicators to display
            
        Returns:
            plotly.graph_objects.Figure: Interactive price chart
        """
        fig = make_subplots(
            rows=1, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=('Bitcoin Price Chart',),
            row_width=[1.0]
        )
        
        # Add candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='Price',
                increasing_line_color='#26a69a',
                decreasing_line_color='#ef5350'
            ),
            row=1, col=1
        )
        
        # Add technical indicators
        if selected_indicators:
            # Moving averages
            if 'SMA_20' in selected_indicators and 'SMA_20' in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['SMA_20'],
                        mode='lines',
                        name='SMA 20',
                        line=dict(color='blue', width=2)
                    ),
                    row=1, col=1
                )
            
            if 'SMA_50' in selected_indicators and 'SMA_50' in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['SMA_50'],
                        mode='lines',
                        name='SMA 50',
                        line=dict(color='red', width=2)
                    ),
                    row=1, col=1
                )
            
            if 'EMA_12' in selected_indicators and 'EMA_12' in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['EMA_12'],
                        mode='lines',
                        name='EMA 12',
                        line=dict(color='purple', width=2, dash='dash')
                    ),
                    row=1, col=1
                )
            
            if 'EMA_26' in selected_indicators and 'EMA_26' in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['EMA_26'],
                        mode='lines',
                        name='EMA 26',
                        line=dict(color='orange', width=2, dash='dash')
                    ),
                    row=1, col=1
                )
            
            # Bollinger Bands
            if 'Bollinger_Bands' in selected_indicators and all(col in df.columns for col in ['BB_Upper', 'BB_Middle', 'BB_Lower']):
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['BB_Upper'],
                        mode='lines',
                        name='BB Upper',
                        line=dict(color='gray', width=1),
                        showlegend=False
                    ),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['BB_Lower'],
                        mode='lines',
                        name='Bollinger Bands',
                        line=dict(color='gray', width=1),
                        fill='tonexty',
                        fillcolor='rgba(128,128,128,0.1)'
                    ),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['BB_Middle'],
                        mode='lines',
                        name='BB Middle',
                        line=dict(color='gray', width=2),
                        showlegend=False
                    ),
                    row=1, col=1
                )
        
        # Update layout
        fig.update_layout(
            title={
                'text': 'Bitcoin Price Analysis with Technical Indicators',
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            height=600,
            showlegend=True,
            hovermode='x unified',
            xaxis_rangeslider_visible=False
        )
        
        # Update axes
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        
        return fig
    
    def create_rsi_chart(self, df):
        """
        Create RSI indicator chart
        
        Args:
            df (pandas.DataFrame): DataFrame with RSI values
            
        Returns:
            plotly.graph_objects.Figure: RSI chart
        """
        fig = go.Figure()
        
        if 'RSI' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['RSI'],
                    mode='lines',
                    name='RSI',
                    line=dict(color='purple', width=2)
                )
            )
            
            # Add overbought and oversold lines
            fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
            fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
            fig.add_hline(y=50, line_dash="dot", line_color="gray", annotation_text="Neutral (50)")
            
            # Add colored background for zones
            fig.add_hrect(y0=70, y1=100, fillcolor="red", opacity=0.1, layer="below", line_width=0)
            fig.add_hrect(y0=0, y1=30, fillcolor="green", opacity=0.1, layer="below", line_width=0)
        
        fig.update_layout(
            title='RSI (Relative Strength Index)',
            xaxis_title='Date',
            yaxis_title='RSI',
            height=300,
            yaxis=dict(range=[0, 100]),
            showlegend=False
        )
        
        return fig
    
    def create_macd_chart(self, df):
        """
        Create MACD indicator chart
        
        Args:
            df (pandas.DataFrame): DataFrame with MACD values
            
        Returns:
            plotly.graph_objects.Figure: MACD chart
        """
        fig = go.Figure()
        
        if all(col in df.columns for col in ['MACD', 'MACD_Signal', 'MACD_Histogram']):
            # MACD line
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['MACD'],
                    mode='lines',
                    name='MACD',
                    line=dict(color='blue', width=2)
                )
            )
            
            # Signal line
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['MACD_Signal'],
                    mode='lines',
                    name='Signal',
                    line=dict(color='red', width=2)
                )
            )
            
            # Histogram
            colors = ['green' if val >= 0 else 'red' for val in df['MACD_Histogram']]
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df['MACD_Histogram'],
                    name='Histogram',
                    marker_color=colors,
                    opacity=0.6
                )
            )
            
            # Zero line
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
        
        fig.update_layout(
            title='MACD (Moving Average Convergence Divergence)',
            xaxis_title='Date',
            yaxis_title='MACD',
            height=300,
            showlegend=True
        )
        
        return fig
    
    def create_volume_chart(self, df):
        """
        Create volume chart
        
        Args:
            df (pandas.DataFrame): DataFrame with volume data
            
        Returns:
            plotly.graph_objects.Figure: Volume chart
        """
        fig = go.Figure()
        
        if 'volume' in df.columns:
            # Color bars based on price change
            colors = []
            for i in range(len(df)):
                if i == 0:
                    colors.append('gray')
                else:
                    if df['close'].iloc[i] >= df['close'].iloc[i-1]:
                        colors.append('green')
                    else:
                        colors.append('red')
            
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df['volume'],
                    name='Volume',
                    marker_color=colors
                )
            )
        
        fig.update_layout(
            title='Trading Volume',
            xaxis_title='Date',
            yaxis_title='Volume',
            height=200,
            showlegend=False
        )
        
        return fig
    
    def create_correlation_heatmap(self, correlation_matrix):
        """
        Create correlation heatmap
        
        Args:
            correlation_matrix (pandas.DataFrame): Correlation matrix
            
        Returns:
            plotly.graph_objects.Figure: Correlation heatmap
        """
        fig = px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            title="Cryptocurrency Price Correlation Matrix"
        )
        
        fig.update_layout(
            height=400,
            title_x=0.5
        )
        
        return fig
    
    def create_comparison_chart(self, comparison_data):
        """
        Create price comparison chart (normalized)
        
        Args:
            comparison_data (dict): Dictionary with cryptocurrency data
            
        Returns:
            plotly.graph_objects.Figure: Comparison chart
        """
        fig = go.Figure()
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        
        for i, (crypto, data) in enumerate(comparison_data.items()):
            if data is not None and len(data) > 0:
                # Normalize to percentage change from first value
                normalized = ((data['price'] / data['price'].iloc[0]) - 1) * 100
                
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=normalized,
                        mode='lines',
                        name=crypto.title(),
                        line=dict(color=colors[i % len(colors)], width=2)
                    )
                )
        
        fig.update_layout(
            title='Normalized Price Comparison (% Change)',
            xaxis_title='Date',
            yaxis_title='Percentage Change (%)',
            height=500,
            hovermode='x unified'
        )
        
        return fig
    
    def create_metrics_gauge(self, current_value, min_value, max_value, title):
        """
        Create gauge chart for metrics
        
        Args:
            current_value (float): Current value
            min_value (float): Minimum value for scale
            max_value (float): Maximum value for scale
            title (str): Chart title
            
        Returns:
            plotly.graph_objects.Figure: Gauge chart
        """
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = current_value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title},
            gauge = {
                'axis': {'range': [min_value, max_value]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [min_value, min_value + (max_value - min_value) * 0.33], 'color': "lightgray"},
                    {'range': [min_value + (max_value - min_value) * 0.33, min_value + (max_value - min_value) * 0.66], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_value * 0.9
                }
            }
        ))
        
        fig.update_layout(height=300)
        
        return fig
