"""The tournament screens, re-exported so castle_chess.py can import them
all from one place (the club screens do the same in screens/__init__.py).
"""

from .advance import AdvanceRound
from .create import TournamentCreate
from .delete import DeleteTournament
from .main import TournamentMain
from .register import PlayerRegister
from .report import TournamentReport
from .results import EnterResults
from .view import TournamentView

# The names this package exports. It is also what tells flake8 the imports
# above are deliberate, since nothing else in this file uses them
__all__ = [
    "AdvanceRound",
    "TournamentCreate",
    "DeleteTournament",
    "TournamentMain",
    "PlayerRegister",
    "TournamentReport",
    "EnterResults",
    "TournamentView",
]
