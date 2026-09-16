from commands.context import Context

from .base import BaseCommand


class AdvanceRoundCmd(BaseCommand):
    """Command to advance a tournament to its next round (or, if the round
    just played was the last one, to close the tournament).
    """

    def __init__(self, tournament):
        self.tournament = tournament

    def execute(self):
        self.tournament.generate_next_round()
        return Context("tournament-view", tournament=self.tournament)
