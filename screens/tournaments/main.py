from commands import ExitCmd, NoopCmd

from ..base_screen import BaseScreen


class TournamentMain(BaseScreen):
    """Main screen: lists tournaments (sorted by start date, descending),
    or lets the user create a new one.
    """

    def __init__(self, tournaments):
        self.tournaments = tournaments

    def display(self):
        if not self.tournaments:
            print("No tournaments yet.")
            return

        for idx, t in enumerate(self.tournaments, 1):
            status = "completed" if t.completed else f"round {t.current_round}/{t.number_of_rounds}"
            print(idx, t.name, f"({t.date_start})", f"- {status}")

    def get_command(self):
        while True:
            print("Type C to create a tournament or a tournament number to view/manage it.")
            print("Type X to exit.")
            value = self.input_string()
            if value.isdigit():
                value = int(value)
                if value in range(1, len(self.tournaments) + 1):
                    return NoopCmd("tournament-view", tournament=self.tournaments[value - 1])
            elif value.upper() == "C":
                return NoopCmd("tournament-create")
            elif value.upper() == "X":
                return ExitCmd()
