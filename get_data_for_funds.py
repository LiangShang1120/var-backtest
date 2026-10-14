import pandas as pd
import yfinance as yf
#Import data from yfinance to csv form for further analysis
closes = {}
for t in ["SPY", "XIU.TO", "TLT", "GLD"]:
    s=yf.Ticker(t).history(start="2021-10-13", end="2026-10-14")["Close"]
    s.index=s.index.strftime('%Y-%m-%d')
    closes[t]=s
prices = pd.DataFrame(closes).dropna()
prices.to_csv("prices_4funds.csv")
print(len(prices), "days saved")
