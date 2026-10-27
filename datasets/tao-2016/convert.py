"""Convert raw/*.json to processed/ for this dataset. See SCHEMA.md and the dataset README."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from tools.json_format import convert  # noqa: E402


def nominal_by_ply(ply, terms):
    """87 plywood/OSB files omit nominal_data, but every file uses the same nominal
    elastic moduli, so elastic_modulus is flagged nominal for all specimens."""
    return ["elastic_modulus"]


if __name__ == "__main__":
    convert(HERE, length="mm", force="N", stress="MPa", nominal_by_ply=nominal_by_ply)
