# NBA_Analysis

The purpose of this project is to predict the outcomes of basketball games in the NBA.

## Getting Started

### Virtual Environment Setup

Run the following commands:

```
python3.10 -m venv ./nba_analysis_venv
./nba_analysis_venv/Scripts/activate
```

### Requirements Management

To install the packages, first ensure your virtual environment is activated. Nex run:

```
pip install -r ./requirements.txt
```

If you added a new package to the project, run the following to ensure it is in the requirements:

```
pip freeze > requirements.txt
```

### Setup SQL Cloud Access

Run the following command and fill out your access details:

```
python3.10 ./src/setup_access.py
```