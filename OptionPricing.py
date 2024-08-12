import yfinance as yf
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Step 1: Gather Data from Yahoo Finance
# Example stock
ticker = 'AAPL'
stock = yf.Ticker(ticker)

# Get historical market data for volatility calculation
hist = stock.history(period="1y")

# Get current stock price
current_price = stock.history(period="1d")['Close'].iloc[-1]

# Get other necessary data
dividend_yield = stock.info['dividendYield'] or 0
risk_free_rate = 0.05  # Assuming a 5% risk-free rate for simplicity

# Calculate annualized volatility
sigma = np.std(hist['Close'].pct_change()) * np.sqrt(252)  # Annualized volatility

# Step 2: Black-Scholes Option Pricing Model Functions
def black_scholes_call(S, K, T, r, sigma, q=0):
    """Calculate the Black-Scholes call option price."""
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price, d1, d2

def greeks(S, K, T, r, sigma, q=0):
    """Calculate the Greeks for a call option."""
    call_price, d1, d2 = black_scholes_call(S, K, T, r, sigma, q)
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2))
    rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    return call_price, delta, gamma, vega, theta, rho

# Step 3: Example parameters for option pricing
S = current_price
K = S * 1.05  # Assuming strike price is 5% above current price
T = 1  # 1 year to expiration

# Calculate option price and Greeks
call_price, delta, gamma, vega, theta, rho = greeks(S, K, T, risk_free_rate, sigma)
print(f"Call Price: {call_price:.2f}, Delta: {delta:.2f}, Gamma: {gamma:.2f}, Vega: {vega:.2f}, Theta: {theta:.2f}, Rho: {rho:.2f}")

# Step 4: Hedging Strategy
# Number of options to hedge
num_options = 10
hedge_shares = delta * num_options

# If we buy 10 call options, we should short this many shares to delta hedge
print(f"Number of shares to short for delta hedge: {hedge_shares:.2f}")

# Step 5: Visualization of Greeks
# Generate a range of stock prices
S_range = np.linspace(0.5 * S, 1.5 * S, 100)

# Calculate Greeks for each stock price in the range
deltas, gammas, vegas, thetas, rhos = [], [], [], [], []

for S in S_range:
    _, delta, gamma, vega, theta, rho = greeks(S, K, T, risk_free_rate, sigma)
    deltas.append(delta)
    gammas.append(gamma)
    vegas.append(vega)
    thetas.append(theta)
    rhos.append(rho)

# Plotting the Greeks
plt.figure(figsize=(10, 8))

plt.subplot(3, 2, 1)
plt.plot(S_range, deltas, label='Delta')
plt.title('Delta')
plt.xlabel('Stock Price')
plt.ylabel('Delta')
plt.grid(True)

plt.subplot(3, 2, 2)
plt.plot(S_range, gammas, label='Gamma')
plt.title('Gamma')
plt.xlabel('Stock Price')
plt.ylabel('Gamma')
plt.grid(True)

plt.subplot(3, 2, 3)
plt.plot(S_range, vegas, label='Vega')
plt.title('Vega')
plt.xlabel('Stock Price')
plt.ylabel('Vega')
plt.grid(True)

plt.subplot(3, 2, 4)
plt.plot(S_range, thetas, label='Theta')
plt.title('Theta')
plt.xlabel('Stock Price')
plt.ylabel('Theta')
plt.grid(True)

plt.subplot(3, 2, 5)
plt.plot(S_range, rhos, label='Rho')
plt.title('Rho')
plt.xlabel('Stock Price')
plt.ylabel('Rho')
plt.grid(True)

plt.tight_layout()
plt.show()
