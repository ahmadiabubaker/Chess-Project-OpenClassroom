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

        # The checks below are the same ones Tournament.generate_next_round()
        # enforces. They are repeated here so the user gets a message and is
        # returned to the tournament, instead of the model raising at them
        if t.completed:
            print(f"{t.name} has already been completed.")
            return NoopCmd("tournament-view", tournament=t)

        # The next round's pairings depend on the current standings, so every
        # result has to be in before a new round can be built
        if t.rounds and not t.rounds[-1].completed:
            print("This round's results haven't all been entered yet.")
            return NoopCmd("tournament-view", tournament=t)

        # Confirming from here on will generate a brand new round (rather
        # than close the tournament), which needs an even number of
        # registered players.
        about_to_close = t.rounds and len(t.rounds) == t.number_of_rounds
        if not about_to_close and len(t.players) < 2:
            print("At least two players must be registered to start a round.")
            return NoopCmd("tournament-view", tournament=t)

        if not about_to_close and len(t.players) % 2 != 0:
            print("An even number of players must be registered to start a round.")
            return NoopCmd("tournament-view", tournament=t)

        # The wording changes for the first round, where "advance" would be
        # misleading - nothing has been played yet
        if not t.rounds:
            question = "Are you sure you want to start round 1?"
        else:
            question = "Are you sure you want to advance to the next round?"

        print(question, "(Y/N)")
        value = self.input_string().upper()
        if value == "Y":
            return AdvanceRoundCmd(t)

        # Anything other than Y cancels. Advancing cannot be undone - it locks
        # registration and pairs the round - so the safe answer is the default
        return NoopCmd("tournament-view", tournament=t)
