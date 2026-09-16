class Round:
    """One round of a tournament: a numbered list of matches played at the
    same time.

    A round doesn't track its own 'completed' status as a separate stored
    value - it's derived from its matches instead, so it can never drift out
    of sync with them (there is no flag to forget to update).
    """

    def __init__(self, number, matches=None):
        self.number = number
        self.matches = list(matches) if matches else []

    def __str__(self):
        return f"<Round {self.number}>"

    @property
    def completed(self):
        """A round is complete once it has matches, and every match in it
        has a result."""

        return bool(self.matches) and all(match.completed for match in self.matches)

    def score_for(self, chess_id):
        """Returns the points a player earned in this round."""

        return sum(
            match.score_for(chess_id)
            for match in self.matches
            if chess_id in match.players
        )

    def serialize(self):
        """Serialize the instance in a format compatible with JSON."""

        return {
            "number": self.number,
            "matches": [match.serialize() for match in self.matches],
        }
