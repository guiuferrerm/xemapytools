# xemapytools Documentation

## Library Organization

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



## Example usage

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