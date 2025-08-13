STATIONS_STANDARD_DTYPES_MAPPING = {
    "codi_estacio": str,
    "nom_estacio": str,
    "codi_tipus": str,
    "latitud": float,
    "longitud": float,
    "geocoded_column": str,  # Punt — store as string or parse separately
    "emplacament": str,
    "altitud": float,
    "codi_municipi": str,
    "nom_municipi": str,
    "codi_comarca": str,
    "nom_comarca": str,
    "codi_provincia": str,
    "nom_provincia": str,
    "codi_xarxa": str,
    "nom_xarxa": str,
    "codi_estat_ema": str,
    "nom_estat_ema": str,
    "data_inici": "datetime_utc",
    "data_fi": "datetime_utc",
}

STATIONS_STANDARD_COLTOAPI_MAPPING = {
    "CODI_ESTACIO":        "codi_estacio",
    "NOM_ESTACIO":         "nom_estacio",
    "CODI_TIPUS":          "codi_tipus",
    "LATITUD":             "latitud",
    "LONGITUD":            "longitud",
    "Georeferència":       "geocoded_column",
    "EMPLACAMENT":         "emplacament",
    "ALTITUD":             "altitud",
    "CODI_MUNICIPI":       "codi_municipi",
    "NOM_MUNICIPI":        "nom_municipi",
    "CODI_COMARCA":        "codi_comarca",
    "NOM_COMARCA":         "nom_comarca",
    "CODI_PROVINCIA":      "codi_provincia",
    "NOM_PROVINCIA":       "nom_provincia",
    "CODI_XARXA":          "codi_xarxa",
    "NOM_XARXA":           "nom_xarxa",
    "CODI_ESTAT":          "codi_estat_ema",
    "NOM_ESTAT":           "nom_estat_ema",
    "DATA_ALTA":           "data_inici",
    "DATA_BAIXA":          "data_fi",
}

VARIABLES_STANDARD_DTYPES_MAPPING = {
    "codi_variable": str,  # Portal says "Nombre" but treat as string for consistency
    "nom_variable": str,
    "unitat": str,
    "acronim": str,
    "codi_tipus_var": str,
    "decimals": int,
}

VARIABLES_STANDARD_COLTOAPI_MAPPING = {
    "CODI_VARIABLE":   "codi_variable",
    "NOM_VARIABLE":    "nom_variable",
    "UNITAT":          "unitat",
    "ACRONIM":         "acronim",
    "CODI_TIPUS_VAR":  "codi_tipus_var",
    "DECIMALS":        "decimals",
}

WEATHER_DATA_STANDARD_DTYPES_MAPPING = {
    "id": str,
    "codi_estacio": str,
    "codi_variable": str,  # treat as string
    "data_lectura": "datetime_utc",
    "data_extrem": "datetime_utc",
    "valor_lectura": float,
    "codi_estat": str,
    "codi_base": str,
}

WEATHER_DATA_STANDARD_COLTOAPI_MAPPING = {
    "ID":             "id",
    "CODI_ESTACIO":   "codi_estacio",
    "CODI_VARIABLE":  "codi_variable",
    "DATA_LECTURA":   "data_lectura",
    "DATA_EXTREM":    "data_extrem",
    "VALOR_LECTURA":  "valor_lectura",
    "CODI_ESTAT":     "codi_estat",
    "CODI_BASE":      "codi_base",
}

DAILY_WEATHER_DATA_STANDARD_DTYPES_MAPPING = {
    "id": str,
    "codi_estacio": str,
    "nom_estacio": str,
    "data_lectura": "datetime_utc",
    "codi_variable": str,  # treat as string
    "nom_variable": str,
    "valor": float,
    "unitat": str,
    "hora_tu": str,
    "estat": str,
}

DAILY_WEATHER_DATA_STANDARD_COLTOAPI_MAPPING = {
    "ID":            "id",
    "CODI_ESTACIO":  "codi_estacio",
    "NOM_ESTACIO":   "nom_estacio",
    "DATA_LECTURA":  "data_lectura",
    "CODI_VARIABLE": "codi_variable",
    "NOM_VARIABLE":  "nom_variable",
    "VALOR":         "valor",
    "UNITAT":        "unitat",
    "HORA_TU":       "hora_tu",
    "ESTAT":         "estat",
}
