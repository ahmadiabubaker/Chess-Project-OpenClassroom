from commands.context import Context
from models import TournamentManager

from .base import BaseCommand


class TournamentCreateCmd(BaseCommand):
    """Command to create a tournament"""

    def __init__(self, name, venue, date_start, date_end, number_of_rounds):
        # The screen has already validated all of these - dates in the right
        # format, a whole number of rounds - so they are simply held here
        # until execute() is called
        self.name = name
        self.venue = venue
        self.date_start = date_start
        self.date_end = date_end
        self.number_of_rounds = number_of_rounds

    def execute(self):
        """Uses a TournamentManager instance to create the tournament"""
        # The manager owns the data folder, so it is what works out the file
        # name and performs the first save
        tm = TournamentManager()
        tournament = tm.create(
            self.name, self.venue, self.date_start, self.date_end, self.number_of_rounds
        )
        # Straight into the new tournament, which is where the user needs to
        # be next in order to register players
        return Context("tournament-view", tournament=tournament)
