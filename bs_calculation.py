import numpy as np
from scipy.stats import norm

def black_scholes(s, k, t, r, sigma, option_type = 'call'):
    d1 = (np.log(s/k) + ((r + sigma**2/2) * t)) / (sigma * np.sqrt(t))
    d2 = d1 - (sigma * np.sqrt(t))

    if option_type == 'call':
        price =  s * norm.cdf(d1) - k * np.exp(-r * t) * norm.cdf(d2)
    elif option_type == 'put':
        price = k * np.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)
    else:
        raise ValueError('option_type must be either "call" or "put"')
    
    return price