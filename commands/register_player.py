from commands.context import Context

from .base import BaseCommand


class PlayerRegisterCmd(BaseCommand):
    """Command to register a player for a tournament"""

    def __init__(self, tournament, player):
        self.tournament = tournament
        self.player = player

    def execute(self):
        """Registers the player's chess_id and saves the tournament"""
        self.tournament.register_player(self.player.chess_id)
        return Context("tournament-view", tournament=self.tournament)
