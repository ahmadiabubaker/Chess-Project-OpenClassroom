from commands.context import Context
from models import TournamentManager

from .base import BaseCommand


class TournamentListCmd(BaseCommand):
    """Command to get the list of tournaments.

    Per the spec's Main Screen rule: if exactly one tournament is in
    progress, jump straight to its View/Manage screen. Otherwise (zero or
    several in progress), show the full list, sorted by start date
    descending.
    """

    def execute(self):
        tm = TournamentManager()
        in_progress = tm.in_progress()

        if len(in_progress) == 1:
            return Context("tournament-view", tournament=in_progress[0])

        return Context("tournament-main", tournaments=tm.sorted_by_start_date())
