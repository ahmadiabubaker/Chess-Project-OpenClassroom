import json
from datetime import datetime

from .match import Match
from .matchmaking import generate_pairings
from .round import Round


class Tournament:
    """A chess tournament: a fixed number of rounds played between a
    registered pool of players, run at a single venue over a date range.

    Like ChessClub, the constructor works in two ways:
    - if filepath is provided (and no name), it loads an existing
      tournament from the JSON file
    - otherwise, it builds a brand new tournament from the given details.
      TournamentManager is responsible for computing the filepath and
      calling save() afterwards - the same split of responsibility used
      by ClubManager and ChessClub.
    """

    DATE_FORMAT = "%d-%m-%Y"

    def __init__(self, filepath=None, name=None, venue=None, date_start=None,
                 date_end=None, number_of_rounds=None):
        self.filepath = filepath
        self.name = name
        self.venue = venue
        self.number_of_rounds = number_of_rounds
        self.current_round = 0
        self.players = []
        self.rounds = []
        self.completed = False

        self._date_start = None
        self._date_end = None

        if filepath and not name:
            self._load()
        else:
            if not name:
                raise ValueError("Tournament name is required!")

            self.date_start = date_start
            self.date_end = date_end

    def _load(self):
        """Loads tournament data from the JSON file at self.filepath."""

        with open(self.filepath) as fp:
            data = json.load(fp)

        self.name = data["name"]
        self.venue = data["venue"]
        self.date_start = data["dates"]["from"]
        self.date_end = data["dates"]["to"]
        self.number_of_rounds = data["number_of_rounds"]
        self.current_round = data["current_round"]
        self.completed = data["completed"]
        self.players = list(data["players"])
        self.rounds = [
            Round(
                number=round_dict["number"],
                matches=[Match(**match_dict) for match_dict in round_dict["matches"]],
            )
            for round_dict in data["rounds"]
        ]

    def __str__(self):
        return f"<Tournament: {self.name}>"

    @property
    def date_start(self):
        """Property to get the start date (string) from the stored datetime."""
        return self._date_start.strftime(self.DATE_FORMAT)

    @date_start.setter
    def date_start(self, value):
        """Sets the start date (datetime) from a string."""
        self._date_start = datetime.strptime(value, self.DATE_FORMAT)

    @property
    def date_end(self):
        """Property to get the end date (string) from the stored datetime."""
        return self._date_end.strftime(self.DATE_FORMAT)

    @date_end.setter
    def date_end(self, value):
        """Sets the end date (datetime) from a string."""
        self._date_end = datetime.strptime(value, self.DATE_FORMAT)

    def register_player(self, chess_id):
        """Registers a player (by chess_id) for this tournament."""

        # The spec doesn't say either way - this is our own rule, matching
        # how real Swiss tournaments close registration once round 1 starts.
        if self.rounds:
            raise RuntimeError(f"{self.name} has already started, no more players can be registered!")

        if chess_id in self.players:
            raise ValueError(f"{chess_id} is already registered for this tournament!")

        self.players.append(chess_id)
        self.save()

    def points_for(self, chess_id):
        """Returns the total points a player has earned across every round
        played so far."""

        return sum(round_.score_for(chess_id) for round_ in self.rounds)

    def standings(self):
        """Returns every registered chess_id, sorted by total tournament
        points (descending - highest first)."""

        return sorted(self.players, key=self.points_for, reverse=True)

    def generate_next_round(self):
        """Advances the tournament: generates the next round's pairings, or
        - if the round that was just played was the last one - closes the
        tournament instead, per the spec's "Advance to next round" flow.
        """

        if self.completed:
            raise RuntimeError(f"{self.name} has already been completed!")

        if self.rounds and not self.rounds[-1].completed:
            raise RuntimeError("The current round is not finished yet!")

        # Checked before generating a new round, not after: this means the
        # round that just finished was the last one, so we close the
        # tournament here instead of ever generating a round N+1.
        if self.rounds and len(self.rounds) == self.number_of_rounds:
            self.completed = True
            self.current_round = None
            self.save()
            return

        pairings = generate_pairings(self)
        round_number = len(self.rounds) + 1
        matches = [Match(pair) for pair in pairings]
        self.rounds.append(Round(round_number, matches))
        self.current_round = round_number
        self.save()

    def delete(self):
        """Permanently deletes this tournament's JSON file."""

        self.filepath.unlink()

    def save(self):
        """Serializes the tournament and saves it to the JSON file."""

        with open(self.filepath, "w") as fp:
            json.dump(self.serialize(), fp)

    def serialize(self):
        """Serialize the instance in a format compatible with JSON."""

        return {
            "name": self.name,
            "venue": self.venue,
            "dates": {"from": self.date_start, "to": self.date_end},
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "completed": self.completed,
            "players": list(self.players),
            "rounds": [round_.serialize() for round_ in self.rounds],
        }
