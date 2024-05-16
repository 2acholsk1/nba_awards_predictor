# NBA AWARDS PREDICTOR

## Main goal
The goal of the project is to use statistical data to predict the list of players who will receive awards (first, second and third all-nba team, first and second rookie all-nba team) for the regular season. 

## Description

Data downloaded from Basketball-reference [link](https://www.basketball-reference.com/)

Statistics of players playing in the NBA from the 1999/2000 season to 2023/2024.

Description of shortcuts in data farames [link](https://github.com/2acholsk1/nba_awards_predictor/tree/main/data/desc_short.md)


## Setup

Clone repository:
```bash
git clone https://github.com/2acholsk1/nba_awards_predictor.git
cd nba_award_predictor
```

After that, you need to setup virtual environment with help of Makefile:
```bash
make setup-venv
```
Remember to activate venv with command: `source bin/activate`.

Then you can build and install package:
```bash
make setup
```

## Running

To run the prediction, use command:
```bash
NBA_predict
```

## Documentation