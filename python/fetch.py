import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_data(ticker, years=1):

    start_date = datetime.today()
    end_date = start_date - timedelta(days=365*years)
    try:
        data = yf.download(ticker, start=end_date, end=start_date, auto_adjust=False)

    except Exception as e:
        print(f"❌Error al obtener datos para {ticker}: {e}")
        return pd.DataFrame()

    return data[['Open', 'High', 'Low', 'Adj Close', 'Volume']]
