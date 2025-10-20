# Clasher Engine

A chess-like engine for Clash Royale that analyzes card placements and suggests optimal moves based on game state.

## Overview

Clasher Engine works similarly to a chess engine but for Clash Royale. It evaluates the best positioning for cards in a player's hand or deck to counter opponent strategies. The engine considers multiple factors:

- **Card positioning** relative to objectives (towers)
- **Elixir efficiency** for optimal resource management
- **Card matchups and counters** based on card types and abilities
- **Strategic positioning** for offensive and defensive plays

## Features

- **Card System**: Predefined Clash Royale cards with realistic stats (damage, elixir cost, range, etc.)
- **Board/Arena Representation**: 18x32 tile arena with proper deployment zones and tower positions
- **Move Generation**: Generates all valid moves for a player's current hand
- **Move Evaluation**: Scores moves based on strategic factors
- **Best Move Finder**: Identifies optimal card placements
- **Counter Analysis**: Evaluates moves against known opponent cards

## Installation

No external dependencies required! The engine uses only Python standard library.

```bash
# Clone the repository
git clone https://github.com/bbyrum-del/clasher-engine.git
cd clasher-engine

# Run the example
python3 example.py
```

## Quick Start

```python
from card import KNIGHT, ARCHERS, GIANT, FIREBALL, MUSKETEER, MINI_PEKKA, HOG_RIDER, WIZARD
from board import Side
from player import Player
from engine import ClashRoyaleEngine

# Create a deck (8 cards)
deck = [KNIGHT, ARCHERS, GIANT, FIREBALL, MUSKETEER, MINI_PEKKA, HOG_RIDER, WIZARD]

# Create a player
player = Player(deck, name="Player 1")

# Create the engine
engine = ClashRoyaleEngine()

# Find the best move
best_moves = engine.find_best_move(player, Side.FRIENDLY, top_n=3)

for i, move in enumerate(best_moves, 1):
    print(f"{i}. {move.card.name} at ({move.position.x:.0f}, {move.position.y:.0f})")
    print(f"   Score: {move.score:.2f}")
```

## Architecture

### Core Components

1. **Card** (`card.py`)
   - Represents Clash Royale cards with properties like elixir cost, damage, range, and type
   - Includes predefined common cards (Knight, Giant, Hog Rider, etc.)

2. **Board** (`board.py`)
   - 18x32 tile arena representation
   - Tracks tower positions and deployment zones
   - Validates card placements

3. **Player** (`player.py`)
   - Manages deck (8 cards), hand (4 cards), and elixir
   - Handles card cycling and resource management

4. **Move** (`move.py`)
   - Represents a card placement at a specific position
   - Stores evaluation score

5. **ClashRoyaleEngine** (`engine.py`)
   - Generates possible moves
   - Evaluates moves based on multiple factors
   - Finds best moves for current game state
   - Provides detailed position analysis

### Evaluation Factors

The engine evaluates moves considering:

- **Elixir Efficiency**: Cheaper cards get slight tempo bonus
- **Positioning**: Distance to towers, lane selection, bridge positions
- **Card Type**: Special bonuses for area damage, high damage, range, buildings
- **Counters**: Matchup advantages against opponent cards
- **Strategy**: Lane pressure, offensive vs defensive positioning

## Available Cards

The engine includes these predefined cards:

| Card | Elixir | Type | Target | Damage | Range |
|------|--------|------|--------|--------|-------|
| Knight | 3 | Troop | Ground | 100 | Melee |
| Archers | 3 | Troop | Both | 60 | 5.0 |
| Giant | 5 | Troop | Buildings | 120 | Melee |
| Fireball | 4 | Spell | Both | 325 | Area |
| Musketeer | 4 | Troop | Both | 100 | 6.0 |
| Mini P.E.K.K.A | 4 | Troop | Ground | 400 | Melee |
| Hog Rider | 4 | Troop | Buildings | 150 | Melee |
| Wizard | 5 | Troop | Both | 130 | 5.5 (Area) |
| Cannon | 3 | Building | Ground | 60 | 5.5 |
| Inferno Tower | 5 | Building | Both | 50 | 6.0 |

## Example Output

```
======================================================================
CLASH ROYALE ENGINE - Example Usage
======================================================================

Player created: Player 1: [Knight (3), Archers (3), Giant (5), Fireball (4)] (5.0 elixir)
Deck average elixir: 4.00

Current Hand:
  1. Knight (3) (Type: troop, Cost: 3)
  2. Archers (3) (Type: troop, Cost: 3)
  3. Giant (5) (Type: troop, Cost: 5)
  4. Fireball (4) (Type: spell, Cost: 4)

Top 5 recommended moves:

1. Giant
   Position: (4, 14) on friendly side
   Elixir Cost: 5
   Evaluation Score: 24.50
   Card Type: troop
...
```

## Advanced Usage

### Analyzing with Opponent Information

```python
# Known opponent cards
opponent_cards = [GIANT, HOG_RIDER, WIZARD]

# Find best counter moves
best_counters = engine.find_best_move(
    player, 
    Side.FRIENDLY, 
    opponent_cards=opponent_cards,
    top_n=3
)
```

### Detailed Position Analysis

```python
analysis = engine.analyze_position(player, Side.FRIENDLY, opponent_cards)

print(f"Recommendation: {analysis['recommendation']}")
print(f"Best moves: {analysis['best_moves']}")
```

## How It Works

The engine follows these steps:

1. **Move Generation**: Creates all valid card+position combinations for playable cards
2. **Move Evaluation**: Each move is scored based on:
   - Base elixir efficiency
   - Positioning quality (distance to objectives)
   - Card type advantages (area damage, range, etc.)
   - Counter matchups (if opponent cards known)
   - Strategic value (lane pressure, aggression)
3. **Move Selection**: Moves are sorted by score, and the top N are returned

## Use Cases

- **Learning Tool**: Understand optimal Clash Royale strategies
- **Game Analysis**: Evaluate different deck compositions
- **AI Opponent**: Build bots that make strategic decisions
- **Strategy Testing**: Experiment with card placements before real games

## Future Enhancements

Potential improvements:
- Time-based simulation (elixir regeneration over time)
- Multi-card combo evaluation
- Machine learning integration for learned strategies
- Full game state tracking (cards on board)
- Replay analysis
- More cards and card interactions

## Contributing

Contributions are welcome! Feel free to:
- Add more cards
- Improve evaluation heuristics
- Add game state tracking
- Implement battle simulation

## License

Open source - use freely for learning and development!

## Acknowledgments

Inspired by chess engines like Stockfish, adapted for Clash Royale's unique gameplay mechanics.
