import pandas as pd
import logging
from typing import Mapping, Union, Tuple, Literal, Dict
from pathlib import Path

logger = logging.getLogger(__name__)

DateSpec = Union[Literal["datetime"], Tuple[Literal["datetime"], str]]
TypeSpec = Union[type, DateSpec]
StandardMap = Mapping[str, TypeSpec]

def standardize_dataframe(df: pd.DataFrame, standard_dtype_map: StandardMap, standard_coltoapi_map: Dict[str, str]) -> pd.DataFrame:
    df = df.copy()

    # Rename first so dtype coercion works on internal names
    if standard_coltoapi_map:
        rename_dict = {col: standard_coltoapi_map[col] for col in df.columns if col in standard_coltoapi_map}
        if rename_dict:
            df = df.rename(columns=rename_dict)

    # Now coerce dtypes
    for col, spec in standard_dtype_map.items():
        if col not in df.columns:
            continue

        if spec == "datetime_utc" or (isinstance(spec, tuple) and spec[0] == "datetime_utc"):
            fmt = spec[1] if isinstance(spec, tuple) else None
            if fmt:
                df[col] = pd.to_datetime(df[col], format=fmt, errors="coerce", utc=True)
            else:
                df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)
        else:
            try:
                if spec in (int, float):
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                    if spec is int:
                        df[col] = df[col].astype("Int64")
                else:
                    df[col] = df[col].astype(spec)
            except Exception:
                logger.warning(f"Failed to cast column '{col}' to {spec}; leaving as-is.")

    return df

def save_dataframe_to_local_csv(
    df: pd.DataFrame,
    filepath: Union[Path, str],
    index: bool = False,
    overwrite: bool = True,
) -> None:
    """
    Save DataFrame to CSV, automatically creating parent directories.
    Overwrites by default unless overwrite=False.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} already exists and overwrite=False.")
    df.to_csv(path, index=index)
    logger.info(f"Saved DataFrame to {path}")


def load_local_csv_as_dataframe(filepath: Union[Path, str], **read_csv_kwargs) -> pd.DataFrame:
    """
    Load a local CSV file into a pandas DataFrame.
    Extra keyword arguments are passed to pandas.read_csv().
    """
    path = Path(filepath)
    if not path.exists():
        logger.error(f"CSV file not found: {path}")
        raise FileNotFoundError(f"CSV file not found: {path}")
    logger.info(f"Loading CSV from {path}")
    return pd.read_csv(path, **read_csv_kwargs)
