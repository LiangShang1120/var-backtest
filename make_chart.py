import pandas as pd
import matplotlib.pyplot as plt
#Draw a chart of the result
results=pd.read_csv("results.csv", index_col="Date")
#Two print lines verify that the result is accurate
#print(results.head(3))
#print(len(results), "rows")
#Turns the date text into real dates, so chart aligns with the date
results.index=pd.to_datetime(results.index)
#Calculate exceptions. ie. bad days
exceptions=results[results["return"] < -results["var_hist_95"]]
#Verify the number of exceptions, given 48
#print(len(exceptions), "exceptions")
fig, ax=plt.subplots(figsize=(10, 4))
#Line chart
ax.plot(results.index, results["return"], linewidth=0.6, label="Daily return")
ax.plot(results.index, -results["var_hist_95"], color="orange", label="-VaR 95%")
#Dot point chart
ax.scatter(exceptions.index, exceptions["return"], color="red", s=14, label="Exception")
ax.set_title("Portfolio returns and 95% VaR")
ax.legend()
#Save the picture as var_backtest.png
fig.savefig("var_backtest.png", dpi=150, bbox_inches="tight")
print("saved var_backtest.png")

