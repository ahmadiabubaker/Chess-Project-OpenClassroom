class Match:
    """A single game between two players within one round of a tournament.

    A match does not store a single 'winner' field, because that cannot tell
    an unplayed match apart from a tie (both would read as None). Instead,
    each player's individual score is tracked directly, matching the
    tournament's points system (1 for a win, 0.5 each for a tie, 0 for a
    loss).
    """

    def __init__(self, players, scores=None, completed=False):
        # Two players and no more: a chess match is always one against one,
        # so anything else means the caller (or the JSON file) is wrong
        if len(players) != 2:
            raise ValueError("A match must have exactly two players!")

        # Tuples rather than lists: once a match is paired its players never
        # change, and the scores are always replaced as a pair
        self.players = tuple(players)
        # No scores provided = the match has been paired but not played yet
        self.scores = tuple(scores) if scores else (0, 0)
        self.completed = completed

    def __str__(self):
        return f"<Match: {self.players[0]} vs {self.players[1]}>"

    def set_result(self, winner=None, tie=False):
        """Records the result of the match.

        Pass the winning player's chess_id for a decisive match, or tie=True
        if the match ended in a draw.
        """

        # The tie is checked first: a draw has no winner to compare against
        if tie:
            self.scores = (0.5, 0.5)
        # Otherwise the winner tells us which side of the pair gets the point.
        # The scores are stored in the same order as the players, so matching
        # the winner against each player decides which of the two gets the 1
        elif winner == self.players[0]:
            self.scores = (1, 0)
        elif winner == self.players[1]:
            self.scores = (0, 1)
        else:
            # Neither player matched, so the caller passed the wrong chess_id -
            # better to say so than to silently record a result for nobody
            raise ValueError(f"{winner} did not play in this match!")

        # Only set once a score has actually been assigned above, so a match
        # can never be marked complete without a result
        self.completed = True

    def score_for(self, chess_id):
        """Returns the points earned by the given player in this match."""

        # The players and scores tuples are parallel: position 0 in one lines
        # up with position 0 in the other
        if chess_id == self.players[0]:
            return self.scores[0]
        elif chess_id == self.players[1]:
            return self.scores[1]

        # Asking for the score of somebody who was not in this match is a bug
        # in the caller, not a zero
        raise ValueError(f"{chess_id} did not play in this match!")

    def opponent_of(self, chess_id):
        """Returns the chess_id of the other player in this match."""

        # Returns "the other one" - the matchmaking uses this to work out who
        # a player has already faced
        if chess_id == self.players[0]:
            return self.players[1]
        elif chess_id == self.players[1]:
            return self.players[0]

        raise ValueError(f"{chess_id} did not play in this match!")

    def serialize(self):
        """Serialize the instance in a format compatible with JSON."""

        # The tuples become lists because JSON has no tuple type. Reading the
        # file back gives lists again, which __init__ accepts and re-tuples
        return {
            "players": list(self.players),
            "scores": list(self.scores),
            "completed": self.completed,
        }
