import pandas as pd
import numpy as np
from validate import validate_data

def make_df_w_errors():
    fechas = pd.to_datetime([
        "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05",
        "2024-01-08", "2024-01-09", "2024-01-10", "2024-01-11",
        "2024-01-12", "2024-01-29", "2024-01-30",
    ])
    return pd.DataFrame({
        "Open":      [100, 104, 105, 100, 108, 100, 105, 107, 108, 135, 136],
        "High":      [105, 106, 107,  98, 104, 110, 108, 109, 140, 137, 138],
        "Low":       [ 99, 103, 104, 102, 100, 105, 104, 106, 107, 133, 135],
        "Close":     [104, 105, 106, 101, 103, 107,  -1, 108, 135, 136, 137],
        "Adj Close": [104, 105, 106, 101, 103, 107, 107, 108, 135, 136,   0],
        "Volume":    [1000, 1100, -500, 1200, 1300, 1250, 1400, np.nan, 5000, 1500, 1000],
    }, index=fechas)

def make_df_valid():
    fechas = pd.date_range("2024-01-02", periods=5, freq="B")  # lun-vie, sin fines de semana
    return pd.DataFrame({
        "Open":      [100, 104, 105, 106, 107],
        "High":      [105, 106, 107, 108, 109],
        "Low":       [ 99, 103, 104, 105, 106],
        "Close":     [104, 105, 106, 107, 108],
        "Adj Close": [104, 105, 106, 107, 108],
        "Volume":    [1000, 1100, 1500, 1200, 1300],
    }, index=fechas)

def test_validate_data_empty_dataframe():

    df_empty = pd.DataFrame()
    result = validate_data(df_empty, days=4, verbose=False)
    assert result["df"].empty
    assert not result["valido"]

def test_validate_data_valid_dataframe():

    result = validate_data(make_df_valid(), days=4, verbose=False)
    assert not result["df"].empty
    assert result["valido"]
    assert not result["errores"]
    assert not result["advertencias"]

def test_validate_data_with_errors():

    result = validate_data(make_df_w_errors(), days=4, verbose=False)

    errores = dict(result["errores"])
    advertencias = dict(result["advertencias"])

    assert not result["valido"]
    assert errores == {
        "Precio de cierre <= 0": 1,
        "Precio de cierre ajustado <= 0": 1,
        "Volumen negativo": 1,
        "High menor que Low": 1,
        "High menor que Open o Close": 2,
        "Low mayor que Open o Close": 3,
        "Valores nulos": 1,
    }
    assert advertencias == {
        "Salto diario > 20%": 2,
        "Huecos de dias en el DataFrame": 1,
    }
