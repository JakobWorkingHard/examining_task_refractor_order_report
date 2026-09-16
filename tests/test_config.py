import pytest
from pathlib import Path
from src.lets_goooo.config import load_config_data

def test_file_is_totally_gone_man():
    """ERROR-handling: Testar om vi får felmeddelande när filen är åt pipsvängen"""
    fake_path = Path("någonstans_bortom_oändligheten/config.toml")

    with pytest.raises(FileNotFoundError):
        load_config_data(fake_path)


def test_invalid_toml(tmp_path: Path):
    """ERROR-handling: Testar om vi får valueerror om vi har en trasig toml"""
    broken_toml = tmp_path / "trasig_toml.toml"
    broken_toml.write_text("weird = [", encoding="utf-8"")")

    with pytest.raises(ValueError):
        load_config_data(broken_toml)


def test_key_error_in_toml(tmp_path: Path):
    """ERROR-handling: Testar om [order_report]-rubriken saknas från från config.toml fil"""
    wrong_section = tmp_path / "wrong_section.toml"
    wrong_section.write_text("[fel_rubrik]\ninput_file = 'test.csv'", encoding="utf-8")
    
    with pytest.raises(KeyError):
        load_config_data(wrong_section)

def test_when_it_all_works(tmp_path: Path):
    """Happy-test: Testar så allt fungerar ifall vår temporära tmp fil ser ut som den ska"""
    viva_la_perfectionaz = tmp_path / "perfect.toml"
    viva_la_perfectionaz.write_text("""
    [order_report]
    input_file = "data/orders.csv"
    output_folder = "output"
    nan_warn_pct = 0.05
    nan_error_pct = 0.20
    required_columns = ["order_id", "region"]
    """, 
    encoding="utf-8"
    )

    result = load_config_data(viva_la_perfectionaz)

    assert result["input_file"] == "data/orders.csv"
    assert result["nan_error_pct"] == 0.20
    assert result["nan_warn_pct"] == 0.05
    assert result["required_columns"] == ["order_id", "region"]
    assert result["output_folder"] == "output"


def test_edge_case(tmp_path: Path):
    """Edge-case: Testar när allt NÄSTAN ser helt perfekt ut men finns nåt litet fel i config.toml"""
    almost_perfection = tmp_path / "almost_perfect.toml"
    almost_perfection.write_text("""
    [order_report]
    input_file = "data/orders.csv"
    output_folder = "output"
    nan_warn_pct = 0.00
    nan_error_pct = 0.20
    required_columns = []
    weird_variabel = "Weird"
    """, 
    encoding="utf-8"
    )

    result = load_config_data(almost_perfection)

    assert result["required_columns"] == []
    assert result["nan_warn_pct"] == 0.0