import pandas as pd
import logging
from src.lets_goooo.io import open_my_file_yao
from src.lets_goooo.validate import are_the_columns_really_there

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("loggningsloggen.log"),  # Brevbärare 1: Sparar i filen
        logging.StreamHandler()          # Brevbärare 2: Skriver i terminalen
    ]
)


def main():
    logging.info("Startar projekt")
    data = open_my_file_yao()

    are_the_columns_really_there(data)





if __name__ == "__main__":
    main()