from Func_connections import connect_dydx
from func_public import construct_market_prices
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES, MANAGE_EXITS
from func_private import abort_all_positions
from func_cointegration import store_cointegrated_results, rewrite_files
from func_entr_pairs import open_positions
from func_exit_pairs import manage_trade_exits



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
            
        # Store cointgegrated pairs
        try: 
           print("Storing cointegrated pairs, give my boys a minute...") 
           stores_result = store_cointegrated_results(df_market_prices)
           if stores_result != "saved":
                print("Error saving cointegrated pairs") #If nothign is cointegrated, return nothing or error
                exit(1)
        except Exception as e:
            print("Error saving cointegrated pairs: ", e)
            exit(1)    

        #Skip FIL 
        try:
            print("Storing data without FIL...")
            input = 'cointegrated_pairs.csv' 
            output = 'output.csv'
            forbiden = ['FIL', 'FIL-USD']
            swap_success = rewrite_files(input, output, forbiden)
            if swap_success != "savedF":
                print("Could not save without FIL, FIL too strong...")
                exit(1)
        except Exception as e:
            print("Error saving without FIL...", e)
            exit(1)


    # Run as always 
    while True:

        # Place trade for opening positions
        if MANAGE_EXITS:  
            try: 
                print("Managing exits, give my boys a minute...") 
                manage_trade_exits(client)
            except Exception as e:
                print("Error managing exiting positions: ", e)
                exit(1)  

        # Place trade for opening positions
        if PLACE_TRADES:
            try: 
                print("Finding trading opportunities, give my boys a minute...") 
                open_positions(client)
            except Exception as e:
                print("Error trading pairs: ", e)
                exit(1)   