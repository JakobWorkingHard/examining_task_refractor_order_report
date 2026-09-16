import os
import pandas as pd
from src.lets_goooo.io import open_my_file_yao
from src.lets_goooo.validate import (
are_the_columns_really_there, 
how_many_NaNs_or_weird_stuff_in_the_data_are_we_dealing_with_man
)
from src.lets_goooo.processing import(
    cr_order_value,
    cr_discounted_value,
    cr_total_sales,
    number_of_orders_function,
    number_of_returns_function,
    fillna_numerical,
    fillna_text,
    fix_them_returned
)
from src.lets_goooo.metric import calculate_sales_metrics, create_overview

# INPUT_FILE = "data/orders.csv"
OUTPUT_FOLDER = "output"

print("Startar orderrapport")

try:
    data = open_my_file_yao()

    are_the_columns_really_there(data)


    numerical_columns_list = ["quantity", "unit_price", "discount"]


    data = how_many_NaNs_or_weird_stuff_in_the_data_are_we_dealing_with_man(
        data = data,
        numerical_columns = numerical_columns_list,
        date_time_column = "order_date",
        excluded_columns= {"returned"}
        )

    the_numerical_dic_man = {"quantity": 1, "unit_price": data["unit_price"].median(), "discount": 0}
    the_text_dic_dude = {"region": "Unknown", "product_category": "Unknown"}

    for key, value in the_numerical_dic_man.items():
        data[key] = fillna_numerical(data[key], value)

    for key, value in the_text_dic_dude.items():
        data[key] = fillna_text(data[key], value)



    list_of_true_returned_dudes = ["true", "yes", "1", "ja"]

    data["returned"] = fix_them_returned(data["returned"], "false", list_of_true_returned_dudes)



    data = cr_order_value(data, "quantity", "unit_price")
    data = cr_discounted_value(data, "order_value", "discount")
    total_sales = cr_total_sales(data, "discounted_value")

    number_of_orders = number_of_orders_function(data, "order_id")
    number_of_returns = number_of_returns_function(data, "returned")

    # data["order_value"] = (
    #     data["quantity"] * data["unit_price"]
    # )

    # data["discounted_value"] = (
    #     data["order_value"] * (1 - data["discount"])
    # )

    # total_sales = round(
    #     data["discounted_value"].sum(),
    #     2,
    # )

    # number_of_orders = data["order_id"].nunique()
    # number_of_returns = int(data["returned"].sum())

    # overview = pd.DataFrame(
    #     {
    #         "metric": [
    #             "total_sales",
    #             "order_count",
    #             "return_count",
    #         ],
    #         "value": [
    #             total_sales,
    #             number_of_orders,
    #             number_of_returns,
    #         ],
    #     }
    # )

    overview = create_overview(total_sales, number_of_orders, number_of_returns)

    overview.to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "overview.csv",
        ),
        index=False,
    )

    print("Sparade overview.csv")

    result1 = calculate_sales_metrics(data, "product_category")

    # result1 = (
    #     data.groupby(
    #         "product_category",
    #         as_index=False,
    #     )
    #     .agg(
    #         order_count=("order_id", "nunique"),
    #         total_sales=("discounted_value", "sum"),
    #         returns=("returned", "sum"),
    #     )
    # )

    # result1["total_sales"] = (
    #     result1["total_sales"].round(2)
    # )

    # result1["return_rate"] = (
    #     result1["returns"]
    #     / result1["order_count"]
    # ).round(3)

    # result1 = (
    #     result1
    #     .sort_values(
    #         "total_sales",
    #         ascending=False,
    #     )
    #     .reset_index(drop=True)
    # )

    result1.to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "sales_by_category.csv",
        ),
        index=False,
    )

    print("Sparade sales_by_category.csv")

    result2 = (
        data.groupby(
            "region",
            as_index=False,
        )
        .agg(
            order_count=("order_id", "nunique"),
            total_sales=("discounted_value", "sum"),
            returns=("returned", "sum"),
        )
    )

    result2["total_sales"] = (
        result2["total_sales"].round(2)
    )

    result2["return_rate"] = (
        result2["returns"]
        / result2["order_count"]
    ).round(3)

    result2 = (
        result2
        .sort_values(
            "total_sales",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    result2.to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "sales_by_region.csv",
        ),
        index=False,
    )

    print("Sparade sales_by_region.csv")

    returns_by_category = (
        data.groupby(
            "product_category",
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

    returns_by_category.to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "returns_by_category.csv",
        ),
        index=False,
    )

    print("Sparade returns_by_category.csv")
    print("Klart")

except Exception as error:
    print("Något gick fel:", error)



