# Tao et al. (2016): single-shear screw connections, steel-to-steel and sheathing-to-steel

408 monotonic and cyclic tests of single-shear screw connections, tested at Virginia Tech for the American Iron and Steel Institute. Each test has one screw.

**Cite:** Tao, F., Chatterjee, A., Cole, R., Moen, C.D. (2016). *Monotonic and Cyclic Response of Single Shear Cold-Formed Steel-to-Steel and Sheathing-to-Steel Connections.* Virginia Tech Research Report No. CE/VPI-ST-16/01, American Iron and Steel Institute, Washington, D.C. [PDF](https://www.researchgate.net/publication/333671326)

## Test program

| Connection | Fasteners | Steel thickness | Tests |
|---|---|---|---|
| Steel-to-steel | #8, #10, #12 hex-head screws | 0.50–2.56 mm, both plies | 222 |
| OSB-to-steel | #8, #10, #12 flat-head screws | 0.86–2.56 mm | 78 |
| Plywood-to-steel | #8, #10, #12 flat-head screws | 0.86–2.56 mm | 78 |
| Gypsum-to-steel | #6 bugle-head screws | 0.86–1.44 mm | 30 |

Most configurations were tested 3 times monotonically and 3 times cyclically (204 tests of each). Steel yield and ultimate stresses and thicknesses are measured values. Elastic moduli are nominal.

## Specimen IDs

**Steel-to-steel**, e.g. `4354-12-M2`:

| Part | Meaning |
|---|---|
| `43` | Ply 1 steel designation thickness, mils |
| `54` | Ply 2 steel designation thickness, mils |
| `12` | Screw size (#12) |
| `M` / `C` | Monotonic / cyclic |
| `2` | Replicate |

**Sheathing-to-steel**, e.g. `O243-10-C2`: `O` / `P` / `G` = OSB / plywood / gypsum, then a sheathing thickness index (`1`, `2`, `3`, thinnest to thickest), then the steel designation thickness in mils. The rest is as above.

`26` mil in the IDs corresponds to the 0.50 mm steel sheet.

## What's in `processed/`

Converted by `tools/json_format.py` from the JSON files in `raw/`, which are unchanged. The units were already mm, N, and MPa. Force is the load on the single screw.

## Known issues and open questions

- **Ply order for steel-to-steel:** the IDs and the ply lists in `raw/` give the same order. It's assumed that the first ply is under the screw head, as in the sheathing tests, but this hasn't been checked against the report.
- **`nominal_data` missing in some files:** 87 plywood and OSB files (P133–P397, O297, O397) have no `nominal_data` field. All files use the same nominal elastic moduli, so `convert.py` flags `elastic_modulus` as nominal everywhere.
- **Thickness varies within a series:** a few series have two thickness values for the same nominal ply, e.g. 1.43 and 1.44 mm in `2654-*`, and 0.86 and 0.90 mm in `O133-*` and `O233-*`. These are kept as stored.
- **Date:** the raw files give the source date as 2017-01-01. The report number (CE/VPI-ST-16/01) is 2016, which is used for the dataset ID.

## Regenerating

```bash
python datasets/tao-2016/convert.py
```
