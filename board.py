"""
mansion layot , room connections and movement validation
"""

ROOMS=[
    "Kitchen",
    "Ballroom",
    "Conservatory",
    "Billiard Room",
    "Library",
    "Study",
    "Hall",
    "Lounge",
    "Dining Room",
]
"""
- Each node has: adjacent: list of directly connected nodes and 
secret: secret passage destination (optional , free move)
"""
MANSION_MAP = {
 
    # Rooms
    "Kitchen": {
        "adjacent": ["Kitchen-Ballroom Hallway", "Dining-Kitchen Hallway"],
        "secret": "Study"
    },
    "Ballroom": {
        "adjacent": ["Kitchen-Ballroom Hallway", "Ballroom-Conservatory Hallway"]
    },
    "Conservatory": {
        "adjacent": ["Ballroom-Conservatory Hallway", "Conservatory-Billiard Hallway"],
        "secret": "Lounge"
    },
    "Billiard Room": {
        "adjacent": ["Conservatory-Billiard Hallway", "Billiard-Library Hallway"]
    },
    "Library": {
        "adjacent": ["Billiard-Library Hallway", "Library-Study Hallway"]
    },
    "Study": {
        "adjacent": ["Library-Study Hallway", "Study-Hall Hallway"],
        "secret": "Kitchen"
    },
    "Hall": {
        "adjacent": ["Study-Hall Hallway", "Hall-Lounge Hallway"]
    },
    "Lounge": {
        "adjacent": ["Hall-Lounge Hallway", "Lounge-Dining Hallway"],
        "secret": "Conservatory"
    },
    "Dining Room": {
        "adjacent": ["Lounge-Dining Hallway", "Dining-Kitchen Hallway"]
    },
 
    # Hallways (actual nodes players pass through)
    "Kitchen-Ballroom Hallway": {
        "adjacent": ["Kitchen", "Ballroom"]
    },
    "Ballroom-Conservatory Hallway": {
        "adjacent": ["Ballroom", "Conservatory"]
    },
    "Conservatory-Billiard Hallway": {
        "adjacent": ["Conservatory", "Billiard Room"]
    },
    "Billiard-Library Hallway": {
        "adjacent": ["Billiard Room", "Library"]
    },
    "Library-Study Hallway": {
        "adjacent": ["Library", "Study"]
    },
    "Study-Hall Hallway": {
        "adjacent": ["Study", "Hall"]
    },
    "Hall-Lounge Hallway": {
        "adjacent": ["Hall", "Lounge"]
    },
    "Lounge-Dining Hallway": {
        "adjacent": ["Lounge", "Dining Room"]
    },
    "Dining-Kitchen Hallway": {
        "adjacent": ["Dining Room", "Kitchen"]
    },
}
"""
Character starting positions ( all in hallways) 
"""

#charcters starting positiosn - all of them in the hallways 
STARTING_POSITIONS = {
    "Miss Scarlett":   "Lounge-Dining Hallway",
    "Colonel Mustard": "Dining-Kitchen Hallway",
    "Mrs. White":      "Kitchen-Ballroom Hallway",
    "Reverend Green":  "Ballroom-Conservatory Hallway",
    "Mrs. Peacock":    "Conservatory-Billiard Hallway",
    "Professor Plum":  "Library-Study Hallway",
}

#helper functions
def get_adjacent(location: str) -> list:
    """Return all nodes directly reachable from this location this is 1 step."""
    return MANSION_MAP.get(location, {}).get("adjacent", [])
 
 
def has_secret_passage(location: str) -> bool:
    """Return True if this room has a secret passage."""
    return "secret" in MANSION_MAP.get(location, {})
 
 
def get_secret_passage_destination(location: str) -> str | None:
    """Return the secret passage destination, or None."""
    return MANSION_MAP.get(location, {}).get("secret")
 
 
def is_room(location: str) -> bool:
    """Return True if the location is a room (not a hallway)."""
    return location in ROOMS
 
 
def is_hallway(location: str) -> bool:
    """Return True if the location is a hallway."""
    return location in MANSION_MAP and location not in ROOMS
 
 
def is_valid_location(location: str) -> bool:
    """Return True if the location exists in the mansion map."""
    return location in MANSION_MAP
 
 
def get_reachable_locations(start: str, steps: int) -> list:
    """
    BFS method — return all rooms reachable from start within `steps` moves.
    Players cannot pass THROUGH a room (entering a room ends movement).
    """
    visited = set()
    #frontier storing the  (current_location, steps_remaining)
    frontier = [(start, steps)]
    reachable = []
 
    while frontier:
        current, remaining = frontier.pop(0)
 
        if current in visited:
            continue
        visited.add(current)
 
        # If it's a room and not the start, it's a valid destination
        if is_room(current) and current != start:
            reachable.append(current)
            continue #don't expand further;entering a room ends movement
 
        #If steps remain,expand neighbors
        if remaining > 0:
            for neighbor in get_adjacent(current):
                if neighbor not in visited:
                    frontier.append((neighbor, remaining - 1))
 
    return reachable
 
def display_board_info():

    print("\n" + "=" * 60)
    print("                 CLUE / CLUEDO MANSION OVERVIEW")
    print("=" * 60)

    print("\nROOMS & THEIR CONNECTIONS:")
    print("-" * 60)

    for room in ROOMS:
        info = MANSION_MAP[room]

        #Adjacent hallways or rooms
        adjacent = ", ".join(info["adjacent"])

        #Secret passage (if any)
        if "secret" in info:
            secret_text = f"  (Secret passage → {info['secret']})"
        else:
            secret_text = ""

        print(f"• {room:<18} → {adjacent}{secret_text}")

    print("\n" + "=" * 60)
    print("CHARACTER STARTING POSITIONS:")
    print("-" * 60)

    for character, hallway in STARTING_POSITIONS.items():
        print(f"• {character:<20} starts at: {hallway}")

    print("=" * 60 + "\n")
