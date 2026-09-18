import pandas as pd
import logging
from pathlib import Path

from src.lets_goooo.io import open_my_file_yao
from src.lets_goooo.validate import are_the_columns_really_there
from src.lets_goooo.config import load_config
from src.lets_goooo.report import reports_orchestration


logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("loggningsloggen.log"),  #  Sparar i filen
        logging.StreamHandler()          #  Skriver i terminalen
    ]
)


CONFIG_PATH = Path(__file__).resolve().parent / "config.toml"

def main():
    cfg = load_config(CONFIG_PATH)     
    reports_orchestration(cfg)          

if __name__ == "__main__":
    main()