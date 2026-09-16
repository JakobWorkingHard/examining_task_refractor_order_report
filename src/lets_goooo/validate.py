import pandas as pd
import logging
from src.lets_goooo.config import (
    REQUIRED_COLUMNS, 
    NAN_WARN_PCT, 
    NAN_ERROR_PCT
)


logger = logging.getLogger(__name__)



def are_the_columns_really_there(data, input_required_columns: set = REQUIRED_COLUMNS):
    logger.info("Läser in obligatoriska kolumner")


    if not input_required_columns.issubset(data.columns):
        missing_columns = input_required_columns - set(data.columns)
        raise ValueError(missing_columns, " <- Dessa obligatoriska kolumnner saknas")

    logger.info("Alla obligatoriska kolumner finns med i datan")
    print("Läste in", len(data), "rader")


def pd_to_numeric_function(data, column_name: str):
    logger.info(f"Gör om {column_name} till numerical")
    data[column_name] = pd.to_numeric(data[column_name], errors="coerce")
    return data


def to_datetime(data, column_name: str):
    logger.info(f"Gör om {column_name} till datetime")
    data[column_name] = pd.to_datetime(data[column_name], errors="coerce")
    return data


def how_many_NaNs_or_weird_stuff_in_the_data_are_we_dealing_with_man(
        data, 
        numerical_columns: list, 
        date_time_column: str,
        excluded_columns: set = {"returned"}, 
        nan_warn_pct = NAN_WARN_PCT, 
        nan_error_pct = NAN_ERROR_PCT):

    logger.info("Konverterar konstiga värden till NaN")
    df = data.copy()

    for numerical_column in numerical_columns:
        df = pd_to_numeric_function(df, numerical_column)

    df = to_datetime(df, date_time_column)

    nan_percentages = df.isna().mean()
    columns_with_warnings = []
    columns_with_errors = []

    for col_name, pct in nan_percentages.items():
        if pct >= nan_error_pct and col_name not in excluded_columns:
            columns_with_errors.append(f"{col_name} ({pct:.1%})")
        elif pct >= nan_warn_pct and col_name not in excluded_columns:
            columns_with_warnings.append(f"{col_name} ({pct:.1%})")

    if columns_with_warnings:
        logger.warning(f"VARNING: Hög andel skräp/saknad data i: {columns_with_warnings}")

    if columns_with_errors:
        logger.error(f"FEL: Kritisk andel skräp/saknad data: {columns_with_errors}")
        raise ValueError(f"Datan underkänd. För mycket ogiltig data i: {columns_with_errors}")

    logger.info("Validering godkänd! Skickar vidare konverterad data.")
    
    return df

