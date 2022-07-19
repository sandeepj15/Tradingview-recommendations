import json
import urllib.request as request
import requests
import pandas as  pd
from tradingview_ta import TA_Handler, Interval, Exchange
from tradingview_ta import *
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components


#----------Tradingview recommendations part---------------
with request.urlopen('https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=false') as response:
        source = response.read()
        data = json.loads(source)
usd_pair = []
for i in  range(len(data['data'])):
    coin_usd = {}
    if data['data'][i]['q'] == "USDT":
        coin_usd['coin'] = data['data'][i]['s']
        coin_usd['price'] = float(data['data'][i]['c'])
        usd_pair.append(coin_usd)
pairs =['binance:'+ usd_pair[i]['coin'] for i in range(len(usd_pair))]

#--------for color change-----------------------------------
def color_negative_red(value):

  if value < 0:
    color = 'red'
  elif value > 0:
    color = 'green'
  else:
    color = 'black'

  return 'color: %s' % color
#---------------Indian stocks list---------------------------

equity =["AARTIIND","ABB","ABBOTINDIA","ABCAPITAL","ABFRL","ACC","ADANIENT","ADANIPORTS","ALKEM","AMARAJABAT","AMBUJACEM","APOLLOHOSP","APOLLOTYRE",
         "ASHOKLEY","ASIANPAINT","ASTRAL","ATUL","AUBANK","AUROPHARMA","AXISBANK","BAJAJFINSV","BAJFINANCE","BALKRISIND","BALRAMCHIN","BANDHANBNK",
         "BANKBARODA","BATAINDIA","BEL","BERGEPAINT","BHARATFORG","BHARTIARTL","BHEL","BIOCON","BOSCHLTD","BPCL","BRITANNIA","BSOFT","CANBK","CANFINHOME",
         "CHAMBLFERT","CHOLAFIN","CIPLA","COALINDIA","COFORGE","COLPAL","CONCOR","COROMANDEL","CROMPTON","CUB","CUMMINSIND","DABUR","DALBHARAT","DEEPAKNTR",
         "DELTACORP","DIVISLAB","DIXON","DLF","DRREDDY","EICHERMOT","ESCORTS","EXIDEIND","FEDERALBNK","FSL","GAIL","GLENMARK","GMRINFRA","GNFC","GODREJCP","GODREJPROP",
         "GRANULES","GRASIM","GSPL","GUJGASLTD","HAL","HAVELLS","HCLTECH","HDFC","HDFCAMC","HDFCBANK","HDFCLIFE","HEROMOTOCO","HINDALCO","HINDCOPPER","HINDPETRO","HINDUNILVR",
         "HONAUT","IBULHSGFIN","ICICIBANK","ICICIGI","ICICIPRULI","IDEA","IDFC","IDFCFIRSTB","IEX","IGL","INDHOTEL","INDIACEM","INDIAMART","INDIGO","INDUSINDBK","INDUSTOWER",
         "INFY","INTELLECT","IOC","IPCALAB","IRCTC","ITC","JINDALSTEL","JKCEMENT","JSWSTEEL","JUBLFOOD","KOTAKBANK","L_TFH","LALPATHLAB","LAURUSLABS","LICHSGFIN","LT","LTI","LTTS",
         "LUPIN","MANAPPURAM","MARICO","MARUTI","MCDOWELL_N","MCX","METROPOLIS","MFSL","MGL","MINDTREE","MOTHERSON","MRF","MUTHOOTFIN","NAM_INDIA","NATIONALUM","NAUKRI","NAVINFLUOR",
         "NBCC","NESTLEIND","NMDC","NTPC","OBEROIRLTY","OFSS","ONGC","PAGEIND","PEL","PERSISTENT","PETRONET","PFC","PIDILITIND","PIIND","PNB","POLYCAB","POWERGRID","PVR","RAIN","RAMCOCEM",
         "RBLBANK","RECLTD","RELIANCE","SAIL","SBICARD","SBILIFE","SBIN","SHREECEM","SIEMENS","SRF","SRTRANSFIN","SUNPHARMA","SUNTV","SYNGENE","TATACHEM","TATACOMM","TATACONSUM","TATAMOTORS",
         "TATAPOWER","TATASTEEL","TCS","TECHM","TITAN","TORNTPHARM","TORNTPOWER","TRENT","TVSMOTOR","UBL","ULTRACEMCO","UPL","VEDL","VOLTAS","WHIRLPOOL","WIPRO","ZEEL","ZYDUSLIFE"]

#--------------Streamlit part---------------------------------
#--------------crypto recommendation---------------------------
st.set_page_config(page_title="Financial Dashboard", page_icon=":smiling_imp:", layout="wide")

option = st.sidebar.selectbox("Which Dashboard?", ("TradingView Recommendation (Crypto)", "TradingView Recommendation (Stocks)" ,"Chart", "Crypto Screener", "News", "Stoktwits", "Live Charts"))

st.header(option)

if option == "TradingView Recommendation (Crypto)":
    with st.sidebar:
        Time_frame = st.radio(
        "Select a time frame ranging from 1 hour to 1 month", 
        ("1h" , "2h" , "4h" , "1d" , "1W" , "1M"))
        
        with st.expander("Contact me:"):
            st.write("""[click here >](https://www.linkedin.com/in/jadhavsandeep15/)""")

        
        #random_dog_images
        random_dogs = 'https://dog.ceo/api/breeds/image/random'
        with request.urlopen(random_dogs) as response:
            src = response.read()
            img = json.loads(src)
        st.image(img['message'], use_column_width= 'auto')
        
    analysis = get_multiple_analysis(screener="crypto", 
                                     interval= Time_frame, 
                                     symbols= pairs)

    k = [pairs[i].upper() for i in range(len(pairs))]


    rec_coins = []
    for i in range(len(analysis)):
        try:
            ccoin = {}
            if analysis[k[i]].summary['RECOMMENDATION'][:6:] == 'STRONG': 
                ccoin['Coin']  = usd_pair[i]['coin'][:-4]
                ccoin['Recommendation'] = analysis[k[i]].summary['RECOMMENDATION']
                ccoin['Price_USDT'] = usd_pair[i]['price']
                ccoin['EMA20'] =  analysis[k[i]].indicators['EMA20']
                #ccoin['EMA50'] =  analysis[k[i]].indicators['EMA50']
                ccoin['RSI_14']  =  analysis[k[i]].indicators['RSI']
                ccoin['%_deviation_EMA20'] = ( round(100*(float(ccoin['Price_USDT'])- ccoin['EMA20'])/ccoin['EMA20'] , 3))
                #ccoin['%_deviation_EMA50'] = ( round(100*(float(ccoin['Price_USDT'])- ccoin['EMA50'])/ccoin['EMA50'] , 3))
                ccoin['Change%']  =  analysis[k[i]].indicators['change']
                rec_coins.append(ccoin)
        except:
                pass
    finaldf = pd.DataFrame(rec_coins)

    
    st.write("Time Frame: ",Time_frame)

    st.write(finaldf)
    st.write('----------------')
    figure = px.scatter(x= finaldf["Coin"] , y=finaldf["%_deviation_EMA20"] )
    figure.update_layout(
        xaxis_title = "Coin",
        yaxis_title = "%_deviation_EMA20")
    
    figure1 = px.scatter(x= finaldf["Coin"] , y=finaldf["RSI_14"] )
    figure1.update_layout(
        xaxis_title = "Coin",
        yaxis_title = "RSI_14")
    figure1.update_traces(marker=dict(color='purple'))
    st.subheader("Coins Vs deviaton from EMA20")
    st.write(figure) #fig1
    
    with st.expander("What is EMA?"):
        st.write("""The Exponential Moving Average (EMA) is a technical indicator used in trading practices that shows how the price of an asset or security changes over a certain period of time. The EMA is different from a simple moving average in that it places more weight on recent data points (i.e., recent prices)""")
        
    st.subheader("Coins Vs RSI")
    st.write(figure1) #fig2
    
    
    with st.expander("What is RSI?"):
        st.write("""The Relative Strength Index (RSI), developed by J. Welles Wilder, is a momentum oscillator that measures the speed and change of price movements. The RSI oscillates between zero and 100. Traditionally the RSI is considered overbought when above 70 and oversold when below 30. Signals can be generated by looking for divergences and failure swings. RSI can also be used to identify the general trend.""")

    st.write("Want to start trading in the crypto market? ")
    st.write("[click here >](https://www.binance.me/en/activity/referral/offers/claim?ref=CPA_00ZYAN6SYE)")
        
#---------------Indian Stocks--------------------------------

if option == "TradingView Recommendation (Stocks)":
    st.header("Indian Stocks")
    st.balloons()
    with st.sidebar:
        Time_frame2 = st.radio(
        "Select a time frame ranging from 1 hour to 1 month", 
        ("1h" , "2h" , "4h" , "1d" , "1W" , "1M"))    
        
        eqt = [f"NSE:{equity[i]}" for i in range(len(equity))]
        ind_stocks = get_multiple_analysis(screener="india",
                                 interval= Time_frame2,
                                 symbols= eqt)
    stoc_rec = []
    for i in range(len(ind_stocks)):
        Nse={}
        Nse["Name"]= equity[i]
        Nse["Recommendation"]= ind_stocks[eqt[i]].summary['RECOMMENDATION']
        Nse["Close"]= round(ind_stocks[eqt[i]].indicators['close'] ,2) 
        Nse["RSI_14"]=ind_stocks[eqt[i]].indicators['RSI']
        Nse["EMA20"]=ind_stocks[eqt[i]].indicators['EMA20']
        Nse["%_Dev_EMA20"] = (round(100*(float(Nse['Close'])- Nse['EMA20'])/Nse['EMA20'] , 3))
        Nse["Change%"]=ind_stocks[eqt[i]].indicators['change']
        Nse["Volume"]=ind_stocks[eqt[i]].indicators['volume']

        stoc_rec.append(Nse)

    stocksdf= pd.DataFrame(stoc_rec)
    st.write("Time Frame: ",Time_frame2)

    st.write(stocksdf)
    st.write('----------------')
    

#-------------Chart------------------------------------------    
if option == "Chart":
    st.snow()
    st.subheader("Charts for US stocks")
    symbol = st.sidebar.text_input("Enter Symbol: ", value = 'AAPL', max_chars = 10)

    rr = (f"https://finviz.com/chart.ashx?t={symbol}")
    st.subheader("Stock: " +symbol)
    st.image(rr)

#----------Crypto_Screener------------------------------------
if option == "Crypto Screener":
    with st.sidebar:
        Time_frame1 = st.radio(
        "Select a time frame ranging from 1 hour to 1 month", 
        ("1h" , "2h" , "4h" , "1d" , "1W" , "1M"))
        
    analysis = get_multiple_analysis(screener="crypto", 
                                     interval= Time_frame1, 
                                     symbols= pairs)

    k1 = [pairs[i].upper() for i in range(len(pairs))]


    
    usdt_coins = []
    for i in range(len(analysis)):
        try:
            usdt = {}
            usdt['Coin']  = usd_pair[i]['coin'][:-4]
            #usdt['Recommendation'] = analysis[k1[i]].summary['RECOMMENDATION']
            usdt['Price_USDT'] = float(usd_pair[i]['price'])
            usdt['EMA20'] =  analysis[k1[i]].indicators['EMA20']
            #usdt['EMA50'] =  analysis[k1[i]].indicators['EMA50']
            usdt['RSI_14']  =  analysis[k1[i]].indicators['RSI']
            usdt['%_deviation_EMA20'] = ( round(100*(float(usdt['Price_USDT'])- usdt['EMA20'])/usdt['EMA20'] , 3))
            #usdt['%_deviation_EMA50'] = ( round(100*(float(usdt['Price_USDT'])- usdt['EMA50'])/usdt['EMA50'] , 3))
            usdt['Change%']  =  analysis[k1[i]].indicators['change']
            usdt['Volume'] =  analysis[k1[i]].indicators['volume']
            usdt_coins.append(usdt)
        except:
                pass
            
    finaldf1 = pd.DataFrame(usdt_coins)
    finaldf1['M.cap'] =finaldf1['Price_USDT']*finaldf1['Volume']

    st.subheader("USDT Market")
    st.write("Time Frame: ",Time_frame1)
    st.balloons()
    st.write(finaldf1.sort_values(by=['Change%'], ascending = False).style.applymap(color_negative_red, subset=['Change%']))
    st.write("----------------")
    
    st.subheader("Coin Vs Change(%)")
    fig = px.scatter(x= finaldf1["Coin"] , y= finaldf1['Change%'])
    fig.update_traces(marker=dict(color='tomato'))
    st.write(fig)
    
    st.subheader("Market cap based on trading Volume at current price")

    #fig1 = px.scatter(x= finaldf1["Coin"] , y= finaldf1['Volume']*finaldf1['Price_USDT']) for scatter
    fig1 = px.pie(finaldf1, names = "Coin", values = "M.cap")
    fig1.update_traces(textposition='inside')
    fig1.update_layout(uniformtext_minsize=12)
    st.write(fig1)
    
    
#--------------NEWS---------------------------------    
if option == "News":
    with st.sidebar:
        category = st.radio(
            "Choose a category",
            ("business", "entertainment" , "general", 'health' , 'science' , 'sports' , 'technology'))
        #news_type = ['business' , 'entertainment' , 'general' , 'health' , 'science' , 'sports' , 'technology']
        country = st.sidebar.text_input("2-letter ISO 3166-1 code of the country ex: in, us, se" , value = 'in', max_chars =2)
    st.subheader("Top headlines")
    api_key = '18c2d254fa0340f1811267af97225b14'
    
    r = f'https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={api_key}'
    with request.urlopen(r) as response:
        source = response.read()
        news = json.loads(source)
    for i in  range(len(news['articles'])):
        try:
            st.subheader(news['articles'][i]['title'])
            st.write(news['articles'][i]['description'])
            st.write("source ⏩ :" , news['articles'][i]['url'])
            st.image(news['articles'][i]['urlToImage'])
            st.write(news['articles'][i]['publishedAt'])
            st.write('-----------------------')
            st.write("##")
        except:
                pass

#-----------------Stoktwits------------------------------------

if option == "Stoktwits":
    symbol = st.sidebar.text_input("Symbol", value = 'AAPL', max_chars = 5)

    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")
    st.subheader(f"Showing recent Tweets related to: {symbol}")
    data = r.json()
    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.text(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])
        st.write('------------------')
#--------------------------Live charts------------------------
if option == "Live Charts":
    components.html("""
    <script type="text/javascript" src="https://files.coinmarketcap.com/static/widget/coinMarquee.js"></script><div id="coinmarketcap-widget-marquee" coins="1,1027,1839,2010,3890,5426,4195,52,74,5994,6636,5805,7083,1975,6535,3794,4030,18876,1966,6210,2011,1958,6783,7278,3513" currency="USD" theme="light" transparent="false" show-symbol-logo="true"></div>

    """)
    
    st.write("------------")
    
    components.html(
        """
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div id="tradingview_b7851"></div>
  <div class="tradingview-widget-copyright"><a href="https://in.tradingview.com/symbols/BTCUSDT/?exchange=BINANCE" rel="noopener" target="_blank"><span class="blue-text">BTCUSDT Chart</span></a> by TradingView</div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget(
  {
  "width": 750,
  "height": 540,
  "symbol" : "BINANCE:BTCUSDT",
  "interval": "D",
  "timezone": "Etc/UTC",
  "theme": "dark",
  "style": "1",
  "locale": "in",
  "toolbar_bg": "#f1f3f6",
  "enable_publishing": false,
  "withdateranges": true,
  "hide_side_toolbar": false,
  "allow_symbol_change": true,
  "container_id": "tradingview_b7851"
}
  );
  </script>
</div>
<!-- TradingView Widget END -->
""", height =630, width = 770, scrolling=False )
    
    st.write("--------------")
    st.header("Crypto News")

    components.html("""
   <script src="https://www.cryptohopper.com/widgets/js/script"></script> <div class="cryptohopper-web-widget" data-id="5"></div> 
    """, height =1330, width = 720, scrolling=False)
    
    st.write("---------------------")
    
    
    