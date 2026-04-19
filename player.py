"""
player.py - Player class for Cluedo.
"""

from board import STARTING_POSITIONS


class Player:
    """Represents one Cluedo player (human or future AI)."""
    def __init__(self, character: str):
        """
            character: One of the 6 standard Cluedo character names.
        """
        self.character = character
        self.position = STARTING_POSITIONS[character]   # starting hallway
        self.hand: list = []          # cards dealt to this player
        self.eliminated = False       # True if player made a wrong accusation
        self.in_room = False          # True when player is inside a room
        self.current_room: str = ""   # empty string when in a hallway

    #Movement
    def move_to_room(self, room_name: str):
        """Move the player into a room."""
        self.position = room_name
        self.current_room = room_name
        self.in_room = True
    def move_to_hallway(self, hallway_label: str):
        """Move the player back into a hallway."""
        self.position = hallway_label
        self.current_room = ""
        self.in_room = False
    #  Card helpers
    def receive_cards(self, cards: list):
        """Add a list of cards to this player's hand."""
        self.hand.extend(cards)

    def has_card(self, card: str) -> bool:
        """Return True if this player holds the given card."""
        return card in self.hand

    def show_hand(self):
        """Print the player's hand (their private view)."""
        print(f"\n  Your cards ({self.character}): {', '.join(self.hand)}")

    #  Display

    def status(self) -> str:
        """Return a short status string for the scoreboard."""
        loc = self.current_room if self.in_room else self.position
        return f"{self.character:<20} | Location: {loc}"

    def __repr__(self):
        return f"Player({self.character}, pos={self.position})"