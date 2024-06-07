# Milk Tracker

![Release](https://img.shields.io/github/v/release/tmlmt/milk-tracker?color=%23007ec6
 "Version") ![Coverage](./coverage.svg "Coverage")

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
- Typing python code and checking it with [mypy](https://mypy.readthedocs.io/en/stable/)

Huge thanks to the Open Source community for providing such great tools to the world.

## Features

- Protect access with password
- Record meals start and end times
- Lock start time of new meal
- See latest three days trends in graphs
- See daily stats in a table

## Backlog

- Better responsiveness
- Keep track of meal rounds during ongoing meal
- More daily stats and visualisation in graphs
- Remember daily intake of vitamins
- Keep a log of daily observations
- Edit and delete any meal

## License

MIT License

Copyright (c) 2024 Thomas Lamant