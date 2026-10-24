from commands import TournamentListCmd
from screens.tournaments import (
    AdvanceRound,
    DeleteTournament,
    EnterResults,
    PlayerRegister,
    TournamentCreate,
    TournamentMain,
    TournamentReport,
    TournamentView,
)


class App:
    """The main controller for the tournament management program"""

    # Maps the screen name carried by a Context to the class that draws it.
    # Adding a screen to the program means adding a line here and a Context
    # that names it - nothing else in this file has to change
    SCREENS = {
        "tournament-main": TournamentMain,
        "tournament-create": TournamentCreate,
        "tournament-view": TournamentView,
        "tournament-register": PlayerRegister,
        "tournament-results": EnterResults,
        "tournament-advance": AdvanceRound,
        "tournament-report": TournamentReport,
        "tournament-delete": DeleteTournament,
        # "exit" is never looked up: ExitCmd returns a context with run=False,
        # so the loop below stops before it would reach this entry
        "exit": False,
    }

    def __init__(self):
        # We start with the list of tournaments (= main menu)
        command = TournamentListCmd()
        self.context = command()

    def run(self):
        # The whole program is this loop: a context says which screen to
        # show, the screen returns a command, the command returns the next
        # context. It ends when a command returns one with run=False
        while self.context.run:
            # Get the screen class from the mapping
            screen = self.SCREENS[self.context.screen]
            try:
                # Run the screen and get the command. The context's kwargs
                # are unpacked into the screen's constructor, which is how
                # data - a tournament, a list of them - reaches the screen
                command = screen(**self.context.kwargs).run()
                # Run the command and get a context back
                self.context = command()
            except KeyboardInterrupt:
                # Ctrl-C
                print("Bye!")
                self.context.run = False


if __name__ == "__main__":
    # Only runs when the file is executed directly, per the spec's
    # "python <program name>.py" requirement - not when it is imported
    app = App()
    app.run()
