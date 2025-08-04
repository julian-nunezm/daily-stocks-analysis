import yfinance as yf

from local_sources import tickets
from functions import general_functions


def get_yahoo_data(ticket:str, period:int=60):
    df = yf.download(ticket, period=f'{period}d', interval='1d', progress=False)
    print(type(df), len(df))
    if df.empty or len(df) < 20:    # TODO: Why?
        return {}
    return df

def get_stock_info(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    history = ticker.history(period='30d')
    print(history.tail())
    close = history['Close'].iloc[-1]
    volume = history['Volume'].iloc[-1]
    avg_volume = history['Volume'].rolling(20).mean().iloc[-1]
    volume_spike = volume > 1.5 * avg_volume
    # general_functions.format_number(close)
    # general_functions.format_number(volume)
    # general_functions.format_number(avg_volume)
    print(close, volume, avg_volume, volume_spike)

def main():
    for ticket in tickets.TICKETS:
        print(ticket)
        df = get_yahoo_data(ticket)
        # general_functions.print_as_json(df)
        print(df.head())
        get_stock_info(ticket)

if __name__ == "__main__":
    main()