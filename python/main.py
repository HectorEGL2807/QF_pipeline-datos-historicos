from fetch import fetch_data
from validate import validate_data
from pathlib import Path
import os

def main():
    ticker = input("Ingresa el simbolo de la accion: ")
    years = int(input("Ingresa el numero de años de datos a obtener: "))

    df = fetch_data(ticker, years)

    file_path = Path.cwd() / "data"

    if not Path.exists(file_path):
        Path.mkdir(file_path)

    raw_path = file_path / "raw"

    if not Path.exists(raw_path):
        Path.mkdir(raw_path)

    output_filecsv_raw = os.path.join(raw_path, f"{ticker}_data_raw.csv")
    output_filexlsx_raw = os.path.join(raw_path, f"{ticker}_data_raw.xlsx")

    print(f"✅ Datos sin procesar guardados en: {output_filecsv_raw} y {output_filexlsx_raw}")

    if df is False:
        print("❌ No se puede continuar debido a errores en la obtencion de datos.")
        return

    if validate_data(df) is False:
        print("❌ No se puede continuar debido a errores en los datos.")
        return
    else:
        print(f"✅ Datos obtenidos para {ticker}:")

        processed_path = file_path / "processed"
        if not Path.exists(processed_path):
            Path.mkdir(processed_path)

        output_filecsv_processed = os.path.join(processed_path, f"{ticker}_data_prossesed.csv")
        output_filexlsx_processed = os.path.join(processed_path, f"{ticker}_data_prossesed.xlsx")

        df.to_csv(output_filecsv_processed)
        df.to_excel(output_filexlsx_processed)
        print(f"\t✅ Datos verificados guardados en: {output_filecsv_processed} y {output_filexlsx_processed}")

main()