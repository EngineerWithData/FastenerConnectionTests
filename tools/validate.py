"""Check every dataset in datasets/ against schema/schema.yaml.

    python tools/validate.py              # all datasets
    python tools/validate.py tao-2016

Exits non-zero and lists every problem if anything fails.
"""
import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = yaml.safe_load((ROOT / "schema" / "schema.yaml").read_text())
REQUIRED_META = ["id", "title", "authors", "citation", "license", "contact", "original_units"]


def check_table(name, spec, df, errors):
    cols = spec["columns"]
    missing = [c for c in cols if c not in df.columns]
    extra = [c for c in df.columns if c not in cols]
    if missing:
        errors.append(f"{name}: missing columns {missing}")
    if extra:
        errors.append(f"{name}: unknown columns {extra} (add them to schema/schema.yaml first)")
    for col, rule in cols.items():
        if col not in df.columns:
            continue
        s = df[col]
        if rule.get("required") and s.isna().any():
            errors.append(f"{name}.{col}: {s.isna().sum()} empty values in a required column")
        s = s.dropna()
        if rule["type"] in ("number", "integer"):
            num = pd.to_numeric(s, errors="coerce")
            if num.isna().any():
                errors.append(f"{name}.{col}: non-numeric values {s[num.isna()].unique()[:5].tolist()}")
            if rule["type"] == "integer" and (num.dropna() % 1 != 0).any():
                errors.append(f"{name}.{col}: non-integer values")
            if "min" in rule and (num < rule["min"]).any():
                errors.append(f"{name}.{col}: values below {rule['min']}")
        if "vocabulary" in rule:
            allowed = SCHEMA["vocabularies"][rule["vocabulary"]]
            bad = sorted(set(s) - set(allowed))
            if bad:
                errors.append(f"{name}.{col}: {bad} not in vocabulary {rule['vocabulary']}={allowed}")


def check_curves(path, sp, errors):
    spec = SCHEMA["tables"]["curves"]
    folder = path / "processed" / Path(spec["file"]).parent
    expected = {str(s): n for s, n in zip(sp["specimen_id"], sp["point_count"])}
    found = {f.stem for f in folder.glob("*.csv")} if folder.exists() else set()
    if expected.keys() - found:
        errors.append(f"curves: no curve file for {sorted(expected.keys() - found)[:5]}")
    if found - expected.keys():
        errors.append(f"curves: files with no row in specimens.csv: {sorted(found - expected.keys())[:5]}")
    for sid in sorted(expected.keys() & found):
        sub = []
        df = pd.read_csv(folder / f"{sid}.csv")
        check_table(f"curves/{sid}", spec, df, sub)
        if len(df) != expected[sid]:
            sub.append(f"curves/{sid}: {len(df)} rows but point_count is {expected[sid]}")
        errors += sub[:3]


def check_dataset(path):
    errors = []
    meta_file = path / "dataset.yaml"
    if not meta_file.exists():
        return ["missing dataset.yaml"]
    meta = yaml.safe_load(meta_file.read_text())
    errors += [f"dataset.yaml: missing '{k}'" for k in REQUIRED_META if k not in meta]
    if meta.get("id") != path.name:
        errors.append(f"dataset.yaml: id '{meta.get('id')}' must match folder name '{path.name}'")
    if not (path / "README.md").exists():
        errors.append("missing README.md")

    tables = {}
    for name, spec in SCHEMA["tables"].items():
        if spec.get("per_specimen"):
            continue
        f = path / "processed" / spec["file"]
        if not f.exists():
            if not spec.get("optional"):
                errors.append(f"missing processed/{spec['file']}")
            continue
        df = pd.read_csv(f, dtype={"specimen_id": str}, low_memory=False)
        tables[name] = df
        check_table(name, spec, df, errors)
        if "dataset_id" in df and set(df["dataset_id"].dropna()) - {path.name}:
            errors.append(f"{name}: dataset_id must be '{path.name}' everywhere")
        pk = spec.get("primary_key")
        if pk and set(pk) <= set(df.columns) and df.duplicated(pk).any():
            errors.append(f"{name}: duplicate keys {df.loc[df.duplicated(pk), pk].values.tolist()[:5]}")

    sp = tables.get("specimens")
    if sp is None:
        return errors
    for name, df in tables.items():
        fk = SCHEMA["tables"][name].get("foreign_key")
        if fk and "specimen_id" in df:
            orphans = sorted(set(df["specimen_id"]) - set(sp["specimen_id"]))
            if orphans:
                errors.append(f"{name}: specimen_id not in specimens.csv: {orphans[:5]}")
    pl = tables.get("plies")
    if pl is not None and {"ply_count", "specimen_id"} <= set(sp.columns):
        counts = pl.groupby("specimen_id").size()
        bad = [s for s, n in zip(sp["specimen_id"], sp["ply_count"]) if counts.get(s, 0) != n]
        if bad:
            errors.append(f"plies: row count does not match ply_count for {bad[:5]}")
    for f in sp.get("source_file", pd.Series(dtype=str)).dropna():
        if not (path / f).exists():
            errors.append(f"specimens.source_file: {f} does not exist")
            break
    if "point_count" in sp:
        check_curves(path, sp, errors)
    return errors


def main(names):
    datasets = sorted(p for p in (ROOT / "datasets").iterdir() if p.is_dir())
    if names:
        datasets = [p for p in datasets if p.name in names]
    failed = False
    for path in datasets:
        errors = check_dataset(path)
        print(f"{'FAIL' if errors else 'ok  '} {path.name}")
        for e in errors:
            print(f"     - {e}")
        failed |= bool(errors)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
