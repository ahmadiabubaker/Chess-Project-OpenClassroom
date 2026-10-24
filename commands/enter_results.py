from commands.context import Context

from .base import BaseCommand


class EnterResultsCmd(BaseCommand):
    """Command to record the results of every match in the current round"""

    def __init__(self, tournament, results):
        """results is a list of (winner_chess_id_or_None, is_tie) tuples,
        one per match in the tournament's current round, in the same order.
        """
        self.tournament = tournament
        self.results = results

    def execute(self):
        """Applies each result to its match, then saves the tournament -
        this is what makes the spec's "points are automatically updated"
        rule true, since points are always computed from the matches
        directly rather than tracked separately.
        """
        # Rounds are only ever appended, so the current one is always the last
        current_round = self.tournament.rounds[-1]
        # zip() walks the matches and the collected results together, which is
        # why the screen has to return them in the order it displayed them.
        # Each tuple is unpacked straight into the arguments set_result takes
        for match, (winner, tie) in zip(current_round.matches, self.results):
            match.set_result(winner=winner, tie=tie)

        # One save for the whole round. Each set_result() above has updated
        # the objects in memory; this is the line that puts them on disk
        self.tournament.save()
        return Context("tournament-view", tournament=self.tournament)
