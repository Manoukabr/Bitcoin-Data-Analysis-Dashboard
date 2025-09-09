# Bitcoin Data Analysis Dashboard

## Overview

A real-time Bitcoin data analysis dashboard built with Streamlit that provides cryptocurrency market insights, technical indicators, and interactive visualizations. The application fetches live Bitcoin price data from the CoinGecko API and displays comprehensive market analytics including price charts, technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands), and market statistics. The dashboard features auto-refresh capabilities, customizable time periods for historical data analysis, and interactive Plotly charts for data visualization.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Streamlit Web Framework**: Single-page dashboard application with reactive UI components
- **Interactive Visualizations**: Plotly-based charts with real-time data updates and user controls
- **Session State Management**: Streamlit session state for caching data and maintaining application state
- **Responsive Layout**: Wide layout configuration with expandable sidebar for controls

### Backend Architecture
- **Modular Design Pattern**: Separated concerns across specialized classes:
  - `DataFetcher`: Handles API communication and data retrieval
  - `TechnicalIndicators`: Calculates financial technical analysis indicators
  - `ChartVisualizer`: Creates interactive charts and visualizations
  - `utils`: Provides formatting and calculation utilities
- **Object-Oriented Structure**: Class-based architecture for maintainability and code organization
- **Error Handling**: Built-in exception handling for API failures and data processing errors

### Data Processing
- **Pandas DataFrames**: Primary data structure for time-series analysis and manipulation
- **NumPy Integration**: Mathematical calculations for technical indicators
- **Real-time Data Updates**: Automatic refresh mechanisms with configurable intervals
- **Data Caching**: Session-based caching to minimize API calls and improve performance

### API Integration Pattern
- **RESTful API Client**: HTTP session management with proper headers and timeout handling
- **Rate Limiting Awareness**: Designed to work within CoinGecko API rate limits
- **Data Transformation**: Raw API data converted to analysis-ready formats

## External Dependencies

### Core Framework Dependencies
- **Streamlit**: Web application framework for the dashboard interface
- **Pandas**: Data manipulation and analysis library
- **NumPy**: Numerical computing for mathematical operations
- **Plotly**: Interactive charting and visualization library

### API Services
- **CoinGecko API**: Primary data source for Bitcoin price data, market statistics, and historical information
  - Endpoint: `https://api.coingecko.com/api/v3`
  - No authentication required for basic usage
  - Rate limits apply to free tier usage

### Python Standard Libraries
- **requests**: HTTP client for API communication
- **datetime**: Date and time manipulation for historical data queries
- **time**: Sleep functionality for refresh intervals
- **os**: Environment variable access for configuration

### Visualization Components
- **Plotly Graph Objects**: Advanced chart creation and customization
- **Plotly Express**: Simplified chart generation for quick visualizations
- **Plotly Subplots**: Multi-panel chart layouts for comprehensive analysis