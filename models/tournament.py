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

    # Shared by the date properties below, and by TournamentManager when it
    # sorts tournaments by start date. Same format as Player.DATE_FORMAT
    DATE_FORMAT = "%d-%m-%Y"

    def __init__(self, filepath=None, name=None, venue=None, date_start=None,
                 date_end=None, number_of_rounds=None):
        self.filepath = filepath
        self.name = name
        self.venue = venue
        self.number_of_rounds = number_of_rounds
        # A brand new tournament has not started: no round, nobody registered,
        # nothing played. _load() overwrites all of these for an existing file
        self.current_round = 0
        self.players = []
        self.rounds = []
        self.completed = False

        # Two private attributes for the dates (datetime), with public string
        # getters/setters below - the same pattern Player uses for its birthday
        self._date_start = None
        self._date_end = None

        # A filepath and no name means "load this existing tournament";
        # anything else means "build a new one from these details"
        if filepath and not name:
            self._load()
        else:
            # Without a name there is nothing to identify the tournament by,
            # and TournamentManager could not work out a file name for it
            if not name:
                raise ValueError("Tournament name is required!")

            # Assigned through the properties below, which parse the strings
            self.date_start = date_start
            self.date_end = date_end

    def _load(self):
        """Loads tournament data from the JSON file at self.filepath."""

        with open(self.filepath) as fp:
            data = json.load(fp)

        self.name = data["name"]
        self.venue = data["venue"]
        # The dates are nested under their own key in the file, and go through
        # the properties so they are parsed on the way in
        self.date_start = data["dates"]["from"]
        self.date_end = data["dates"]["to"]
        self.number_of_rounds = data["number_of_rounds"]
        self.current_round = data["current_round"]
        self.completed = data["completed"]
        # The players are stored as chess_ids only: the club file owns the
        # player's real details. list() takes a copy of what json gave us
        self.players = list(data["players"])
        # Rounds and matches come back as plain nested dictionaries, so they
        # are rebuilt into objects here - the spec asks for class instances
        # rather than dictionaries being passed around the program
        self.rounds = [
            Round(
                number=round_dict["number"],
                # Each match dict's keys line up with Match's arguments
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
        # Parsing here means an invalid date is rejected the moment it is set,
        # rather than at some later point when it is displayed or sorted
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
        # Letting somebody join mid-tournament would also give them 0 points
        # and change the number of matches per round
        if self.rounds:
            raise RuntimeError(f"{self.name} has already started, no more players can be registered!")

        # Registering somebody twice would give them two matches in a round.
        # The register screen hides players who are already on the list, so
        # this is the model backing that rule up rather than relying on it
        if chess_id in self.players:
            raise ValueError(f"{chess_id} is already registered for this tournament!")

        self.players.append(chess_id)
        # Saved immediately: the spec asks for the JSON files to be updated
        # every time a change is made, so nothing is ever only in memory
        self.save()

    def points_for(self, chess_id):
        """Returns the total points a player has earned across every round
        played so far."""

        # Points are never stored, only summed from the matches, so they
        # cannot drift out of sync with the results that produced them.
        # This is what makes the spec's "points are automatically updated"
        # rule true: recording a result *is* updating the points
        return sum(round_.score_for(chess_id) for round_ in self.rounds)

    def standings(self):
        """Returns every registered chess_id, sorted by total tournament
        points (descending - highest first)."""

        # Used by the report, which displays the ranking, and by the
        # matchmaking, which needs to know who is at the top
        return sorted(self.players, key=self.points_for, reverse=True)

    def generate_next_round(self):
        """Advances the tournament: generates the next round's pairings, or
        - if the round that was just played was the last one - closes the
        tournament instead, per the spec's "Advance to next round" flow.
        """

        # The two guards below repeat checks the AdvanceRound screen already
        # makes. The screen checks them so the user gets a readable message;
        # they are repeated here so the rules hold however the model is used
        if self.completed:
            raise RuntimeError(f"{self.name} has already been completed!")

        # The next round's pairings depend on the current standings, so the
        # round in progress has to be finished before the next one is built
        if self.rounds and not self.rounds[-1].completed:
            raise RuntimeError("The current round is not finished yet!")

        # Checked before generating a new round, not after: this means the
        # round that just finished was the last one, so we close the
        # tournament here instead of ever generating a round N+1.
        # current_round becomes None because no round is in progress any more
        if self.rounds and len(self.rounds) == self.number_of_rounds:
            self.completed = True
            self.current_round = None
            self.save()
            return

        # The pairing rules live in matchmaking.py so they stay a pure
        # function of the tournament, easy to follow and to test on their own
        pairings = generate_pairings(self)
        # The rounds list is the source of truth for how far we have got, so
        # the new round's number comes from its length rather than a counter
        round_number = len(self.rounds) + 1
        # Each pair becomes a match with no result yet
        matches = [Match(pair) for pair in pairings]
        self.rounds.append(Round(round_number, matches))
        self.current_round = round_number
        self.save()

    def delete(self):
        """Permanently deletes this tournament's JSON file."""

        # The file *is* the tournament, so removing it is the whole deletion.
        # The object itself is dropped by the caller afterwards, and the next
        # TournamentManager simply will not find this file any more
        self.filepath.unlink()

    def save(self):
        """Serializes the tournament and saves it to the JSON file."""

        # Mirrors ChessClub.save(): the whole tournament is rewritten each
        # time, which keeps the file and the object in step with no partial
        # updates to get wrong
        with open(self.filepath, "w") as fp:
            json.dump(self.serialize(), fp)

    def serialize(self):
        """Serialize the instance in a format compatible with JSON."""

        # The keys here are exactly the ones _load() reads back, so saving and
        # loading stay symmetrical. The dates go through the properties, which
        # turn them back into strings - datetime is not JSON-serializable
        return {
            "name": self.name,
            "venue": self.venue,
            "dates": {"from": self.date_start, "to": self.date_end},
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "completed": self.completed,
            "players": list(self.players),
            # Each round serializes itself, and each of its matches in turn
            "rounds": [round_.serialize() for round_ in self.rounds],
        }
