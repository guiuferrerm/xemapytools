import urllib.request
import urllib.parse
import pandas as pd
import io
import gzip
import zlib
import logging
from typing import Optional, Dict, Tuple, Union, List
from datetime import datetime

logger = logging.getLogger(__name__)


def download_simple_csv_from_url_as_dataframe(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    encoding: str = "utf-8",
) -> pd.DataFrame:
    """
    Download a CSV from the given URL using urllib and return a pandas DataFrame.
    Handles gzip/deflate response encoding if present.
    """
    req = urllib.request.Request(url)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    else:
        req.add_header("User-Agent", "python-urllib/3.x")

    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            content_encoding = resp.getheader("Content-Encoding", "").lower()
    except Exception as e:
        logger.error(f"Error downloading CSV from {url}: {e}")
        raise

    try:
        if "gzip" in content_encoding:
            raw = gzip.decompress(raw)
        elif "deflate" in content_encoding:
            try:
                raw = zlib.decompress(raw)
            except zlib.error:
                raw = zlib.decompress(raw, -zlib.MAX_WBITS)
    except Exception as e:
        logger.warning(f"Failed to decompress content from {url}: {e}")

    try:
        text = raw.decode(encoding, errors="replace")
        df = pd.read_csv(io.StringIO(text))
        logger.info(f"Downloaded and parsed CSV from {url} with {len(df)} rows.")
        return df
    except Exception as e:
        logger.error(f"Failed to decode or parse CSV from {url}: {e}")
        raise


# Constants for datetime columns and formats
_DATETIME_SOURCE_COLUMNS = {"data_lectura", "data_extrem"}
_DATETIME_INPUT_FORMAT = "%d/%m/%Y %I:%M:%S %p"
_DATETIME_SOQL_FORMAT = "%Y-%m-%dT%H:%M:%S"

Condition = Union[
    str,
    int,
    float,
    Tuple[str, Union[str, int, float]],
    List[Union[Tuple[str, Union[str, int, float]], str, int, float]],
]


def _format_soql_literal(v: Union[str, int, float]) -> str:
    if isinstance(v, str):
        escaped_v = v.replace("'", "''")
        return f"'{escaped_v}'"
    return str(v)


def build_soql_where_clause(
    filters: Optional[Dict[str, Condition]] = None,
    raw_filter: Optional[str] = None,
) -> str:
    """
    Build a SOQL WHERE clause from filter dictionary or raw string.
    """
    if raw_filter:
        logger.debug(f"Using raw SOQL filter: {raw_filter}")
        return raw_filter.strip()
    if not filters:
        return ""

    clauses = []

    def process_datetime_soql(col, c_val):
        try:
            if isinstance(c_val, tuple):
                op, v_str = c_val
                dt_obj = datetime.strptime(v_str, _DATETIME_INPUT_FORMAT)
                soql_dt_str = dt_obj.strftime(_DATETIME_SOQL_FORMAT)
                return f"{col} {op} '{soql_dt_str}'"
            else:
                dt_obj = datetime.strptime(str(c_val), _DATETIME_INPUT_FORMAT)
                soql_dt_str = dt_obj.strftime(_DATETIME_SOQL_FORMAT)
                return f"{col} = '{soql_dt_str}'"
        except ValueError as e:
            logger.warning(
                f"Could not parse date string '{c_val}' for filter '{col}': {e}. "
                "This filter will be applied locally only."
            )
            return None

    for col, cond in filters.items():
        if col in _DATETIME_SOURCE_COLUMNS:
            if isinstance(cond, list):
                sub_clauses = []
                for piece in cond:
                    soql_piece = process_datetime_soql(col, piece)
                    if soql_piece:
                        sub_clauses.append(soql_piece)
                if sub_clauses:
                    clauses.append(f"({' AND '.join(sub_clauses)})")
            else:
                soql_cond = process_datetime_soql(col, cond)
                if soql_cond:
                    clauses.append(soql_cond)
        else:

            def process_single_general(c):
                if isinstance(c, tuple):
                    op, v = c
                    right = _format_soql_literal(v)
                    return f"{col} {op} {right}"
                else:
                    right = _format_soql_literal(c)
                    return f"{col} = {right}"

            if isinstance(cond, list):
                sub_clauses = [process_single_general(piece) for piece in cond]
                clauses.append(f"({' AND '.join(sub_clauses)})")
            else:
                clauses.append(process_single_general(cond))

    where_clause = " AND ".join(clauses)
    logger.debug(f"Built SOQL where clause: {where_clause}")
    return where_clause


def fetch_socrata_csv_with_filters(
    base_url_soql: str,
    filters: Optional[Dict[str, Condition]] = None,
    raw_filter: Optional[str] = None,
    limit: int = 5000,
    max_rows: Optional[int] = 50000,
    app_token: Optional[str] = None,
    timeout: float = 30.0,
) -> pd.DataFrame:
    """
    Fetch CSV from Socrata using filters, returning a pandas DataFrame.
    Handles pagination with $limit and $offset.
    """
    headers = {
        "User-Agent": "python-urllib/3.x",
    }
    if app_token:
        headers["X-App-Token"] = app_token

    soql_where_clause_server = build_soql_where_clause(filters, raw_filter)

    logger.info(
        f"Starting data fetch from {base_url_soql} with filters: {filters}"
    )

    offset = 0
    chunks = []

    try:
        while True:
            params = {}
            if limit is not None:
                params["$limit"] = limit
            if offset > 0:
                params["$offset"] = offset
            if soql_where_clause_server:
                params["$where"] = soql_where_clause_server

            url_with_extension = (
                base_url_soql
                if base_url_soql.endswith(".csv")
                else f"{base_url_soql}.csv"
            )
            encoded = "&".join(
                f"{k}={urllib.parse.quote(str(v), safe='')}"
                for k, v in params.items()
            )
            url = f"{url_with_extension}?{encoded}"

            logger.debug(f"Fetching URL: {url}")

            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                csv_bytes = resp.read()
                csv_str = csv_bytes.decode("utf-8", errors="replace")

                if not csv_str.strip() or csv_str.strip().count("\n") == 0:
                    df_chunk = pd.DataFrame()
                else:
                    try:
                        df_chunk = pd.read_csv(io.StringIO(csv_str))
                    except pd.errors.EmptyDataError:
                        df_chunk = pd.DataFrame()
                    except Exception as e:
                        logger.error(
                            f"Error reading CSV chunk: {e}. Raw CSV snippet: "
                            f"{csv_str[:500]}..."
                        )
                        df_chunk = pd.DataFrame()

            if df_chunk.empty:
                logger.info("No more data to fetch; exiting loop.")
                break

            chunks.append(df_chunk)
            offset += limit

            if max_rows is not None and sum(len(c) for c in chunks) >= max_rows:
                logger.info(f"Reached max_rows limit of {max_rows}; stopping fetch.")
                break
            if len(df_chunk) < limit:
                logger.info("Received less rows than limit; assuming last page.")
                break

    except urllib.error.HTTPError as e:
        error_message = e.read().decode(errors="ignore")
        logger.error(f"HTTP Error {e.code}: {error_message}")
        logger.error(f"Problematic URL: {url}")
        return pd.DataFrame()
    except urllib.error.URLError as e:
        logger.error(f"URL Error: {e.reason}")
        logger.error(f"Problematic URL: {url}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Unexpected error during data fetch: {e}")
        logger.error(f"Problematic URL: {url}")
        return pd.DataFrame()

    if not chunks:
        logger.warning("No data fetched, returning empty DataFrame.")
        return pd.DataFrame()

    result_df = pd.concat(chunks, ignore_index=True)
    logger.info(f"Fetched total {len(result_df)} rows from {base_url_soql}")
    return result_df
