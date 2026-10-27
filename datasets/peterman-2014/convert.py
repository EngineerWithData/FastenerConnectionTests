"""Convert raw/*.json to processed/ for this dataset. See SCHEMA.md and the dataset README."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from tools.json_format import convert  # noqa: E402


def nominal_by_ply(ply, terms):
    """The raw files flag ply thicknesses as nominal ("steel ply thickness",
    "sheathing ply thickness"). Material properties stored as "unknown" are left blank."""
    is_steel = ply["type"].lower() == "steel"
    if ("steel ply thickness" if is_steel else "sheathing ply thickness") in terms:
        return ["thickness"]
    return []


if __name__ == "__main__":
    convert(HERE, length="in", force="lbf", stress="psi", nominal_by_ply=nominal_by_ply)
