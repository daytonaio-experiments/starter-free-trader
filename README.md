# Starter Free Trader

## A systematic trading algorithm

### Motivation and initial approach

This project came from the idea of wanting to develop a systematic trading program, which autonomously managed a portfolio for its user. 

The initial project -seen in the PortfolioModel file- was a simple stock selection from a basket of 6 stocks. Inspired by Markowitz's Modern Portfolio Theory, we sought to maximize the return for a given level of risk. By downloading market data from the past 3 years, we calculated the average volatility of each equity, as well as its return on investment (ROI). From this data, we simulate a large number of portfolios, giving different weights to the different equities in each of the portfolios, and reach a portfolio with the maximum Sharpe ratio, meaning that it is optimized for risk versus ROI.

Nevertheless, the problem remained that this wasn't a systematic trading program, as it only interacted with the market at the beginning of the simulation, where it selected the weight each stock should be given, and then held those stocks until the end.

### Exponential Moving Averages and Decision-making 

In order to develop a systematic approach, we had to design an algorithm which would interact with the market at several points during the simulation. So the issue arised of when should it make its moves.

We decided to use the popular strategy of Exponential Moving Averages (EMA), which give a decent framework for us to know when a stock's price is moving up or down in price. Basically, we calculate the EMA of the stock price of 2 different time periods -in our case we chose a 20 day period for the small EMA, and a 35 day period for the large EMA. Intuitively, if the stock price is moving up for some time, the small EMA will have a bigger value than the big EMA (simply because the big EMA will also take into account earlier data in which the stock price was lower, given that in this assumption it is going up in price). Similarly, when the big EMA has a bigger value than the small EMA, the stock price will tend to move down. Given that the small and big EMAs will be changing throughout the simulation, we chose the points in which the small EMA and big EMA cross as signals for us to make a trade. Initially, the idea was to buy a fixed amount of stock when the small EMA crossed the big EMA and became bigger in value (and thus the stock price tends to rise), and to sell a fixed amount of stock when the big EMA crossed the small EMA and became bigger in value (and thus the stock price tends to drop).

### Stock options and derivatives

To add a layer of complexity, we also looked at the use of stock options such as calls and puts in order to hedge the risk of the transactions. Additionally, the use of calls and puts adds the complexity of not only having to calculate their pricing using the Black-Scholes formula, but also to calculate the different derivatives in order to better hedge the portfolio.

For this purpose, we first developped the tools to calculate the pricing of options and their respective derivatives in the files called OptionPricing1 and OptionPricing2.

From here, we sought to implement the tools together with the EMA trading strategy -the code can be found in the EMA_trading_with_Options file. The strategy now changed from only buying/selling stocks to also operating with their options. The 2 operations that we can apply are to buy/sell the stock, and buy/sell put options. For those unfamiliar with the functionality of put options, they are a contract between two parties, in which the buyer of the put option has the possibility but not the obligation of selling the underlying stock at a fixed price on the date of maturity of the option (simply put as an example: I have a stock with a high volatility which trades at $100 per share, and I pay $10 to another trader for a put option in which I have the possibility but not the obligation to sell him my stock at $100 in one year's time. If the stock goes up, I can keep the stock. However, given that the stock has a lot of volatility, if it went down to $80 per share, I can exercise my option to sell it at the aforementioned price of $100, which limits my potential downside on owning the stock). These put options go up in value as the stock drops in price, and go down in value as the stock goes up. As their value moves opposite to the value of the underlying stock, we can use them to hedge our portfolio. Additionally, we can also use them to doubly capitalize on price movements -if we believe a stock will go up, we can sell some of our puts (which will go down in value) to gain cash, and use it to buy more stocks.

Initially, with the EMA strategy we bought and sold a fixed amount of stock at each transaction, but it is also important to note that the option's price doesn't move the same amount if it is in deep In the Money or Out of the Money positions. For this, instead of buying/selling an arbitrary amount of stocks and options at each transaction, we used delta hedging to figure out the amount we should trade in each case.

## Features
- **Retrieve Historical Data:** Pulls stock data from sources like Yahoo Finance using `yfinance` and `pandas_datareader`.
- **Options Pricing Models:** Implements the Black-Scholes model and other pricing strategies using `py_vollib`.
- **Mathematical Computations:** Leverages `numpy` and `scipy` for numerical operations.
- **Visualization:** Plots the performance of different pricing strategies using `matplotlib`.

## Libraries and Tools
- **yfinance:** Downloads stock data from Yahoo Finance.
- **numpy:** Provides tools for matrix operations and numerical calculations.
- **matplotlib:** Plots graphs and visualizes pricing strategies.
- **pandas_datareader:** Fetches data from Yahoo Finance and other sources.
- **scipy:** Supports optimization and advanced math functions.
- **py_vollib:** Implements Black-Scholes and other pricing models.

## Starter Free Trader Results
ROI on different stocks when backtesting the tradding algorithm over the past year:
- MSFT: +21.1% (+28.9% stock performance)
- MCD: +2.3% (-5.0% stock performance)
- JPM: +32.8% (+39.5% stock performance)
- AAPL: +24.0% (+22.7% stock performance)
- GOOGL: +22.8% (+28.3% stock performance)
- KO: +16.5% (+16.4% stock performance)
- GRFS: +2.2% (-29.4% stock performance)
- GS: +35.7% (45.8% stock performance)

**Observations:** Even though the performance of the algorithm was below the stock's performance in some cases, it has to be noted that this was a specifically bullish year for a lot of stocks. When considering that this trader is designed to hedge the risk of each trade instead of making a directional strategy, it has worked as expected. It is difficult to outperform a stock that increases its price by 39.5% in a single year, as did the stock of JPM, when we are trying to hedge in case there is a downturn. Nevertheless, when looking at stocks that have gone down in price, such as is the case of GRFS or MCD, that have dropped 29.4% and 5.0% respectively, the trader not only did not loose any money, but made small gains of 2.2% in both cases. Given that the objective of the algorithm was not only to maximize the profit, but to also minimize the risk, we can consider the Starter Free Trader algorithm to have been a success.

## Setting Up Workspace for the Project with Daytona
### Requirements:

Preinstalled Daytona and Docker.
Steps to Set Up Daytona Workspace:

**Create Daytona Workspace:**

**Clone the repository into a Daytona workspace:**

```bash
daytona create https://github.com/yourusername/option-pricing-app.git
```
Select Preferred IDE:
```bash
daytona ide
```
Open the Workspace:
```bash
daytona code
```

## Running the Option Pricing App
### Daytona devcontainer.json Configuration

**Here is a simplified devcontainer.json configuration used for this project:**

```json
{
    "name": "Python Finance Dev Container",
    "build": {
        "dockerfile": "Dockerfile",
        "context": ".."
    },
    "features": {
        "ghcr.io/devcontainers/features/common-utils:2.4.7": {
            "username": "daytona",
            "userUid": 1000,
            "userGid": 1000,
            "configureZshAsDefaultShell": true
        }
    },
    "customizations": {
        "vscode": {
            "settings": {
                "python.pythonPath": "/usr/local/bin/python3"
            },
            "extensions": [
                "ms-python.python",
                "ms-toolsai.jupyter"
            ]
        }
    },
    "forwardPorts": [],
    "postCreateCommand": "pip install --no-cache-dir -r requirements.txt",
    "postStartCommand": "git config --global --add safe.directory ${containerWorkspaceFolder}",
    "remoteUser": "daytona"
}
```
This configuration ensures the environment is equipped with Python 3.10, common utilities, and essential VSCode extensions.

## Why Daytona?
Daytona is a radically simple open source development environment manager.

Setting up development environments has become increasingly challenging over time, especially when aiming to set up remotely, where the complexity increases by an order of magnitude. The process is so complex that we've compiled a comprehensive guide detailing all the necessary steps to set one up—spanning 5,000 words, 7 steps, and requiring anywhere from 15 to 45 minutes.

This complexity is unnecessary.

With Daytona, you need only to execute a single command: daytona create --code.

Daytona automates the entire process; provisioning the instance, interpreting and applying the configuration, setting up prebuilds, establishing a secure VPN connection, securely connecting your local or a Web IDE, and assigning a fully qualified domain name to the development environment for easy sharing and collaboration.

As a developer, you can immediately start focusing on what matters most—your code.

## Getting Started

### Requirements

Before starting the installation script, please go over all the necessary requirements:

- **Hardware Resources**: Depending on the project requirements, ensure your machine has sufficient resources. Minimum hardware specification is 1cpu, 2GB of RAM and 10GB of disk space.
- **Docker**: Ensure [Docker](https://www.docker.com/products/docker-desktop/) is installed and running.

### Initializing Daytona

To initialize Daytona, follow these steps:

**1. Start the Daytona Server:**
This initiates the Daytona Server in daemon mode. Use the command:

```bash
daytona server
```

**2. Add Your Git Provider of Choice:**
Daytona supports GitHub, GitLab, Bitbucket, Bitbucket Server, Gitea, Gitness and Azure DevOps. To add them to your profile, use the command:

```bash
daytona git-providers add

```

Follow the steps provided.

**3. Add Your Provider Target:**
This step is for choosing where to deploy Development Environments. By default, Daytona includes a Docker provider to spin up environments on your local machine. For remote development environments, use the command:

```bash
daytona target set
```

Following the steps this command adds SSH machines to your targets.

**4. Choose Your Default IDE:**
The default setting for Daytona is VS Code locally. If you prefer, you can switch to VS Code - Browser or any IDE from the JetBrains portfolio using the command:

```bash
daytona ide
```

Now that you have installed and initialized Daytona, you can proceed to setting up your development environments and start coding instantly.

### Creating Dev Environments

Creating development environments with Daytona is a straightforward process, accomplished with just one command:

```bash
daytona create --code
```

You can skip the `--code` flag if you don't wish to open the IDE immediately after creating the environment.

Upon executing this command, you will be prompted with two questions:

1. Choose the provider to decide where to create a dev environment.
2. Select or type the Git repository you wish to use to create a dev environment.

After making your selections, press enter, and Daytona will handle the rest. All that remains for you to do is to execute the following command to open your default IDE:

```bash
daytona code
```

This command opens your development environment in your preferred IDE, allowing you to start coding instantly.

### Stopping the Daytona Server:

```bash
daytona server stop
```

### Restarting the Daytona Server:

```bash
daytona server restart
```

## License

This repository contains Daytona, covered under the [Apache License 2.0](https://github.com/daytonaio/daytona/blob/main/LICENSE), except where noted (any Daytona logos or trademarks are not covered under the Apache License, and should be explicitly noted by a LICENSE file.)

Daytona is a product produced from this open source software, exclusively by Daytona Platforms, Inc. It is distributed under our commercial terms.

Others are allowed to make their own distribution of the software, but they cannot use any of the Daytona trademarks, cloud services, etc.

We explicitly grant permission for you to make a build that includes our trademarks while developing Daytona itself. You may not publish or share the build, and you may not use that build to run Daytona for any other purpose.

## Legal disclaimer
This material has been prepared for informational purposes only, and is not intended to provide, and should not be relied on for, financial tax, legal or accounting advice. You should consult your own financial, tax, legal and accounting advisors before engaging in any transaction.
