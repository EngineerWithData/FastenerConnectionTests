"""Merge every dataset's processed tables into combined/ (one file per table).

    python tools/build_combined.py

combined/ is a build output: it is git-ignored and attached to GitHub releases.
curves.parquet stacks every load-deformation curve, with dataset_id, specimen_id,
and the point index added. Run tools/validate.py first.
"""
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = yaml.safe_load((ROOT / "schema" / "schema.yaml").read_text())
OUT = ROOT / "combined"


def read_curves(path):
    sp = pd.read_csv(path / "processed" / "specimens.csv", dtype={"specimen_id": str})
    folder = path / "processed" / Path(SCHEMA["tables"]["curves"]["file"]).parent
    for sid in sp["specimen_id"]:
        df = pd.read_csv(folder / f"{sid}.csv")
        df.insert(0, "point", range(len(df)))
        df.insert(0, "specimen_id", sid)
        df.insert(0, "dataset_id", path.name)
        yield df


def main():
    OUT.mkdir(exist_ok=True)
    datasets = sorted(p for p in (ROOT / "datasets").iterdir() if (p / "processed").is_dir())
    for name, spec in SCHEMA["tables"].items():
        if spec.get("per_specimen"):
            parts = [df for p in datasets for df in read_curves(p)]
            cols = ["dataset_id", "specimen_id", "point", *spec["columns"]]
        else:
            parts = [pd.read_csv(p / "processed" / spec["file"], dtype={"specimen_id": str}, low_memory=False)
                     for p in datasets if (p / "processed" / spec["file"]).exists()]
            cols = list(spec["columns"])
        if not parts:
            continue
        df = pd.concat(parts, ignore_index=True)[cols]
        df.to_parquet(OUT / f"{name}.parquet", index=False)
        print(f"{name}: {len(df)} rows")


if __name__ == "__main__":
    main()
