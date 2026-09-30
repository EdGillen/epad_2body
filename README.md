# EPAD: the two-body problem

Interactive notebooks on Kepler's laws and the radial velocity method. Click a badge to open a
notebook in your browser via [Binder](https://mybinder.org); nothing needs to be installed.

| Notebook | App: text, sliders and plots (code hidden) | Code: read, run and edit in JupyterLab |
|---|---|---|
| Kepler's laws | [![Kepler's laws: app](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/EdGillen/epad_2body/HEAD?urlpath=voila/render/kepler.ipynb) | [![Kepler's laws: code](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/EdGillen/epad_2body/HEAD?urlpath=lab/tree/kepler.ipynb) |
| Radial velocity method | [![Radial velocity: app](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/EdGillen/epad_2body/HEAD?urlpath=voila/render/radvel.ipynb) | [![Radial velocity: code](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/EdGillen/epad_2body/HEAD?urlpath=lab/tree/radvel.ipynb) |

Notes:
- Starting Binder can take a minute or two (longer the first time after the repository changes).
- The app view runs the whole notebook before it appears, and each slider move recomputes the orbit,
  so allow a few seconds.
- In the code view the notebook opens without any plots: click inside the notebook, then choose
  **Run > Run All Cells**.
- Binder sessions are temporary: they stop after about 10 minutes of inactivity and any changes you
  make in the code view are not saved. Download a notebook (File > Download) to keep your edits.

## Running locally

```bash
conda env create -f environment.yml
conda activate epad_2body
jupyter lab              # code view
voila kepler.ipynb       # app view (likewise for radvel.ipynb)
```

## Credits

Original notebooks by Sijme-Jan Paardekooper ([SijmeJan/epad_2body](https://github.com/SijmeJan/epad_2body)).
Updated in 2026 for current Jupyter, Matplotlib and Binder.
