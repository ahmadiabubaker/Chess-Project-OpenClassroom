from commands import NoopCmd, TournamentMainCmd
from models import ClubManager
from models.player_search import display_name

from ..base_screen import BaseScreen


class TournamentView(BaseScreen):
    """Screen displayed when viewing/managing a tournament"""

    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        # Shortened to "t" because it is used on nearly every line below
        t = self.tournament
        print("##", t.name)
        print(f"{t.date_start} to {t.date_end}  |  {t.venue}")

        if t.completed:
            print("Status: completed")
        else:
            # "or 0" covers a tournament created but not yet started, where
            # current_round is still 0 and no round exists
            print(f"Round {t.current_round or 0} of {t.number_of_rounds}")

        print("")
        print("Players:")
        # The tournament stores chess_ids, so the names have to come from the
        # club files - one ClubManager for the whole list, not one per player
        club_manager = ClubManager()
        for idx, chess_id in enumerate(t.players, 1):
            # display_name falls back to the id if the player is no longer
            # in any club
            print(idx, display_name(club_manager, chess_id), f"({chess_id})")

    def get_command(self):
        while True:
            # The menu changes with the tournament's state: registering,
            # entering results and advancing are all meaningless once it is
            # finished, so they are not offered
            if self.tournament.completed:
                print(f"{self.tournament.name} is complete!")
                print("Type V to view the report, D to delete this tournament,")
                print("or B to go back to the main menu.")
            else:
                print("Type R to register a player, E to enter round results,")
                print("A to advance to the next round, V to view the report.")
                print("Type D to delete this tournament, or B to go back to the main menu.")

            # upper() once here, so each option below is a simple comparison
            value = self.input_string().upper()

            # These three are available whatever state the tournament is in
            if value == "B":
                # TournamentMainCmd, not TournamentListCmd: the latter would
                # re-apply the "one tournament in progress" rule and send the
                # user straight back to this screen
                return TournamentMainCmd()
            elif value == "V":
                return NoopCmd("tournament-report", tournament=self.tournament)
            elif value == "D":
                return NoopCmd("tournament-delete", tournament=self.tournament)
            elif self.tournament.completed:
                # R/E/A aren't offered once finished (see the printed menu
                # above); ignore a stray keystroke instead of matching one
                # of them by accident.
                continue
            # Only reachable while the tournament is still running. Each of
            # these just moves to another screen, carrying the tournament
            elif value == "R":
                return NoopCmd("tournament-register", tournament=self.tournament)
            elif value == "E":
                return NoopCmd("tournament-results", tournament=self.tournament)
            elif value == "A":
                return NoopCmd("tournament-advance", tournament=self.tournament)
