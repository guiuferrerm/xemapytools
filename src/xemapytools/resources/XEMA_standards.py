STATIONS_STANDARD_DTYPES_MAPPING = {
    "codi_estacio": str,
    "nom_estacio": str,
    "codi_tipus": str,
    "latitud": float,
    "longitud": float,
    "geocoded_column": str,  # Point data can be kept as string or parsed separately later
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
    "codi_estat": str,
    "nom_estat": str,
    "data_alta": "datetime",
    "data_baixa": "datetime"
}

VARIABLES_STANDARD_DTYPES_MAPPING = {
    "codi_variable": str, #inconsistency
    "nom_variable": str,
    "unitat": str,
    "acronim": str,
    "codi_tipus_var": str,
    "decimals": int
}

WEATHER_DATA_STANDARD_DTYPES_MAPPING = {
    "id": str,
    "codi_estacio": str,
    "codi_variable": str,
    "data_lectura": "datetime_utc",
    "data_extrem": "datetime_utc",
    "valor_lectura": float,
    "codi_estat": str,
    "codi_base": str,
}
