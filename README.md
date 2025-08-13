 # xemapytools
 
 A lightweight Python library to fetch, standardize, and manage meteorological data from the XEMA Open Data API of Catalonia's transparency portal.
 
 ## Features
 
 - Download CSV data directly from Socrata SoQL endpoints with support for server-side filtering.
 - Handle compressed HTTP responses (gzip, deflate).
 - Standardize data columns with precise type coercion, including timezone-aware UTC datetime parsing
 - Save and load dataframes with automatic directory creation.
 - Detailed warnings and logs on data coercion and fetch errors.
 
 ## Installation & updates

 To install the package, run those two commands on terminal (pandas required):

 ```
 pip install pandas
 pip install --upgrade git+https://github.com/guiuferrerm/xemapytools.git@v0.1.1
 ```

 To update the package, just run:
 ```
 pip install --upgrade git+https://github.com/guiuferrerm/xemapytools.git@v0.1.1
 ```
 
 ## Data Type Mappings & URLs
 
 The library provides standard dtype:
 - `STATIONS_STANDARD_DTYPES_MAPPING`
 - `VARIABLES_STANDARD_DTYPES_MAPPING`
 - `WEATHER_DATA_STANDARD_DTYPES_MAPPING`
 - `DAILY_WEATHER_DATA_STANDARD_DTYPES_MAPPING`
 
 And column name mappings:
 - `STATIONS_STANDARD_COLTOAPI_MAPPING`
 - `VARIABLES_STANDARD_COLTOAPI_MAPPING`
 - `WEATHER_DATA_STANDARD_COLTOAPI_MAPPING`
 - `DAILY_WEATHER_DATA_STANDARD_COLTOAPI_MAPPING`
 
 for the main XEMA datasets
 
 Use them along with the function `standardize_dataframe()` for consistent column types.

 There are also the four main URL endpoints for data fetching:
 - `VARIABLES_METADATA_CSV_URL` , accessed with `download_simple_csv_from_url_as_dataframe()`
 - `STATIONS_METADATA_CSV_URL` , accessed with `download_simple_csv_from_url_as_dataframe()`
 - `WEATHER_DATA_CSV_URL` , accessed with `fetch_socrata_csv_with_filters()`
 - `DAILY_WEATHER_DATA_CSV_URL` , accessed with `fetch_socrata_csv_with_filters()`

 Access those resources from `xemapytools.resources.XEMA_standards` and `xemapytools.resources.url_list` respectively`
 
 ## Logging
 
 The library uses Python's `logging` module to warn about coercion issues during parsing. Configure your logging to see these messages.
 
 Example:
 
 ```
 import logging
 logging.basicConfig(level=logging.WARNING)
 ```
 
 ## Contributing
 
 ⚠️ This project is **not actively maintained**.  
 However, if you want to submit issues or pull requests, please follow **PEP 8** style guidelines for Python code.
 
 ## License
 
 This project is licensed under the Mozilla Public License 2.0 (MPL-2.0).
 
 See [LICENSE](LICENSE) for details.
 
 ## References
 
 - [XEMA Open Data Portal](https://analisi.transparenciacatalunya.cat/Medi-Ambient/Dades-meteorol-giques-de-la-XEMA/nzvn-apee/about_data)
 - [Socrata Open Data API](https://dev.socrata.com/)
