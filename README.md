# Fastener Connection Test Database

Load-deformation test data for fastened connections to cold-formed steel. The tests come from multiple research programs and are converted to one shared, open format (CSV).

Each test is a single-shear connection: screws or power-actuated fasteners (PAFs) through steel, OSB, plywood, or gypsum, loaded monotonically or cyclically. Every specimen has its full force-displacement curve, plus the fastener and ply properties needed to model it. The data is meant for calibrating connection backbone and hysteresis models, for training and checking machine-learning predictors, and for comparing design equations against tests.

**612 tests from 3 research programs so far, and the database grows with contributions. If you have fastener connection test data, see [Contribute your data](#contribute-your-data).**

## Datasets

| Dataset | Connections | Fasteners | Tests | Source |
|---|---|---|---|---|
| [peterman-2014](datasets/peterman-2014/) | OSB- and gypsum-to-steel stud | #6, #8 screws | 48 | [Peterman, Nakata & Schafer (2014)](https://www.sciencedirect.com/science/article/abs/pii/S0143974X14001618) |
| [tao-2016](datasets/tao-2016/) | Steel-to-steel; OSB-, plywood-, and gypsum-to-steel | #6–#12 screws | 408 | [Tao, Chatterjee, Cole & Moen (2016)](https://www.researchgate.net/publication/333671326) |
| [zhang-2020](datasets/zhang-2020/) | Steel sheet-to-steel (2- and 3-ply) | #8–#12 screws, PAFs | 156 | [Zhang & Schafer (2020)](https://doi.org/10.1061/(ASCE)ST.1943-541X.0003233) |

Each dataset folder has its own README (test program, specimen naming, known issues), its own `dataset.yaml` (authors, citation, license), and the original files in `raw/`.

## Using the data

Every dataset has the same files in `processed/`. All values are in mm, N, and MPa. The columns are defined in [SCHEMA.md](SCHEMA.md).

| File | Contents |
|---|---|
| `specimens.csv` | One row per test: loading, fastener type, size, and geometry |
| `plies.csv` | One row per ply: material, thickness, and steel or sheathing properties |
| `curves/<specimen_id>.csv` | The force-displacement curve for one test |

```python
import pandas as pd

ds = "datasets/tao-2016/processed"
specimens = pd.read_csv(f"{ds}/specimens.csv")
plies = pd.read_csv(f"{ds}/plies.csv")

# Monotonic #10 screw steel-to-steel tests, with the peak load of each
mono = specimens.query("loading == 'monotonic' and fastener_size == '#10'")
for sid in mono["specimen_id"]:
    curve = pd.read_csv(f"{ds}/curves/{sid}.csv")
    print(sid, curve["force_n"].max())
```

To get every dataset in one table, run `python tools/build_combined.py`. It writes `combined/specimens.parquet`, `combined/plies.parquet`, and `combined/curves.parquet` (every curve stacked, about 7 million rows).

## Contribute your data

Connection tests are expensive. Most of them end up as a figure in a paper or as a spreadsheet on one lab's drive. Pooled, they are worth much more: models calibrated on several labs' tests, design equations checked against hundreds of tests instead of dozens, and fewer repeated tests. Contributions of any size are welcome, from a whole test program to a single series.

**Useful data includes:**

- Screw, PAF, nail, bolt, rivet, or other fastener tests on cold-formed steel
- Steel-to-steel, or sheathing-to-steel with any sheathing
- Monotonic or cyclic loading
- Older tests that were never published as data, and new tests from current projects

**What you need:** a force-displacement record for each test, plus whatever fastener and ply information you have (thicknesses, material properties, fastener size). Missing fields are fine: leave them blank.

**What you get:** your dataset keeps your name, your citation, and the license you choose. Everyone who uses it is asked to cite your original work, and your dataset gets a folder and a row in the table above.

**How to contribute:**

- **Not comfortable with Git, or your data is in raw spreadsheets?** [Open an issue](https://github.com/EngineerWithData/FastenerConnectionTests/issues/new?template=new-dataset.md) describing what you have. We'll help convert it.
- **Comfortable with Python and Git?** Follow [CONTRIBUTING.md](CONTRIBUTING.md). In short: add a folder under `datasets/` with your raw files, a `convert.py` script, a README, and a `dataset.yaml`. Then run `python tools/validate.py` and open a pull request.

Corrections to existing datasets are just as welcome. If you find a problem, open an issue or a pull request.

### Wanted

These programs have published fastener tests that aren't in the database yet. If you're an author, we'd especially like to hear from you:

- Derveni, F., et al. (2021). High-fidelity finite element modeling of wood-sheathed cold-formed steel shear walls. *Journal of Structural Engineering* 147(2).
- Torabian, S., and Schafer, B.W. (2021). Cyclic experiments on sidelap and structural connectors in steel deck diaphragms. *Journal of Structural Engineering* 147(4).

## Citing

Cite the original source of each dataset you use. Its `dataset.yaml` has the citation. To cite the database itself, see [CITATION.cff](CITATION.cff).

## License

Each dataset keeps the license chosen by its contributors (see its `dataset.yaml`). The code in `tools/` and `schema/` is MIT-licensed (see [LICENSE](LICENSE)).
