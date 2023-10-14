from Func_connections import connect_dydx
from func_public import construct_market_prices
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED
from func_private import abort_all_positions



if __name__ == "__main__":

    #Connect to client 
    try: 
        print("Connecting to client...")
        client = connect_dydx()
    except Exception as e: 
       
        print("ERROR CONNECTING TO CLIENT", e) #We print because we will be on cloud, not always looking at terminal
        exit(1) #Something goes wrong exits file


    # Abort all open positions
    if ABORT_ALL_POSITIONS: 
        try: 
           print("Closing all positions...") 
           close_orders = abort_all_positions(client)
        except Exception as e:
            print("ERROR closing all positions", e)
            exit(1) 

    # Find cointegrated pairs
    if FIND_COINTEGRATED:

        # Construct market prices
        try: 
           print("Fetching Market Prices, give my boys a minute...") 
           df_market_prices = construct_market_prices(client)
        except Exception as e:
            print("ERROR constructing market prices: ", e)
            exit(1)         