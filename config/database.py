from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def get_database_uri() -> str:
    DATA_DIR.mkdir(exist_ok=True)
    return f"sqlite:///{DATA_DIR / 'feasibility_reports.db'}"
