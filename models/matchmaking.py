import random


def generate_pairings(tournament):
    """Generates the pairings for the next round of a tournament.

    Round 1 pairings are randomized. Every round after that pairs players
    by their current standings (highest points first), trying to avoid a
    match that has already been played when another opponent is available -
    see notes/matchmaking.md for the rules this follows.
    """

    # Everybody must have an opponent. There is no "bye" in the rules we were
    # given, so an odd roster is refused here rather than silently leaving
    # somebody out. AdvanceRound checks this first so the user gets a message
    if len(tournament.players) % 2 != 0:
        raise ValueError("An even number of players is required to generate pairings!")

    # No rounds played yet = round 1, where nobody has points to sort by, so
    # the spec says to pair players at random
    if not tournament.rounds:
        pool = list(tournament.players)
        random.shuffle(pool)
    else:
        # Every round after the first is driven by the current standings
        pool = _standings_with_random_tiebreak(tournament)

    # Walk down the pool taking the top player each time and finding them an
    # opponent. Both are removed from the pool, so each player is paired once
    # and the loop ends when the pool runs out
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

    # The shuffle is what implements the random tiebreak: a stable sort keeps
    # equal-scoring players in the order it found them, so randomising that
    # order first means ties are broken randomly, with no special-case code
    players = list(tournament.players)
    random.shuffle(players)
    return sorted(players, key=tournament.points_for, reverse=True)


def _pick_opponent(tournament, player, pool):
    """Picks an opponent for a player from the remaining pool: the first
    one they haven't already played, or - if every remaining player is a
    repeat - simply the next one in line.
    """

    # The pool is in standings order, so the first player who is not a repeat
    # is also the highest-ranked available opponent
    for candidate in pool:
        if not _already_played(tournament, player, candidate):
            return candidate

    # Everybody left has been played before. The spec only asks the system to
    # *try* to avoid repeats, so we take the closest-ranked player instead of
    # refusing to build the round
    return pool[0]


def _already_played(tournament, player_a, player_b):
    """Returns True if the two players have already faced each other in an
    earlier round of this tournament.
    """

    # Scanning every past match is a handful of comparisons even for a long
    # tournament, so there is nothing to gain from caching the answer
    for round_ in tournament.rounds:
        for match in round_.matches:
            # Order does not matter: a match stores its two players in
            # whichever order they happened to be paired
            if player_a in match.players and player_b in match.players:
                return True

    return False
