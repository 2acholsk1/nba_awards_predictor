# nba_awards_predictor

## Main goal
The goal of the project is to use statistical data to predict the list of players who will receive awards (first, second and third all-nba team, first and second rookie all-nba team) for the regular season. 

## Setup

Firstly make sure you have Python on your system

Next, clone this repository:
```bash
$ git clone https://github.com/2acholsk1/nba_awards_predictor.git
```

After that, you need to setup environment with the help of Makefile:
```bash
$ make setup-venv
```
which setup virtualenvironment, then building and installing package:
```bash
$ make setup
```

## Running

To run the prediction, use command:
```bash
$ NBA_predict
```

## Documentation