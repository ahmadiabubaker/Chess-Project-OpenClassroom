"""Small helpers to search for players across every club's roster.

These are kept separate from ClubManager and ChessClub (part of the given
club management program) rather than added to them, since a tournament only
needs to look players up, never to modify a club's roster.
"""


def all_players(club_manager):
    """Yields every player across every club managed by club_manager."""

    for club in club_manager.clubs:
        yield from club.players


def find_by_chess_id(club_manager, chess_id):
    """Returns the Player with the given chess_id, or None if not found."""

    for player in all_players(club_manager):
        if player.chess_id == chess_id:
            return player

    return None


def search_by_name(club_manager, query):
    """Returns every player whose name contains query, case-insensitively."""

    query = query.lower()
    return [player for player in all_players(club_manager) if query in player.name.lower()]
