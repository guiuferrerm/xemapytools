# xemapytools

A lightweight Python library to fetch, standardize, and manage meteorological data from the XEMA Open Data API of Catalonia's transparency portal.

## Features

- Download CSV data directly from Socrata SoQL endpoints with support for server-side filtering.
- Handle compressed HTTP responses (gzip, deflate).
- Standardize data columns with precise type coercion, including timezone-aware UTC datetime parsing
- Save and load dataframes with automatic directory creation.
- Detailed warnings and logs on data coercion and fetch errors.

---

## Installation & updates

To install or update the package, run those two commands on terminal (pandas required):

```bash
pip install pandas
pip install --upgrade git+https://github.com/guiuferrerm/xemapytools.git@v1.1.0
```

---

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

Access those resources from `xemapytools.resources.XEMA_standards` and `xemapytools.resources.url_list` respectively

---

## Logging

The library uses Python's `logging` module to warn about coercion issues during parsing. Configure your logging to see these messages.

Example:

```python
import logging
logging.basicConfig(level=logging.WARNING)  # Shows warnings about type coercion during parsing

```

---

## For developers: testing and modifying own copies
This guide explains how to install `xemapytools` in **editable mode** so you can test, modify, and contribute to the library, and how to fully uninstall it afterwards.

### **1. Clone the repository**

```bash
git clone https://github.com/guiuferrerm/xemapytools.git
cd xemapytools
```

---

### **2. Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

---

### **3. Install the library in editable mode**

```bash
pip install -e .
```

- The `-e` flag installs the library in **development/editable mode**.  
- Changes you make to the source code will immediately affect the installed library without reinstalling.

---

### **4. Verify installation**

```bash
pip list | grep xemapytools
```

You should see something like:

```
xemapytools (0.1.2, editable)
```

---
---

### **5. Uninstall the editable package**

```bash
pip uninstall xemapytools
```

#### Optional: Remove leftover files

1. Find your site-packages directory:

```bash
python -m site
```

2. Locate the `.egg-link` file corresponding to `xemapytools` in `site-packages`.

```bash
ls path_to_site_packages/*.egg-link
```

3. Remove the `.egg-link` file manually:

```bash
rm path_to_site_packages/xemapytools.egg-link
```

4. (Optional) Edit `easy-install.pth` in the same `site-packages` folder and remove the line pointing to the development directory.

---

### **6. Reinstall normally (optional)**

After uninstalling, if you want a regular install:

```bash
pip install .
```
---

This setup allows contributors to **test and improve the library directly from the GitHub repository**, and to create own variations of the software. Any changes made to the source code will immediately reflect in the environment.

---

## Contributing

⚠️⚠️ This project is **not actively maintained** ⚠️⚠️

However, if you want to submit issues or pull requests, please follow **PEP 8** style guidelines for Python code.

---

## License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0).

See [LICENSE](LICENSE) for details.

---

## References

- [XEMA Open Data Portal](https://analisi.transparenciacatalunya.cat/Medi-Ambient/Dades-meteorol-giques-de-la-XEMA/nzvn-apee/about_data)
- [Socrata Open Data API](https://dev.socrata.com/)
