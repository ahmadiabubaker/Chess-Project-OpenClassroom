from commands import NoopCmd, PlayerRegisterCmd
from models import ClubManager
from models.player_search import all_players, find_by_chess_id, search_by_name

from ..base_screen import BaseScreen


class PlayerRegister(BaseScreen):
    """Screen displayed when registering a player for a tournament"""

    def __init__(self, tournament):
        self.tournament = tournament
        # Built once for the whole screen: the user may search several times
        # before picking somebody, and every search reads this same roster
        self.club_manager = ClubManager()

    def display(self):
        print("## Register a player -", self.tournament.name)

    def get_command(self):
        # Mirrors the same rule Tournament.register_player() enforces, so
        # the user gets a clear message here instead of a raised error.
        if self.tournament.rounds:
            print(f"{self.tournament.name} has already started - no new players can be registered.")
            return NoopCmd("tournament-view", tournament=self.tournament)

        # Loops so the user can search as many times as they like before
        # choosing somebody, or give up and go back
        while True:
            print("Type L to list every player, I to search by chess ID,")
            print("N to search by name, or B to go back.")
            value = self.input_string().upper()

            if value == "B":
                return NoopCmd("tournament-view", tournament=self.tournament)
            elif value == "L":
                # Every player in every club. all_players() is a generator,
                # so it is wrapped in list() to be displayed and indexed
                candidates = list(all_players(self.club_manager))
            elif value == "I":
                # input_chess_id enforces the XXNNNNN format before searching
                chess_id = self.input_chess_id(prompt="Chess ID")
                player = find_by_chess_id(self.club_manager, chess_id)
                # Wrapped in a list so all three branches hand the same kind
                # of value to _pick_player() below
                candidates = [player] if player else []
            elif value == "N":
                query = self.input_string(prompt="Name contains", empty=True)
                candidates = search_by_name(self.club_manager, query)
            else:
                # Unrecognised input: show the options again
                continue

            command = self._pick_player(candidates)
            # None means "nothing chosen", so loop round and search again
            if command:
                return command

    def _pick_player(self, candidates):
        """Displays the candidate players and lets the user register one
        of them - returns None to go back to the search options.
        """

        if not candidates:
            print("No matching player found.")
            return None

        # Numbered from 1, matching the prompt below
        for idx, player in enumerate(candidates, 1):
            print(idx, player.name, player.chess_id)

        print("Type a number to register that player, or anything else to search again.")
        value = self.input_string()
        # The range() check keeps a number outside the list from being used
        # as an index; -1 converts the displayed number back to a position
        if value.isdigit() and int(value) in range(1, len(candidates) + 1):
            return PlayerRegisterCmd(self.tournament, candidates[int(value) - 1])

        # Anything else is treated as "search again" rather than an error,
        # which gives the user a way out of a long list
        return None
