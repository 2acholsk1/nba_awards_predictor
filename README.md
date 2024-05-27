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

After that, you need to find `prediction_config.yaml` file, which is in configs folder.
There are parameters defining data features to train model and also model configuration.
If you have set the given configuration, you can call the command"
```bash
make data-work
```
Which will prepare, format and then label the data.
The next step is to deal with models, you can train them independently, with commands:
-Model #1: all-NBA 1st, 2nd and 3rd teams:
```bash
make model-all-nba
```
-Model #2: rookie all-NBA 1st and  2nd teams:
```bash
make model-rookie
```

## Running

The program has a model prepared for prediction all-NBA 1st, 2nd, 3rd teams and rookie all-NBA 1st, 2nd teams 
To run the prediction, use command and specify the path to save :
```bash
NBA_predict your/path/to/save/file
```

## Documentation