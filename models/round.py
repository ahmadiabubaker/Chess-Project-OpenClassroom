class Round:
    """One round of a tournament: a numbered list of matches played at the
    same time.

    A round doesn't track its own 'completed' status as a separate stored
    value - it's derived from its matches instead, so it can never drift out
    of sync with them (there is no flag to forget to update).
    """

    def __init__(self, number, matches=None):
        # The number is the round's position in the tournament (1, 2, 3...),
        # which is what the screens and the report display
        self.number = number
        # Copied into a new list so the caller's list - including the one that
        # came out of the JSON file - cannot be modified from under us
        self.matches = list(matches) if matches else []

    def __str__(self):
        return f"<Round {self.number}>"

    @property
    def completed(self):
        """A round is complete once it has matches, and every match in it
        has a result."""

        # A property, not a stored attribute, so it is recalculated on every
        # read and can never disagree with the matches it describes.
        # bool(self.matches) matters: an empty round is unplayed, not finished,
        # and all() on an empty list would otherwise return True
        return bool(self.matches) and all(match.completed for match in self.matches)

    def score_for(self, chess_id):
        """Returns the points a player earned in this round."""

        # sum(), not "find their one match and return it": a player can be
        # in zero matches this round (e.g. registered after this round was
        # generated), and sum() of nothing is 0 - no extra check needed.
        # The "if" also keeps Match.score_for from raising on a match this
        # player was not part of
        return sum(
            match.score_for(chess_id)
            for match in self.matches
            if chess_id in match.players
        )

    def serialize(self):
        """Serialize the instance in a format compatible with JSON."""

        # 'completed' is deliberately absent: it is derived from the matches
        # (see the property above), so storing it would only let it go stale.
        # Each match serializes itself, the same way a club serializes players
        return {
            "number": self.number,
            "matches": [match.serialize() for match in self.matches],
        }
