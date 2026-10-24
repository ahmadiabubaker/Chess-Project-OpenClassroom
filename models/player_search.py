"""Small helpers to search for players across every club's roster.

These are kept separate from ClubManager and ChessClub (part of the given
club management program) rather than added to them, since a tournament only
needs to look players up, never to modify a club's roster.
"""


def all_players(club_manager):
    """Yields every player across every club managed by club_manager."""

    # A generator rather than a list: callers either loop over it once or wrap
    # it in list() themselves, so there is no reason to build the list here.
    # "yield from" hands back each player of each club in turn, flattening the
    # clubs-of-players structure into a single stream of players
    for club in club_manager.clubs:
        yield from club.players


def find_by_chess_id(club_manager, chess_id):
    """Returns the Player with the given chess_id, or None if not found."""

    # Chess IDs are unique across the federation, so the first match is the
    # only match and we can stop looking as soon as we find it
    for player in all_players(club_manager):
        if player.chess_id == chess_id:
            return player

    # None rather than an exception: failing to find a player is a normal
    # outcome here (the user may type an ID that does not exist), and the
    # callers fall back to displaying the raw chess_id
    return None


def display_name(club_manager, chess_id):
    """Returns the name of the player with the given chess_id, falling back
    to the raw id if they can't be found in any club roster.
    """

    # The fallback matters: a tournament stores chess_ids, so a player who has
    # since been removed from their club would otherwise break the screen or
    # the report. Showing the bare id is less useful than a name, but it is
    # still correct
    player = find_by_chess_id(club_manager, chess_id)
    return player.name if player else chess_id


def search_by_name(club_manager, query):
    """Returns every player whose name contains query, case-insensitively."""

    # Lower-cased once here, and on each name below, so that "smith", "Smith"
    # and "SMITH" all match. The spec asks for a search on *part* of the name,
    # which is why this is "in" rather than "==" or startswith()
    query = query.lower()
    return [player for player in all_players(club_manager) if query in player.name.lower()]
