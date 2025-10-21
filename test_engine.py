"""
Basic tests for the Clash Royale Engine.
"""

from card import Card, CardType, Rarity, TargetType, KNIGHT, GIANT, FIREBALL
from board import Board, Position, Side
from player import Player
from move import Move
from engine import ClashRoyaleEngine


def test_card_creation():
    """Test card creation and properties."""
    print("Testing card creation...")
    card = Card("Test Card", CardType.TROOP, 3, Rarity.COMMON, TargetType.GROUND)
    assert card.name == "Test Card"
    assert card.elixir_cost == 3
    assert card.card_type == CardType.TROOP
    print("✓ Card creation works")


def test_board_positions():
    """Test board position validation."""
    print("Testing board positions...")
    board = Board()
    
    # Valid position
    valid_pos = Position(9, 8, Side.FRIENDLY)
    assert board.is_valid_position(valid_pos)
    
    # Invalid position (out of bounds)
    invalid_pos = Position(20, 8, Side.FRIENDLY)
    assert not board.is_valid_position(invalid_pos)
    
    # Get deployment positions
    friendly_positions = board.get_deployment_positions(Side.FRIENDLY)
    assert len(friendly_positions) > 0
    print(f"✓ Board has {len(friendly_positions)} friendly deployment positions")


def test_player_mechanics():
    """Test player elixir and card management."""
    print("Testing player mechanics...")
    deck = [KNIGHT, GIANT, FIREBALL, KNIGHT, GIANT, FIREBALL, KNIGHT, GIANT]
    player = Player(deck, "Test Player")
    
    # Check initial state
    assert player.elixir == Player.STARTING_ELIXIR
    assert len(player.hand) == Player.HAND_SIZE
    
    # Test elixir
    player.add_elixir(3)
    assert player.elixir == 8
    
    # Test card playing
    initial_elixir = player.elixir
    playable = player.get_playable_cards()
    if playable:
        card = playable[0]
        success = player.play_card(card)
        assert success
        assert player.elixir == initial_elixir - card.elixir_cost
    
    print("✓ Player mechanics work correctly")


def test_move_generation():
    """Test move generation."""
    print("Testing move generation...")
    deck = [KNIGHT, GIANT, FIREBALL, KNIGHT, GIANT, FIREBALL, KNIGHT, GIANT]
    player = Player(deck)
    engine = ClashRoyaleEngine()
    
    moves = engine.generate_moves(player, Side.FRIENDLY)
    assert len(moves) > 0
    print(f"✓ Generated {len(moves)} possible moves")


def test_move_evaluation():
    """Test move evaluation."""
    print("Testing move evaluation...")
    deck = [KNIGHT, GIANT, FIREBALL, KNIGHT, GIANT, FIREBALL, KNIGHT, GIANT]
    player = Player(deck)
    engine = ClashRoyaleEngine()
    
    # Create a test move
    position = Position(9, 14, Side.FRIENDLY)
    move = Move(GIANT, position)
    
    # Evaluate it
    score = engine.evaluate_move(move, Side.FRIENDLY)
    assert score > 0  # Should have some positive score
    print(f"✓ Move evaluation score: {score:.2f}")


def test_best_move_finder():
    """Test finding best moves."""
    print("Testing best move finder...")
    deck = [KNIGHT, GIANT, FIREBALL, KNIGHT, GIANT, FIREBALL, KNIGHT, GIANT]
    player = Player(deck)
    engine = ClashRoyaleEngine()
    
    best_moves = engine.find_best_move(player, Side.FRIENDLY, top_n=3)
    assert len(best_moves) > 0
    assert best_moves[0].score >= best_moves[-1].score  # Sorted by score
    print(f"✓ Best move: {best_moves[0].card.name} at ({best_moves[0].position.x:.0f}, {best_moves[0].position.y:.0f})")
    print(f"  Score: {best_moves[0].score:.2f}")


def test_engine_analysis():
    """Test full engine analysis."""
    print("Testing engine analysis...")
    deck = [KNIGHT, GIANT, FIREBALL, KNIGHT, GIANT, FIREBALL, KNIGHT, GIANT]
    player = Player(deck)
    engine = ClashRoyaleEngine()
    
    analysis = engine.analyze_position(player, Side.FRIENDLY)
    assert 'player' in analysis
    assert 'elixir' in analysis
    assert 'best_moves' in analysis
    assert 'recommendation' in analysis
    print(f"✓ Analysis recommendation: {analysis['recommendation']}")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("RUNNING CLASH ROYALE ENGINE TESTS")
    print("=" * 70)
    print()
    
    tests = [
        test_card_creation,
        test_board_positions,
        test_player_mechanics,
        test_move_generation,
        test_move_evaluation,
        test_best_move_finder,
        test_engine_analysis
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
            print()
        except Exception as e:
            print(f"✗ Test failed: {e}")
            failed += 1
            print()
    
    print("=" * 70)
    print(f"TESTS COMPLETE: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
