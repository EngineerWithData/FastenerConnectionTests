# Zhang & Schafer (2020): steel sheet connections for CFS-framed steel sheet shear walls

156 monotonic and cyclic tests of thin steel sheet connected to cold-formed steel framing with screws or power-actuated fasteners (PAFs), tested at Johns Hopkins University. Each test has one fastener.

**Cite:** Zhang, Z., Schafer, B.W. (2020). *Test Report: Cyclic Performance of Steel Sheet Connections for CFS Steel Sheet Shear Walls.* Research Report No. CFSRC R-2020-06, Cold-Formed Steel Research Consortium.

The tests are also published in:

- Zhang, Z., Singh, A., Derveni, F., Torabian, S., Peterman, K.D., Hutchinson, T.C., Schafer, B.W. (2022). Cyclic experiments on steel sheet connections for standard CFS framed steel sheet sheathed shear walls. *Journal of Structural Engineering* 148(2), 04021261. <https://doi.org/10.1061/(ASCE)ST.1943-541X.0003233>
- Zhang, Z., et al. (2021). Cyclic experiments on isolated steel sheet connections for CFS framed steel sheet sheathed shear walls with new configurations. *Engineering Structures* 244, 112805. [Link](https://www.sciencedirect.com/science/article/abs/pii/S014102962100955X)

## Test program

| Fastener | Product | Plies | Tests |
|---|---|---|---|
| #8 and #10 pan-head screws | McMaster-Carr drilling screws | 2 or 3 | 105 |
| #12 pan-head screws | Grabber FP121878JBWZ | 2 or 3 | 23 |
| PAF | Hilti X-HSN 24 | 2 or 3 | 21 |
| PAF | Hilti X-ENP-19 | 2 | 7 |

Steel sheets are 0.31–0.78 mm. The thicker plies are 1.47–3.11 mm, plus 4.7 and 9.41 mm for some #12 screw and PAF tests. 133 tests are cyclic and 23 are monotonic. Steel properties are measured. Elastic moduli are nominal.

## Specimen IDs

The raw files name tests by number (`1` to `156`), and the IDs here keep those numbers. The test number to configuration mapping is in the report.

## What's in `processed/`

Converted by `tools/json_format.py` from the JSON files in `raw/`, which are unchanged. The units were already mm, N, and MPa. Force is the load on the single fastener.

For PAFs, the raw files store the product code (e.g. `XHSN24`) in the size field and `PAF_N/A_large flat` as the head shape. Here `fastener_size` and `head_shape` are blank for PAFs, and the product is in `fastener_product`.

## Known issues and open questions

- **3-ply specimens:** 42 tests (28 screw, 14 PAF) have three plies (thick–thin–thick, e.g. 2.54, 0.78, 2.54 mm), stored in that order. How they were assembled isn't recorded in the raw files. See the report.
- **Ply order:** for 2-ply tests the thin sheet is listed first and is assumed to be under the head.

## Regenerating

```bash
python datasets/zhang-2020/convert.py
```
