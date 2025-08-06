import yfinance as yf
import pandas as pd
import datetime as dt

from local_sources import tickets
from functions import general, file

def compute_rsi(prices:pd.Series, period=14) -> pd.Series:
    """Calculate the Relative Strength Index"""
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    # general.display_df_tail(prices, 'Prices')
    # general.display_df_tail(delta, 'Delta')
    # general.display_df_tail(gain, 'Gain')
    # general.display_df_tail(loss, 'Loss')
    # general.display_df_tail(avg_gain, 'Avg Gain')
    # general.display_df_tail(avg_loss, 'Avg Loss')
    #
    # rolling(): It's about aggregating data over a dynamic window to reveal patterns or smooth variations.
    # clip(): It's about constraining individual data points within a defined range to handle outliers or enforce business rules.
    # gain = delta.where(delta > 0.0)
    # avg_gain = gain.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    # print(f'RSI: {rsi}')
    return rsi

def get_stock_info(ticker_symbol:str, period:int=60) -> dict:
    """
    Return general financial information of the given stock.
    
    Default period: 60 Days

    Args:
        ticker_simbol (str): A string for the ticker sumbol
    
    Returns:
        dict: A dict containing the relevant data information of the stock
    """
    analysis = []
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    # general.print_as_json(info)
    history = ticker.history(period=f'{period}d')
    close_history = history['Close']
    close = close_history.iloc[-1]
    volume = history['Volume'].iloc[-1]
    avg_volume = history['Volume'].rolling(20).mean().iloc[-1]
    volume_spike = volume > 1.5 * avg_volume
    rsi_14 = compute_rsi(close_history, 14)
    overbought = rsi_14.iloc[-1] > 70
    oversold = rsi_14.iloc[-1] < 30
    if not ticker.calendar: # print('HTTP Error 404', type(ticker), type(ticker.calendar), ticker.calendar)
        earnings_dates = []
    else:
        earnings_dates = ticker.calendar.get('Earnings Date', [])
    if len(earnings_dates) > 0:
        earnings_date = ticker.calendar['Earnings Date'][0]
        day_to_earnings = (earnings_date - dt.datetime.today().date()).days if not pd.isna(earnings_date) else None
    else:
        earnings_date = "N/A"
        day_to_earnings = "N/A"

    # Analysis
    if volume_spike:
        analysis.append("Volume is spiking, something's happening. Watch the price closely.")
    if day_to_earnings != "N/A" and day_to_earnings >= 7 and day_to_earnings <= 10:
        analysis.append("Close earning date, volatility may increase.")
    if overbought:
        analysis.append("Likely overbought, might fall.")
    elif overbought:
        analysis.append("Oversold, potential rebound.")

    relevant_info = {
        "Ticker": ticker_symbol,
        "Name": info.get('displayName'),
        "Short Name": info.get('shortName'),
        "Long Name": info.get('longName'),
        "Type": info.get('quoteType'),
        "Current Price": round(close, 2),
        '52-week Low': info.get('fiftyTwoWeekLow'),
        '52-week High': info.get('fiftyTwoWeekHigh'),
        "Volume": f'{volume:,.2F}',
        "Volume Spike": volume_spike,
        "RSI": round(rsi_14.iloc[-1], 2),
        "Overbought": overbought,
        "Oversold": oversold,
        "Earnings Date": earnings_date,
        "Days to Earnings": day_to_earnings,
        "Country": info.get('country'),
        "Industry": info.get('industry'),
    }
    return relevant_info, analysis

def main():
    tickets_info = []
    print(f"[Analysis for {len(tickets.TICKETS)} tickets]")
    for i, ticket in enumerate(tickets.TICKETS):
        period = 180
        print(f"{i + 1}. {ticket}")
        info, analysis = get_stock_info(ticket, period)
        tickets_info.append(info)
        
        # print(f"\n{'-'*10} Stock Behaviour Signals ({period} days) {'-'*10}")
        # for key, val in info.items():
        #     print(f"{key}: {val}")
        
        # if len(analysis) > 0:
        #     print(f"\n{'-'*10} Analysis ({period} days) {'-'*10}")
        #     [print(f'- {row}') for row in analysis]

    file.create_csv_from_dict(tickets_info)

if __name__ == "__main__":
    main()