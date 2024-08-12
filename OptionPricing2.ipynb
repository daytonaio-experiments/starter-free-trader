import numpy as np
from scipy.stats import norm
import yfinance as yf
import matplotlib.pyplot as plt

# Function to calculate Black-Scholes price
def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    """Calculate Black-Scholes price for call or put option."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

# Function to calculate Vega of the option
def vega(S, K, T, r, sigma):
    """Calculate Vega of the option."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T)

# Function to calculate implied volatility
def implied_volatility(S, K, T, r, market_price, option_type='call', tol=1e-5, max_iter=100):
    """Calculate the implied volatility using the Newton-Raphson method."""
    sigma = 0.2  # Initial guess
    for i in range(max_iter):
        price = black_scholes_price(S, K, T, r, sigma, option_type)
        diff = market_price - price
        if abs(diff) < tol:
            return sigma
        v = vega(S, K, T, r, sigma)
        sigma += diff / v  # Newton-Raphson update
    raise Exception("Implied volatility did not converge")

# Function to calculate Black-Scholes Greeks
def blackscholes_greeks(S, K, T, r, sigma, option_type='call'):
    """Calculate Black-Scholes option price and Greeks."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        delta = norm.cdf(d1)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = norm.cdf(d1) - 1
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) if option_type == 'call' else (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2))
    rho = K * T * np.exp(-r * T) * norm.cdf(d2) if option_type == 'call' else -K * T * np.exp(-r * T) * norm.cdf(-d2)
    return price, delta, gamma, vega, theta, rho

# Fetch historical data
ticker = 'AAPL'
stock = yf.Ticker(ticker)
hist = stock.history(period="5y")
current_price = hist['Close'].iloc[-1]

# Option parameters
K = current_price * 1.05  # Example strike price
T = 1  # 1 year to expiration
r = 0.05  # Risk-free rate

# Market price of the option (example data)
market_call_price = 10  # Example market price of the call option
market_put_price = 8  # Example market price of the put option

# Calculate implied volatility for call and put options
iv_call = implied_volatility(current_price, K, T, r, market_call_price, option_type='call')
iv_put = implied_volatility(current_price, K, T, r, market_put_price, option_type='put')

print(f"Implied Volatility (Call): {iv_call:.4f}")
print(f"Implied Volatility (Put): {iv_put:.4f}")

# Calculate option price and Greeks using implied volatility
call_price, delta_c, gamma_c, vega_c, theta_c, rho_c = blackscholes_greeks(current_price, K, T, r, iv_call, option_type='call')
put_price, delta_p, gamma_p, vega_p, theta_p, rho_p = blackscholes_greeks(current_price, K, T, r, iv_put, option_type='put')

print("\nCall Option:")
print(f"Price: {call_price:.2f}, Delta: {delta_c:.2f}, Gamma: {gamma_c:.2f}, Vega: {vega_c:.2f}, Theta: {theta_c:.2f}, Rho: {rho_c:.2f}")

print("\nPut Option:")
print(f"Price: {put_price:.2f}, Delta: {delta_p:.2f}, Gamma: {gamma_p:.2f}, Vega: {vega_p:.2f}, Theta: {theta_p:.2f}, Rho: {rho_p:.2f}")

# Plot the Greeks for visualization
greeks = {
    'Delta': [delta_c, delta_p],
    'Gamma': [gamma_c, gamma_p],
    'Vega': [vega_c, vega_p],
    'Theta': [theta_c, theta_p],
    'Rho': [rho_c, rho_p]
}

fig, axs = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('Option Greeks')

option_types = ['Call', 'Put']
for i, (greek, values) in enumerate(greeks.items()):
    ax = axs[i // 3, i % 3]
    ax.bar(option_types, values)
    ax.set_title(greek)
    ax.set_ylabel('Value')

plt.tight_layout()
plt.show()
