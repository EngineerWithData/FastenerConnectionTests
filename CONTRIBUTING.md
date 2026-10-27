# Adding a dataset

Thank you for contributing. If any step below is a problem, [open an issue](https://github.com/EngineerWithData/FastenerConnectionTests/issues/new?template=new-dataset.md) and we'll help. You don't need to finish every step yourself.

1. **Create the folder.** Copy `templates/new-dataset/` to `datasets/<firstauthor>-<year>/`. Use lowercase with hyphens, e.g. `smith-2024`. If an author has more than one dataset from the same year, add a short suffix, e.g. `smith-2024-paf`.

2. **Add the original files to `raw/` exactly as received.** Never edit them. If the files total more than about 100 MB, put them on Zenodo instead, and list them in `dataset.yaml` under `external_files`.

3. **Write `convert.py`.** It reads `raw/` and writes `processed/specimens.csv`, `processed/plies.csv`, and one `processed/curves/<specimen_id>.csv` per test, following [SCHEMA.md](SCHEMA.md). It should:
   - convert to mm, N, and MPa
   - number plies from the fastener head (ply 1 is under the head)
   - map the source's terms onto the shared vocabularies (`loading`, `fastener_type`, `head_shape`, `material`)
   - fill `source_file` so every specimen can be traced back to `raw/`
   - read values from the source files rather than retyping them

   If your raw files are already in this repository's JSON format (see SCHEMA.md), `convert.py` is a few lines: call `tools/json_format.py`, as `datasets/tao-2016/convert.py` does.

4. **Fill in `dataset.yaml` and `README.md`.** The README must cover:
   - the test program and test fixture
   - how specimens are named
   - how displacement was measured, and what it includes (fastener slip only, or ply deformation too)
   - whether force is per fastener or the total for a specimen with several fasteners
   - which properties are measured and which are nominal
   - known problems with the data

5. **Check your work.**
   ```bash
   pip install -r requirements.txt
   python datasets/<id>/convert.py
   python tools/validate.py <id>
   ```

6. **Open a pull request.** CI runs every `convert.py`, checks that the committed `processed/` files match the output, and runs the validator.

7. **Add your dataset** to the table in the top-level `README.md`.

If your data needs a column or term the schema doesn't have, propose the schema change in the same pull request (see SCHEMA.md).
