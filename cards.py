"""
Cards.py -- Characters, weapons and solution selection for Cluedo/Clue ! 
"""

import random 

CHARACTERS = ["Miss Scarlett","Colonel Mustard", "Mrs. White", "Reverend Green", "Mrs. Peacock", "Professor Plum",]

WEAPONS = ["Candlestick","Dagger","Lead Pipe", "Revolver","Rope","Wrench",]



def setup_cards(rooms : list) -> tuple[dict,list]:
    """
        randomly select the murder solutions ( one char, one weapon, and one eroom ), 
        shuffle the deck and return the remaining card as a deck. 

        return: 
        solution(dict) : form {"char":... , "weapon" :... , "room":...}
        deck ( list ) : remaining cards to be dealt to players 
    """
    solution= {
        "character": random.choice(CHARACTERS),
        "weapon": random.choice(WEAPONS),
        "room": random.choice(rooms),
    }

    all_cards = CHARACTERS+WEAPONS+rooms
    deck = [c for c in all_cards if c not in solution.values()]
    random.shuffle(deck)

    return solution,deck 

def deal_cards(deck: list,num_players:int)-> list[list]:
    """
        give the cards evenly among all players 
        return a list of hands and one list per player
    """

    hands = []
    for _ in range(num_players):
        hands.append([])

        """deal cards in order """

    player_index  = 0 
    for card in deck: 
        hands[player_index].append(card)
        player_index+=1
        if player_index == num_players:
            player_index =0 


    return hands


def display_hand(player_name: str, hand: list):
    """Pretty-print a player's hand."""
    print(f"\n  {player_name}'s cards: {', '.join(hand)}")