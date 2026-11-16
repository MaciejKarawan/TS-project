from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
TABLES = ROOT / "results" / "tables"
GENERATED = ROOT / "results" / "generated"
def output(name):
    GENERATED.mkdir(parents=True, exist_ok=True)
    return GENERATED / name
