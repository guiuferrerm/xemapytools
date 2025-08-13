import plotly.express as px

import logging
from pathlib import Path
import pandas as pd

import xemapytools.data_management_main_functions as dmmf
import xemapytools.data_treatment as dtre
import xemapytools.data_download as ddow
from xemapytools.resources import url_list, XEMA_standards

logging.basicConfig(level=logging.INFO)

BASE_DIR = Path("examples/data_store")

UPDATE_REFERENCE_DATAFRAMES = True
DOWNLOAD_WEATHER_DATA = True

if UPDATE_REFERENCE_DATAFRAMES:
    paths = dmmf.download_and_backup_XEMA_reference_dataframes(BASE_DIR)
else:
    paths = {
        "stations_raw": BASE_DIR / "stations_raw_metadata.csv",
        "variables_raw": BASE_DIR / "variables_raw_metadata.csv",
    }

stations_metadata = dtre.load_local_csv_as_dataframe(paths["stations_raw"])
variables_metadata = dtre.load_local_csv_as_dataframe(paths["variables_raw"])

if DOWNLOAD_WEATHER_DATA:
    filters = {
        "codi_estacio": "V4",
        "data_lectura": [
            (">=", "01/01/2009 12:00:00 AM"),
            ("<=", "10/01/2009 12:00:00 AM"),
        ],
    }
    weather_data = ddow.fetch_socrata_csv_with_filters(
        base_url_soql=url_list.WEATHER_DATA_CSV_URL,
        filters=filters,
        limit=5000,
        app_token="",  # Optional
    )
    dtre.save_dataframe_to_local_csv(weather_data, BASE_DIR / "downloaded_weather_data.csv")
else:
    weather_data = dtre.load_local_csv_as_dataframe(BASE_DIR / "downloaded_weather_data.csv")

stdz_data = dtre.standardize_dataframe(weather_data, XEMA_standards.WEATHER_DATA_STANDARD_DTYPES_MAPPING, XEMA_standards.WEATHER_DATA_STANDARD_COLTOAPI_MAPPING)

# Load the variables metadata
variables_metadata = dtre.load_local_csv_as_dataframe("examples/data_store/variables_raw_metadata.csv")

variables_metadata = dtre.standardize_dataframe(variables_metadata, XEMA_standards.VARIABLES_STANDARD_DTYPES_MAPPING, XEMA_standards.VARIABLES_STANDARD_COLTOAPI_MAPPING)

# Map codi_variable to nom_variable
variable_map = dict(zip(variables_metadata['codi_variable'], variables_metadata['nom_variable']))
stdz_data['variable_name'] = stdz_data['codi_variable'].map(variable_map)

# Plot all variables over time, with log scale
fig = px.line(
    stdz_data,
    x='data_lectura',
    y='valor_lectura',
    color='variable_name',       # readable variable names
    line_group='codi_estacio',   # different lines for different stations
    title='Weather Measurements Over Time (Log Scale)',
    labels={
        'data_lectura': 'Date',
        'valor_lectura': 'Value',
        'variable_name': 'Variable',
        'codi_estacio': 'Station'
    },
    log_y=True                   # log scale on y-axis
)

fig.show()
