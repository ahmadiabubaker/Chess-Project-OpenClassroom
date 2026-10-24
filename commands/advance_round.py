from commands.context import Context

from .base import BaseCommand


class AdvanceRoundCmd(BaseCommand):
    """Command to advance a tournament to its next round (or, if the round
    just played was the last one, to close the tournament).
    """

    def __init__(self, tournament):
        self.tournament = tournament

    def execute(self):
        # The model decides whether this pairs a new round or closes the
        # tournament, depending on how many rounds have been played - the
        # command only has to ask. generate_next_round() saves the file itself
        self.tournament.generate_next_round()
        # Either way the user goes back to the tournament, which will now show
        # the new round, or that the tournament has finished
        return Context("tournament-view", tournament=self.tournament)
