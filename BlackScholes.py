import streamlit as st
import yfinance as yf
from bs_calculation import black_scholes
from binomial import binomial_tree_fast
from visualizations import generate_heatmap


# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page:", ["Black-Scholes Option Pricer", "Binomial Option Pricing"])

if page == "Black-Scholes Option Pricer":
    st.title('Black-Scholes Option Pricer')

    # Set S to None initially
    S = None

    # Checkbox to choose stock symbol
    use_stock = st.checkbox('Use a stock ticker')
    if use_stock:
        S = 0
        stock_ticker = st.text_input("Enter Stock Ticker (e.g., AAPL for Apple)")
        
        if stock_ticker:
            try:
                stock_data = yf.Ticker(stock_ticker)
                S = stock_data.info.get('currentPrice')  # Fetch the latest price
                st.write(f"Current price of {stock_ticker.upper()}: ${S:.2f}")
            except Exception as e:
                st.write(f"Failed to retrieve data for {stock_ticker.upper()}. Please check the ticker symbol.")
        else:
            st.write("Please enter a stock ticker.")

    # If ticker option not used, allow manual entry
    if not use_stock or S is None:
        S = st.number_input('Asset Price (USD)', value=100.0)

    K = st.number_input('Strike Price (USD)', value=100.0)
    T = st.number_input('Time to Expiration (Years)', value=1.0)
    r = st.number_input('Risk-Free Interest Rate (USD)', value=0.05)
    sigma = st.number_input('Volatility', value=0.2)
    option_type = st.selectbox('Option Type', ('call', 'put'))

    if st.button('Calculate and Generate Heatmap'):
        price = black_scholes(S, K, T, r, sigma, option_type)
        st.write(f'The {option_type} option price is: ${price:.2f}')
        st.write('### Option Price Heatmap')
        sigma_range = (0.1, 0.5)
        S_range = (S / 2, S * 1.5)
        generate_heatmap(S, K, T, r, sigma_range, S_range, option_type)



elif page == "Binomial Option Pricing":
    st.title('Binomial Option Pricing')
    S = None

    # Checkbox to choose stock symbol or manually enter asset price
    use_stock = st.checkbox('Use a stock ticker')
    if use_stock:
        S = 0
        stock_ticker = st.text_input("Enter Stock Ticker (e.g., AAPL for Apple)")
        
        if stock_ticker:
            try:
                stock_data = yf.Ticker(stock_ticker)
                S = stock_data.info.get('currentPrice')  # Fetch the latest price
                st.write(f"Current price of {stock_ticker.upper()}: ${S:.2f}")
            except Exception as e:
                st.write(f"Failed to retrieve data for {stock_ticker.upper()}. Please check the ticker symbol.")
        else:
            st.write("Please enter a stock ticker.")

    # If ticker option not used, allow manual entry
    if not use_stock or S is None:
        S = st.number_input('Asset Price (USD)', value=100.0)

    K = st.number_input('Strike Price (USD)', value=100.0)
    T = st.number_input('Time to Expiration (Years)', value=1.0)
    r = st.number_input('Risk-Free Interest Rate (USD)', value=0.05)
    sigma = st.number_input('Volatility', value=0.2)
    n = st.number_input('Number of Steps (n)', value=100, min_value=1)  # Number of steps for the binomial tree
    option_type = st.selectbox('Option Type', ('call', 'put'))

    if st.button('Calculate Binomial Price and Generate Heatmap'):
        binomial_price = binomial_tree_fast(K, T, S, r, n, sigma, option_type)
        st.write(f'The {option_type} option price using the binomial model is: ${binomial_price:.2f}')
        st.write('### Option Price Heatmap')
        sigma_range = (0.1, 0.5)
        S_range = (S / 2, S * 1.5)
        generate_heatmap(S, K, T, r, sigma_range, S_range, option_type)