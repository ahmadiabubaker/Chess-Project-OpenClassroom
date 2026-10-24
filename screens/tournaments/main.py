from commands import ExitCmd, NoopCmd

from ..base_screen import BaseScreen


class TournamentMain(BaseScreen):
    """Main screen: lists tournaments (sorted by start date, descending),
    or lets the user create a new one.
    """

    def __init__(self, tournaments):
        # The list arrives ready to display: the command that built this
        # context has already sorted it. A screen never reads the data files
        self.tournaments = tournaments

    def display(self):
        # An empty data folder is normal the first time the program is run,
        # and also happens once every tournament has been deleted
        if not self.tournaments:
            print("No tournaments yet.")
            return

        # enumerate() starting at 1 produces the numbers the user types to
        # pick a tournament, so the list and the prompt below agree
        for idx, t in enumerate(self.tournaments, 1):
            # A finished tournament has no current round left to show
            status = "completed" if t.completed else f"round {t.current_round}/{t.number_of_rounds}"
            print(idx, t.name, f"({t.date_start})", f"- {status}")

    def get_command(self):
        # Loops until the user types something valid: an unrecognised entry
        # simply reprints the options rather than crashing or exiting
        while True:
            print("Type C to create a tournament or a tournament number to view/manage it.")
            print("Type X to exit.")
            value = self.input_string()
            if value.isdigit():
                value = int(value)
                # range() guards against a number outside the list, so "99"
                # falls through and the options are shown again
                if value in range(1, len(self.tournaments) + 1):
                    # -1 converts the displayed number back to a list index
                    return NoopCmd("tournament-view", tournament=self.tournaments[value - 1])
            # upper() so that "c" and "C" both work
            elif value.upper() == "C":
                return NoopCmd("tournament-create")
            elif value.upper() == "X":
                return ExitCmd()
