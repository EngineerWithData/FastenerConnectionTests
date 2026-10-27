# Peterman, Nakata & Schafer (2014): stud-to-sheathing screw connections

48 monotonic and cyclic tests of sheathing (OSB or gypsum) screwed to cold-formed steel studs, tested at Johns Hopkins University as part of the CFS-NEES project.

**Cite:** Peterman, K.D., Nakata, N., Schafer, B.W. (2014). Hysteretic characterization of cold-formed steel stud-to-sheathing connections. *Journal of Constructional Steel Research* 101: 254–264. [Link](https://www.sciencedirect.com/science/article/abs/pii/S0143974X14001618)

The steel material properties come from Table 2 of Peterman, K.D., Schafer, B.W. (2013), *Hysteretic shear response of fasteners connecting sheathing to cold-formed steel studs*, CFS-NEES Research Report RR04.

## Test program

| Sheathing | Thickness | Screw | Steel | Tests |
|---|---|---|---|---|
| OSB | 7/16 in (11.2 mm) | #8 Simpson Strong-Tie Quik Drive | 33, 54, 97 mil | 24 |
| Gypsum | 1/2 in (12.7 mm) | #6 Simpson Strong-Tie Quik Drive | 33, 54, 97 mil | 24 |

Each specimen has **8 screws** (`fastener_count` = 8). **Force is the total on all 8 screws**, not the force per screw. Divide `force_n` by 8 for an average per-screw value.

## Specimen IDs

e.g. `c54o6_1`:

| Part | Meaning |
|---|---|
| `c` / `m` | Cyclic / monotonic |
| `54` | Steel designation thickness, mils |
| `o` / `g` | OSB / gypsum |
| `6` / `12` | A test-configuration parameter defined in the paper; not recorded elsewhere in the raw files |
| `1` | Replicate |

## What's in `processed/`

Converted by `tools/json_format.py` from the JSON files in `raw/`, which are unchanged. The raw files are in inches, lbf, and psi, and are converted to mm, N, and MPa.

- Ply thicknesses are **nominal** (`nominal` = `thickness`), as the raw files state.
- Sheathing material properties are stored as `unknown` in the raw files and are blank here.
- From the raw files' notes: the data were zeroed using the average of the first 10 load and displacement readings, and load and displacement voltages were scaled by factors provided by the first author.

## Known issues and open questions

- **Meaning of `6` / `12` in the IDs:** not recorded in the raw files. See the paper.
- **Unequal replicates:** `c54o12` has one test, and `m97o12` has three.

## Regenerating

```bash
python datasets/peterman-2014/convert.py
```
