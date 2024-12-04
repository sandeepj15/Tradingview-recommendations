import aiohttp
import asyncio
import orjson
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

data_url = os.getenv("DATA_URL")
image_url = os.getenv("IMAGE_URL")
chart_url = os.getenv("CHART_URL")

equity = ["AARTIIND", "ABB", "ABBOTINDIA", "ABCAPITAL", "ABFRL", "ACC", "ADANIENT", "ADANIPORTS", "ALKEM",
          "AMARAJABAT", "AMBUJACEM", "APOLLOHOSP", "APOLLOTYRE",
          "ASHOKLEY", "ASIANPAINT", "ASTRAL", "ATUL", "AUBANK", "AUROPHARMA", "AXISBANK", "BAJAJFINSV",
          "BAJFINANCE", "BALKRISIND", "BALRAMCHIN", "BANDHANBNK",
          "BANKBARODA", "BATAINDIA", "BEL", "BERGEPAINT", "BHARATFORG", "BHARTIARTL", "BHEL", "BIOCON", "BOSCHLTD",
          "BPCL", "BRITANNIA", "BSOFT", "CANBK", "CANFINHOME",
          "CHAMBLFERT", "CHOLAFIN", "CIPLA", "COALINDIA", "COFORGE", "COLPAL", "CONCOR", "COROMANDEL", "CROMPTON",
          "CUB", "CUMMINSIND", "DABUR", "DALBHARAT", "DEEPAKNTR",
          "DELTACORP", "DIVISLAB", "DIXON", "DLF", "DRREDDY", "EICHERMOT", "ESCORTS", "EXIDEIND", "FEDERALBNK",
          "FSL", "GAIL", "GLENMARK", "GMRINFRA", "GNFC", "GODREJCP", "GODREJPROP",
          "GRANULES", "GRASIM", "GSPL", "GUJGASLTD", "HAL", "HAVELLS", "HCLTECH", "HDFC", "HDFCAMC", "HDFCBANK",
          "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDCOPPER", "HINDPETRO", "HINDUNILVR",
          "HONAUT", "IBULHSGFIN", "ICICIBANK", "ICICIGI", "ICICIPRULI", "IDEA", "IDFC", "IDFCFIRSTB", "IEX", "IGL",
          "INDHOTEL", "INDIACEM", "INDIAMART", "INDIGO", "INDUSINDBK", "INDUSTOWER",
          "INFY", "INTELLECT", "IOC", "IPCALAB", "IRCTC", "ITC", "JINDALSTEL", "JKCEMENT", "JSWSTEEL", "JUBLFOOD",
          "KOTAKBANK", "L_TFH", "LALPATHLAB", "LAURUSLABS", "LICHSGFIN", "LT", "LTI", "LTTS",
          "LUPIN", "MANAPPURAM", "MARICO", "MARUTI", "MCDOWELL_N", "MCX", "METROPOLIS", "MFSL", "MGL", "MINDTREE",
          "MOTHERSON", "MRF", "MUTHOOTFIN", "NAM_INDIA", "NATIONALUM", "NAUKRI", "NAVINFLUOR",
          "NBCC", "NESTLEIND", "NMDC", "NTPC", "OBEROIRLTY", "OFSS", "ONGC", "PAGEIND", "PEL", "PERSISTENT",
          "PETRONET", "PFC", "PIDILITIND", "PIIND", "PNB", "POLYCAB", "POWERGRID", "PVR", "RAIN", "RAMCOCEM",
          "RBLBANK", "RECLTD", "RELIANCE", "SAIL", "SBICARD", "SBILIFE", "SBIN", "SHREECEM", "SIEMENS", "SRF",
          "SRTRANSFIN", "SUNPHARMA", "SUNTV", "SYNGENE", "TATACHEM", "TATACOMM", "TATACONSUM", "TATAMOTORS",
          "TATAPOWER", "TATASTEEL", "TCS", "TECHM", "TITAN", "TORNTPHARM", "TORNTPOWER", "TRENT", "TVSMOTOR", "UBL",
          "ULTRACEMCO", "UPL", "VEDL", "VOLTAS", "WHIRLPOOL", "WIPRO", "ZEEL", "ZYDUSLIFE"]


async def get_binance_data_async():
    async with aiohttp.ClientSession() as session:
        async with session.get(data_url) as response:
            source = await response.read()
            data = orjson.loads(source)
    usd_pairs = [
        {'coin': item['s'], 'price': float(item['c'])}
        for item in data['data'] if item['q'] == "USDT"
    ]
    return usd_pairs

@st.cache_data(ttl=90)
def get_binance_data():
    return asyncio.run(get_binance_data_async())


async def get_dog_image_async():
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            source = await response.read()
            return orjson.loads(source)['message']

def get_dog_image():
    return asyncio.run(get_dog_image_async())

def color_negative_red(value):
    color = 'red' if value < 0 else 'green' if value > 0 else 'black'
    return f'color: {color}'

def select_time_frame(label="Select a time frame", options=None, default="1h"):
    if options is None:
        options = ("1h", "2h", "4h", "1d", "1W", "1M")
    return st.radio(label, options, index=options.index(default))

def get_chart(symbol):
    return f"{chart_url}{symbol}"