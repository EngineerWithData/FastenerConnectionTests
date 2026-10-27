"""Convert raw/ to processed/ for this dataset. See SCHEMA.md and datasets/tao-2016/convert.py.

If raw/ holds files in this repository's JSON format, replace this file with a call to
tools/json_format.py, as datasets/tao-2016/convert.py does.
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
OUT = HERE / "processed"
DATASET_ID = HERE.name


def main():
    (OUT / "curves").mkdir(parents=True, exist_ok=True)
    specimens = pd.DataFrame(columns=[
        "dataset_id", "specimen_id", "loading", "fastener_type", "fastener_count",
        "fastener_size", "fastener_diameter_mm", "fastener_length_mm", "head_diameter_mm",
        "head_shape", "coating", "fastener_product", "ply_count", "point_count",
        "source_file", "notes"])
    plies = pd.DataFrame(columns=[
        "dataset_id", "specimen_id", "ply", "material", "thickness_mm",
        "elastic_modulus_mpa", "yield_stress_mpa", "ultimate_stress_mpa", "nominal"])
    # ... read RAW files, fill the tables, convert to mm / N / MPa ...
    # For each test, write its curve:
    #   pd.DataFrame({"displacement_mm": d, "force_n": f}).to_csv(
    #       OUT / "curves" / f"{specimen_id}.csv", index=False, float_format="%.6g")
    specimens.to_csv(OUT / "specimens.csv", index=False)
    plies.to_csv(OUT / "plies.csv", index=False)


if __name__ == "__main__":
    main()
