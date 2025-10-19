🏰 HOTK-Minimax-AI
 A Game of Thrones: Hand of the King — Artificial Intelligence Project

An **AI-powered adaptation** of the board game *A Game of Thrones: Hand of the King*, implemented in **Python** with **Pygame**.  
This project allows full play between **human vs AI**, **AI vs AI**, or **human vs human**. It integrates a dynamic graphical interface and a strategic **Minimax decision-making system**.

 🎮 Overview

In *Hand of the King*, players guide **Varys** across a 6x6 grid, collecting character cards of noble houses.  
Each move is determined by Varys’s position and available characters in the same row or column.  
Control over houses grants banners, and the player with more banners wins.

 🧠 AI System (Minimax Engine)

- **Depth-limited Minimax Search**
- **Alpha-Beta Pruning** for computation efficiency
- **Heuristic Scoring Function** combining:
  - `BANNER_WEIGHT` → evaluates control of banners  
  - `CARD_WEIGHT` → counts owned cards  
  - `PROXIMITY_WEIGHT` → optional spatial heuristic for closeness to targets  

Each potential move is simulated on deep-copied game states, and the agent picks the highest-scoring one.

Graphical System (Pygame Interface)

**Features:**
- Loads all character images and text from `/assets`
- Dynamically scales the board to fit system display
- Detects mouse clicks and translates them to board grid positions
- Displays winner screens and transition footers

**Main functions:**
```python
init_board()          # sets up the board and loads assets
draw_board(board, cards, footer)  # draws grid and footer message
get_player_move()     # returns clicked location by human user
display_winner(board, winner, agent_name)  # shows winner info
show_board(seconds)   # pauses screen for animation timing
```

 📁 Directory Structure

```
Ai-prog-SaharShahrajabian-hodaAttari/
│
├── main.py                     # Core gameplay, loop, and rules
├── minimax.py                  # AI agent implementing Minimax
├── minimax2.py                 # Alternative search version
├── main_tester.py              # Batch testing for AI evaluation
│
├── utils/
│   ├── pygraphics.py           # Pygame rendering module
│   ├── classes.py              # Card and Player classes
│
├── assets/
│   ├── cards/                  # Card images
│   ├── icons/                  # Window icon
│   ├── backgrounds/            # Winner background image
│   └── characters.json         # Character listings by house
│
├── boards/                     # Saved board setups (.json)
└── gozareshkar.pdf             # Persian report of the project
```

---
🚀 Run Instructions

🧩 Requirements
Ensure Python and Pygame are installed:
```bash
pip install pygame
```

▶️ Run Game
To start interactive gameplay:
```bash
python main.py --player1 human --player2 minimax
```

To run AI vs AI simulations:
```bash
python main_tester.py --player1 minimax --player2 minimax
```

Optional arguments:
- `--load <filename>` to load a board setup from `/boards`
- `--save <filename>` to save the current board
- Players can be `"human"` or any AI module with a `get_move()` function.

🏆 Game Logic and Scoring

Each turn:
1. The active player moves **Varys** to choose a card.  
2. All cards between Varys and that position (same house) are collected.  
3. Banner ownership is updated depending on who holds more cards of a house.  
4. In ties, banners follow last-house priority rules.  
5. When no valid moves remain, winner determination is based on banner totals and house precedence.


📊 Example Output
```
Board initialized.
Round summary:
Player 1 banners: 4 | Player 2 banners: 3
Winner → Player 1
```

📖 Academic Context
Developed as part of *Artificial Intelligence Programming and Strategy Games* —  
**Final Project, Fall 2024**,  
Department of Computer Engineering.


📚 References
- *A Game of Thrones: Hand of the King* (Fantasy Flight Games)
- Minimax and Alpha–Beta algorithms in deterministic board environments
- Strategic heuristic design for adversarial search systems.
