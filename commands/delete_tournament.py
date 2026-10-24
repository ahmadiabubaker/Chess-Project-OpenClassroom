from .base import BaseCommand
from .tournament_main import TournamentMainCmd


class TournamentDeleteCmd(BaseCommand):
    """Command to permanently delete a tournament"""

    def __init__(self, tournament):
        self.tournament = tournament

    def execute(self):
        """Deletes the tournament's file, then shows the tournament list so
        the user can see what's left and pick what to do next.
        """
        # The screen has already asked for confirmation, so by the time this
        # runs the decision is made. Removing the file is the whole deletion
        self.tournament.delete()
        # Deliberately not a Context("tournament-view"): the tournament no
        # longer exists, so there is nothing left to display.
        # TournamentMainCmd re-reads the folder, which is what drops the
        # deleted tournament from the list the user sees next.
        # Called directly rather than returned, because run() expects a
        # Context back from this method, not another command
        return TournamentMainCmd().execute()
