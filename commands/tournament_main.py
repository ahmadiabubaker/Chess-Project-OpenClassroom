from commands.context import Context
from models import TournamentManager

from .base import BaseCommand


class TournamentMainCmd(BaseCommand):
    """Command to show the tournament list, unconditionally.

    Unlike TournamentListCmd, this never auto-opens a sole in-progress
    tournament - it's used whenever the user explicitly navigates back to
    the main menu from inside the app, so they can always reach "create a
    new tournament" even while one is already in progress. TournamentListCmd
    is reserved for the one-time startup check described in the spec.
    """

    def execute(self):
        # Re-read from disk, so a tournament just created, completed or
        # deleted is reflected in the list the user is sent back to
        tm = TournamentManager()
        # Straight to the list screen with no in_progress() check: that check
        # is exactly what would bounce the user back where they came from
        return Context("tournament-main", tournaments=tm.sorted_by_start_date())
