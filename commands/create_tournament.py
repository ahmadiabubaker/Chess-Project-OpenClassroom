from commands.context import Context
from models import TournamentManager

from .base import BaseCommand


class TournamentCreateCmd(BaseCommand):
    """Command to create a tournament"""

    def __init__(self, name, venue, date_start, date_end, number_of_rounds):
        self.name = name
        self.venue = venue
        self.date_start = date_start
        self.date_end = date_end
        self.number_of_rounds = number_of_rounds

    def execute(self):
        """Uses a TournamentManager instance to create the tournament"""
        tm = TournamentManager()
        tournament = tm.create(
            self.name, self.venue, self.date_start, self.date_end, self.number_of_rounds
        )
        return Context("tournament-view", tournament=tournament)
