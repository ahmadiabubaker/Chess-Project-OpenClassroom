from commands.context import Context

from .base import BaseCommand


class PlayerRegisterCmd(BaseCommand):
    """Command to register a player for a tournament"""

    def __init__(self, tournament, player):
        # The whole Player object is taken rather than just an id, so the
        # screen can hand over exactly what the user picked from the list
        self.tournament = tournament
        self.player = player

    def execute(self):
        """Registers the player's chess_id and saves the tournament"""
        # Only the chess_id is stored: the club file remains the owner of the
        # player's actual details, so a name or email corrected later in
        # manage_clubs.py is picked up by the tournament automatically.
        # register_player() enforces the rules and saves the file itself
        self.tournament.register_player(self.player.chess_id)
        return Context("tournament-view", tournament=self.tournament)
