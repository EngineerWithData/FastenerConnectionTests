"""Convert specimen files in this repository's JSON format to the shared CSV tables.

The JSON format (one file per specimen) is described in SCHEMA.md. A dataset whose
raw/ folder holds files in this format can use a convert.py as short as:

    from tools.json_format import convert
    convert(Path(__file__).resolve().parent, length="mm", force="N", stress="MPa")

Dataset-specific differences (units, material names, which properties are nominal)
are passed in as arguments rather than edited into the raw files.
"""
import json
import shutil
from pathlib import Path

import pandas as pd

TO_MM = {"mm": 1.0, "in": 25.4}
TO_N = {"N": 1.0, "lbf": 4.4482216152605}
TO_MPA = {"MPa": 1.0, "psi": 0.006894757293168361}

MATERIALS = {"steel": "steel", "osb": "osb", "plywood": "plywood", "gypsum": "gypsum"}
FASTENER_TYPES = {"screw": "screw", "paf": "paf"}
HEAD_SHAPES = {"hex": "hex", "flat": "flat", "pan": "pan", "bugle": "bugle"}

# Ply properties a source can flag as nominal, keyed by the spellings used in raw files.
NOMINAL_TERMS = {
    "elastic modulus": "elastic_modulus",
    "elastic_modulus": "elastic_modulus",
}


def _num(v, factor):
    """Scale a number; return None for blanks and text such as 'unknown'."""
    return v * factor if isinstance(v, (int, float)) else None


def _one(values, what, path):
    """Collapse a per-fastener list to one value; fail if fasteners differ."""
    distinct = {json.dumps(v, sort_keys=True) for v in values}
    if len(distinct) > 1:
        raise ValueError(f"{path.name}: fasteners have different {what}; schema allows one per specimen")
    return values[0]


def convert(here, length, force, stress, nominal_by_ply=None, specimen_notes=None):
    """Read here/raw/*.json and write here/processed/.

    length, force, stress: units used in the raw files (keys of TO_MM, TO_N, TO_MPA).
    nominal_by_ply: function(ply_dict, source_nominal_terms) -> list of nominal property
        names for one ply. Defaults to mapping the source's nominal_data terms onto
        every ply.
    specimen_notes: dict of specimen_id -> note text.
    """
    here = Path(here)
    dataset_id = here.name
    out = here / "processed"
    curves_dir = out / "curves"
    if curves_dir.exists():
        shutil.rmtree(curves_dir)
    curves_dir.mkdir(parents=True)
    lf, ff, sf = TO_MM[length], TO_N[force], TO_MPA[stress]
    specimen_notes = specimen_notes or {}

    specimens, plies = [], []
    for path in sorted((here / "raw").glob("*.json")):
        j = json.loads(path.read_text())
        sources = j["source"] if isinstance(j["source"], list) else [j["source"]]
        terms = [t for s in sources for t in (s.get("nominal_data") or [])]
        test, fast, ply = j["test"], j["fastener"], j["ply"]
        sid = str(test["name"])

        ftype = _one(fast["type"], "types", path)
        d = _one(fast["details"], "details", path)
        size = d.get("size")
        head = d.get("head shape")
        specimens.append({
            "dataset_id": dataset_id,
            "specimen_id": sid,
            "loading": test["loading"],
            "fastener_type": FASTENER_TYPES[ftype.lower()],
            "fastener_count": len(fast["type"]),
            # PAF records store the product code in "size"; it is kept in fastener_product.
            "fastener_size": size if ftype.lower() == "screw" else None,
            "fastener_diameter_mm": _num(d.get("major thread diameter"), lf),
            "fastener_length_mm": _num(d.get("length"), lf),
            "head_diameter_mm": _num(d.get("head diameter"), lf),
            "head_shape": HEAD_SHAPES.get(str(head).lower()) if head else None,
            "coating": d.get("coating"),
            "fastener_product": d.get("product number") or d.get("product name"),
            "ply_count": len(ply["type"]),
            "point_count": len(test["force"]),
            "source_file": f"raw/{path.name}",
            "notes": specimen_notes.get(sid),
        })

        for i, mat in enumerate(ply["type"]):
            p = {k: ply[k][i] for k in ("type", "thickness", "elastic_modulus", "yield_stress", "ultimate_stress")}
            if nominal_by_ply:
                nominal = nominal_by_ply(p, terms)
            else:
                nominal = [NOMINAL_TERMS[t] for t in terms]
            plies.append({
                "dataset_id": dataset_id,
                "specimen_id": sid,
                "ply": i + 1,
                "material": MATERIALS[mat.lower()],
                "thickness_mm": _num(p["thickness"], lf),
                "elastic_modulus_mpa": _num(p["elastic_modulus"], sf),
                "yield_stress_mpa": _num(p["yield_stress"], sf),
                "ultimate_stress_mpa": _num(p["ultimate_stress"], sf),
                "nominal": ";".join(dict.fromkeys(nominal)) or None,
            })

        curve = pd.DataFrame({
            "displacement_mm": pd.Series(test["displacement"], dtype=float) * lf,
            "force_n": pd.Series(test["force"], dtype=float) * ff,
        })
        curve.to_csv(curves_dir / f"{sid}.csv", index=False, float_format="%.6g")

    pd.DataFrame(specimens).to_csv(out / "specimens.csv", index=False, float_format="%.6g")
    pd.DataFrame(plies).to_csv(out / "plies.csv", index=False, float_format="%.6g")
    print(f"{dataset_id}: {len(specimens)} specimens, {len(plies)} plies")
