from fetch import fetch_data
import pandas as pd
import os

def main():
    ticker = input("Ingresa el simbolo de la accion: ")
    years = int(input("Ingresa el numero de años de datos a obtener: "))

    df = fetch_data(ticker, years)

    if df.empty:
        print(f"❌No se pudieron obtener datos de: {ticker}. Verifica que el simbolo sea correcto.")

    else:
        print(f"✅Datos obtenidos para {ticker}:")

        file_path = r"/Users/hectoregl/Documents/Quant finance/EJEMPLOS/QF_proyecto-1/data"

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        output_filecsv = os.path.join(file_path, f"{ticker}_data.csv")
        output_filexlsx = os.path.join(file_path, f"{ticker}_data.xlsx")

        df.to_csv(output_filecsv, index=False)
        df.to_excel(output_filexlsx)
        print(f"✅Datos guardados en: {output_filecsv} y {output_filexlsx}")

main()