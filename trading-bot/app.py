from SmartApi import SmartConnect
import pyotp
import pandas as pd
from logzero import logger
from configurations.config import config
from datetime import datetime, timedelta

# API Credentials
API_KEY = config.api_key
CLIENT_ID = config.client_id
PIN = config.pin
TOTP_SECRET = "CFPOSNGKLE4ABYH7AP2NFEP2JU"

# Generate TOTP
try:
    totp = pyotp.TOTP(TOTP_SECRET).now()
except Exception as e:
    logger.error("Invalid TOTP Token: Please check your secret key.")
    raise e

# Initialize API connection
smart_api = SmartConnect(api_key=API_KEY)

# Authenticate with API
try:
    login_response = smart_api.generateSession(CLIENT_ID, PIN, totp)
    logger.info(f"Login Response: {login_response}")

except Exception as e:
    logger.info(f"Error during login: {e}")

if login_response.get("status") is False:
    logger.error(f"Login Failed: {login_response}")
    exit()
else:
    logger.info("✅ Login Successful!")

# Verify Symbol Token
exchange = "NSE"
tradingsymbol = "RELIANCE"
symboltoken = "2885"  # Check this first!

try:
    symbol_response = smart_api.searchScrip(exchange, tradingsymbol)
    logger.info(f"Symbol Response: {symbol_response}")
except Exception as e:
    logger.error(f"Error during symbol search: {e}")

# Correct Date Format
to_date = datetime.today().strftime("%Y-%m-%d %H:%M")
from_date = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d %H:%M")

params = {
    "exchange": exchange,
    "tradingsymbol": tradingsymbol,
    "symboltoken": symboltoken,
    "interval": "15MIN",
    "fromdate": from_date,
    "todate": to_date,
}

# Fetch Historical Data
try:
    historical_data = smart_api.getCandleData(params)
    logger.info(f"Historical Data Response: {historical_data}")
except Exception as e:
    logger.error(f"Error during historical data fetch: {e}")
    
# Check if Data Exists
if historical_data["status"]:
    data = historical_data["data"]
    df = pd.DataFrame(data, columns=["Datetime", "Open", "High", "Low", "Close", "Volume"])
    df.to_csv("reliance_stock_data.csv", index=False)
    logger.info("✅ Data saved to reliance_stock_data.csv")
else:
    logger.error(f"Failed to fetch historical data: {historical_data}")
