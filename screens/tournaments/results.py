from commands import EnterResultsCmd, NoopCmd
from models import ClubManager
from models.player_search import find_by_chess_id

from ..base_screen import BaseScreen


class EnterResults(BaseScreen):
    """Screen displayed when entering results for the current round"""

    def __init__(self, tournament):
        self.tournament = tournament
        self.club_manager = ClubManager()

    def display(self):
        print("## Enter results -", self.tournament.name)

    def _name(self, chess_id):
        player = find_by_chess_id(self.club_manager, chess_id)
        return player.name if player else chess_id

    def get_command(self):
        if not self.tournament.rounds:
            print("No round has been generated yet.")
            return NoopCmd("tournament-view", tournament=self.tournament)

        current_round = self.tournament.rounds[-1]
        if current_round.completed:
            print("This round's results have already been entered.")
            return NoopCmd("tournament-view", tournament=self.tournament)

        results = []
        for match in current_round.matches:
            name1 = self._name(match.players[0])
            name2 = self._name(match.players[1])

            print(f"{name1} vs {name2}")
            print(f"Type 1 if {name1} won, 2 if {name2} won, or T for a tie.")
            value = self.input_string(prompt="Result").upper()
            while value not in ("1", "2", "T"):
                print("Please type 1, 2, or T.")
                value = self.input_string(prompt="Result").upper()

            if value == "T":
                results.append((None, True))
            elif value == "1":
                results.append((match.players[0], False))
            else:
                results.append((match.players[1], False))

        return EnterResultsCmd(self.tournament, results)
