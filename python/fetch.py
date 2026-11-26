import yfinance as yf
from datetime import datetime, timedelta
from config import DATA_DIR

def fetch_data(ticker, years=1):

    end_date = datetime.today()
    start_date = end_date - timedelta(days=365*years)
    try:
        data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False, multi_level_index=False)

    except Exception as e:
        print(f"❌Error al obtener datos para {ticker}: {e}")
        return False

    return data

def save_data_to_csv(data, ticker, stage="raw"):
    try:
        output_dir = DATA_DIR / stage
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{ticker}_data_{stage}.csv"
        data.to_csv(output_file)
        print(f"✅ Datos guardados en: {output_file}")
        return True
    except Exception as e:
        print(f"❌Error al guardar datos para {ticker}: {e}")
        return False
