
def validate_data(df):
    if df.empty:
        print("❌El DataFrame esta vácio.")
        return False

    print(df.info())
    print(f"📊 Tipos de datos: \n {df.dtypes}")
    print(f"📊 El índice es monotónico creciente: \n {df.index.is_monotonic_increasing}")
    print(f"📊 Columnas con valores nulos: \n {df.isna().sum()}")

    hay_errores = False

    reglas = {
        "Precio de cierre <= 0": df["Close"] <= 0,
        "Volumen negativo": df["Volume"] < 0,
        "High menor que Low": df["High"] < df["Low"],
        "High menor que Open o Close": (df["High"] < df["Open"]) | (df["High"] < df["Close"]),
        "Low mayor que Open o Close": (df["Low"] > df["Open"]) | (df["Low"] > df["Close"]),
        "Salto diario > 20%": df["Close"].pct_change().abs() > 0.20,
    }

    print("🔍 Validando datos del DataFrame...")

    errores = []

    for regla, condicion in reglas.items():

        n = condicion.sum()

        if n > 0:
            print(f"\t❌ ERROR: {regla}. Filas afectadas: {n}")
            hay_errores = True
            errores.append((regla, n))
            print(df[condicion].head(10))
        else:
            print(f"\t✅ {regla}: No se encontraron errores.")

    faltantes = df.isna().sum()

    if faltantes.any():
        hay_errores = True
        print(f"❌ Columnas con valores nulos: \n {faltantes[faltantes > 0]}")
    else:
        print("✅ No se encontraron valores nulos.")

    if hay_errores:

        if errores:
            print("\nResumen de errores encontrados:")
            for regla, n in errores:
                if regla == "Salto diario > 20%":
                    print(f"\t❕ {regla}: {n} filas afectadas (puede ser un evento de mercado válido)")
                    pass
                else:
                    print(f"\t❌ {regla}: {n} filas afectadas")
        
        print("❌ Se encontraron errores en los datos. Por favor, revisa el DataFrame.")
        return False
    else:
        print("✅ No se encontraron errores en los datos. El DataFrame es válido.")
        return True
    