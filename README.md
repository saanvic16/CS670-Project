# Chougule_Readme — Cluedo (Clue) Game — CS670 Project 2

## Overview
A text-based (CLI) implementation of the classic murder mystery board game **Cluedo (Clue)**,
built in Python for NJIT CS670 Project 2, Part 1.
---

## Prerequisites
- **Python 3.10 or higher** (uses `str | None` type hints — requires 3.10+)
- No external libraries required — uses only Python's standard library.

### Check your Python version:
```bash
python --version
# or
python3 --version
```

---

## How to Run
### 1. Clone or download the project
If using Git:
```bash
git clone <your-repo-url>
```
Or unzip the submitted folder.

### 2. Navigate to the source code directory
```bash
cd Chougule_Project2_SourceCode
```

### 3. Run the game
```bash
python main.py
# or on some systems:
python3 main.py
```

---

## File Structure

```
Chougule_Project2_SourceCode/
├── main.py       # Entry point — run this file
├── game.py       # Core game loop, turn logic, suggestions, accusations
├── board.py      # Mansion layout, room adjacency, secret passages
├── cards.py      # Characters, weapons, card dealing, solution selection
├── player.py     # Player class woth the position, hand, movement
└── README.md     # This file
```

---

## Gameplay Instructions
1. Run `main.py` and enter the number of players (2–6).
2. Each player selects a character.
3. Cards are dealt privately — each player reviews their hand in turn.
4. Players take turns in order:
   - **In a hallway:** Roll the dice, move to a reachable room, then make a suggestion.
   - **In a room:** Choose to use a secret passage, roll to an adjacent room, or stay.
5. **Suggestions** prompt other players to refute with a matching card (shown privately).
6. At any time, a player may make a **final accusation** :correct = win, wrong = eliminated.
7. The game ends when a player solves the mystery or all players are eliminated.

### Secret Passages
| From          | To            |
|---------------|---------------|
| Study         | Kitchen       |
| Kitchen       | Study         |
| Conservatory  | Lounge        |
| Lounge        | Conservatory  |

---

## Notes
- The screen is cleared between private card views to keep hands secret.
- All input is validated; invalid entries prompt a retry.
- The murder solution is randomly generated each game.