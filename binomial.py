import numpy as np

def binomial_tree_fast(K, T, S0, r, N, sigma, option_type='call'):
    #precompute constants
    dt = T/N
    u = np.exp(sigma * np.sqrt(dt))
    d = np.exp( -sigma * np.sqrt(dt) )
    q = (np.exp(r*dt) - d) / (u-d)
    disc = np.exp(-r*dt)

    # initialise asset prices at maturity - Time step N
    C = S0 * d ** (np.arange(N,-1,-1)) * u ** (np.arange(0,N+1,1))

    # initialise option values at maturity
    if option_type == 'call':  # Call option
        C = np.maximum(C - K, np.zeros(N + 1))
    elif option_type == 'put':  # Put option
        C = np.maximum(K - C, np.zeros(N + 1))

    # step backwards through tree
    for i in np.arange(N,0,-1):
        C = disc * ( q * C[1:i+1] + (1-q) * C[0:i] )

    return C[0]