# NBA AWARDS PREDICTOR

## Main goal
The goal of the project is to use statistical data to predict the list of players who will receive awards (first, second and third all-nba team, first and second rookie all-nba team) for the regular season. 

## Setup

Firstly make sure you have Python on your system

Next, clone this repository:
```bash
git clone https://github.com/2acholsk1/nba_awards_predictor.git
cd nba_award_predictor
```

After that, you need to setup virtual environment with the help of Makefile:
```bash
make setup-venv
```
Remember to activate venv with command: 'source bin/activate'
then you can build and install package:
```bash
make setup
```

## Running

To run the prediction, use command:
```bash
NBA_predict
```

## Documentation