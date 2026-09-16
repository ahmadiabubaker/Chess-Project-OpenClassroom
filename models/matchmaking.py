import random


def generate_pairings(tournament):
    """Generates the pairings for the next round of a tournament.

    Round 1 pairings are randomized. Every round after that pairs players
    by their current standings (highest points first), trying to avoid a
    match that has already been played when another opponent is available -
    see notes/matchmaking.md for the rules this follows.
    """

    if len(tournament.players) % 2 != 0:
        raise ValueError("An even number of players is required to generate pairings!")

    if not tournament.rounds:
        pool = list(tournament.players)
        random.shuffle(pool)
    else:
        pool = _standings_with_random_tiebreak(tournament)

    pairs = []
    while pool:
        player = pool.pop(0)
        opponent = _pick_opponent(tournament, player, pool)
        pool.remove(opponent)
        pairs.append((player, opponent))

    return pairs


def _standings_with_random_tiebreak(tournament):
    """Sorts players by tournament points (descending). Players are shuffled
    first so that, since sorted() is stable, players tied on points end up
    in a random relative order - matching the spec's "if two players have
    the same number of points, randomly pick one" rule.
    """

    players = list(tournament.players)
    random.shuffle(players)
    return sorted(players, key=tournament.points_for, reverse=True)


def _pick_opponent(tournament, player, pool):
    """Picks an opponent for a player from the remaining pool: the first
    one they haven't already played, or - if every remaining player is a
    repeat - simply the next one in line.
    """

    for candidate in pool:
        if not _already_played(tournament, player, candidate):
            return candidate

    return pool[0]


def _already_played(tournament, player_a, player_b):
    """Returns True if the two players have already faced each other in an
    earlier round of this tournament.
    """

    for round_ in tournament.rounds:
        for match in round_.matches:
            if player_a in match.players and player_b in match.players:
                return True

    return False
