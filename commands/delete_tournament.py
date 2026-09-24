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
        self.tournament.delete()
        return TournamentMainCmd().execute()
