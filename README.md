# Analysis code for "Evolution of Non-Metallic Inclusions During the Industrial Secondary Refining of an Al-Killed, Ca-Treated, Low-S Steel"

Code used for the typification, statistical evaluation, and visualisation of
non-metallic inclusion (NMI) data in:

> R. Musi, K. Thiele, S. Ilie, R. Rössler, S.K. Michelic (2026). Evolution of Non-Metallic Inclusions During the 
> Industrial Secondary Refining of an Al-Killed, Ca-Treated, Low-S Steel. *Scientific Reports*, [doi]

---

## Contents

| Path | Description |
|------|-------------|
| [`Code/Functions.py`](Code/Functions.py) | Shared functions: plot styling, ternary coordinate transforms, von Mises-Fisher KDE |
| [`Code/Figure - Boxplots of ECD.ipynb`](Code/Figure%20-%20Boxplots%20of%20ECD.ipynb) | Boxplots of equivalent circle diameter |
| [`Code/Figure - KDE in ternary Systems.ipynb`](Code/Figure%20-%20KDE%20in%20ternary%20Systems.ipynb) | Ternary kernel density estimation of NMI compositions |
| [`Code/Figure - Violinplots NMI composition.ipynb`](Code/Figure%20-%20Violinplots%20NMI%20composition.ipynb) | Violin plots of logarithmic oxide ratios |
| [`Code/Figure - Type distribution across stages.ipynb`](Code/Figure%20-%20Type%20distribution%20across%20stages.ipynb) | Number density of inclusion types along the process route |
| [`Code/Statistical analysis NMI size.ipynb`](Code/Statistical%20analysis%20NMI%20size.ipynb) | Mann-Whitney U tests, effect sizes, multiple-comparison correction |
| [`Data files/`](Data%20files) | Input data: inclusion lists per stage and type distributions |
| [`pyproject.toml`](pyproject.toml) | Declared dependencies |
| [`uv.lock`](uv.lock) | Fully resolved environment, with hashes |
| [`requirements.txt`](requirements.txt) | Flat pinned dependency list, generated from `uv.lock` |

## Requirements

- Python 3.14
- Packages as declared in `pyproject.toml`

### With uv (recommended)

[uv](https://docs.astral.sh/uv/) reproduces the exact environment from
`uv.lock`, including transitive dependencies:

```
uv sync --locked
```

### With pip

```
pip install -r requirements.txt
```

## Running the notebooks

Launch JupyterLab from the repository root, with the root on `PYTHONPATH` so
that `Code.Functions` is importable from the notebooks:

```
PYTHONPATH=$PWD uv run --with jupyterlab jupyter lab
```

Then open any notebook under `Code/` and run all cells. The notebooks resolve
the input data relative to their own directory, so they must be executed with
`Code/` as the working directory — which is what Jupyter does by default.

## Data


### `Data files/Inclusion lists per stage/`

All data in this folder is **synthetic**.

One file per sampling stage and heat, each with a `README` sheet and an
`NMI data` sheet holding one row per detected inclusion:

| Column | Description |
|--------|-------------|
| `Column A` | Identifier, format `<stage>-<heat>_<running number>` |
| `MgO`, `CaO`, `Al2O3`, `CaS`, `MnS` | Phase fractions of the inclusion, summing to 1 |
| `ECD (µm)` | Equivalent circle diameter |
| `Type` | Inclusion type from the classification scheme |


These files contain randomly generated values with the same structure and
column layout as the measured data. They exist so that the analysis code can be
executed and inspected without access to the measured datasets. Every file is a
copy of the same synthetic dataset, so all stages and heats yield identical
distributions: the figures and test statistics produced from them are
structurally valid but numerically meaningless. They are **not** measurements
and cannot reproduce or verify any result reported in the publication.

### `Data files/Type distribution/Type distribution.xlsx`

Number densities per inclusion type, in two sheets — `S1-S3` and `S4-S8`.


## Statistical evaluation

`Statistical analysis NMI size.ipynb` compares the ECD distributions at S7-CT and S8-TU for each
heat, for all NMIs and separately for the two Ca-aluminate types. It reports:

- **Mann-Whitney U test** — rank-based, no distributional assumptions
- **Cliff's δ** — effect size, with the consistent-variance confidence
  interval of Cliff (1993); magnitudes classified after Romano et al. (2006)
- **Hodges-Lehmann estimator** — location shift in µm, with the
  distribution-free Moses confidence interval
- **Holm-Bonferroni correction** across all twelve tests

Effect sizes are reported alongside p-values because the large particle counts
make small shifts statistically significant.


## Data availability

The particle-level data are available from the corresponding author on
reasonable request and with permission of voestalpine Stahl GmbH.

## Citation

Please cite the publication above. To cite this code, use the archived version
on Zenodo: https://doi.org/10.5281/zenodo.22756292 (concept DOI, resolves to the
latest version).

Machine-readable metadata is in [`CITATION.cff`](CITATION.cff).

## License

[MIT](LICENSE), covering both the code and the synthetic data files.

## Contact

Robert Musi, Montanuniversität Leoben — robert.musi@unileoben.ac.at
