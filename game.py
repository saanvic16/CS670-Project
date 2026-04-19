"""
game setup (players, cards, board)
turn structures - roll - move - suggest 
suggestion refute 
accusations and win/loss conditions
"""

import random
from board import (
    ROOMS, get_adjacent, has_secret_passage,
    get_secret_passage_destination, get_reachable_locations,
    is_room, is_hallway, display_board_info
)
from cards import CHARACTERS, WEAPONS, setup_cards, deal_cards
from player import Player


def roll_dice() -> int:
    """Simulate one standard 6-sided die."""
    return random.randint(1, 6)

def separator(char="─", width=55):
    print(char * width)

def press_enter(prompt="Press Enter to continue..."):
    input(f"\n  {prompt}")

def numbered_choice(options: list, prompt: str) -> str:
    """
    Show a numbered list of options and let the user pick one.
    Returns the actual item they selected.
    """

    print()  #blank line for spacing

    # Display each option with a number
    for index, option in enumerate(options, start=1):
        print(f"    [{index}] {option}")

    # Keep asking until the user enters a valid number
    while True:
        user_input = input(f"  {prompt} (enter number): ").strip()

        # Check if the input is a valid number within range
        if user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= len(options):
                return options[choice - 1]

        # If we reach here, the input was invalid
        print("Invalid choice, try again.")

# GAME SETUP
class CluedoGame:

    def __init__(self):         
        self.players = []
        self.solution = {}
        self.game_over = False
        self.winner = None
    def setup(self):
        """Run the full game setup sequence."""

        print("\n" + "=" * 55)
        print("            W E L C O M E   T O   C L U E D O")
        print("=" * 55)

        # Ask for number of players
        while True:
            raw = input("\n  How many players? (2–6): ").strip()
            if raw.isdigit() and 2 <= int(raw) <= 6:
                num_players = int(raw)
                break
            print("  Please enter a number between 2 and 6.")

        # Character selection
        available_chars = list(CHARACTERS)
        print("\n  Available characters:")
        for i, c in enumerate(available_chars, 1):
            print(f"    [{i}] {c}")

        chosen_chars = []
        for p in range(1, num_players + 1):
            remaining = [c for c in available_chars if c not in chosen_chars]
            print(f"\n  Player {p}, choose your character:")
            choice = numbered_choice(remaining, "Your choice")
            chosen_chars.append(choice)
            print(f"  Player {p} is {choice}.")

        # Create Player objects
        self.players = [Player(c) for c in chosen_chars]

        # Deal cards and determine solution
        self.solution, deck = setup_cards(ROOMS)
        hands = deal_cards(deck, num_players)

        for player, hand in zip(self.players, hands):
            player.receive_cards(hand)

        # Private card viewing
        print("\n" + "=" * 55)
        print("  DEAL COMPLETE — Each player, review your cards.")
        print("=" * 55)

        for player in self.players:
            press_enter(f"{player.character}: press Enter to see your cards (keep secret!)")
            player.show_hand()
            press_enter("Done viewing? Press Enter to continue.")
            print("\033[2J\033[H", end="")  # clear screen

        display_board_info()
        print("  Game setup complete! Let’s begin.\n")
    # turning logc
    def play_turn(self, player: Player):
        """Handle one player's full turn."""

        separator()
        print(f"  {player.character}'s Turn")
        separator()
        print(f"  Location: {player.position}")

        if player.in_room:
            self._handle_room_turn(player)
        else:
            self._handle_hallway_turn(player)


    def _handle_hallway_turn(self, player: Player):
        """Player is in a hallway — roll and move to a reachable room."""

        press_enter(f"{player.character}, press Enter to roll the dice.")
        roll = roll_dice()
        print(f"\n  You rolled: {roll}")

        reachable = get_reachable_locations(player.position, roll)

        if not reachable:
            print("  No rooms reachable with that roll. Turn skipped.")
            return

        print("\n  Rooms you can reach:")
        destination = numbered_choice(reachable, "Move to which room")
        player.move_to_room(destination)

        print(f"\n  ✓ {player.character} moved to the {destination}.")
        self._handle_suggestion(player)


    def _handle_room_turn(self, player: Player):
        """Player is in a room — choose secret passage or roll to leave."""

        room = player.current_room

        options = [
            "Roll dice to move to adjacent room",
            "Make an accusation",
            "End turn (stay in room)"
        ]

        if has_secret_passage(room):
            dest = get_secret_passage_destination(room)
            options.insert(0, f"Use secret passage to {dest}")

        choice = numbered_choice(options, "What would you like to do")

        if choice.startswith("Use secret passage"):
            dest = get_secret_passage_destination(room)
            player.move_to_room(dest)
            print(f"\n  {player.character} took the secret passage to {dest}!")
            self._handle_suggestion(player)

        elif choice == "Roll dice to move to adjacent room":
            press_enter(f"{player.character}, press Enter to roll the dice.")
            roll = roll_dice()
            print(f"\n  You rolled: {roll}")

            reachable = get_reachable_locations(player.current_room, roll)
            if not reachable:
                print("  No rooms reachable. Turn ends.")
                return

            print("\n  Rooms you can reach:")
            destination = numbered_choice(reachable, "Move to which room")
            player.move_to_room(destination)

            print(f"\n  {player.character} moved to the {destination}.")
            self._handle_suggestion(player)

        elif choice == "Make an accusation":
            self._handle_accusation(player)

        else:
            print("  Turn ended — staying in room.")

    # SUGGESTIONS
    def _handle_suggestion(self, suggesting_player: Player):
        """Prompt the player to make a suggestion, then handle refutation."""

        room = suggesting_player.current_room
        print(f"\nMake a suggestion about the {room}.")

        suspect = numbered_choice(CHARACTERS, "Suspect (character)")
        weapon = numbered_choice(WEAPONS, "Weapon")

        print(f"\n  Suggestion: {suggesting_player.character} suggests it was")
        print(f"    {suspect}, with the {weapon}, in the {room}.")

        #moving suggested character’s token
        for p in self.players:
            if p.character == suspect and p.current_room != room:
                p.move_to_room(room)
                print(f"  ↳ {suspect}'s token moved to {room}.")

        self._refute_suggestion(suggesting_player, suspect, weapon, room)


    def _refute_suggestion(self, suggester: Player, suspect: str, weapon: str, room: str):
        #Go around the table; first player who can refute does so.
        cards_in_suggestion = [suspect, weapon, room]
        refuted = False

        for player in self.players:
            if player is suggester or player.eliminated:
                continue

            matching = [c for c in player.hand if c in cards_in_suggestion]

            if matching:
                print(f"\n  {player.character} can refute the suggestion!")
                press_enter(f"{suggester.character}, press Enter to see the refutation (keep private).")

                if len(matching) == 1:
                    shown_card = matching[0]
                else:
                    shown_card = numbered_choice(matching, f"{player.character}, which card do you show")

                print(f"\n  *** {player.character} shows you: [{shown_card}] ***")
                press_enter("Press Enter when done (others must not look).")
                print("\033[2J\033[H", end="")  # clear screen

                refuted = True
                break

        if not refuted:
            print("\nNo one could refute the suggestion!")


    # accusations in the game
    def _handle_accusation(self, player: Player):
        """Player makes a final accusation — check against solution."""

        print("\nFINAL ACCUSATION — this ends your game if wrong!")
        confirm = input("  Are you sure? (yes/no): ").strip().lower()

        if confirm != "yes":
            print("  Accusation cancelled.")
            return

        suspect = numbered_choice(CHARACTERS, "Accuse which character")
        weapon = numbered_choice(WEAPONS, "With which weapon")
        room = numbered_choice(ROOMS, "In which room")

        print(f"\n  Accusation: {suspect}, {weapon}, in the {room}.")

        correct = (
            suspect == self.solution["character"] and
            weapon == self.solution["weapon"] and
            room == self.solution["room"]
        )

        if correct:
            print(f"\n CORRECT! {player.character} solved the mystery!")
            print(f"     The murderer was {suspect}, with the {weapon}, in the {room}.")
            self.game_over = True
            self.winner = player
        else:
            print(f"\n  Wrong! {player.character} is eliminated from making further accusations.")
            player.eliminated = True

            active = [p for p in self.players if not p.eliminated]
            if not active:
                print("\n  No players left — the mystery remains unsolved!")
                print(f"  The solution was: {self.solution['character']}, "
                    f"{self.solution['weapon']}, in the {self.solution['room']}.")
                self.game_over = True

    def run(self):
        """Run the full game from setup to finish."""

        self.setup()
        turn_index = 0

        while not self.game_over:
            active_players = [p for p in self.players if not p.eliminated]
            if not active_players:
                break

            current = self.players[turn_index % len(self.players)]

            if not current.eliminated:
                self.play_turn(current)

                # Optional accusation at end of turn
                if not self.game_over and not current.eliminated:
                    acc = input("\n  Make a final accusation this turn? (yes/no): ").strip().lower()
                    if acc == "yes":
                        self._handle_accusation(current)

            turn_index += 1

        print("\n" + "=" * 55)
        if self.winner:
            print(f"  GAME OVER — {self.winner.character} wins!")
        else:
            print("  GAME OVER — Nobody solved the mystery.")
        print("=" * 55 + "\n")
