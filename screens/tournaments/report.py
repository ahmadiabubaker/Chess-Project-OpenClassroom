from commands import NoopCmd
from models.report import build_report

from ..base_screen import BaseScreen


class TournamentReport(BaseScreen):
    """Screen displayed when viewing a tournament's report"""

    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        # The formatting lives in the model layer, so this screen only hands
        # back the finished text - BaseScreen.run() prints whatever display()
        # returns. That keeps displaying and building the report separate,
        # which is what the spec's code structure section asks for
        return build_report(self.tournament)

    def get_command(self):
        # The report is read-only, so the only thing to do here is leave.
        # This screen needs no command of its own: NoopCmd simply carries the
        # tournament back to the view screen
        while True:
            print("Type B to go back.")
            if self.input_string().upper() == "B":
                return NoopCmd("tournament-view", tournament=self.tournament)
