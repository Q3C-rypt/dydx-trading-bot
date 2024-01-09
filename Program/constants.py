from dydx3.constants import API_HOST_GOERLI, API_HOST_MAINNET
from decouple import config

# SELECT MODE
MODE = "TESTING"

#Close all open positions and orders
ABORT_ALL_POSITIONS = True #true would close all positions

#Find cointegrated pairs
FIND_COINTEGRATED = False

#place trade
PLACE_TRADES = False

#Exit trades
MANAGE_EXITS = False

#Resolution
RESOLUTION = "1HOUR" #candlestick time

#Stats window 
WINDOW = 21 #21 previous days of stock to look at

#ThreshHolds - opening trade
MAX_HALF_LIFE = 24
ZSCORE_THRESH = 1.5
USD_PER_TRADE = 100 #trade of 100$
USD_MIN_COLLATERAL = 1875 #reflects how much you have in accounts, min floor to work with so bot doesnt keep trading

#Thresholds - Closing
CLOSE_AT_ZSCORE_CROSS = True #closes trade once zscore passes ZSCORE_THRESH, or whatever limit we set it at

#Ethereum Address
ETHEREUM_ADDRESS = "0x91D6bC6561209d0Cc19756247cd84784F6c40827"

#KEYS - TESTING
STARK_PRIVATE_KEY_TESTNET = config("STARK_PRIVATE_KEY_TESTNET")
DYDX_API_KEY_TESTNET = config("DYDX_API_KEY_TESTNET")
DYDX_API_SECRET_TESTNET = config("DYDX_API_SECRET_TESTNET")
DYDX_API_PASSPHRASE_TESTNET = config("DYDX_API_PASSPHRASE_TESTNET")

# KEYS - Export
STARK_PRIVATE_KEY = STARK_PRIVATE_KEY_TESTNET if MODE == "TESTING" else print("Thers is no mainnet setup yet")
DYDX_API_KEY = DYDX_API_KEY_TESTNET if MODE == "TESTING" else print("Thers is no mainnet setup yet")
DYDX_API_SECRET = DYDX_API_SECRET_TESTNET if MODE == "TESTING" else print("Thers is no mainnet setup yet")
DYDX_API_PASSPHRASE = DYDX_API_PASSPHRASE_TESTNET if MODE == "TESTING" else print("Thers is no mainnet setup yet")

#HOST - Export
HOST = API_HOST_GOERLI if MODE == "TESTING" else API_HOST_MAINNET

#HTTP - Provider
HTTP_PROVIDER_TESTNET = "https://eth-goerli.g.alchemy.com/v2/vorhqizwadvUJVZYJz1nN-ap5aUH8Gaz"
HTTP_PROVIDER = HTTP_PROVIDER_TESTNET if MODE == "TESTING" else print("There is no mainnet yet")