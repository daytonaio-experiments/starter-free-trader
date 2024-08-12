import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from datetime import date, timedelta
from scipy.optimize import newton
from scipy.optimize import brentq
from scipy.stats import norm
import py_vollib
from py_vollib.black_scholes.implied_volatility import implied_volatility as iv


# Calculate Exponential Moving Averages (EMAs)

# Fetch data function using yfinance
def fetch_data(ticker, years, date):
    start = (date - timedelta(days=years * 365)).strftime('%Y-%m-%d')
    end = date.strftime('%Y-%m-%d')
    df = yf.download(ticker, start=start, end=end)
    return df['Adj Close'].values, df.index.values

def calculate_ema(values, span):
    alpha = 2 / (span + 1)
    ema_values = np.zeros_like(values)
    ema_values[0] = values[0]
    for i in range(1, len(values)):
        ema_values[i] = alpha * values[i] + (1 - alpha) * ema_values[i - 1]
    return ema_values


def signal_present(small_ema, big_ema):
  if small_ema[-1] > big_ema[-1]:
    return 1
  elif small_ema[-1] < big_ema[-1]:
    return -1
  else:
    return 0

# Black-Scholes Option Pricing Model Functions

def blackscholes_put(S, K, T, r, sigma):
    """Calculate Black-Scholes put option price and Greeks."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price, d1, d2


def greeks_put(S, K, T, r, sigma, q=0):
    """Calculate the Greeks for a call option."""
    put_price, d1, d2 = blackscholes_put(S, K, T, r, sigma)
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2))
    rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    return put_price, delta, gamma, vega, theta, rho


def buy(direction, delta, stock_price, put_price, prev_delta, prev_put, prev_price):
  pnl=0
  if direction == 'buy':
    # Buy stocks and sell options, so we get money from the selling and invest money in the buying
    pnl += (stock_price - prev_price) * (delta - prev_delta) + (prev_put - put_price)
    stocks = stock_price * delta
    puts = put_price
  elif direction == 'sell':
    # Sell stocks and buy options, so we get money from the selling and invest money in the buying
    pnl += (stock_price - prev_price) * (delta - prev_delta) + (prev_put - put_price)
    stocks = stock_price * delta
    puts = put_price
  return stocks, puts, pnl


def EMA_trader(ticker, date=date.today()):
  # Fetch data
  # 1 year and 1 day
  prices, dates = fetch_data(ticker, 1 + 2/250, date)
  stock = yf.Ticker(ticker)
  # Calculate EMA
  small_ema = calculate_ema(prices, 20)
  big_ema = calculate_ema(prices, 35)


  # Get historical market data
  hist = stock.history(period="5y")

  # Divide data into training (first 4 years) and testing (last year) sets
  training_data = hist[:-250]  # Assuming 252 trading days per year
  testing_data = hist[-250:]

  # Calculate annualized volatility from training data
  sigma = np.std(training_data['Close'].pct_change().dropna()) * np.sqrt(252)  # Annualized volatility

  # Calculate current stock price from testing data
  current_price = testing_data['Close'].iloc[0]


  # Example parameters for option pricing
  S = current_price
  K = S * 1.05  # Assuming strike price is 5% above current price
  T = 1  # 1 year to expiration
  risk_free_rate = 0.05  # Assuming a 5% risk-free rate for simplicity

  # Calculate option price and Greeks
  put_price, delta, gamma, vega, theta, rho = greeks_put(S, K, T, risk_free_rate, sigma)
  print(f"Put Price: {put_price:.2f}, Delta: {delta:.2f}, Gamma: {gamma:.2f}, Vega: {vega:.2f}, Theta: {theta:.2f}, Rho: {rho:.2f}")

  # Set parameters of total investment and get testing data
  total_investment = 100000
  testing_prices = testing_data['Close']

  # Initial portfolio value
  initial_portfolio_value = total_investment

  # Calculate daily returns
  portfolio = [[],[],[]]
  # Initial asset allocation
  stock_price_past = current_price
  put_price_past = put_price
  pnl = 0
  stocks = delta * total_investment
  puts = put_price

  transactions= []

  quantity = total_investment/S

  for i, (date, price) in enumerate(testing_prices.items()):

    # calculate the greeks
    put_price, delta, gamma, vega, theta, rho = greeks_put(price, K, T - (i / len((testing_prices))), risk_free_rate, sigma)
    # update the pnl based on the opening prices and the new put value
    cash = total_investment - stocks - puts
    put_price_past = put_price
    stock_price_past = price
    # update the total investment
    total_investment = pnl + cash
    # add the values to the history tracker
    portfolio[0].append(stocks)
    portfolio[1].append(puts)
    if i == 0:
      prev_put = put_price
      prev_price = price
      prev_delta = delta

  # Buy/sell based on the EMA
    if small_ema[i] < big_ema[i] and small_ema[i+1] >= big_ema[i+1]:
      stocks, puts, pnl = buy('buy', delta, price, put_price, prev_delta, prev_put, prev_price)
      pnl*=quantity
      print(f'buy EMA, delta {delta}, stock price {price}, previous price {prev_price}, pnl {pnl}')
      portfolio[2].append(pnl)
      transactions.append(i)
      prev_delta = delta
      prev_put = put_price
      prev_price = price
    elif small_ema[i] > big_ema[i] and small_ema[i+1] <= big_ema[i+1]:
      stocks, puts, pnl = buy('sell', delta, price, put_price, prev_delta, prev_put, prev_price)
      pnl*=quantity
      print(f'sell EMA, delta {delta}, stock price {price}, previous price {prev_price}, pnl {pnl}')
      portfolio[2].append(pnl)
      transactions.append(i)
      prev_delta = delta
      prev_put = put_price
      prev_price = price
    else:
      portfolio[2].append(0)

  # Buy/sell based on the EMA on the last day to find the unrealised portfolio
  if small_ema[250] >= big_ema[250]:
    stocks, puts, pnl = buy('buy', delta, price, put_price, prev_delta, prev_put, prev_price)
    pnl*=quantity
    print(f'buy EMA, delta {delta}, stock price {price}, previous price {prev_price}, pnl {pnl}')
    portfolio[2].append(pnl)
    transactions.append(i)
    prev_delta = delta
    prev_put = put_price
    prev_price = price
  elif small_ema[250] <= big_ema[250]:
    stocks, puts, pnl = buy('sell', delta, price, put_price, prev_delta, prev_put, prev_price)
    pnl*=quantity
    print(f'sell EMA, delta {delta}, stock price {price}, previous price {prev_price}, pnl {pnl}')
    portfolio[2].append(pnl)
    transactions.append(i)
    prev_delta = delta
    prev_put = put_price
    prev_price = price



  # Plotting
  pnl = portfolio[2]
  cumulative_returns = np.cumsum(pnl)/quantity + S
  # EMAs
  plt.figure(figsize=(12, 6))
  plt.plot(prices, label='Adjusted Close Prices')
  plt.plot(small_ema, label=f'EMA 20', color='red')
  plt.plot(big_ema, label=f'EMA 35', color='green')
  plt.plot(cumulative_returns, label=f'Return', color='blue')
  plt.title(f'{ticker} Adjusted Close Prices and 20-35-Day EMA')
  plt.xlabel('Date')
  plt.ylabel('Price')
  plt.legend()
  plt.grid(True)
  plt.show()



  # Plot cumulative returns
  plt.plot(cumulative_returns-S)
  plt.title('Daily Returns of the Hedged Portfolio')
  plt.xlabel('Days')
  plt.ylabel('Daily Returns')
  plt.grid(True)
  plt.show()

  print(f'ROI % on {ticker}: {100*(cumulative_returns[-1]-S)/S}')


### Test the code with different stocks
EMA_trader('MSFT')
EMA_trader('JPM')
EMA_trader('AAPL')
EMA_trader('GOOGL')
EMA_trader('KO')
EMA_trader('MCD')
EMA_trader('GRF')
EMA_trader('GS')
