import pandas as pd
import logging
from src.lets_goooo.config import INPUT_FILE, OUTPUT_FOLDER


logger = logging.getLogger(__name__)


def open_my_file_yao(filepath=INPUT_FILE):
    logger.info("Öppnar den vackraste filen i hela Minnesota från: ", INPUT_FILE)

    try:
        logger.info("Puuh, filen lyckades läsas in, det var tur det!")
        return pd.read_csv(filepath)

    except FileNotFoundError:
        logger.error("Nu är det nåt som är galet, har du verkligen satt in rätt sökväg till filen? Ändra i config.toml, för ", INPUT_FILE, "finns inte.")
        raise

    except PermissionError:
        logger.error("Du din lilla skit, du har inte tillåtelse att öppna såhär viktiga dokument!")
        raise

    except Exception as e:
        logger.error("Någonting oväntat har skett här, dags att ta på sig detektivglasögonen och börja leta fel!")
        raise
