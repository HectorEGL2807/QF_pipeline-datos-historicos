import yfinance as yf
from datetime import datetime, timedelta

def fetch_data(ticker, years=1):

    ticker = ticker.upper()

    start_date = datetime.today()
    end_date = start_date - timedelta(days=365*years)
    try:
        data = yf.download(ticker, start=end_date, end=start_date, auto_adjust=False, multi_level_index=False)

    except Exception as e:
        print(f"❌Error al obtener datos para {ticker}: {e}")
        return False

    return data
