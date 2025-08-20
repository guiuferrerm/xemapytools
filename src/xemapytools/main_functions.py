from pathlib import Path
import logging
from typing import Union
import pandas as pd
import numpy as np
import math

import xemapytools._utils as _utils
import xemapytools.data_download as xptdd
import xemapytools.data_treatment as xptdt
import xemapytools.resources.XEMA_standards as XEMA_standards
import xemapytools.resources.url_list as url_list

logger = logging.getLogger(__name__)


def download_and_backup_XEMA_reference_dataframes(
    base_dir: Union[Path, str],
    overwrite: bool = True,
) -> dict[str, Path]:
    """
    Download XEMA reference CSVs (stations and variables) and save standardized copies
    with standardized column names only.

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
            XEMA_standards.STATIONS_STANDARD_COLTOAPI_MAPPING,
            base / "stations_raw_metadata.csv",
        ),
        (
            "variables_raw",
            url_list.VARIABLES_METADATA_CSV_URL,
            XEMA_standards.VARIABLES_STANDARD_COLTOAPI_MAPPING,
            base / "variables_raw_metadata.csv",
        ),
    ]

    for name, url, col_map, path in resources:
        try:
            logger.info(f"Downloading {name} metadata from {url}")
            raw_df: pd.DataFrame = xptdd.download_simple_csv_from_url_as_dataframe(url)
            if raw_df.empty:
                logger.warning(f"Downloaded {name} metadata is empty.")
        except Exception as e:
            logger.error(f"Failed to download {name} metadata: {e}")
            raise

        try:
            stdz_df = xptdt.standardize_dataframe(raw_df, standard_coltoapi_map=col_map)
            xptdt.save_dataframe_to_local_csv(stdz_df, path, overwrite=overwrite)
            logger.info(f"{name.capitalize()} metadata saved to {path}")
            saved_paths[name] = path
        except Exception as e:
            logger.error(f"Failed to save {name} metadata CSV: {e}")
            raise

    logger.info("Completed downloading and saving XEMA reference dataframes.")
    return saved_paths

def get_stations_by_radius(
    lat: float,
    lon: float,
    radius_km: float,
    data_source: Union[pd.DataFrame, Path, str],
) -> pd.DataFrame:
    """
    Filters XEMA station data by a specific radius and returns a DataFrame
    with the stations found.

    Args:
        lat (float): Latitude of the central search point.
        lon (float): Longitude of the central search point.
        radius_km (float): Search radius in kilometers.
        data_source (Union[pd.DataFrame, Path, str]): The source of the station
                                                      data. Can be a pandas DataFrame
                                                      or a file path (str or Path).

    Returns:
        pd.DataFrame: A DataFrame with the filtered stations, including
                      the distance from the central point. If no stations are found,
                      an empty DataFrame is returned.
    """
    try:
        # Check if the data source is a DataFrame or a file path
        if isinstance(data_source, pd.DataFrame):
            df_stations = data_source
            logger.info("Using DataFrame provided as data source.")
        elif isinstance(data_source, (Path, str)):
            # 1. Load the standardized DataFrame from the local file
            logger.info(f"Loading XEMA station data from {data_source}...")
            df_stations = xptdt.load_local_csv_as_dataframe(data_source)
        else:
            raise TypeError("data_source must be a pandas DataFrame or a file path.")

        # 2. Add distance and filter the stations
        if df_stations.empty:
            logger.warning("No station data found. Returning empty DataFrame.")
            return df_stations
            
        df_stations['dist_km'] = df_stations.apply(
            lambda row: _utils.haversine_km(lat, lon, row['latitud'], row['longitud']),
            axis=1
        )
        df_filtered = df_stations[df_stations['dist_km'] <= radius_km].copy()
        
        # 3. Sort the stations by distance
        df_filtered.sort_values('dist_km', inplace=True)
        
        logger.info(f"Found {len(df_filtered)} stations within the {radius_km} km radius.")
        return df_filtered
        
    except Exception as e:
        logger.error(f"An error occurred while getting the stations: {e}")
        return pd.DataFrame()

def get_geographic_circle(center_lat, center_lon, radius_km, n_points=100):
    """
    Returns the latitudes and longitudes that form a geographic circle of radius_km.
    """
    angles = np.linspace(0, 2*np.pi, n_points)
    lats, lons = [], []
    d = radius_km / _utils.R_EARTH_KM
    lat_rad = math.radians(center_lat)
    lon_rad = math.radians(center_lon)

    for angle in angles:
        lat_p = math.asin(
            math.sin(lat_rad)*math.cos(d) + math.cos(lat_rad)*math.sin(d)*math.cos(angle)
        )
        lon_p = lon_rad + math.atan2(
            math.sin(angle)*math.sin(d)*math.cos(lat_rad),
            math.cos(d) - math.sin(lat_rad)*math.sin(lat_p)
        )
        lats.append(math.degrees(lat_p))
        lons.append(math.degrees(lon_p))
    return lats, lons
