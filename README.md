Bitcoin Data Analysis Dashboard
Overview

A real-time Bitcoin data analysis dashboard built with Streamlit that provides cryptocurrency market insights, technical indicators, and interactive visualizations. The application fetches live Bitcoin price data from the CoinGecko API and displays comprehensive market analytics including price charts, technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands), and market statistics.

The dashboard features:

Auto-refresh for live data updates

Customizable time periods for historical analysis

Interactive Plotly charts for visualization

Features

Real-time Bitcoin price tracking

Visualization of historical price data

Technical indicators: SMA, EMA, RSI, MACD, Bollinger Bands

Interactive and responsive dashboard with Streamlit

Modular and maintainable code structure

Error handling for API failures

System Architecture
Frontend

Streamlit Web Framework: Single-page dashboard with reactive UI

Interactive Visualizations: Plotly charts with zoom, pan, and filter

Responsive Layout: Sidebar for user controls

Session Management: Caches data to improve performance

Backend

Modular Design:

DataFetcher → fetches data from API

TechnicalIndicators → calculates SMA, EMA, RSI, MACD, Bollinger Bands

ChartVisualizer → creates interactive charts

utils → helper functions for formatting and calculations

Object-Oriented Structure for maintainable code

Error Handling for API and processing failures

Data Processing

Pandas DataFrames for time-series analysis

NumPy for numerical computations

Real-time data updates with configurable refresh intervals

Session-based caching to minimize API calls

API Integration

RESTful API Client: connects to CoinGecko API

Endpoint: https://api.coingecko.com/api/v3

No authentication required for basic usage

Rate-limiting considered for free tier

External Dependencies

Core Libraries: Streamlit, Pandas, NumPy, Plotly

API Services: CoinGecko for Bitcoin price data

Python Standard Libraries: requests, datetime, time, os

Visualization

Plotly Graph Objects: for advanced chart customization

Plotly Express: for simple, quick chart creation

Plotly Subplots: for multi-panel chart layouts

Installation

Clone the repository or create a new Replit project

Install dependencies:

pip install streamlit pandas numpy plotly requests


Run the dashboard:

streamlit run main.py

Usage

Open the dashboard in your browser

Use the sidebar to select time periods and indicators

Explore interactive charts and technical analysis
