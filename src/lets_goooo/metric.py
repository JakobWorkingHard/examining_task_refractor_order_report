import pandas as pd
import logging

logger = logging.getLogger(__name__)

def create_overview(total_sales, order_count, return_count):
    """Skapar en översikts-DataFrame."""

    return pd.DataFrame({
        "metric": ["total_sales", "order_count", "return_count"],
        "value": [total_sales, order_count, return_count],
    })



def calculate_sales_metrics(data, groupby_column: str):
    result = (data.groupby(
        groupby_column,
        as_index=False,
        )
        .agg(
            order_count=("order_id", "nunique"),
            total_sales=("discounted_value", "sum"),
            returns=("returned", "sum"),
        )
    )


    result["total_sales"] = (
    result["total_sales"].round(2)
    )

    result["return_rate"] = (
        result["returns"]
        / result["order_count"]
    ).round(3)

    result = (
        result
        .sort_values(
            "total_sales",
            ascending=False,
        )
        .reset_index(drop=True)
    )
    return result


def calculate_return_rate(data, grouped_by: str):
        returns_by_category = (
        data.groupby(
            grouped_by,
            as_index=False,
        )
        .agg(
            order_count=("order_id", "nunique"),
            returns=("returned", "sum"),
        )
         )

        returns_by_category["return_rate"] = (
            returns_by_category["returns"]
            / returns_by_category["order_count"]
        ).round(3)

        returns_by_category = (
            returns_by_category
            .sort_values(
                "return_rate",
                ascending=False,
            )
            .reset_index(drop=True)
        )

        return returns_by_category