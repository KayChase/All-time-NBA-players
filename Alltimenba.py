# All-Time NBA Players Ranking Manager
# Demonstrates: Linear Search, Selection Sort, Insert, Update, Delete, and user interaction.

from dataclasses import dataclass

@dataclass
class Player:
    name: str
    rings: int
    mvps: int
    points: int         # career points (approximate, for demo)
    position: str

def seed_players():
    # Sample starting list (you can adjust values as you like)
    return [
        Player("Michael Jordan", 6, 5, 32292, "SG"),
        Player("LeBron James", 4, 4, 40000, "SF"),
        Player("Kareem Abdul-Jabbar", 6, 6, 38387, "C"),
        Player("Magic Johnson", 5, 3, 17707, "PG"),
        Player("Larry Bird", 3, 3, 21791, "SF"),
        Player("Wilt Chamberlain", 2, 4, 31419, "C"),
        Player("Shaquille O'Neal", 4, 1, 28596, "C"),
        Player("Tim Duncan", 5, 2, 26496, "PF"),
        Player("Kobe Bryant", 5, 1, 33643, "SG"),
        Player("Hakeem Olajuwon", 2, 1, 26946, "C"),
        Player("Bill Russell", 11, 5, 14522, "C"),
        Player("Stephen Curry", 4, 2, 23000, "PG"),
        Player("Kevin Durant", 2, 1, 28000, "SF"),
        Player("Giannis Antetokounmpo", 1, 2, 17000, "PF"),
    ]

# ---------- Algorithms ----------

def selection_sort(players, key_func, descending=True):
    """
    Classic Selection Sort to make algorithmic steps explicit.
    Time: O(n^2), Space: O(1) extra.
    """
    n = len(players)
    for i in range(n - 1):
        best = i
        for j in range(i + 1, n):
            a = key_func(players[j])
            b = key_func(players[best])
            if descending:
                if a > b:
                    best = j
            else:
                if a < b:
                    best = j
        if best != i:
            players[i], players[best] = players[best], players[i]
    return players

def linear_search_by_name(players, query):
    """
    Linear Search: collect all indices whose name contains the query (case-insensitive).
    Time: O(n).
    """
    q = query.strip().lower()
    hits = []
    for i, p in enumerate(players):
        if q in p.name.lower():
            hits.append(i)
    return hits

# ---------- Helpers ----------

def display_table(players):
    if not players:
        print("\n[Empty list]\n")
        return
    print("\nCurrent Ranking")
    print("-" * 80)
    print(f"{'Idx':>3}  {'Name':<24} {'Rings':>5} {'MVPs':>5} {'Points':>8}  {'Pos':<3}")
    print("-" * 80)
    for i, p in enumerate(players):
        print(f"{i:>3}  {p.name:<24} {p.rings:>5} {p.mvps:>5} {p.points:>8}  {p.position:<3}")
    print("-" * 80)

def read_int(prompt, low=None, high=None):
    while True:
        s = input(prompt).strip()
        try:
            val = int(s)
            if low is not None and val < low:
                print(f"  (!) Enter >= {low}.")
                continue
            if high is not None and val > high:
                print(f"  (!) Enter <= {high}.")
                continue
            return val
        except ValueError:
            print("  (!) Please enter an integer.")

def read_nonempty(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("  (!) Cannot be empty.")

def key_selector_menu():
    print("\nSort by which metric?")
    print(" 1) Rings (desc)")
    print(" 2) MVPs  (desc)")
    print(" 3) Points (desc)")
    print(" 4) Name (A→Z)")
    print(" 5) Composite score (desc)  [5*rings + 3*mvps + points/10000]")
    choice = input("Choose 1-5: ").strip()
    if choice == "1":
        return (lambda p: p.rings, True, "rings")
    elif choice == "2":
        return (lambda p: p.mvps, True, "mvps")
    elif choice == "3":
        return (lambda p: p.points, True, "points")
    elif choice == "4":
        return (lambda p: p.name.lower(), False, "name")
    else:
        # Composite favors championships + MVPs and lightly scales points.
        return (lambda p: 5*p.rings + 3*p.mvps + p.points/10000.0, True, "composite")

# ---------- CRUD operations ----------

def insert_player(players):
    print("\nInsert New Player")
    name = read_nonempty("Name: ")
    rings = read_int("Rings: ", 0)
    mvps = read_int("MVPs: ", 0)
    points = read_int("Career points (approx ok): ", 0)
    position = read_nonempty("Position (PG/SG/SF/PF/C): ").upper()
    idx = read_int(f"Insert at index (0..{len(players)}): ", 0, len(players))
    players.insert(idx, Player(name, rings, mvps, points, position))
    print("Inserted.")

def update_player(players):
    if not players:
        print("List empty; nothing to update.")
        return
    display_table(players)
    idx = read_int(f"Choose index to update (0..{len(players)-1}): ", 0, len(players)-1)
    p = players[idx]
    print(f"\nEditing {p.name}:")
    print(" 1) Name")
    print(" 2) Rings")
    print(" 3) MVPs")
    print(" 4) Points")
    print(" 5) Position")
    field = input("Choose 1-5: ").strip()
    if field == "1":
        p.name = read_nonempty("New name: ")
    elif field == "2":
        p.rings = read_int("New rings: ", 0)
    elif field == "3":
        p.mvps = read_int("New MVPs: ", 0)
    elif field == "4":
        p.points = read_int("New points: ", 0)
    elif field == "5":
        p.position = read_nonempty("New position: ").upper()
    else:
        print("No change.")
        return
    print("Updated.")

def delete_player(players):
    if not players:
        print("List empty; nothing to delete.")
        return
    mode = (input("Delete by (I)ndex or exact (N)ame? [I]: ").strip().lower() or "i")
    if mode.startswith("n"):
        name = read_nonempty("Exact name to delete: ")
        for i, p in enumerate(players):
            if p.name == name:
                players.pop(i)
                print(f"Deleted {name}.")
                return
        print("Name not found; nothing deleted.")
    else:
        display_table(players)
        idx = read_int(f"Index to delete (0..{len(players)-1}): ", 0, len(players)-1)
        removed = players.pop(idx)
        print(f"Deleted {removed.name} at index {idx}.")

# ---------- Main loop ----------

def show_menu():
    print("\n=== All-Time NBA Ranking Manager ===")
    print(" 1) Show current ranking")
    print(" 2) Search player by name (Linear Search)")
    print(" 3) Sort ranking (Selection Sort)")
    print(" 4) Insert new player at index")
    print(" 5) Update a player’s field")
    print(" 6) Delete a player (by index or exact name)")
    print(" 0) Quit")

def main():
    players = seed_players()
    # Default: sort by composite so the initial table looks like a ranking
    key_func, desc, label = key_selector_menu()  # or choose a default silently
    selection_sort(players, key_func, descending=desc)
    print(f"\n(Pre-sorted by {label})")
    display_table(players)

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_table(players)

        elif choice == "2":
            q = read_nonempty("Search name (substring ok): ")
            hits = linear_search_by_name(players, q)
            if not hits:
                print("No matches.")
            else:
                print(f"Found {len(hits)} match(es) at indices: {hits}")
                # Show matched rows
                for i in hits:
                    p = players[i]
                    print(f"  [{i}] {p.name} | Rings={p.rings}, MVPs={p.mvps}, Pts={p.points}, Pos={p.position}")

        elif choice == "3":
            key_func, desc, label = key_selector_menu()
            selection_sort(players, key_func, descending=desc)
            print(f"Sorted by {label} ({'desc' if desc else 'asc'}).")
            display_table(players)

        elif choice == "4":
            insert_player(players)
            display_table(players)

        elif choice == "5":
            update_player(players)
            display_table(players)

        elif choice == "6":
            delete_player(players)
            display_table(players)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 0–6.")

if __name__ == "__main__":
    main()
