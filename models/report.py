from models.club_manager import ClubManager
from models.player_search import find_by_chess_id


def _player_name(club_manager, chess_id):
    """Looks up a player's display name from their chess_id, falling back
    to the raw id if they can't be found in any club roster.
    """

    # The fallback matters: a tournament stores chess_ids, so a player who has
    # since been removed from their club would otherwise break the report.
    # Showing the bare id is less useful than a name, but it is still correct
    player = find_by_chess_id(club_manager, chess_id)
    return player.name if player else chess_id


def build_report(tournament):
    """Builds a plain-text report for a tournament: its name and dates, the
    standings (points descending), and the full round-by-round match
    history - per the spec's Tournament Reports section.
    """

    # One ClubManager for the whole report, rather than re-reading the club
    # files for every single name looked up below
    club_manager = ClubManager()
    # The report is built as a list of lines and joined at the end, which is
    # cheaper than repeatedly adding strings together and makes the shape of
    # the finished page easy to see here
    lines = [
        tournament.name,
        f"{tournament.date_start} to {tournament.date_end}  |  {tournament.venue}",
        "",
        "STANDINGS",
    ]

    # standings() has already sorted the players by points, so enumerate()
    # starting at 1 gives each of them their rank
    for rank, chess_id in enumerate(tournament.standings(), 1):
        name = _player_name(club_manager, chess_id)
        points = tournament.points_for(chess_id)
        lines.append(f"  {rank}. {name} ({chess_id}) - {points} pts")

    lines.append("")
    lines.append("ROUNDS")

    # A tournament that has been created but not started still gets a report,
    # so say so rather than printing an empty heading
    if not tournament.rounds:
        lines.append("  No rounds played yet.")

    for round_ in tournament.rounds:
        lines.append(f"  Round {round_.number}")
        for match in round_.matches:
            name1 = _player_name(club_manager, match.players[0])
            name2 = _player_name(club_manager, match.players[1])
            score1, score2 = match.scores

            # An unplayed match also has equal scores (0-0), so it has to be
            # checked before the tie, or it would be reported as a draw
            if not match.completed:
                result = "not yet played"
            elif score1 == score2:
                result = "tie"
            else:
                # Not a draw, so the higher score identifies the winner
                result = f"{name1 if score1 > score2 else name2} wins"

            lines.append(f"    {name1} vs {name2}  -  {result}")

    # One string, ready for the screen to print in a single call
    return "\n".join(lines)
