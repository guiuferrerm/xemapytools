from pathlib import Path
import logging
import xemapytools.data_download as data_download
import xemapytools.resources.url_list as url_list
import xemapytools.data_treatment as data_treatment
from typing import Union
import pandas as pd

logger = logging.getLogger(__name__)

def download_and_backup_XEMA_reference_dataframes(
    base_dir: Union[Path, str],
    overwrite: bool = True,
) -> dict[str, Path]:
    """
    Download the XEMA reference CSVs (stations and variables) and save raw copies
    into `base_dir`. Returns a mapping of descriptive names to saved file paths.

    :param base_dir: Directory where the raw CSVs will be stored.
    :param overwrite: If False, existing files will not be overwritten.
    :return: Dict like {"stations_raw": Path(...), "variables_raw": Path(...)}
    :raises: Exception on download or save failure.
    """
    base = Path(base_dir)
    base.mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensured base directory exists: {base.resolve()}")

    saved_paths: dict[str, Path] = {}

    # Download and save stations metadata
    try:
        logger.info(f"Downloading stations metadata from {url_list.STATIONS_METADATA_CSV_URL}")
        stations_raw: pd.DataFrame = data_download.download_csv_from_url_as_dataframe(
            url_list.STATIONS_METADATA_CSV_URL
        )
    except Exception as e:
        logger.error(f"Failed to download stations metadata: {e}")
        raise

    if stations_raw.empty:
        logger.warning("Downloaded stations metadata is empty.")

    stations_path = base / "stations_raw_metadata.csv"
    try:
        data_treatment.save_dataframe_to_local_csv(stations_raw, stations_path, overwrite=overwrite)
        logger.info(f"Stations metadata saved to {stations_path}")
        saved_paths["stations_raw"] = stations_path
    except Exception as e:
        logger.error(f"Failed to save stations metadata CSV: {e}")
        raise

    # Download and save variables metadata
    try:
        logger.info(f"Downloading variables metadata from {url_list.VARIABLES_METADATA_CSV_URL}")
        variables_raw: pd.DataFrame = data_download.download_csv_from_url_as_dataframe(
            url_list.VARIABLES_METADATA_CSV_URL
        )
    except Exception as e:
        logger.error(f"Failed to download variables metadata: {e}")
        raise

    if variables_raw.empty:
        logger.warning("Downloaded variables metadata is empty.")

    variables_path = base / "variables_raw_metadata.csv"
    try:
        data_treatment.save_dataframe_to_local_csv(variables_raw, variables_path, overwrite=overwrite)
        logger.info(f"Variables metadata saved to {variables_path}")
        saved_paths["variables_raw"] = variables_path
    except Exception as e:
        logger.error(f"Failed to save variables metadata CSV: {e}")
        raise

    logger.info("Completed downloading and saving XEMA reference dataframes.")
    return saved_paths
