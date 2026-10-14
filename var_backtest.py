#This is a 1 day Value at Risk (VaR) for a four-fund portfolio, backtested on real days
import math
import pandas as pd
#Window is days of history used for each VaR
Window=250
#Followed the normal distribution, this represents the value for normal-curve multipliers
ncm={0.95: 1.645, 0.99:2.326}
#load_prices returns the table of prices, one column per fund
def load_prices(path='prices_4funds.csv'):
    return pd.read_csv(path, index_col='Date')
#portfolio_returns gives the daily returns of the portfolio. All funds get equal weights when weights=None
def portfolio_returns(prices, weights=None):
    returns=prices.pct_change().dropna()
    if weights is None:
        return returns.mean(axis=1)
    return (returns*weights).sum(axis=1)
#historical_var returns a positive loss for VaR
def historical_var(window_returns, level):
    return -window_returns.quantile(1-level)
#parametric_var function does the same as the previous one, but it assumes the return from a normal distribution instead of past returns
def parametric_var(window_returns, level):
    average_window_returns=window_returns.mean()
    std_window_returns=window_returns.std()
    return -(average_window_returns - ncm[level]*std_window_returns)
#rolling_var VaR calculation for everyday
#It does an estimate about how bad the day could be based on the result of 250 previous days
#returns is the portfolio's daily returns
#method is either historical or parametric
#level is either 0.95 or 0.99
def rolling_var(returns, method, level, window=Window):
    results=[]
    dates=[]
    for t in range(window, len(returns)):
        past=returns.iloc[t-window:t]
        if method=='historical':
            results.append(historical_var(past, level))
        elif method=='parametric':
            results.append(parametric_var(past, level))
        dates.append(returns.index[t])
    return pd.Series(results, index=dates)
#backtest counts the days when loss was bigger than VaR
def backtest(returns, var_series):
    exceptions=0
    days=0
    for date in var_series.index:
        days+=1
        if returns[date]<-var_series[date]:
            exceptions+=1
    rate=exceptions/days
    return exceptions, days, rate
#check the results
if __name__=="__main__":
    prices=load_prices()
    port=portfolio_returns(prices)
    hist95=rolling_var(port, "historical", 0.95)
    results=pd.DataFrame({"return": port.loc[hist95.index], "var_hist_95": hist95})
    results.to_csv("results.csv", index_label="Date")
    print("saved results.csv with", len(results), "rows")
    all_returns=pd.DataFrame({"return": port, "var_hist_95": hist95})
    all_returns.to_csv("returns_for_excel.csv", index_label="Date")
    print("saved returns_for_excel.csv with", len(all_returns), "rows")
    for method in ["historical", "parametric"]:
        for level in [0.95, 0.99]:
            var_series=rolling_var(port, method, level)
            exceptions, days, rate=backtest(port, var_series)
            print(method, level, exceptions, days, rate)
