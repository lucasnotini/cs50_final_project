import pandas as pd
import yfinance as yf
import quantstats as qs


def main():
    # asks the user for a ticker until he inputs a valid yfinance ticker
    while True:
        ticker = input("Type an asset ticker according to Yahoo Finance: ").strip()
        if check_ticker(ticker) == True:
            break
        elif check_ticker(ticker) == False:
            print("Invalid ticker {ticker} - please try again.")
            pass

    # asks the user for the initial capital to invest
    while True:
        try:
            initial_capital = float(input("How much capital you want to invest: "))
            if check_capital(initial_capital) == True:
                break
            elif check_capital(initial_capital) == False:
                print("The capital must be greater than 0 - please try again.")
                pass
        except ValueError:
            print("Invalid input. The capital value must be a number.")
            pass

    # create a pandas dataframe with the data
    df = get_data(ticker, initial_capital)

    # get the metrics dict
    metrics_dict = metrics(df)

    # print the metrics
    print("\n")
    print(f"--- PERFORMANCE METRICS FOR THE SYMBOL: {ticker} ---")
    print(
        f"START DATE: {metrics_dict['first_day']} - END DATE: {metrics_dict['last_day']}"
    )
    print("\n")
    print(f"TOTAL PROFIT $: {metrics_dict['total_profit']}")
    print(f"TOTAL RETURN: {metrics_dict['total_return']}%")
    print(f"COMPOUND ANNUAL GROWTH RATE (CAGR): {metrics_dict['cagr']}%")
    print(f"MAXIMUM DRAWDOWN: {metrics_dict['max_drawdown']}%")
    print(f"SHARPE RATIO: {metrics_dict['sharpe_ratio']}")
    print("\n")
    print("---------------------------------------------")


# check if the user passed a valid ticker
def check_ticker(ticker):
    try:
        yf.Ticker(ticker).info
        return True
    except:
        return False


# checks the initial capital
def check_capital(initial_capital):
    try:
        float(initial_capital)
        if initial_capital > 0:
            return True
        else:
            return False
    except ValueError:
        return False


# download the closing prices for the user's ticker
def get_data(ticker, initial_capital):
    df = yf.download(ticker)
    # using .loc[] to avoid SettingWithCopyWarning
    df.loc[:, "Returns"] = df["Close"].pct_change()
    # generate a column with the % returns
    df["Returns"] = df["Close"].pct_change()
    df.dropna(inplace=True)
    # generate the cummulative returns and calculates the equity using the initial_capital
    df["Cum_Returns"] = (1 + df["Returns"]).cumprod() - 1
    df["Equity"] = (1 + df["Cum_Returns"]) * initial_capital

    return df


# creates a dictionary with multiple metrics for the investment
def metrics(df):
    # save first and last trading days
    first_day = df.index[0]
    last_day = df.index[-1]
    # calculate total return and $ profit
    total_return = round(
        (df["Equity"].iloc[-1] - df["Equity"].iloc[0]) / df["Equity"].iloc[0] * 100, 2
    )
    total_profit = f" {df['Equity'].iloc[-1] - df['Equity'].iloc[0]:.2f}"
    # get metrics from quantstats
    cagr = round(qs.stats.cagr(df["Returns"]) * 100, 2)
    max_drawdown = round(qs.stats.max_drawdown(df["Returns"]) * 100, 2)
    sharpe_ratio = round(qs.stats.sharpe(df["Returns"]), 2)

    # filling a dict with the metrics
    metrics_dict = {
        "first_day": first_day,
        "last_day": last_day,
        "total_profit": total_profit,
        "total_return": total_return,
        "cagr": cagr,
        "max_drawdown": max_drawdown,
        "sharpe_ratio": sharpe_ratio,
    }
    return metrics_dict


if __name__ == "__main__":
    main()
