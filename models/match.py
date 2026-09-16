class Match:
    """A single game between two players within one round of a tournament.

    A match does not store a single 'winner' field, because that cannot tell
    an unplayed match apart from a tie (both would read as None). Instead,
    each player's individual score is tracked directly, matching the
    tournament's points system (1 for a win, 0.5 each for a tie, 0 for a
    loss).
    """

    def __init__(self, players, scores=None, completed=False):
        if len(players) != 2:
            raise ValueError("A match must have exactly two players!")

        self.players = tuple(players)
        self.scores = tuple(scores) if scores else (0, 0)
        self.completed = completed

    def __str__(self):
        return f"<Match: {self.players[0]} vs {self.players[1]}>"

    def set_result(self, winner=None, tie=False):
        """Records the result of the match.

        Pass the winning player's chess_id for a decisive match, or tie=True
        if the match ended in a draw.
        """

        if tie:
            self.scores = (0.5, 0.5)
        elif winner == self.players[0]:
            self.scores = (1, 0)
        elif winner == self.players[1]:
            self.scores = (0, 1)
        else:
            raise ValueError(f"{winner} did not play in this match!")

        self.completed = True

    def score_for(self, chess_id):
        """Returns the points earned by the given player in this match."""

        if chess_id == self.players[0]:
            return self.scores[0]
        elif chess_id == self.players[1]:
            return self.scores[1]

        raise ValueError(f"{chess_id} did not play in this match!")

    def opponent_of(self, chess_id):
        """Returns the chess_id of the other player in this match."""

        if chess_id == self.players[0]:
            return self.players[1]
        elif chess_id == self.players[1]:
            return self.players[0]

        raise ValueError(f"{chess_id} did not play in this match!")

    def serialize(self):
        """Serialize the instance in a format compatible with JSON."""

        return {
            "players": list(self.players),
            "scores": list(self.scores),
            "completed": self.completed,
        }
