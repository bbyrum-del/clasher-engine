"""
Example usage of the Clash Royale Engine.
"""

from card import KNIGHT, ARCHERS, GIANT, FIREBALL, MUSKETEER, MINI_PEKKA, HOG_RIDER, WIZARD
from board import Board, Side
from player import Player
from engine import ClashRoyaleEngine


def main():
    """Demonstrate the Clash Royale engine."""
    
    print("=" * 70)
    print("CLASH ROYALE ENGINE - Example Usage")
    print("=" * 70)
    print()
    
    # Create a deck for the player
    deck = [KNIGHT, ARCHERS, GIANT, FIREBALL, MUSKETEER, MINI_PEKKA, HOG_RIDER, WIZARD]
    
    # Create player
    player = Player(deck, name="Player 1")
    print(f"Player created: {player}")
    print(f"Deck average elixir: {player.get_average_elixir():.2f}")
    print()
    
    # Create the engine
    board = Board()
    engine = ClashRoyaleEngine(board)
    
    print("Current Hand:")
    for i, card in enumerate(player.hand, 1):
        print(f"  {i}. {card} (Type: {card.card_type.value}, Cost: {card.elixir_cost})")
    print()
    
    # Find best move
    print("Analyzing best moves...")
    print("-" * 70)
    
    best_moves = engine.find_best_move(player, Side.FRIENDLY, top_n=5)
    
    if best_moves:
        print(f"\nTop {len(best_moves)} recommended moves:")
        print()
        for i, move in enumerate(best_moves, 1):
            print(f"{i}. {move.card.name}")
            print(f"   Position: ({move.position.x:.0f}, {move.position.y:.0f}) on {move.position.side.value} side")
            print(f"   Elixir Cost: {move.card.elixir_cost}")
            print(f"   Evaluation Score: {move.score:.2f}")
            print(f"   Card Type: {move.card.card_type.value}")
            print()
    else:
        print("No moves available (insufficient elixir)")
    
    print("-" * 70)
    print()
    
    # Perform detailed analysis
    print("Detailed Position Analysis:")
    print("-" * 70)
    analysis = engine.analyze_position(player, Side.FRIENDLY)
    
    print(f"Player: {analysis['player']}")
    print(f"Elixir: {analysis['elixir']}/{Player.MAX_ELIXIR}")
    print(f"Playable Cards: {analysis['playable_cards']}")
    print()
    print("Hand:", ", ".join(analysis['hand']))
    print()
    print(f"Recommendation: {analysis['recommendation']}")
    print()
    
    # Simulate with opponent information
    print("=" * 70)
    print("SCENARIO: Analyzing with opponent's known cards")
    print("=" * 70)
    print()
    
    opponent_cards = [GIANT, HOG_RIDER, WIZARD]
    print("Opponent's known cards:", ", ".join(str(c) for c in opponent_cards))
    print()
    
    best_counter_moves = engine.find_best_move(
        player, 
        Side.FRIENDLY, 
        opponent_cards=opponent_cards,
        top_n=3
    )
    
    print("Top 3 counter moves:")
    print()
    for i, move in enumerate(best_counter_moves, 1):
        print(f"{i}. {move.card.name} at ({move.position.x:.0f}, {move.position.y:.0f})")
        print(f"   Score: {move.score:.2f} | Cost: {move.card.elixir_cost} elixir")
    
    print()
    print("=" * 70)
    print("Engine demonstration complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
