import pandas as pd
import logging


logger = logging.getLogger(__name__)


def fillna_numerical(data_with_column, fill_with):
    return data_with_column.fillna(fill_with)



def fillna_text(data_with_column, fill_with):
    return data_with_column.fillna(fill_with).astype(str).str.strip().str.title()


def fix_them_returned(data_with_column, fill_na_with, fill_is_in_true: list):
    return (data_with_column.fillna(fill_na_with).astype(str).str.strip().str.lower().isin(fill_is_in_true))



def cr_order_value(data, 
                   quantity_column: str = "quantity", 
                   unit_price_column: str = "unit_price"
                   ):
    """Tar in quantity och unit price och returnerar en df med
    kalkylerad "order_value"""""

    logger.info("Beräknar order_value")
    data["order_value"] = data[quantity_column] * data[unit_price_column]
    return data



def cr_discounted_value(data, 
                   order_value_column: str = "order_value", 
                   discount_column: str = "discount"
                   ):
    """Tar in order value och discount och returnerar en df med
    kalkylerad "discounted_value"""

    logger.info("Beräknar discounted value")
    data["discounted_value"] = data[order_value_column] * (1 - data[discount_column])
    return data



def cr_total_sales(data,
                   discounted_value_column: str = "discounted_value"):
    """Summerar hela discounted_value kolumnen i total_sales"""

    logger.info("Beräknar total sales")
    total_sales = round(data[discounted_value_column].sum(),2,)
    return total_sales



def number_of_orders(data, order_id_column: str = "order_id"):
    """Returnerar antal ordrar"""

    logger.info("Beräknar antal ordrar")
    number_of_orders = data[order_id_column].nunique()
    return number_of_orders



def number_of_returns(data, returned_column: str = "returned"):
    """Returnerar antal returer"""

    logger.info("Beräknar antal returer")
    number_of_returns = int(data[returned_column].sum())
    return number_of_returns



    
