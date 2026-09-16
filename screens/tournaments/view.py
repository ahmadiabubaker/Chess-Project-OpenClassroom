from commands import NoopCmd, TournamentListCmd
from models import ClubManager
from models.player_search import find_by_chess_id

from ..base_screen import BaseScreen


class TournamentView(BaseScreen):
    """Screen displayed when viewing/managing a tournament"""

    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        t = self.tournament
        print("##", t.name)
        print(f"{t.date_start} to {t.date_end}  |  {t.venue}")

        if t.completed:
            print("Status: completed")
        else:
            print(f"Round {t.current_round or 0} of {t.number_of_rounds}")

        print("")
        print("Players:")
        club_manager = ClubManager()
        for idx, chess_id in enumerate(t.players, 1):
            player = find_by_chess_id(club_manager, chess_id)
            label = player.name if player else chess_id
            print(idx, label, f"({chess_id})")

    def get_command(self):
        while True:
            print("Type R to register a player, E to enter round results,")
            print("A to advance to the next round, V to view the report.")
            print("Type B to go back to the main menu.")
            value = self.input_string().upper()

            if value == "B":
                return TournamentListCmd()
            elif value == "R":
                return NoopCmd("tournament-register", tournament=self.tournament)
            elif value == "E":
                return NoopCmd("tournament-results", tournament=self.tournament)
            elif value == "A":
                return NoopCmd("tournament-advance", tournament=self.tournament)
            elif value == "V":
                return NoopCmd("tournament-report", tournament=self.tournament)
