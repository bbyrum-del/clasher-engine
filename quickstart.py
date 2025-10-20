"""
Clash Royale Engine - Quick Start Guide
"""

from card import (
    Card, CardType, Rarity, TargetType,
    KNIGHT, ARCHERS, GIANT, FIREBALL, MUSKETEER, 
    MINI_PEKKA, HOG_RIDER, WIZARD, CANNON, INFERNO_TOWER,
    CARD_POOL
)
from board import Board, Position, Side
from player import Player
from engine import ClashRoyaleEngine


def basic_usage():
    """Basic usage example."""
    print("\n=== BASIC USAGE ===\n")
    
    # 1. Create a deck
    deck = [KNIGHT, ARCHERS, GIANT, FIREBALL, MUSKETEER, MINI_PEKKA, HOG_RIDER, WIZARD]
    
    # 2. Create a player
    player = Player(deck, name="Player 1")
    print(f"Player: {player}")
    
    # 3. Create the engine
    engine = ClashRoyaleEngine()
    
    # 4. Find best move
    best_move = engine.find_best_move(player, Side.FRIENDLY, top_n=1)[0]
    print(f"Best move: {best_move}")


def analyzing_multiple_moves():
    """Example of analyzing multiple moves."""
    print("\n=== ANALYZING MULTIPLE MOVES ===\n")
    
    deck = [KNIGHT, ARCHERS, GIANT, FIREBALL, MUSKETEER, MINI_PEKKA, HOG_RIDER, WIZARD]
    player = Player(deck)
    engine = ClashRoyaleEngine()
    
    # Get top 5 moves
    top_moves = engine.find_best_move(player, Side.FRIENDLY, top_n=5)
    
    print("Top 5 moves:")
    for i, move in enumerate(top_moves, 1):
        print(f"{i}. {move.card.name} at ({move.position.x:.0f}, {move.position.y:.0f}) - Score: {move.score:.2f}")


def counter_analysis():
    """Example with opponent card information."""
    print("\n=== COUNTER ANALYSIS ===\n")
    
    deck = [KNIGHT, ARCHERS, GIANT, FIREBALL, MUSKETEER, MINI_PEKKA, HOG_RIDER, WIZARD]
    player = Player(deck)
    engine = ClashRoyaleEngine()
    
    # Opponent's known cards
    opponent_cards = [GIANT, HOG_RIDER, WIZARD]
    print(f"Opponent cards: {', '.join(c.name for c in opponent_cards)}")
    
    # Find best counter
    best_counter = engine.find_best_move(
        player, 
        Side.FRIENDLY, 
        opponent_cards=opponent_cards,
        top_n=3
    )
    
    print("\nBest counter plays:")
    for i, move in enumerate(best_counter, 1):
        print(f"{i}. {move.card.name} - Score: {move.score:.2f}")


def detailed_analysis():
    """Example of detailed position analysis."""
    print("\n=== DETAILED ANALYSIS ===\n")
    
    deck = [KNIGHT, ARCHERS, GIANT, FIREBALL, MUSKETEER, MINI_PEKKA, HOG_RIDER, WIZARD]
    player = Player(deck)
    engine = ClashRoyaleEngine()
    
    analysis = engine.analyze_position(player, Side.FRIENDLY)
    
    print(f"Player: {analysis['player']}")
    print(f"Elixir: {analysis['elixir']}/{Player.MAX_ELIXIR}")
    print(f"Playable cards: {analysis['playable_cards']}")
    print(f"Recommendation: {analysis['recommendation']}")


def custom_deck():
    """Example of creating a custom card and deck."""
    print("\n=== CUSTOM CARD & DECK ===\n")
    
    # Create a custom card
    custom_card = Card(
        name="Super Troop",
        card_type=CardType.TROOP,
        elixir_cost=6,
        rarity=Rarity.LEGENDARY,
        target_type=TargetType.BOTH,
        damage=200,
        hit_speed=1.0,
        range_=5.0,
        area_damage=True,
        splash_radius=2.0
    )
    
    print(f"Custom card created: {custom_card}")
    
    # Create deck with custom card
    deck = [custom_card, KNIGHT, ARCHERS, GIANT, FIREBALL, MUSKETEER, MINI_PEKKA, HOG_RIDER]
    player = Player(deck)
    
    # Analyze
    engine = ClashRoyaleEngine()
    best_move = engine.find_best_move(player, Side.FRIENDLY, top_n=1)
    
    if best_move:
        print(f"Best move with custom deck: {best_move[0]}")


def exploring_positions():
    """Example of exploring different positions."""
    print("\n=== EXPLORING POSITIONS ===\n")
    
    board = Board()
    
    # Get deployment zones
    friendly_zones = board.get_deployment_positions(Side.FRIENDLY)
    print(f"Friendly deployment zones: {len(friendly_zones)} positions")
    
    # Show some positions
    print("\nSample positions:")
    for i, pos in enumerate(friendly_zones[:5], 1):
        print(f"{i}. ({pos.x:.0f}, {pos.y:.0f})")
    
    # Check tower positions
    print(f"\nFriendly King Tower: {board.FRIENDLY_KING_TOWER}")
    print(f"Enemy King Tower: {board.ENEMY_KING_TOWER}")


def simulating_game():
    """Example of simulating a simple game scenario."""
    print("\n=== SIMULATING A GAME SCENARIO ===\n")
    
    deck = [KNIGHT, ARCHERS, GIANT, FIREBALL, MUSKETEER, MINI_PEKKA, HOG_RIDER, WIZARD]
    player = Player(deck, name="Player 1")
    engine = ClashRoyaleEngine()
    
    print(f"Starting state: {player}")
    
    # Turn 1: Play a card
    best_move = engine.find_best_move(player, Side.FRIENDLY, top_n=1)[0]
    print(f"\nTurn 1 - Playing: {best_move}")
    player.play_card(best_move.card)
    print(f"After playing: Elixir = {player.elixir:.1f}")
    
    # Regenerate some elixir (simulating time passing)
    player.add_elixir(2.0)
    print(f"After elixir regen: Elixir = {player.elixir:.1f}")
    
    # Turn 2: Play another card
    best_moves = engine.find_best_move(player, Side.FRIENDLY, top_n=1)
    if best_moves:
        best_move = best_moves[0]
        print(f"\nTurn 2 - Playing: {best_move}")
        player.play_card(best_move.card)
        print(f"After playing: Elixir = {player.elixir:.1f}")
    else:
        print(f"\nTurn 2 - Not enough elixir to play any card")
    
    print(f"\nCurrent hand: {', '.join(c.name for c in player.hand)}")


def main():
    """Run all examples."""
    print("=" * 70)
    print("CLASH ROYALE ENGINE - QUICK START GUIDE")
    print("=" * 70)
    
    examples = [
        basic_usage,
        analyzing_multiple_moves,
        counter_analysis,
        detailed_analysis,
        custom_deck,
        exploring_positions,
        simulating_game
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")
    
    print("\n" + "=" * 70)
    print("For more information, see README.md or run example.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
