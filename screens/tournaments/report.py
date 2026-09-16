from commands import NoopCmd
from models.report import build_report

from ..base_screen import BaseScreen


class TournamentReport(BaseScreen):
    """Screen displayed when viewing a tournament's report"""

    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        return build_report(self.tournament)

    def get_command(self):
        while True:
            print("Type B to go back.")
            if self.input_string().upper() == "B":
                return NoopCmd("tournament-view", tournament=self.tournament)
