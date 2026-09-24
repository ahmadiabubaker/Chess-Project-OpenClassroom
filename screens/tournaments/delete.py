from commands import NoopCmd, TournamentDeleteCmd

from ..base_screen import BaseScreen


class DeleteTournament(BaseScreen):
    """Screen displayed when confirming permanent deletion of a tournament"""

    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print("## Delete tournament -", self.tournament.name)

    def get_command(self):
        print("This cannot be undone. Delete", self.tournament.name, "? (Y/N)")
        value = self.input_string().upper()
        if value == "Y":
            return TournamentDeleteCmd(self.tournament)

        return NoopCmd("tournament-view", tournament=self.tournament)
