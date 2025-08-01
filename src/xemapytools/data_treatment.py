import pandas as pd
import logging
from typing import Mapping, Union, Tuple, Literal
from pathlib import Path

logger = logging.getLogger(__name__)

DateSpec = Union[Literal["datetime"], Tuple[Literal["datetime"], str]]
TypeSpec = Union[type, DateSpec]
StandardMap = Mapping[str, TypeSpec]


def standardize_dataframe(df: pd.DataFrame, standard_map: StandardMap) -> pd.DataFrame:
    """
    Returns a new DataFrame with columns coerced according to standard_map.
    standard_map values can be:
      - "datetime" or ("datetime", fmt) for parsing datetimes
      - int, float, str, etc. for type coercion (numeric coercion is safe)
    """
    df = df.copy()
    for col, spec in standard_map.items():
        if col not in df.columns:
            continue

        if spec == "datetime_utc" or (isinstance(spec, tuple) and spec[0] == "datetime_utc"):
            fmt = spec[1] if isinstance(spec, tuple) else None
            before_na = df[col].isna().sum()
            if fmt:
                df[col] = pd.to_datetime(df[col], format=fmt, errors="coerce", utc=True)
            else:
                df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)
            after_na = df[col].isna().sum()
            coerced = after_na - before_na
            if coerced > 0:
                logger.warning(
                    f"Column '{col}': {coerced} values coerced to NaT during datetime parsing."
                )
        else:
            # numeric safe coercion
            if spec in (int, float):
                before_na = df[col].isna().sum()
                df[col] = pd.to_numeric(df[col], errors="coerce")
                after_na = df[col].isna().sum()
                coerced = after_na - before_na
                if coerced > 0:
                    logger.warning(
                        f"Column '{col}': {coerced} values coerced to NaN during numeric parsing."
                    )
                if spec is int:
                    # use pandas nullable integer dtype to handle NaNs properly
                    df[col] = df[col].astype("Int64")
            else:
                try:
                    df[col] = df[col].astype(spec)
                except Exception:
                    logger.warning(
                        f"Failed to cast column '{col}' to {spec}; leaving as-is."
                    )
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
