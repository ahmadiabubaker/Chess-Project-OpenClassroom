# Castle Chess

A standalone, offline console application for managing chess clubs and running Swiss-style
tournaments, built for the OpenClassrooms WPS | P3 project. See `DESIGN.md` for the
architecture and build plan behind the tournament module.

## Setup

Requires Python 3.9 or later. From the project root:

```
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

`requirements.txt` includes:
- `faker` - used by `data/make-club.py` to generate sample club data (not required to run
  the applications themselves, which have no third-party dependencies)
- `flake8` and `flake8-html` - used to lint the code and generate the report described below

## Running the program

There are two entry points, run from the project root:

```
python manage_clubs.py   # create/manage chess clubs and their players
python castle_chess.py   # create and run tournaments, from registration to final report
```

Both are interactive: the program prints information and options, and you respond by typing
a value and pressing Enter. Data is read from and saved to the JSON files under `data/clubs/`
and `data/tournaments/` after every change, so the program can be stopped and restarted at any
time without losing data.

A tournament's players must already be registered in a club (via `manage_clubs.py`) before
they can be registered for a tournament - `castle_chess.py` searches across every club's
roster when registering a player.

## Code structure

### Data files

- JSON files for the chess clubs of Springfield and Cornville, under `data/clubs/`
- JSON files for tournaments, under `data/tournaments/`

### Models (`models/`)

- `Player` represents a chess player
- `ChessClub` represents a chess club (including its `Player`s)
- `ClubManager` manages every club (and creates new ones)
- `Tournament` represents a tournament: its players, rounds, and current state
- `Round` and `Match` represent one round of a tournament and one game within it
- `TournamentManager` manages every tournament (and creates new ones)
- `matchmaking.py` generates a round's pairings from the tournament's current standings
- `player_search.py` searches across every club's roster (used when registering a player)
- `report.py` builds a tournament's plain-text report

### Screens (`screens/`)

This package contains classes that display information from the models on the screen. Each
screen returns a Command instance (= the action to be carried out). Club/player screens live
under `screens/clubs/` and `screens/players/`; tournament screens live under
`screens/tournaments/`.

### Commands (`commands/`)

This package contains "commands" - instances of classes that are used to perform operations
from the program. Commands follow a *template pattern*. They **must** define the `execute`
method. When executed, a command returns a context.

### Main application

Each entry point (`manage_clubs.py`, `castle_chess.py`) is controlled by an `App` class. Based
on the current `Context` instance, it instantiates the corresponding screen and runs it. The
command returned by the screen is then executed to obtain the next context.

The main application is an infinite loop and stops when a context has the attribute `run` set
to `False`.

## Code quality

The project is linted with `flake8` (`max-line-length=119`). To check the code and regenerate
the HTML report under `flake8_report/`:

```
python -m flake8 --max-line-length=119 --exclude=venv,flake8_report --format=html --htmldir=flake8_report .
```

Open `flake8_report/index.html` in a browser to view it.

The `--exclude` is needed so the check covers this project only: without it, flake8 also
walks the `venv/` folder and reports thousands of violations from the installed
third-party packages.
