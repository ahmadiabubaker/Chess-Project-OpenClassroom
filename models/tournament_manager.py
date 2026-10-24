import json
from datetime import datetime
from pathlib import Path

from .tournament import Tournament


class TournamentManager:
    def __init__(self, data_folder="data/tournaments"):
        # Path() rather than string juggling, so building file names with "/"
        # below behaves the same on Windows, macOS and Linux
        datadir = Path(data_folder)
        self.data_folder = datadir
        self.tournaments = []
        # One JSON file in the folder = one tournament, exactly the way
        # ClubManager treats data/clubs/
        for filepath in datadir.iterdir():
            # Skips sub-folders and any non-JSON file that happens to be there
            if filepath.is_file() and filepath.suffix == ".json":
                try:
                    self.tournaments.append(Tournament(filepath))
                except (json.JSONDecodeError, KeyError, TypeError) as exc:
                    # Malformed JSON, missing fields, or the wrong shape
                    # entirely (e.g. an old-format sample file) - skip it
                    # instead of crashing the whole app on startup.
                    print(filepath, "could not be loaded:", exc)

    def create(self, name, venue, date_start, date_end, number_of_rounds):
        # The file name is derived from the tournament name, the same way
        # ClubManager builds a club's file name
        stem = name.replace(" ", "")
        filepath = self.data_folder / (stem + ".json")
        # A second tournament whose name produces the same file name would
        # otherwise overwrite the first one's file, so the name is suffixed
        # until a free one is found
        suffix = 2
        while filepath.exists():
            filepath = self.data_folder / f"{stem}-{suffix}.json"
            suffix += 1
        tournament = Tournament(
            filepath=filepath,
            name=name,
            venue=venue,
            date_start=date_start,
            date_end=date_end,
            number_of_rounds=number_of_rounds,
        )
        # The manager owns the file name, so the manager does the first save -
        # the same split of responsibility ClubManager and ChessClub use
        tournament.save()

        # Added to the in-memory list too, so a caller that has just created a
        # tournament sees it without re-reading the folder
        self.tournaments.append(tournament)
        return tournament

    def in_progress(self):
        """Returns every tournament that hasn't been completed yet."""

        # Used by TournamentListCmd at startup to decide whether to open a
        # tournament straight away or show the list
        return [t for t in self.tournaments if not t.completed]

    def sorted_by_start_date(self):
        """Returns every tournament sorted by start date, descending
        (upcoming/most recent first) - per the spec's Main Screen rule.
        """

        # The dates are stored as strings, so they have to be parsed back into
        # datetimes before sorting: as text, "21-06-2022" would sort after
        # "03-12-2022" because it compares the day numbers first
        return sorted(
            self.tournaments,
            key=lambda t: datetime.strptime(t.date_start, Tournament.DATE_FORMAT),
            reverse=True,
        )
