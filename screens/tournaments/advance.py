from commands import AdvanceRoundCmd, NoopCmd

from ..base_screen import BaseScreen


class AdvanceRound(BaseScreen):
    """Screen displayed when confirming advancement to the next round"""

    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print("## Advance round -", self.tournament.name)

    def get_command(self):
        t = self.tournament

        if t.completed:
            print(f"{t.name} has already been completed.")
            return NoopCmd("tournament-view", tournament=t)

        if t.rounds and not t.rounds[-1].completed:
            print("This round's results haven't all been entered yet.")
            return NoopCmd("tournament-view", tournament=t)

        # Confirming from here on will generate a brand new round (rather
        # than close the tournament), which needs an even number of
        # registered players.
        about_to_close = t.rounds and len(t.rounds) == t.number_of_rounds
        if not about_to_close and len(t.players) % 2 != 0:
            print("An even number of players must be registered to start a round.")
            return NoopCmd("tournament-view", tournament=t)

        if not t.rounds:
            question = "Are you sure you want to start round 1?"
        else:
            question = "Are you sure you want to advance to the next round?"

        print(question, "(Y/N)")
        value = self.input_string().upper()
        if value == "Y":
            return AdvanceRoundCmd(t)

        return NoopCmd("tournament-view", tournament=t)
