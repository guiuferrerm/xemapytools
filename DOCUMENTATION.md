# xemapytools Documentation

## 0. Library Organization

The `xemapytools` library is now structured as follows, with the addition of a new internal utility module and updated functions.

```
xemapytools/
├── resources/
│   ├── url_list.py
│   └── XEMA_standards.py
├── data_download.py
│   ├── download_simple_csv_from_url_as_dataframe()
│   └── fetch_socrata_csv_with_filters()
├── _utils.py
│   └── haversine_km()
├── main_functions.py
│   ├── download_and_backup_XEMA_reference_dataframes()
│   ├── get_stations_by_radius()
│   └── get_geographic_circle()
└── data_treatment.py
    ├── standardize_dataframe()
    ├── save_dataframe_to_local_csv()
    └── load_local_csv_as_dataframe()


```

### Description of Modules

* **data_download**: Functions to download data from URLs, such as CSV files, into pandas DataFrames.

* **data_treatment**: Functions for cleaning, standardizing, and transforming DataFrames.

* **main_functions**: High-level orchestration and utility functions that handle data processing pipelines and advanced geospatial tasks.

* **resources**: Contains reference files and mappings used across the library, including URLs (`url_list.py`) and standard column definitions (`XEMA_standards.py`).

* **\_utils**: An internal-only module containing auxiliary functions not intended for direct use by the end user, such as geospatial calculations. This is used by `main_functions`.

### Importing

When importing, the commands should follow the structure described above:

```
import xemapytools.main_functions as xptmf
import xemapytools.data_treatment as xptdt
import xemapytools.data_download as xptdd
from xemapytools.resources import url_list, XEMA_standards


```

And the modules should be later accessed as:

```
xptdt.load_local_csv_as_dataframe(...)
XEMA_standards.WEATHER_DATA_STANDARD_COLTOAPI_MAPPING
...


```

## 1. resources/url_list.py

This module stores URLs for reference and weather data.

### Main URL Endpoints

* `VARIABLES_METADATA_CSV_URL`

  * Accessed with `download_simple_csv_from_url_as_dataframe()`.

* `STATIONS_METADATA_CSV_URL`

  * Accessed with `download_simple_csv_from_url_as_dataframe()`.

* `WEATHER_DATA_CSV_URL`

  * Accessed with `fetch_socrata_csv_with_filters()`.

* `DAILY_WEATHER_DATA_CSV_URL`

  * Accessed with `fetch_socrata_csv_with_filters()`.

## 2. resources/XEMA_standards.py

This module defines standard column names and data type mappings for XEMA datasets.

### Examples:

* `STATIONS_STANDARD_COLTOAPI_MAPPING`

* `VARIABLES_STANDARD_COLTOAPI_MAPPING`

* `WEATHER_DATA_STANDARD_COLTOAPI_MAPPING`

* `DAILY_WEATHER_DATA_STANDARD_COLTOAPI_MAPPING`

* `STATIONS_STANDARD_DTYPES_MAPPING`

* `VARIABLES_STANDARD_DTYPES_MAPPING`

* `WEATHER_DATA_STANDARD_DTYPES_MAPPING`

* `DAILY_WEATHER_DATA_STANDARD_DTYPES_MAPPING`

## 3. data_download.py

Contains functions for downloading data from URLs.

### Functions:

* `download_simple_csv_from_url_as_dataframe(url: str, headers: Optional[Dict[str, str]] = None, encoding: str = "utf-8") -> pd.DataFrame`

  * Downloads a CSV file from a URL using `urllib`. Handles gzip/deflate response encoding if present, decodes with the specified encoding, and returns a pandas DataFrame.

* `build_soql_where_clause(filters: Optional[Dict[str, Condition]] = None, raw_filter: Optional[str] = None) -> str`

  * Builds a SOQL `where` clause from a filter dictionary or a raw filter string. This function internally formats SOQL where clauses from filter dictionaries; users do not need to call helper functions directly.

* `fetch_socrata_csv_with_filters(base_url_soql: str, filters: Optional[Dict[str, Condition]] = None, raw_filter: Optional[str] = None, limit: int = 5000, max_rows: Optional[int] = 50000, app_token: Optional[str] = None, timeout: float = 30.0) -> pd.DataFrame`

  * Fetches CSV data from a Socrata endpoint using the given filters. Handles pagination with `limit` and `offset` and returns a concatenated pandas DataFrame.

#### Filters for `fetch_socrata_csv_with_filters`

* Format: `filters: Dict[str, Condition]` where each key is a column name and each value (`Condition`) can be:

  * A single value → exact match, e.g. `"station_id": "123"`

  * A tuple (`operator`, `value`) → custom operator, e.g. `"temperature": (">=", 25)`

  * A list of values/tuples → combined with AND, e.g. `"temperature": [(">=", 25), ("<=", 30)]`

* Supported operators (examples): `"=", "!=", ">", ">=", "<", "<="`

* Datetime columns are automatically converted to SOQL format.

## 4. \_utils.py

This new internal module contains auxiliary functions not intended for direct use by the end user.

### Functions:

* `haversine_km(lat1, lon1, lat2, lon2)`: Calculates the great-circle distance (in km) between two points using the Haversine formula.

## 5. main_functions.py

This module now includes high-level geospatial functions, in addition to the existing data downloading and backup function.

### Functions:

* `download_and_backup_XEMA_reference_dataframes(base_dir: Union[Path, str], overwrite: bool = True) -> dict[str, Path]`: Downloads XEMA reference CSVs (stations and variables), standardizes them, and saves them locally. Returns a mapping of descriptive names to saved file paths.

* `get_stations_by_radius(lat: float, lon: float, radius_km: float, data_source: Union[pd.DataFrame, Path, str]) -> pd.DataFrame`: Filters XEMA station data by a specific radius and returns a DataFrame with the stations found, including the distance from the central point.

* `get_geographic_circle(center_lat, center_lon, radius_km, n_points=100)`: Returns the latitudes and longitudes that form a geographic circle of `radius_km`.

## Example usage app

⚠️ (Uses extra library: `plotly` to plot the data)

```
import plotly.express as px

import logging
from pathlib import Path
import pandas as pd

import xemapytools.main_functions as xptmf
import xemapytools.data_treatment as xptdt
import xemapytools.data_download as xptdd
from xemapytools.resources import url_list, XEMA_standards

logging.basicConfig(level=logging.INFO)

BASE_DIR = Path("examples/data_store")

# CHECK THIS: IF NO DATA, MUST BE SET TO TRUE TO FETCH
UPDATE_REFERENCE_DATAFRAMES = True
DOWNLOAD_WEATHER_DATA = True

if UPDATE_REFERENCE_DATAFRAMES:
    paths = xptmf.download_and_backup_XEMA_reference_dataframes(BASE_DIR)
else:
    paths = {
        "stations_raw": BASE_DIR / "stations_raw_metadata.csv",
        "variables_raw": BASE_DIR / "variables_raw_metadata.csv",
    }

stations_metadata = xptdt.load_local_csv_as_dataframe(paths["stations_raw"])
variables_metadata = xptdt.load_local_csv_as_dataframe(paths["variables_raw"])

# New example demonstrating the get_stations_by_radius function
central_lat, central_lon = 41.3851, 2.1734  # Barcelona
radius = 10  # km
nearby_stations = xptmf.get_stations_by_radius(
    lat=central_lat,
    lon=central_lon,
    radius_km=radius,
    data_source=stations_metadata # Can be a DataFrame or a path
)
print(f"Stations found within {radius} km of Barcelona:")
print(nearby_stations[['codi_estacio', 'nom_estacio', 'dist_km']])

# Rest of the original plotting code remains the same
if DOWNLOAD_WEATHER_DATA:
    filters = {
        "codi_estacio": "V4",
        "data_lectura": [
            (">=", "01/01/2015 12:00:00 AM"),
            ("<=", "03/01/2015 12:00:00 AM"),
        ],
    }
    weather_data = xptdd.fetch_socrata_csv_with_filters(
        base_url_soql=url_list.WEATHER_DATA_CSV_URL,
        filters=filters,
        limit=5000,
        app_token="",  # Optional
    )
    xptdt.save_dataframe_to_local_csv(weather_data, BASE_DIR / "downloaded_weather_data.csv")
else:
    weather_data = xptdt.load_local_csv_as_dataframe(BASE_DIR / "downloaded_weather_data.csv")

stdz_data = xptdt.standardize_dataframe(weather_data, XEMA_standards.WEATHER_DATA_STANDARD_DTYPES_MAPPING, XEMA_standards.WEATHER_DATA_STANDARD_COLTOAPI_MAPPING)

# Load the variables metadata
variables_metadata = xptdt.load_local_csv_as_dataframe("examples/data_store/variables_raw_metadata.csv")

variables_metadata = xptdt.standardize_dataframe(variables_metadata, XEMA_standards.VARIABLES_STANDARD_DTYPES_MAPPING, XEMA_standards.VARIABLES_DATA_STANDARD_COLTOAPI_MAPPING)

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
    title='Weather Measurements Over Time',
    labels={
        'data_lectura': 'Date',
        'valor_lectura': 'Value',
        'variable_name': 'Variable',
        'codi_estacio': 'Station'
    }
)

fig.show()
