import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from constants import MAX_HALF_LIFE, WINDOW
import csv

# Calculate half life
def calculate_half_life(spread): #Algorithme that returns really good half life spread
    df_spread = pd.DataFrame(spread, columns = ["spread"])
    spread_lag = df_spread.spread.shift(1)
    spread_lag.iloc[0] = spread_lag.iloc[1]
    spread_ret = df_spread.spread - spread_lag
    spread_ret.iloc[0] = spread_ret.iloc[1]
    spread_lag2 = sm.add_constant(spread_lag)
    model = sm.OLS(spread_ret, spread_lag2)
    res = model.fit()
    halflife = round(-np.log(2) / res.params[1], 0)

    return halflife

# Calculate z-score
def calculate_zscore(spread):
    spread_series = pd.Series(spread)
    mean = spread_series.rolling(center = False,  window = WINDOW).mean()
    std = spread_series.rolling(center = False,  window = WINDOW).std()
    x = spread_series.rolling(center = False, window = 1).mean()

    zscore = (x - mean) / std
    return zscore

# Caluclate Cointegration
def calculate_cointegration(series_1, series_2):

    series_1 = np.array(series_1).astype(np.float64)
    series_2 = np.array(series_2).astype(np.float64)
    coint_flag = 0
    coint_res = coint(series_1, series_2)
    coint_t = coint_res[0]
    p_value = coint_res[1] #if pvalue is less then 0.05, they are cointegrated
    critical_value = coint_res[2][1]
    model = sm.OLS(series_1, series_2).fit()
    hedge_ratio = model.params[0]
    spread = series_1 - (hedge_ratio * series_2)
    half_life = calculate_half_life(spread)
    t_check = coint_t < critical_value
    coint_flag = 1 if p_value < 0.05 and t_check else 0

    return coint_flag, hedge_ratio, half_life

# Store integrated results
def store_cointegrated_results(df_market_prices):

    # Initialize
    markets = df_market_prices.columns.to_list()
    criteria_met_pairs = []

    # Find cointegrated pairs, start with base pair
    for index, base_market in enumerate(markets[:-1]):
        series_1 = df_market_prices[base_market].values.astype(float).tolist()

        # Get quote pair
        for quote_market in markets[index +1:]:
            series_2 = df_market_prices[quote_market].values.astype(float).tolist()

            # Check cointegration
            coint_flag, hedge_ratio, half_life = calculate_cointegration(series_1, series_2)

            #Log pair, log in criteria met array
            if coint_flag == 1 and half_life <= MAX_HALF_LIFE and half_life > 0:
                criteria_met_pairs.append({
                    "base_market": base_market,
                    "quote_market": quote_market,
                    "hedge_ratio": hedge_ratio,
                    "half_life": half_life,
                })

    # Create and save Datafram
    df_criteria_met = pd.DataFrame(criteria_met_pairs)
    df_criteria_met.to_csv("cointegrated_pairs.csv")
    del df_criteria_met

    # Return result
    print("Cointegrated pairs successfully saved")
    return "saved"

#Filter out FIL-USD
def rewrite_files(input, output, forbidden):
    with open(input, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        # header = next(reader)

        filtered_rows = [row for row in reader if not any(char in ''.join(row) for char in forbidden)]

    with open(output, 'w', newline= '') as csvfile:
        writer = csv.writer(csvfile)
        # writer.writerow(header)
        writer.writerows(filtered_rows)

    #Print Success
    print("Successfuly transfered data to output.csv, woohoo")
    return "savedF"
