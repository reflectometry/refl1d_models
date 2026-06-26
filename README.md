# refl1d_models

Curated example reflectometry datasets — together with the **plans** and
**models** generated from them — used to develop and test reflectometry
analysis tools such as [nr-analyzer](https://github.com/neutrons-ai/nr-analyzer)
and AuRE.

Each example is a self-contained folder holding a reduced dataset, the
scientist's description of the sample, and the artifacts a modelling pipeline
produces from them. Having real datasets paired with their expected outputs lets
us exercise the tools end to end and catch regressions against known-good
results.

## Repository layout

Examples live under [`refl1d_models/`](refl1d_models/). Every example follows the
same convention:

```
refl1d_models/<example-name>/
├── context.md            # the scientist's free-form sample description
├── <data files>          # reduced reflectivity data (see "Examples" below)
├── plan/
│   └── job_<id>.yaml      # plan-data output: a create-model-ready config
├── models/
│   └── <name>.py          # create-model output: a refl1d-ready model script
└── reference/             # (optional) hand-written expert model, for comparison
    └── <name>.py
```

The pipeline each example captures:

| Stage | Tool | Input → Output |
|-------|------|----------------|
| Plan  | `plan-data` | `context.md` + a data file → `plan/job_<id>.yaml` |
| Model | `create-model --config plan/job_<id>.yaml` | the plan → `models/<name>.py` |
| Fit   | `run-fit models/<name>.py` | the model script → a fit result |

`context.md` is the **input** a human provides; `plan/` and `models/` are
**outputs** of the tools. A `reference/` model, where present, is a hand-written
model from a domain expert — useful as a ground truth to compare a generated
model against.

## Examples

### `LR-cu-film-corefined` — Liquids Reflectometer (SNS BL-4B)

A copper film (CuOₓ / ~50 nm Cu / ~3 nm Ti on Si, measured in D₂O with neutrons
entering from the silicon side). The dataset is a set of **partial** files for
one measurement sequence that are co-refined as a single state, plus the
combined auto-reduced file:

- `REFL_226642_{1,2,3}_*_partial.txt` — the three angle segments (co-refined)
- `REFL_226642_combined_data_auto.txt` — the auto-stitched combined dataset
- `plan/job_226642.yaml`, `models/sample5_ocv_226642.py`

### `polref-ni58-magnetic` — POLREF (ISIS, polarized neutrons)

A 1200 Å Ni[58] magnetic layer on Si, measured with polarized neutrons (PNR).
The data are header-less three-column (`Q R dR`) spin-state files:

- `Ni58_stitched_u.dat` / `Ni58_stitched_d.dat` — spin-up / spin-down
- `plan/job_Ni58_stitched.yaml`, `models/Ni58_basic_model.py`
- `reference/Ni58_basic_model.py` — the hand-written expert model this example
  was originally built from

## Installing nr-analyzer

The `plan-data`, `create-model`, and `run-fit` commands come from
[nr-analyzer](https://github.com/neutrons-ai/nr-analyzer):

```bash
git clone https://github.com/neutrons-ai/nr-analyzer.git
cd nr-analyzer
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Generating a plan and model from a `context.md` (`plan-data`, and
`create-model`'s LLM mode) additionally needs
[AuRE](https://github.com/neutrons-ai/aure) installed in the same environment
and a configured LLM endpoint — see the nr-analyzer
[installation notes](https://github.com/neutrons-ai/nr-analyzer#installation).
Running a fit on an existing model script (`run-fit`) does not need an LLM.

## Using the examples

Clone the repo and point a tool at an example folder. Each plan references its
data files by bare name, and the data sits one level up from `plan/`, so tell
the tool where the data is. The simplest way is the `--data-dir` flag:

```bash
create-model --config refl1d_models/LR-cu-film-corefined/plan/job_226642.yaml \
  --data-dir refl1d_models/LR-cu-film-corefined
```

`create-model` (and `analyze-sample`) resolve relative data files in this
order: `--data-dir` → the config file's directory → the current directory →
the `ANALYZER_*` data directories. So you can equally just run from the example
folder (the current-directory fallback), or set `ANALYZER_PARTIAL_DATA_DIR` /
`ANALYZER_COMBINED_DATA_DIR` (or a `.env`) to the example folder. Plans are kept
free of machine-specific paths — the data location is supplied at run time, not
baked into the YAML.

The generated `models/*.py` scripts reference the data by absolute path. If you
cloned the repo somewhere other than `~/git/refl1d_models`, update that path
before running a fit.

## Adding a new example

1. Create `refl1d_models/<example-name>/` and drop in the reduced data files.
2. Write a `context.md` describing the sample (substrate, layers, ambient,
   measurement conditions, and any modelling hypotheses).
3. Generate the plan and model with `plan-data` / `create-model` (outputs land
   in `plan/` and `models/`); optionally add a hand-written `reference/` model.

## License

MIT — see [LICENSE](LICENSE).
