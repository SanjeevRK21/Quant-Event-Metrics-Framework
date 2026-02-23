import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm


def plot_return_distribution(
    returns: pd.Series,
    ticker: str,
    var: float,
    cvar: float
):
    plt.figure(figsize=(8, 4))

    plt.hist(returns, bins=50, density=True, alpha=0.6)
    
    mu, sigma = returns.mean(), returns.std()
    x = np.linspace(returns.min(), returns.max(), 500)
    plt.plot(x, norm.pdf(x, mu, sigma), linestyle="--", color = 'green')

    plt.axvline(var, color="red", linestyle="--", label="VaR (95%)")
    plt.axvline(cvar, color="darkred", linestyle="-", label="CVaR (95%)")

    plt.title(f"{ticker} Return Distribution & Tail Risk")
    plt.xlabel("Daily Return")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True)
    plt.show()
