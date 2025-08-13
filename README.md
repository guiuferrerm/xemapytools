 # xemapytools
 
 A lightweight Python library to fetch, standardize, and manage meteorological data from the XEMA Open Data API of Catalonia's transparency portal.
 
 ## Features
 
 - Download CSV data directly from Socrata SoQL endpoints with support for server-side filtering.
 - Handle compressed HTTP responses (gzip, deflate).
 - Standardize data columns with precise type coercion, including timezone-aware UTC datetime parsing
 - Save and load dataframes with automatic directory creation.
 - Detailed warnings and logs on data coercion and fetch errors.
 
 ## Installation
 
 ```
 pip install pandas
 pip install --upgrade git+https://github.com/guiuferrerm/xemapytools.git@v0.1.1
 ```
 
 ## Usage

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

UPDATE_REFERENCE_DATAFRAMES = False
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

stdz_data = dtre.standardize_dataframe(weather_data, XEMA_standards.WEATHER_DATA_STANDARD_DTYPES_MAPPING)

print(stdz_data.head())
```

Without library installed, run the example file with:

```bash
PYTHONPATH=src python examples/examplefile.py
```
 
 ## Data Type Mappings & URLs
 
 The library provides standard dtype mappings for the main XEMA datasets:
 
 - `STATIONS_STANDARD_DTYPES_MAPPING`
 - `VARIABLES_STANDARD_DTYPES_MAPPING`
 - `WEATHER_DATA_STANDARD_DTYPES_MAPPING`
 
 Use them with `standardize_dataframe` for consistent column types.

 It also gives the four main URL endpoints for data fetching:
 - `VARIABLES_METADATA_CSV_URL`
 - `STATIONS_METADATA_CSV_URL`
 - `WEATHER_DATA_CSV_URL`
 - `DAY_SUMMARY_WEATHER_DATA_CSV_URL`

 Access those resources from `xemapytools.resources.XEMA_standards` and `xemapytools.resources.url_list` respectively`
 
 ## Logging
 
 The library uses Python's `logging` module to warn about coercion issues during parsing. Configure your logging to see these messages.
 
 Example:
 
 ```
 import logging
 logging.basicConfig(level=logging.WARNING)
 ```
 
 ## Contributing
 
 Feel free to submit issues or pull requests. Please follow PEP8 style guidelines.
 
 ## License
 
 This project is licensed under the Mozilla Public License 2.0 (MPL-2.0).
 
 See [LICENSE](LICENSE) for details.
 
 ## References
 
 - [XEMA Open Data Portal](https://analisi.transparenciacatalunya.cat/Medi-Ambient/Dades-meteorol-giques-de-la-XEMA/nzvn-apee/about_data)
 - [Socrata Open Data API](https://dev.socrata.com/)
