from src.lets_goooo.config import ReportConfig
from src.lets_goooo import io, validate, processing, metric

def reports_orchestration(cfg: ReportConfig):
    try:
        data = io.open_my_file_yao(cfg.input_file) 
        validate.are_the_columns_really_there(data, cfg.required_columns)

        numerical_columns_list = ["quantity", "unit_price", "discount"]


        data = validate.how_many_NaNs_or_weird_stuff_in_the_data_are_we_dealing_with_man(
            data = data,
            numerical_columns = numerical_columns_list,
            date_time_column = "order_date",
            nan_warn_pct = cfg.nan_warn_pct,
            nan_error_pct = cfg.nan_error_pct,
            excluded_columns= {"returned"}
            )

        if cfg.unit_price_fillna == "unit_price.median":
            unit_price_fillna = data["unit_price"].median()


        fillnadic_numerical = {"quantity": cfg.quantity_fillna, "unit_price": unit_price_fillna, "discount": cfg.discount_fillna}
        fillnadic_text = {"region": cfg.text_fillna, "product_category": cfg.text_fillna}

        for key, value in fillnadic_numerical.items():
            data[key] = processing.fillna_numerical(data[key], value)

        for key, value in fillnadic_text.items():
            data[key] = processing.fillna_text(data[key], value)



        list_of_true_returned_dudes = ["true", "yes", "1", "ja"]

        data["returned"] = processing.fix_them_returned(data["returned"], "false", list_of_true_returned_dudes)



        data = processing.cr_order_value(data, "quantity", "unit_price")
        data = processing.cr_discounted_value(data, "order_value", "discount")
        total_sales = processing.cr_total_sales(data, "discounted_value")

        number_of_orders = processing.number_of_orders_function(data, "order_id")
        number_of_returns = processing.number_of_returns_function(data, "returned")


        overview = metric.create_overview(total_sales, number_of_orders, number_of_returns)
        io.save_my_file_please(overview, "overview.csv", cfg.output_folder)

        result1 = metric.calculate_sales_metrics(data, "product_category")
        io.save_my_file_please(result1, "sales_by_category.csv", cfg.output_folder)

        result2 = metric.calculate_sales_metrics(data, "region")
        io.save_my_file_please(result2, "sales_by_region.csv", cfg.output_folder)

        returns_by_category = metric.calculate_return_rate(data, "product_category")
        io.save_my_file_please(returns_by_category, "returns_by_category.csv", cfg.output_folder)

        print("Sparade returns_by_category.csv")
        print("Klart")

    except Exception as error:
        print("Något gick fel:", error)
