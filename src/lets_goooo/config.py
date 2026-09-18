from dataclasses import dataclass
from pathlib import Path
import tomllib

@dataclass(frozen=True)
class ReportConfig:
    input_file: Path
    output_folder: Path
    nan_warn_pct: float
    nan_error_pct: float
    required_columns: set[str]
    unit_price_fillna: str        
    quantity_fillna: float
    text_fillna: str
    discount_fillna: float

def load_config(path: Path) -> ReportConfig:
    with open(path, "rb") as f:
        raw = tomllib.load(f)         
    o = raw["order_report"]
    fill = raw["fillna"]
    return ReportConfig(
        input_file=Path(o["input_file"]),
        output_folder=Path(o["output_folder"]),
        nan_warn_pct=o["nan_warn_pct"],
        nan_error_pct=o["nan_error_pct"],
        required_columns=set(o["required_columns"]),
        unit_price_fillna=fill["unit_price_fillna"],
        quantity_fillna=fill["quantity_fillna"],
        text_fillna=fill["text_fillna"],
        discount_fillna=fill["discount_fillna"],
    )