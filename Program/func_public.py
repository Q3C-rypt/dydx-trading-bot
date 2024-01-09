from constants import RESOLUTION
from func_utils import get_ISO_times
import pandas as pd
import numpy as np
import time
from pprint import pprint

# Get relevant time period for ISO from and to
ISO_TIMES = get_ISO_times()


# Get candles recents
def get_candles_recent(client, market):

    #Define output
    close_prices = []

    #protect API
    time.sleep(2)

    #Get data
    candles = client.public.get_candles(
        market = market,
        resolution = RESOLUTION,
        limit = 100
    )

    #Strucutre data
    for candle in candles.data["candles"]:
        close_prices.append(candle["close"])

    # Construct and return close price series
    close_prices.reverse()
    prices_result = np.array(close_prices).astype(np.float64)
    return prices_result


# Get candle Stick data
def get_candle_historical(client, market):
    
    #define output
    close_prices = []

    # Exctract historical price data for each time frame
    for timeframe in ISO_TIMES.keys():

        #Confirm time needed
        tf_obj = ISO_TIMES[timeframe]
        from_iso = tf_obj["from_iso"]
        to_iso = tf_obj["to_iso"]

        # Protect API
        time.sleep(0.2)

        # Get data 
        candles = client.public.get_candles(
            market = market,
            resolution = RESOLUTION,
            from_iso = from_iso,
            to_iso = to_iso,
            limit = 100
        )

        # Structure data
        for candle in candles.data["candles"]:
            close_prices.append({"datetime": candle["startedAt"], market: candle["close"]})

    # Construct and return data frame
    close_prices.reverse() #reverses order of inputed data in the cnaldes array so we have old to new
    return close_prices

# Construct market prices
def construct_market_prices(client):
    
    # Assign varaibles
    tradeable_markets = []
    markets = client.public.get_markets()

    #find tradeable pairs
    for market in markets.data["markets"].keys():
        market_info = markets.data["markets"][market]

        if market_info["status"] == "ONLINE" and market_info["type"] == "PERPETUAL":
            tradeable_markets.append(market) #if crypto is online and a perpetual type, it's tradable

    # Set initial Data frame
    close_prices = get_candle_historical(client, tradeable_markets[0])

    df = pd.DataFrame(close_prices)
    df.set_index("datetime", inplace=True)
    print(df.head()) #head gives you first 5 results of array, tail gives you last 5 results

    # Append other prices to Dataframe
    # You can limit the amount to loop through here to save time in development

    for market in tradeable_markets[1:]: #first to fourth item, remove 5 if you want it to check everything
        close_prices_add = get_candle_historical(client, market)
        df_add = pd.DataFrame(close_prices_add)
        df_add.set_index("datetime", inplace=True)
        df = pd.merge(df, df_add, how = "outer", on ="datetime", copy = False)
        del df_add #manages memory, make sure weight of memory doesnt compound

    # Check any columns with NaNs (NaN = Not a Number)
    nans = df.columns[df.isna().any()].tolist()
    if len(nans) > 0:
        print("Dropping columns: ")
        print(nans)
        df.drop(columns = nans, inplace = True)

    #Return result
    return df #Returned results are not super accurate, use mainnet if you want super accurate data

