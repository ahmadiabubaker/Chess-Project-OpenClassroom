from commands import TournamentCreateCmd

from ..base_screen import BaseScreen


class TournamentCreate(BaseScreen):
    """Screen displayed when creating a tournament"""

    # A plain string rather than a method: BaseScreen.run() accepts either,
    # and this screen has nothing to look up before printing its title
    display = "## Create tournament"

    def get_command(self):
        # Each helper below validates as it asks, looping until the answer is
        # usable, so the command receives values it can trust.
        # empty=True means the answer cannot be left blank
        name = self.input_string(prompt="Tournament name", empty=True)
        venue = self.input_string(prompt="Venue", empty=True)
        # input_date rather than input_birthday: a tournament can be upcoming,
        # so unlike a birthday a date in the future has to be allowed here
        date_start = self.input_date(prompt="Start date (dd-mm-yyyy)")
        date_end = self.input_date(prompt="End date (dd-mm-yyyy)")
        # min_value=1 rules out a tournament with no rounds at all
        number_of_rounds = self.input_int(prompt="Number of rounds", min_value=1)

        # No confirmation step: the command, and the model behind it, is what
        # actually creates the file
        return TournamentCreateCmd(name, venue, date_start, date_end, number_of_rounds)
