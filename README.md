# Mutual Fund Analytics

This repository contains a Python data science project for mutual fund analytics, with datasets, notebooks, and dashboard files under `mutual_fund_analytics/`.

## What is included

- `mutual_fund_analytics/data/`: source CSV datasets for the project
- `mutual_fund_analytics/notebooks/`: analysis notebooks
- `mutual_fund_analytics/dashboard/`: dashboard or visualization artifacts
- `.vscode/`: recommended VS Code extensions and settings
- `requirements.txt`: Python dependencies for pip
- `environment.yml`: Conda environment definition

## Setup

### Option 1: Pip + virtual environment

1. Open a terminal in the repository root.
2. Create the virtual environment:

```powershell
python -m venv .venv
```

3. Activate the environment:

```powershell
.venv\Scripts\Activate
```

4. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Option 2: Conda

1. Create the environment:

```powershell
conda env create -f environment.yml
```

2. Activate it:

```powershell
conda activate mutual_fund_analytics
```

## Recommended VS Code setup

Open this repository in VS Code and install the recommended extensions from `.vscode/extensions.json`.

### Recommended extensions

- Python
- Jupyter
- Pylance
- Jupyter Notebook Renderers

## Running the project

- Use `Jupyter Lab` or `Jupyter Notebook` for interactive data analysis.
- Open notebooks from `mutual_fund_analytics/notebooks/`.
- Use the data files in `mutual_fund_analytics/data/`.

## Helpful commands

```powershell
python -m ipykernel install --user --name mutual_fund_analytics --display-name "mutual_fund_analytics"
jupyter lab
```

## Notes

- If you create a new Python script, run it from the repository root so relative paths resolve correctly.
- Keep data files in `mutual_fund_analytics/data/` and notebooks in `mutual_fund_analytics/notebooks/`.
