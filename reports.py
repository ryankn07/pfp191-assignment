"""Create match history, rankings and text reports."""

import os

from data_manager import DataError


def calculate_statistics(players, matches):
    results = {}
    for player in players:
        results[player["id"]] = {
            "name": player["name"],
            "matches": 0,
            "wins": 0,
            "losses": 0,
            "shots": 0,
            "hits": 0,
        }

    for match in matches:
        for player_id in (match.get("player1_id"), match.get("player2_id")):
            if player_id not in results:
                continue
            result = results[player_id]
            result["matches"] += 1
            if match.get("winner_id") == player_id:
                result["wins"] += 1
            else:
                result["losses"] += 1
            game_stats = match.get("stats", {}).get(str(player_id), {})
            result["shots"] += game_stats.get("shots", 0)
            result["hits"] += game_stats.get("hits", 0)

    ranking = list(results.values())
    ranking.sort(
        key=lambda item: (
            -item["wins"],
            -(item["hits"] / item["shots"] if item["shots"] else 0),
            item["name"].lower(),
        )
    )
    return ranking


def percent(part, total):
    if total == 0:
        return 0.0
    return part / total * 100


def report_text(players, matches):
    lines = ["BATTLESHIP - PLAYER STATISTICS", "=" * 52]
    lines.append("Total completed matches: " + str(len(matches)))
    lines.append("")
    lines.append("NAME                MATCH  WIN  LOSS  HIT%   WIN%")
    lines.append("-" * 52)
    for result in calculate_statistics(players, matches):
        hit_rate = percent(result["hits"], result["shots"])
        win_rate = percent(result["wins"], result["matches"])
        lines.append(
            f"{result['name'][:19]:<19} {result['matches']:>5} "
            f"{result['wins']:>4} {result['losses']:>5} "
            f"{hit_rate:>5.1f} {win_rate:>6.1f}"
        )
    return "\n".join(lines)


def history_text(matches):
    if not matches:
        return "No matches have been played yet."
    lines = ["=== MATCH HISTORY (LATEST 10) ==="]
    for match in matches[-10:]:
        lines.append(
            f"#{match['match_id']}  {match['played_at']} | "
            f"{match['player1_name']} vs {match['player2_name']} | "
            f"Winner: {match['winner_name']}"
        )
    return "\n".join(lines)


def report_menu(manager, storage):
    try:
        matches = storage.load_matches()
    except DataError as error:
        print("Cannot read match history:", error)
        return

    while True:
        print("\n=== REPORTS ===")
        print("1. Player rankings and statistics")
        print("2. Match history")
        print("3. Export report to text file")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            print(report_text(manager.all_players(), matches))
        elif choice == "2":
            print(history_text(matches))
        elif choice == "3":
            file_path = os.path.join(storage.folder, "report.txt")
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(report_text(manager.all_players(), matches))
                    file.write("\n\n")
                    file.write(history_text(matches))
                print("Report exported to:", file_path)
            except OSError as error:
                print("Cannot export report:", error)
        elif choice == "0":
            return
        else:
            print("Invalid menu option.")
