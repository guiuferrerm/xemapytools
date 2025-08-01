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
    "codi_xarxa": str
}

VARIABLES_STANDARD_DTYPES_MAPPING = {
    "codi_variable": float,
    "nom_variable": str,
    "unitat": str,
    "acronim": str,
    "codi_tipus_var": str,
    "decimals": float
}

WEATHER_DATA_STANDARD_DTYPES_MAPPING = {
    "id": str,
    "codi_estacio": str,
    "codi_variable": float, #inconsistency
    "data_lectura": "datetime_utc",
    "data_extrem": "datetime_utc",
    "valor_lectura": float,
    "codi_estat": str,
    "codi_base": str,
}
