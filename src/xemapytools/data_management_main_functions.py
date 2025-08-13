from pathlib import Path
import logging
from typing import Union
import pandas as pd

import xemapytools.data_download as data_download
import xemapytools.data_treatment as data_treatment
import xemapytools.resources.XEMA_standards as XEMA_standards
import xemapytools.resources.url_list as url_list

logger = logging.getLogger(__name__)


def download_and_backup_XEMA_reference_dataframes(
    base_dir: Union[Path, str],
    overwrite: bool = True,
) -> dict[str, Path]:
    """
    Download XEMA reference CSVs (stations and variables) and save standardized copies.
    
    Returns a mapping of descriptive names to saved file paths.
    """
    base = Path(base_dir)
    base.mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensured base directory exists: {base.resolve()}")

    saved_paths: dict[str, Path] = {}

    resources = [
        (
            "stations_raw",
            url_list.STATIONS_METADATA_CSV_URL,
            XEMA_standards.STATIONS_STANDARD_DTYPES_MAPPING,
            XEMA_standards.STATIONS_STANDARD_COLTOAPI_MAPPING,
            base / "stations_raw_metadata.csv",
        ),
        (
            "variables_raw",
            url_list.VARIABLES_METADATA_CSV_URL,
            XEMA_standards.VARIABLES_STANDARD_DTYPES_MAPPING,
            XEMA_standards.VARIABLES_STANDARD_COLTOAPI_MAPPING,
            base / "variables_raw_metadata.csv",
        ),
    ]

    for name, url, dtypes_map, col_map, path in resources:
        try:
            logger.info(f"Downloading {name} metadata from {url}")
            raw_df: pd.DataFrame = data_download.download_simple_csv_from_url_as_dataframe(url)
            if raw_df.empty:
                logger.warning(f"Downloaded {name} metadata is empty.")
        except Exception as e:
            logger.error(f"Failed to download {name} metadata: {e}")
            raise

        try:
            stdz_df = data_treatment.standardize_dataframe(raw_df, dtypes_map, col_map)
            data_treatment.save_dataframe_to_local_csv(stdz_df, path, overwrite=overwrite)
            logger.info(f"{name.capitalize()} metadata saved to {path}")
            saved_paths[name] = path
        except Exception as e:
            logger.error(f"Failed to save {name} metadata CSV: {e}")
            raise

    logger.info("Completed downloading and saving XEMA reference dataframes.")
    return saved_paths
