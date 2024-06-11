import numpy as np
#import matplotlib
#matplotlib.use('qtAgg')

# Collect historical stock price data for each stock
stock1_prices = [10, 12, 11, 13, 15]
stock2_prices = [8, 9, 10, 12, 11]
stock3_prices = [20, 18, 19, 21, 22]

# Calculate daily returns for each stock
stock1_returns = np.diff(stock1_prices) / stock1_prices[:-1]
stock2_returns = np.diff(stock2_prices) / stock2_prices[:-1]
stock3_returns = np.diff(stock3_prices) / stock3_prices[:-1]

# Combine daily returns into a matrix
returns_matrix = np.vstack([stock1_returns, stock2_returns, stock3_returns])

# Calculate covariance matrix
cov_matrix = np.cov(returns_matrix)

# Calculate correlation matrix
corr_matrix = np.corrcoef(returns_matrix)

print("Covariance matrix:\n", cov_matrix)
print("Correlation matrix:\n", corr_matrix)


# (15.0 - 13 ) / 13

# return example ( stock1_returns[-1])
# ; ( / (- 15.0 13 ) 13.0)  0.15384615384615385
