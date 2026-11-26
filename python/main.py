from fetch import fetch_data, save_data_to_csv
from validate import validate_data, clean_data
from plot import plot_chart, plot_candle
from config import PLOTS_DIR

def main(tickers, years=1, days=4, verbose=False):
    tickers = list(dict.fromkeys(t for t in tickers if t))

    if not tickers:
        print("❌ No se proporcionaron tickers.")
        return

    results = {}

    for ticker in tickers:
        print(f"📈 Procesando {ticker}...")
        try:
            results[ticker] = process_ticker(ticker, years, days, verbose)
        except Exception as e:
            results[ticker] = failed_result(f"Excepcion: {e}")

    resume_pipeline(results)

def enter_data():
    tickers = input("Ingresa los simbolos de las acciones separados por comas: ").split(",")
    tickers = [ticker.strip().upper() for ticker in tickers]

    try:
        years = int(input("Ingresa el numero de años de datos a obtener: (1)") or 1)
        days = int(input("¿Que umbral de dias sin datos quiere revisar? (4)") or 4)
        verbose_input = input("¿Desea ver información detallada del DataFrame? (s/n) (n): ").strip().lower()
        verbose = True if verbose_input == 's' else False
    except ValueError:
        print("❌ Error: El número de años y dias debe ser un entero.")
        return

    main(tickers, years, days, verbose)

def failed_result(message):
    """Resultado con el mismo formato que validate_data, para tickers que fallan."""
    return {"df": None, "errores": [(message, 0)], "advertencias": [], "valido": False}

def process_ticker(ticker, years, days, verbose=False):
    df = fetch_data(ticker, years)
    if df is False or df.empty:
        return failed_result("Descarga fallida o sin datos")

    save_data_to_csv(df, ticker, stage="raw")
    df_clean = clean_data(df)
    result = validate_data(df_clean, days, verbose=verbose)

    if result["valido"]:
        save_data_to_csv(result["df"], ticker, stage="processed")
        plot_chart(result["df"], ticker, output_dir=PLOTS_DIR, show=False)
        plot_candle(result["df"], ticker, output_dir=PLOTS_DIR, show=False)

    return result

def resume_pipeline(results):
    print("\n" + "=" * 46)
    print(f"{'TICKER':<10}{'ESTADO':<12}{'ERRORES':>12}{'ADVERT.':>12}")
    print("-" * 46)

    for ticker, r in results.items():
        state = "VÁLIDO" if r["valido"] else "CON ERRORES"
        print(f"{ticker:<10}{state:<12}{len(r['errores']):>12}{len(r['advertencias']):>12}")

    total = len(results)
    valid = sum(r["valido"] for r in results.values())
    print("-" * 46)
    print(f"{total} tickers: {valid} válidos, {total - valid} con errores")

    for ticker, r in results.items():
        for name, n in r["errores"]:
            print(f"  ❌ [{ticker}] {name}" + (f": {n}" if n else ""))
        for name, n in r["advertencias"]:
            print(f"  ❕ [{ticker}] {name}" + (f": {n}" if n else ""))

if __name__ == "__main__":
    enter_data()