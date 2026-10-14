import pandas as pd
#Shows when the 95% VaR exceptions happened and what each fund did on those days
results=pd.read_csv("results.csv", index_col="Date")
results.index=pd.to_datetime(results.index)
exceptions=results[results["return"] < -results["var_hist_95"]]
#Register the frequency that the red dot appear in year and month
by_month=exceptions.index.strftime("%Y-%m").value_counts()
print(by_month.head(4))
print(len(by_month), "months had at least one exception")
prices=pd.read_csv("prices_4funds.csv", index_col="Date")
#fund_returns do the same thing as portfolio_returns, but with individual fund
fund_returns=prices.pct_change().dropna()*100
fund_returns.index=pd.to_datetime(fund_returns.index)
print(fund_returns.loc[exceptions.index].round(2).loc["2025-04"])
print(fund_returns.loc[exceptions.index].round(2).loc["2026-03"])
