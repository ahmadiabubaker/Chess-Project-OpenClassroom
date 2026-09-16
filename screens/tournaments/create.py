from commands import TournamentCreateCmd

from ..base_screen import BaseScreen


class TournamentCreate(BaseScreen):
    """Screen displayed when creating a tournament"""

    display = "## Create tournament"

    def get_command(self):
        name = self.input_string(prompt="Tournament name", empty=True)
        venue = self.input_string(prompt="Venue", empty=True)
        date_start = self.input_date(prompt="Start date (dd-mm-yyyy)")
        date_end = self.input_date(prompt="End date (dd-mm-yyyy)")
        number_of_rounds = self.input_int(prompt="Number of rounds", min_value=1)

        return TournamentCreateCmd(name, venue, date_start, date_end, number_of_rounds)
