# xemapytools Documentation

## 0. Library Organization

The `xemapytools` library is structured as follows:

```
xemapytools/
├── resources/
│   ├── url_list.py
│   └── XEMA_standards.py
├── data_download.py
│   ├── download_simple_csv_from_url_as_dataframe()
│   └── fetch_socrata_csv_with_filters()
├── data_management_main_functions.py
│   └── download_and_backup_XEMA_reference_dataframes()
└── data_treatment.py
    ├── standardize_dataframe()
    ├── save_dataframe_to_local_csv()
    └── load_local_csv_as_dataframe()
```

### Description of Modules

- **data_download**: Functions to download data from URLs, such as CSV files, into pandas DataFrames.
- **data_treatment**: Functions for cleaning, standardizing, and transforming DataFrames.
- **data_management_main_functions**: High-level functions that orchestrate downloading, standardizing, and saving reference data.
- **resources**: Contains reference files and mappings used across the library:
  - `url_list.py`: Stores URLs for reference data sources, including:
    - `STATIONS_STANDARD_DTYPES_MAPPING`
    - `VARIABLES_STANDARD_DTYPES_MAPPING`
    - `WEATHER_DATA_STANDARD_DTYPES_MAPPING`
    - `DAILY_WEATHER_DATA_STANDARD_DTYPES_MAPPING`
  - `XEMA_standards.py`: Defines standard column names and data type mappings for XEMA datasets, including:
    - `STATIONS_STANDARD_COLTOAPI_MAPPING`
    - `VARIABLES_STANDARD_COLTOAPI_MAPPING`
    - `WEATHER_DATA_STANDARD_COLTOAPI_MAPPING`
    - `DAILY_WEATHER_DATA_STANDARD_COLTOAPI_MAPPING`

### Importing

When importing, the commands should follow the structure described above:

```python
import xemapytools.data_management_main_functions as xptdmmf
import xemapytools.data_treatment as xptdt
import xemapytools.data_download as xptdd
from xemapytools.resources import url_list, XEMA_standards
```

And the modules should be later accessed as:

```python
xptdt.load_local_csv_as_dataframe(...)
XEMA_standards.WEATHER_DATA_STANDARD_COLTOAPI_MAPPING
...
```

---

## 1. resources/url_list.py

This module stores URLs for reference and weather data.

### Main URL Endpoints
- `VARIABLES_METADATA_CSV_URL`  
  Accessed with `download_simple_csv_from_url_as_dataframe()`.
- `STATIONS_METADATA_CSV_URL`  
  Accessed with `download_simple_csv_from_url_as_dataframe()`.
- `WEATHER_DATA_CSV_URL`  
  Accessed with `fetch_socrata_csv_with_filters()`.
- `DAILY_WEATHER_DATA_CSV_URL`  
  Accessed with `fetch_socrata_csv_with_filters()`.

---

## 2. resources/XEMA_standards.py

This module defines standard column names and data type mappings for XEMA datasets.  

### Examples:
- `STATIONS_STANDARD_COLTOAPI_MAPPING`
- `VARIABLES_STANDARD_COLTOAPI_MAPPING`
- `WEATHER_DATA_STANDARD_COLTOAPI_MAPPING`
- `DAILY_WEATHER_DATA_STANDARD_COLTOAPI_MAPPING`
- `STATIONS_STANDARD_DTYPES_MAPPING`
- `VARIABLES_STANDARD_DTYPES_MAPPING`
- `WEATHER_DATA_STANDARD_DTYPES_MAPPING`
- `DAILY_WEATHER_DATA_STANDARD_DTYPES_MAPPING`

---
## 3. data_download.py

Contains functions for downloading data from URLs and fetching Socrata CSVs with optional filters. Handles decompression, encoding, and pagination.

### Functions:

- `download_simple_csv_from_url_as_dataframe(url: str, headers: Optional[Dict[str, str]] = None, encoding: str = "utf-8") -> pd.DataFrame`
 Downloads a CSV file from the specified URL using `urllib`. Returns a pandas DataFrame.
 - Parameters:
 - `url` – The CSV URL to download.
 - `headers` – Optional dictionary of HTTP headers to include in the request. Defaults to `{"User-Agent": "python-urllib/3.x"}` if not provided.
 - `encoding` – Text encoding used to decode the response. Defaults to `"utf-8"`.
 - Returns:
 - A pandas DataFrame containing the CSV data.
 - Behavior:
 - Handles gzip and deflate encoded responses.
 - Logs download progress, errors, and the number of rows successfully parsed.

- `fetch_socrata_csv_with_filters(base_url_soql: str, filters: Optional[Dict[str, Condition]] = None, raw_filter: Optional[str] = None, limit: int = 5000, max_rows: Optional[int] = 50000, app_token: Optional[str] = None, timeout: float = 30.0) -> pd.DataFrame`
 Fetches CSV data from a Socrata endpoint using the given filters. Handles pagination with `$limit` and `$offset` and returns a concatenated pandas DataFrame.
 - Parameters:
    - `base_url_soql` – Base Socrata URL (CSV or API endpoint).
    - `filters` – Optional dictionary mapping column names to conditions for filtering. Conditions can be:
        - `str`, `int`, `float` → equality filter
        - `(operator, value)` tuple → e.g., `(">", 100)`
        - List of values or tuples → combined with `AND`
        - `raw_filter` – Optional raw SOQL `$where` clause as a string. Overrides `filters` if provided.
        - `limit` – Number of rows to fetch per request (pagination). Defaults to 5000.
        - `max_rows` – Maximum total rows to fetch. Defaults to 50,000.
        - `app_token` – Optional Socrata App Token for authentication.
        - `timeout` – Timeout in seconds for each HTTP request. Defaults to 30.0.
 - Returns:
    - A pandas DataFrame containing all rows fetched from the endpoint, concatenated across pages.
 - Behavior:
    - Builds a SOQL `$where` clause from `filters` internally.
     - Handles datetime columns (`data_lectura`, `data_extrem`) by converting input strings to Socrata datetime format.
    - Logs each fetch, including URL, HTTP errors, and number of rows returned per page.
    - Stops fetching when fewer rows than `limit` are returned or `max_rows` is reached.
    - Returns an empty DataFrame if errors occur or no data is returned.
 - Supported filter operators: `=`, `!=`, `>`, `<`, `>=`, `<=`

---

## 4. data_management_main_functions.py

Contains high-level orchestration functions.

### Functions:
- `download_and_backup_XEMA_reference_dataframes(base_dir: Union[Path, str], overwrite: bool = True) -> dict[str, Path]`  
  Downloads XEMA reference CSVs (stations and variables), standardizes them, and saves locally. Returns a mapping of descriptive names to saved file paths.

---

## 5. data_treatment.py

Contains functions for cleaning and standardizing DataFrames.

### Functions:
- `standardize_dataframe(df: pd.DataFrame, standard_dtype_map: StandardMap, standard_coltoapi_map: Dict[str, str]) -> pd.DataFrame`  
  Standardizes column names and coerces data types according to mapping.
- `save_dataframe_to_local_csv(df: pd.DataFrame, filepath: Union[Path, str], index: bool = False, overwrite: bool = True) -> None`  
  Saves a DataFrame to a local CSV file, creating parent directories automatically.
- `load_local_csv_as_dataframe(filepath: Union[Path, str], **read_csv_kwargs) -> pd.DataFrame`  
  Loads a CSV from local storage into a pandas DataFrame.

---

## Example usage app

```python
import logging
from pathlib import Path

import xemapytools.data_management_main_functions as dmmf
import xemapytools.data_treatment as dtre
import xemapytools.data_download as ddow
from xemapytools.resources import url_list, XEMA_standards

logging.basicConfig(level=logging.INFO)

BASE_DIR = Path("examples/data_store")
BASE_DIR.mkdir(exist_ok=True)

UPDATE_REFERENCE_DATAFRAMES = True
DOWNLOAD_WEATHER_DATA = False

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

print(stdz_data)

'''

Use stdz data and metadata for what you need: plotting, studying data, ...

'''

```