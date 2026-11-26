
def validate_data(df, days=4, verbose=True):
    """Funcion para validar un DataFrame de datos financieros.
    Args:
        df (pd.DataFrame): DataFrame con datos financieros.
        days (int): Umbral de días sin datos para revisar huecos en el índice.
    Returns:
        dict: Diccionario con el DataFrame limpio, errores, advertencias y validez del DataFrame.
    """

    df_clean = df.copy()
    errors = []
    alerts = []
    valid = True

    if df_clean.empty:
        print("❌El DataFrame esta vácio.")
        errors.append(("DataFrame vacío", 0))
        valid = False

        return {
            "df": df_clean, 
            "errores": errors, 
            "advertencias": alerts, 
            "valido": valid
        }

    if verbose:
        df_clean.info()
        print(f"📊 Tipos de datos: \n {df_clean.dtypes}")
        print(f"📊 El índice es monotónico creciente: \n {df_clean.index.is_monotonic_increasing}")

    reglas = {
        "Precio de cierre <= 0": df_clean["Close"] <= 0,
        "Precio de cierre ajustado <= 0": df_clean["Adj Close"] <= 0,
        "Volumen negativo": df_clean["Volume"] < 0,
        "High menor que Low": df_clean["High"] < df_clean["Low"],
        "High menor que Open o Close": (df_clean["High"] < df_clean["Open"]) | (df_clean["High"] < df_clean["Close"]),
        "Low mayor que Open o Close": (df_clean["Low"] > df_clean["Open"]) | (df_clean["Low"] > df_clean["Close"]),
    }

    advertencias = {
        "Salto diario > 20%": df_clean["Adj Close"].pct_change().abs() > 0.20,
    }

    if verbose:
        print("🔍 Validando datos del DataFrame...")

    for regla, condicion in reglas.items():
        n = condicion.sum()

        if n > 0:
            print(f"\t❌ ERROR: {regla}. Filas afectadas: {n}")
            valid = False
            errors.append((regla, n))
        elif verbose:
            print(f"\t✅ {regla}: No se encontraron errores.")

    for advertencia, condicion in advertencias.items():
        n = condicion.sum()

        if n > 0:
            print(f"\t❕ ADVERTENCIA: {advertencia}. Filas afectadas: {n}")

            alerts.append((advertencia, n))
        elif verbose:
            print(f"\t✅ {advertencia}: No se encontraron advertencias.")

    gaps = check_gaps(df_clean, days)
    if gaps > 0:
        alerts.append(("Huecos de dias en el DataFrame", gaps))

    faltantes = df_clean.isna().sum()
    if faltantes.any():
        print(f"❌ Se encontraron valores nulos en las siguientes columnas: \n{faltantes[faltantes > 0]}")
        errors.append(("Valores nulos", int(faltantes.sum())))
        valid = False

    if valid == False:
        print("❌ Se encontraron errores en los datos. Por favor, revisa el DataFrame.")
    else:
        if verbose:
            print("✅ No se encontraron errores en los datos. El DataFrame es válido.")

    return {
        "df": df_clean, 
        "errores": errors, 
        "advertencias": alerts, 
        "valido": valid
    }

def clean_data(df):
    """Funcion para limpiar un DataFrame de datos financieros.
    Args:
        df (pd.DataFrame): DataFrame con datos financieros.
    Returns:
        pd.DataFrame: DataFrame limpio y ordenado."""

    df = df.copy()
    n = df.index.duplicated().sum()
    if n > 0:
        print(f"❕ Se eliminaron {n} fechas duplicadas")
    df = df[~df.index.duplicated(keep="last")]
    return df.sort_index()

def check_gaps(df, max_dias=4):
    fechas = df.index.to_series()
    dif = fechas.diff().dt.days
    mask = dif > max_dias

    for hasta, desde, dias in zip(fechas[mask], fechas.shift()[mask], dif[mask]):
        print(f"\t❕ Hueco de {int(dias)} días entre {desde.date()} y {hasta.date()}")

    return int(mask.sum())