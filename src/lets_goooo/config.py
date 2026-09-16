from pathlib import Path
import tomllib


def load_config_data(path_to_file):
    try:
        with open(path_to_file, "rb") as f:
            _cfg = tomllib.load(f)["order_report"]
            return _cfg
    except FileNotFoundError:
        raise FileNotFoundError("ERROR: Hittade ej din config.toml via sökvägen ", path_to_file)

    except tomllib.TOMLDecodeError as e:
        raise ValueError("ERROR: Går ej att läsa din config.toml fil")

    except KeyError:
        raise KeyError("ERROR: Någonting är fel med sektionen [order_report] i din config.toml")


huvudmapp = Path(__file__).resolve().parent.parent.parent
config_sökväg = huvudmapp / "config.toml"

_cfg = load_config_data(config_sökväg)

INPUT_FILE = Path(_cfg["input_file"])
OUTPUT_FOLDER = Path(_cfg["output_folder"])


NAN_WARN_PCT = _cfg["nan_warn_pct"]
NAN_ERROR_PCT = _cfg["nan_error_pct"]


REQUIRED_COLUMNS = set(_cfg["required_columns"])

