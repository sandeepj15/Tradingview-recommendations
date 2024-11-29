import json
import urllib.request as request
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

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


@st.cache_data(ttl=60)
def get_binance_data():
    data_url = os.getenv("DATA_URL")
    with request.urlopen(data_url) as response:
        source = response.read()
        data = json.loads(source)
    usd_pairs = []
    for i in range(len(data['data'])):
        coin_usd = {}
        if data['data'][i]['q'] == "USDT":
            coin_usd['coin'] = data['data'][i]['s']
            coin_usd['price'] = float(data['data'][i]['c'])
            usd_pairs.append(coin_usd)
    return usd_pairs


def get_dog_image():
    image_url = os.getenv("IMAGE_URL")
    with request.urlopen(image_url) as response:
        return json.loads(response.read())['message']


def color_negative_red(value):
    if value < 0:
        color = 'red'
    elif value > 0:
        color = 'green'
    else:
        color = 'black'
    return 'color: %s' % color

def select_time_frame(label="Select a time frame", options=None, default="1h"):
    if options is None:
        options = ("1h", "2h", "4h", "1d", "1W", "1M")
    return st.radio(label, options, index=options.index(default))

def get_chart(symbol):
    chart_url = os.getenv("CHART_URL")
    return f"{chart_url}{symbol}"