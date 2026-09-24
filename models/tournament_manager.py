import json
from datetime import datetime
from pathlib import Path

from .tournament import Tournament


class TournamentManager:
    def __init__(self, data_folder="data/tournaments"):
        datadir = Path(data_folder)
        self.data_folder = datadir
        self.tournaments = []
        for filepath in datadir.iterdir():
            if filepath.is_file() and filepath.suffix == ".json":
                try:
                    self.tournaments.append(Tournament(filepath))
                except (json.JSONDecodeError, KeyError, TypeError) as exc:
                    # Malformed JSON, missing fields, or the wrong shape
                    # entirely (e.g. an old-format sample file) - skip it
                    # instead of crashing the whole app on startup.
                    print(filepath, "could not be loaded:", exc)

    def create(self, name, venue, date_start, date_end, number_of_rounds):
        filepath = self.data_folder / (name.replace(" ", "") + ".json")
        tournament = Tournament(
            filepath=filepath,
            name=name,
            venue=venue,
            date_start=date_start,
            date_end=date_end,
            number_of_rounds=number_of_rounds,
        )
        tournament.save()

        self.tournaments.append(tournament)
        return tournament

    def in_progress(self):
        """Returns every tournament that hasn't been completed yet."""

        return [t for t in self.tournaments if not t.completed]

    def sorted_by_start_date(self):
        """Returns every tournament sorted by start date, descending
        (upcoming/most recent first) - per the spec's Main Screen rule.
        """

        return sorted(
            self.tournaments,
            key=lambda t: datetime.strptime(t.date_start, Tournament.DATE_FORMAT),
            reverse=True,
        )
