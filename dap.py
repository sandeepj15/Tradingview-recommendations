from utils.logger import setup_logger
from tradingview_ta import get_multiple_analysis
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
from utils.api_utils import get_binance_data, equity, color_negative_red, get_dog_image, select_time_frame, get_chart
from utils.data_processing import stock_rec, process_crypto_data
from utils.components import ticker_component, tradinfview_component, cryptonews_component

# Initialize logger
logger = setup_logger()

# Set Streamlit page configuration
st.set_page_config(page_title="Financial Dashboard", page_icon=":smiling_imp:", layout="wide")

try:
    # Fetch dog image
    get_dog_image = get_dog_image()
    logger.info("Dog image fetched successfully.")
except Exception as e:
    logger.error(f"Error fetching dog image: {e}")

try:
    # Fetch Binance USD pairs
    usd_pair = get_binance_data()
    logger.info("Fetched Binance USDT pairs successfully.")
except Exception as e:
    logger.error(f"Error fetching Binance data: {e}")

# Generate pairs list
pairs = ['binance:' + usd_pair[i]['coin'] for i in range(len(usd_pair))]
logger.debug(f"Generated pairs count: {len(pairs)}")

# Dashboard option selection
option = st.sidebar.selectbox(
    "Which Dashboard?",
    (
        "TradingView Recommendation (Crypto)",
        "TradingView Recommendation (Stocks)",
        "Chart",
        "Crypto Screener",
        "Live Charts",
    )
)
logger.info(f"User selected dashboard option: {option}")

# Display the selected dashboard header
st.header(option)

# TradingView Recommendation (Crypto)
if option == "TradingView Recommendation (Crypto)":
    try:
        with st.sidebar:
            Time_frame = select_time_frame(label="Time frame for Crypto Analysis", default="4h")
            logger.debug(f"Selected time frame for Crypto Analysis: {Time_frame}")

            with st.expander("Contact me:"):
                st.write("[click here >](https://www.linkedin.com/in/jadhavsandeep15/)")
            st.image(get_dog_image, use_container_width='auto')

        analysis = get_multiple_analysis(screener="crypto", interval=Time_frame, symbols=pairs)
        logger.info(f"Analysis data fetched for {len(pairs)} crypto pairs.")

        k = [pairs[i].upper() for i in range(len(pairs))]
        finaldf = process_crypto_data(analysis, usd_pair, k, include_volume=False)
        finaldf = finaldf[finaldf['Recommendation'].isin(['STRONG_BUY', 'STRONG_SELL'])]
        logger.info("Processed crypto data successfully.")

        st.write("Time Frame: ", Time_frame)
        st.write(finaldf)
        logger.debug(f"Displayed processed data: {finaldf.head()}")

        st.write('----------------')
        figure = px.scatter(x=finaldf["Coin"], y=finaldf["%_deviation_EMA20"])
        figure.update_layout(xaxis_title="Coin", yaxis_title="%_deviation_EMA20")
        logger.info("Generated scatter plot for Coins vs Deviation from EMA20.")

        figure1 = px.scatter(x=finaldf["Coin"], y=finaldf["RSI_14"])
        figure1.update_layout(xaxis_title="Coin", yaxis_title="RSI_14")
        figure1.update_traces(marker=dict(color='purple'))
        logger.info("Generated scatter plot for Coins vs RSI.")

        st.subheader("Coins Vs Deviation from EMA20")
        st.write(figure)
        st.subheader("Coins Vs RSI")
        st.write(figure1)

    except Exception as e:
        logger.error(f"Error in TradingView Recommendation (Crypto) section: {e}")

# TradingView Recommendation (Stocks)
elif option == "TradingView Recommendation (Stocks)":
    try:
        st.header("Indian Stocks")
        st.balloons()
        with st.sidebar:
            Time_frame2 = select_time_frame(label="Time frame for Stock Analysis", default="1d")
            logger.debug(f"Selected time frame for Stock Analysis: {Time_frame2}")

        eqt = [f"NSE:{equity[i]}" for i in range(len(equity))]
        ind_stocks = get_multiple_analysis(screener="india", interval=Time_frame2, symbols=eqt)
        logger.info("Fetched stock analysis data.")

        stocksdf = stock_rec(ind_stocks, equity, eqt)
        st.write("Time Frame: ", Time_frame2)
        st.write(stocksdf)
        logger.debug(f"Displayed stocks data: {stocksdf.head()}")

        st.write('----------------')
    except Exception as e:
        logger.error(f"Error in TradingView Recommendation (Stocks) section: {e}")

# Chart section
elif option == "Chart":
    try:
        st.snow()
        st.subheader("Charts for US stocks")
        symbol = st.sidebar.text_input("Enter Symbol: ", value='AAPL', max_chars=10)
        logger.debug(f"User entered symbol: {symbol}")

        rr = get_chart(symbol)
        st.subheader(f"Stock: {symbol}")
        st.image(rr)
        logger.info("Displayed chart for the selected stock.")
    except Exception as e:
        logger.error(f"Error in Chart section: {e}")

# Crypto Screener section
elif option == "Crypto Screener":
    try:
        with st.sidebar:
            Time_frame1 = select_time_frame(label="Time frame for Crypto Analysis", default="1d")
            logger.debug(f"Selected time frame for Crypto Screener: {Time_frame1}")

        analysis = get_multiple_analysis(screener="crypto", interval=Time_frame1, symbols=pairs)
        k1 = [pairs[i].upper() for i in range(len(pairs))]
        finaldf1 = process_crypto_data(analysis, usd_pair, k1, include_volume=True)
        logger.info("Processed crypto screener data successfully.")

        st.subheader("USDT Market")
        st.write("Time Frame: ", Time_frame1)
        st.write(finaldf1.sort_values(by=['Change%'], ascending=False).style.map(color_negative_red,
                                                                                 subset=['Change%']))
        logger.debug(f"Displayed sorted screener data.")

        st.subheader("Coin Vs Change(%)")
        fig = px.scatter(x=finaldf1["Coin"], y=finaldf1['Change%'])
        fig.update_traces(marker=dict(color='tomato'))
        st.write(fig)
        logger.info("Generated scatter plot for Coin vs Change(%).")

        st.subheader("Market cap based on trading Volume at current price")
        fig1 = px.pie(finaldf1, names="Coin", values="M.cap")
        fig1.update_traces(textposition='inside')
        fig1.update_layout(uniformtext_minsize=12)
        st.write(fig1)
        logger.info("Generated pie chart for market cap.")
    except Exception as e:
        logger.error(f"Error in Crypto Screener section: {e}")

# Live Charts section
elif option == "Live Charts":
    try:
        components.html(ticker_component)
        components.html(tradinfview_component, height=630, width=770, scrolling=False)
        logger.info("Displayed live charts.")

        st.write("--------------")
        st.header("Crypto News")
        components.html(cryptonews_component, height=1330, width=720, scrolling=True)
        logger.info("Displayed crypto news.")
    except Exception as e:
        logger.error(f"Error in Live Charts section: {e}")