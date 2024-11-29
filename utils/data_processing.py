import pandas as pd
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger()

def stock_rec(ind_stocks, equity, eqt):
    """
    Processes stock recommendations and metrics into a DataFrame.

    Args:
        ind_stocks (list): List of stock analysis data.
        equity (list): List of stock names.
        eqt (list): List of stock symbols.

    Returns:
        pd.DataFrame: DataFrame containing processed stock data.
    """
    logger.info("Starting stock_rec function.")
    stoc_rec = []
    for i in range(len(ind_stocks)):
        try:
            Nse = {
                "Name": equity[i],
                "Recommendation": ind_stocks[eqt[i]].summary['RECOMMENDATION'],
                "Close": round(ind_stocks[eqt[i]].indicators['close'], 2),
                "RSI_14": ind_stocks[eqt[i]].indicators['RSI'],
                "EMA20": ind_stocks[eqt[i]].indicators['EMA20'],
                "%_Dev_EMA20": round(
                    100 * (float(ind_stocks[eqt[i]].indicators['close']) - ind_stocks[eqt[i]].indicators['EMA20'])
                    / ind_stocks[eqt[i]].indicators['EMA20'],
                    3,
                ),
                "Change%": ind_stocks[eqt[i]].indicators['change'],
                "Volume": ind_stocks[eqt[i]].indicators['volume'],
            }
            stoc_rec.append(Nse)

        except KeyError as e:
            logger.warning(f"Missing key: {e} at index {i} for stock {equity[i]}")
        except Exception as e:
            logger.error(f"Error: {e} at index {i} for stock {equity[i]}")

    logger.debug(f"Processed stock data count: {len(stoc_rec)}")
    df_stock = pd.DataFrame(stoc_rec)
    logger.info(f"Generated DataFrame with {len(df_stock)} records.")
    return df_stock


def process_crypto_data(analysis, usd_pair, keys, include_volume=False):
    """
    Processes cryptocurrency data into a DataFrame.

    Args:
        analysis (dict): Dictionary containing analysis data for cryptocurrencies.
        usd_pair (list): List of cryptocurrency USD pairs.
        keys (list): List of keys for the analysis data.
        include_volume (bool): Whether to include volume in the output.

    Returns:
        pd.DataFrame: DataFrame containing processed cryptocurrency data.
    """
    logger.info("Starting process_crypto_data function.")
    processed_coins = []
    for i in range(len(analysis)):
        try:
            coin_data = {
                "Coin": usd_pair[i]['coin'][:-4],
                "Recommendation": analysis[keys[i]].summary['RECOMMENDATION'],
                "Price_USDT": float(usd_pair[i]['price']),
                "EMA20": analysis[keys[i]].indicators['EMA20'],
                "RSI_14": analysis[keys[i]].indicators['RSI'],
                "%_deviation_EMA20": round(
                    100 * (float(usd_pair[i]['price']) - analysis[keys[i]].indicators['EMA20'])
                    / analysis[keys[i]].indicators['EMA20'],
                    3,
                ),
                "Change%": analysis[keys[i]].indicators['change'],
            }
            if include_volume:
                coin_data["Volume"] = analysis[keys[i]].indicators['volume']
            processed_coins.append(coin_data)
        except KeyError as e:
            logger.warning(f"Missing key: {e} at index {i} for coin {usd_pair[i]['coin']}")
        except ValueError as e:
            logger.warning(f"ValueError: {e} at index {i} for coin {usd_pair[i]['coin']}")
        except Exception as e:
            logger.error(f"Error: {e} at index {i} for coin {usd_pair[i]['coin']}")

    logger.debug(f"Processed crypto data count: {len(processed_coins)}")
    df = pd.DataFrame(processed_coins)
    if include_volume and 'Volume' in df.columns:
        df['M.cap'] = df['Price_USDT'] * df['Volume']
        logger.debug("Calculated market capitalization for cryptocurrencies.")
    logger.info(f"Generated DataFrame with {len(df)} records.")
    return df
