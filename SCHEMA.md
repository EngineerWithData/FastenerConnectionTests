# Data schema (v1.0.0)

Every dataset writes the same files to `datasets/<id>/processed/`. The machine-readable version of this file is [schema/schema.yaml](schema/schema.yaml), and `tools/validate.py` enforces it.

**Units:** lengths are in **mm**, forces in **N**, and stresses in **MPa**. Convert in `convert.py`, and record the original units in `dataset.yaml`.

## `specimens.csv`: one row per test

| Column | Required | Description |
|---|---|---|
| `dataset_id` | yes | Folder name of the dataset, e.g. `tao-2016` |
| `specimen_id` | yes | Unique within the dataset. Use the source's own naming where possible. |
| `loading` | yes | `monotonic` or `cyclic` |
| `fastener_type` | yes | `screw`, `paf` (power-actuated fastener), `nail`, `bolt`, `rivet`, or `other` |
| `fastener_count` | yes | Number of fasteners in the specimen. Each dataset README says whether force is per fastener or the total. |
| `fastener_size` | no | Nominal size, e.g. `#10` |
| `fastener_diameter_mm` | no | Major thread (or shank) diameter |
| `fastener_length_mm` | no | Fastener length |
| `head_diameter_mm` | no | Head diameter |
| `head_shape` | no | `hex`, `flat`, `pan`, `bugle`, `wafer`, `truss`, or `other` |
| `coating` | no | e.g. `clear zinc` |
| `fastener_product` | no | Manufacturer and product number or name |
| `ply_count` | yes | Number of plies; must match the rows in `plies.csv` |
| `point_count` | yes | Number of points in the curve file; must match its row count |
| `source_file` | yes | The file in the dataset folder this specimen came from, e.g. `raw/Tao_2016_4354-12-M2.json` |
| `notes` | no | Anything a user should know about this specimen |

## `plies.csv`: one row per ply

| Column | Required | Description |
|---|---|---|
| `dataset_id`, `specimen_id` | yes | Must match a row in `specimens.csv` |
| `ply` | yes | 1, 2, …, numbered from the fastener head (ply 1 is under the head) |
| `material` | yes | `steel`, `osb`, `plywood`, `gypsum`, or `other` |
| `thickness_mm` | yes | Ply thickness. For steel, the base metal thickness where known. |
| `elastic_modulus_mpa` | no | Elastic modulus |
| `yield_stress_mpa` | no | Yield stress |
| `ultimate_stress_mpa` | no | Ultimate (tensile) stress |
| `nominal` | no | Which of this ply's values are nominal rather than measured, separated by `;`, e.g. `thickness;elastic_modulus`. Blank means all values given are measured. |

## `curves/<specimen_id>.csv`: one file per test

| Column | Required | Description |
|---|---|---|
| `displacement_mm` | yes | Connection displacement. The dataset README says how it was measured. |
| `force_n` | yes | Applied force |

Rows are in the order recorded. `tools/build_combined.py` stacks every curve into one table and adds `dataset_id`, `specimen_id`, and `point` (the row index).

## The JSON format

The first datasets were contributed as one JSON file per test, and those files are kept unchanged in each dataset's `raw/` folder. New contributors can use this format too, and convert it with `tools/json_format.py`:

```json
{
  "source":   {"authors": [], "date": "YYYY-MM-DD", "title": "", "bibtex": "",
               "units": ["mm", "N"], "nominal_data": ["elastic modulus"], "notes": ""},
  "fastener": {"type": ["screw"],
               "details": [{"size": "#10", "major thread diameter": 4.8, "length": 25,
                            "head diameter": 10.2, "head shape": "hex",
                            "coating": "clear zinc", "product number": ""}]},
  "ply":      {"type": ["steel", "steel"], "thickness": [1.11, 1.43],
               "elastic_modulus": [203395, 203395], "yield_stress": [590, 393],
               "ultimate_stress": [615, 493]},
  "test":     {"name": "4354-12-M2", "loading": "monotonic",
               "force": [], "displacement": []}
}
```

`source` may also be a list, when properties come from more than one publication. `fastener.type` and `fastener.details` have one entry per fastener. The `ply` lists start at the fastener head.

## Changing the schema

Add columns or vocabulary terms by pull request. Update `schema/schema.yaml` and this file together, and bump the version: minor for additions, major for anything that breaks existing datasets.
