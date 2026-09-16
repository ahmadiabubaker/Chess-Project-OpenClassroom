from models.club_manager import ClubManager
from models.player_search import find_by_chess_id


def _player_name(club_manager, chess_id):
    """Looks up a player's display name from their chess_id, falling back
    to the raw id if they can't be found in any club roster.
    """

    player = find_by_chess_id(club_manager, chess_id)
    return player.name if player else chess_id


def build_report(tournament):
    """Builds a plain-text report for a tournament: its name and dates, the
    standings (points descending), and the full round-by-round match
    history - per the spec's Tournament Reports section.
    """

    club_manager = ClubManager()
    lines = [
        tournament.name,
        f"{tournament.date_start} to {tournament.date_end}  |  {tournament.venue}",
        "",
        "STANDINGS",
    ]

    for rank, chess_id in enumerate(tournament.standings(), 1):
        name = _player_name(club_manager, chess_id)
        points = tournament.points_for(chess_id)
        lines.append(f"  {rank}. {name} ({chess_id}) - {points} pts")

    lines.append("")
    lines.append("ROUNDS")

    if not tournament.rounds:
        lines.append("  No rounds played yet.")

    for round_ in tournament.rounds:
        lines.append(f"  Round {round_.number}")
        for match in round_.matches:
            name1 = _player_name(club_manager, match.players[0])
            name2 = _player_name(club_manager, match.players[1])
            score1, score2 = match.scores

            if not match.completed:
                result = "not yet played"
            elif score1 == score2:
                result = "tie"
            else:
                result = f"{name1 if score1 > score2 else name2} wins"

            lines.append(f"    {name1} vs {name2}  -  {result}")

    return "\n".join(lines)
