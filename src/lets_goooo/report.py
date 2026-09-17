import os
import pandas as pd
import logging
from src.lets_goooo.io import open_my_file_yao, save_my_file_please
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
from src.lets_goooo.metric import (
    calculate_sales_metrics, 
    create_overview, 
    calculate_return_rate
)

logger = logging.getLogger(__name__)

def reports_orchestration(data):
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

        fillnadic_numerical = {"quantity": 1, "unit_price": data["unit_price"].median(), "discount": 0}
        fillnadic_text = {"region": "Unknown", "product_category": "Unknown"}

        for key, value in fillnadic_numerical.items():
            data[key] = fillna_numerical(data[key], value)

        for key, value in fillnadic_text.items():
            data[key] = fillna_text(data[key], value)



        list_of_true_returned_dudes = ["true", "yes", "1", "ja"]

        data["returned"] = fix_them_returned(data["returned"], "false", list_of_true_returned_dudes)



        data = cr_order_value(data, "quantity", "unit_price")
        data = cr_discounted_value(data, "order_value", "discount")
        total_sales = cr_total_sales(data, "discounted_value")

        number_of_orders = number_of_orders_function(data, "order_id")
        number_of_returns = number_of_returns_function(data, "returned")


        overview = create_overview(total_sales, number_of_orders, number_of_returns)
        save_my_file_please(overview, "overview.csv")

        result1 = calculate_sales_metrics(data, "product_category")
        save_my_file_please(result1, "sales_by_category.csv")

        result2 = calculate_sales_metrics(data, "region")
        save_my_file_please(result2, "sales_by_region.csv")

        returns_by_category = calculate_return_rate(data, "product_category")
        save_my_file_please(returns_by_category, "returns_by_category.csv")

        print("Sparade returns_by_category.csv")
        print("Klart")

    except Exception as error:
        print("Något gick fel:", error)