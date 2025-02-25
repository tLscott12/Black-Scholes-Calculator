import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from bs_calculation import black_scholes

def generate_heatmap(S, K, T, r, sigma_range, S_range, option_type='call'):
    sigma_values = np.linspace(*sigma_range, 10)
    S_values = np.linspace(*S_range, 10)
    
    price_matrix = np.zeros((len(S_values), len(sigma_values)))
    
    for i, S_val in enumerate(S_values):
        for j, sigma_val in enumerate(sigma_values):
            price_matrix[i, j] = black_scholes(S_val, K, T, r, sigma_val, option_type)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(price_matrix, xticklabels=np.round(sigma_values, 2), yticklabels=np.round(S_values, 2),
                cmap='YlGnBu', cbar_kws={'label': 'Option Price'}, square=True, annot=False)
    plt.xlabel('Volatility (σ)')
    plt.ylabel('Stock Price (S)')
    plt.title(f'{option_type.capitalize()} Option Price Heatmap', fontsize=16, fontweight='bold')
    

    st.pyplot(plt.gcf())
    plt.close()
