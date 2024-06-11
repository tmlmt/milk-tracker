# Milk Tracker

![GitHub License](https://img.shields.io/github/license/tmlmt/milk-tracker?color=green) ![Release](https://img.shields.io/github/v/release/tmlmt/milk-tracker?color=blue "Version") ![Coverage](./coverage.svg "Coverage")

<p float="left">
    <img src="screenshot-01.png" width="400" />
    <img src="screenshot-02.png" width="400" />
</p>

Basic breastfeeding data analysis and tracking

## Introduction

The idea of this app stemmed from the need to track and visualize breastfeeding meal statistics stored in a Pandas DataFrame. This was the opportunity to learn how to create and deploy a web app based on python-based nicegui, an alternative to streamlit with better state management and handling of user interaction. It quickly expanded to learn even more how to develop python applications with best development practices like:

- formatting and linting with [ruff](https://github.com/astral-sh/ruff)
- deploying with GitHub Actions
- split code using a model-view-controller design pattern
- validate data using [pydantic](https://github.com/pydantic/pydantic) models
- keep track of changes using [git-cliff](https://github.com/orhun/git-cliff)
- managing a python environment using [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html)
- Testing the code prior to releasing using [pytest](https://pytest.org/)
- Calculating the coverage of tests using [coverage](https://coverage.readthedocs.io/en/latest/)
- Typing python code and checking it with [mypy](https://mypy.readthedocs.io/en/stable/)

Huge thanks to the Open Source community for providing such great tools to the world.

## Features

- Protect access with password
- Record meals start and end times
- Lock start time of new meal
- Keep track of meal rounds during ongoing meal
- Reminders for daily intake of vitamins
- See latest three days trends in graphs
- See daily stats in a table

## Backlog

- Keep a log of daily observations
- Edit and delete any meal
- Prediction of next meal's time and duration

## License

MIT License

Copyright (c) 2024 Thomas Lamant