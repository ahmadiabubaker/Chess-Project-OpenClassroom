from commands import NoopCmd, TournamentDeleteCmd

from ..base_screen import BaseScreen


class DeleteTournament(BaseScreen):
    """Screen displayed when confirming permanent deletion of a tournament"""

    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print("## Delete tournament -", self.tournament.name)

    def get_command(self):
        # A whole screen for one question, because deleting removes the JSON
        # file outright - there is no undo and no copy kept anywhere.
        # The name is repeated in the prompt so the user can see exactly
        # which tournament they are about to lose
        print("This cannot be undone. Delete", self.tournament.name, "? (Y/N)")
        value = self.input_string().upper()
        if value == "Y":
            return TournamentDeleteCmd(self.tournament)

        # Anything other than an explicit Y cancels and goes back untouched -
        # for a destructive action, the safe answer has to be the default
        return NoopCmd("tournament-view", tournament=self.tournament)
