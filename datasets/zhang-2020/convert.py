"""Convert raw/*.json to processed/ for this dataset. See SCHEMA.md and the dataset README."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from tools.json_format import convert  # noqa: E402

if __name__ == "__main__":
    convert(HERE, length="mm", force="N", stress="MPa")
