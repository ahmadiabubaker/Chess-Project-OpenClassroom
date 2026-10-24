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
        # Reloaded from disk on every call, so the list always reflects what
        # is actually in the JSON files - including a tournament created,
        # completed or deleted since the last time this ran
        tm = TournamentManager()
        in_progress = tm.in_progress()

        # "A tournament is happening": exactly one unfinished tournament, so
        # there is no ambiguity about which one the user means. This is the
        # startup shortcut only - TournamentMainCmd is used for navigation
        # back to the menu, so the user is never trapped on this screen
        if len(in_progress) == 1:
            return Context("tournament-view", tournament=in_progress[0])

        # Zero or several in progress, so the user has to choose. The sorting
        # happens in the model layer, leaving the screen only to display
        return Context("tournament-main", tournaments=tm.sorted_by_start_date())
