"""
Clash Royale Engine - Main engine for evaluating moves and suggesting best plays.
"""

from typing import List, Optional, Dict, Tuple
from card import Card, CardType, TargetType
from board import Board, Position, Side
from move import Move
from player import Player


class ClashRoyaleEngine:
    """
    Engine for evaluating Clash Royale moves, similar to a chess engine.
    
    The engine analyzes the current game state and suggests the best card
    placements based on various strategic factors.
    """
    
    def __init__(self, board: Optional[Board] = None):
        """
        Initialize the engine.
        
        Args:
            board: Game board (creates new if None)
        """
        self.board = board or Board()
    
    def generate_moves(self, player: Player, side: Side) -> List[Move]:
        """
        Generate all possible moves for a player.
        
        Args:
            player: Player to generate moves for
            side: Which side the player is on
            
        Returns:
            List of possible moves
        """
        moves = []
        playable_cards = player.get_playable_cards()
        positions = self.board.get_deployment_positions(side)
        
        for card in playable_cards:
            for position in positions:
                if self.board.is_valid_position(position):
                    move = Move(card, position)
                    moves.append(move)
        
        return moves
    
    def evaluate_move(
        self, 
        move: Move, 
        player_side: Side,
        opponent_cards: Optional[List[Card]] = None
    ) -> float:
        """
        Evaluate a move and assign it a score.
        
        Higher scores indicate better moves. The evaluation considers:
        - Card positioning relative to objectives (towers)
        - Elixir efficiency
        - Card matchups and counters
        - Strategic positioning
        
        Args:
            move: Move to evaluate
            player_side: Which side the player is on
            opponent_cards: Known opponent cards (if any)
            
        Returns:
            Score for the move (higher is better)
        """
        score = 0.0
        card = move.card
        position = move.position
        
        # Base score inversely proportional to elixir cost
        # (cheaper cards are slightly favored for tempo)
        score += (10 - card.elixir_cost) * 0.5
        
        # Evaluate positioning
        score += self._evaluate_positioning(card, position, player_side)
        
        # Evaluate card type advantages
        score += self._evaluate_card_type(card, position, player_side)
        
        # Evaluate counters if opponent cards are known
        if opponent_cards:
            score += self._evaluate_counters(card, opponent_cards)
        
        # Evaluate strategic value
        score += self._evaluate_strategy(card, position, player_side)
        
        return score
    
    def _evaluate_positioning(
        self, 
        card: Card, 
        position: Position, 
        player_side: Side
    ) -> float:
        """
        Evaluate how good the positioning is for a card.
        
        Args:
            card: Card being played
            position: Position to evaluate
            player_side: Which side the player is on
            
        Returns:
            Positioning score
        """
        score = 0.0
        
        # Get nearest enemy tower
        enemy_side = Side.ENEMY if player_side == Side.FRIENDLY else Side.FRIENDLY
        nearest_tower = self.board.get_nearest_tower(position, enemy_side)
        
        if nearest_tower:
            distance = position.distance_to(nearest_tower)
            
            # Troops targeting buildings should be closer to towers
            if card.card_type == CardType.TROOP and card.target_type == TargetType.BUILDINGS:
                score += max(0, 20 - distance * 0.5)  # Closer is better
            
            # Defensive cards should be positioned further back
            elif card.card_type == CardType.BUILDING:
                score += distance * 0.3  # Further is better for buildings
            
            # Spells are position-dependent on targets (simplified)
            elif card.card_type == CardType.SPELL:
                score += 5.0  # Base spell value
        
        # Bridge positions are valuable for offensive troops
        is_bridge = (player_side == Side.FRIENDLY and position.y >= 14) or \
                    (player_side == Side.ENEMY and position.y <= 18)
        
        if is_bridge and card.card_type == CardType.TROOP:
            score += 3.0
        
        return score
    
    def _evaluate_card_type(
        self, 
        card: Card, 
        position: Position, 
        player_side: Side
    ) -> float:
        """
        Evaluate card based on its type and characteristics.
        
        Args:
            card: Card being evaluated
            position: Position of the card
            player_side: Which side the player is on
            
        Returns:
            Card type score
        """
        score = 0.0
        
        # High damage cards get bonus
        if card.damage > 200:
            score += 3.0
        
        # Area damage is valuable
        if card.area_damage:
            score += 2.5
        
        # Long range cards get positioning flexibility bonus
        if card.range > 5.0:
            score += 2.0
        
        # Buildings provide defensive value
        if card.card_type == CardType.BUILDING:
            score += 4.0  # Base defensive value
        
        return score
    
    def _evaluate_counters(self, card: Card, opponent_cards: List[Card]) -> float:
        """
        Evaluate how well a card counters known opponent cards.
        
        Args:
            card: Card being evaluated
            opponent_cards: Known opponent cards
            
        Returns:
            Counter score
        """
        score = 0.0
        
        for opp_card in opponent_cards:
            # Area damage counters swarms
            if card.area_damage and opp_card.elixir_cost <= 3:
                score += 3.0
            
            # Buildings counter building-targeting troops
            if (card.card_type == CardType.BUILDING and 
                opp_card.target_type == TargetType.BUILDINGS):
                score += 4.0
            
            # High damage counters tanks
            if card.damage > 300 and opp_card.elixir_cost >= 5:
                score += 2.5
            
            # Air targeting counters air troops
            if (card.target_type in [TargetType.AIR, TargetType.BOTH] and
                opp_card.target_type == TargetType.AIR):
                score += 2.0
        
        return score
    
    def _evaluate_strategy(
        self, 
        card: Card, 
        position: Position, 
        player_side: Side
    ) -> float:
        """
        Evaluate strategic considerations for a move.
        
        Args:
            card: Card being played
            position: Position to evaluate
            player_side: Which side the player is on
            
        Returns:
            Strategic score
        """
        score = 0.0
        
        # Lane pressure: playing in different lanes spreads defense
        if position.x < 7:  # Left lane
            score += 1.0
        elif position.x > 11:  # Right lane
            score += 1.0
        else:  # Center
            score += 0.5
        
        # Offensive positioning (closer to enemy side)
        if player_side == Side.FRIENDLY:
            if position.y > 10:
                score += 2.0  # Aggressive positioning
        else:
            if position.y < 22:
                score += 2.0
        
        return score
    
    def find_best_move(
        self, 
        player: Player, 
        side: Side,
        opponent_cards: Optional[List[Card]] = None,
        top_n: int = 1
    ) -> List[Move]:
        """
        Find the best move(s) for a player.
        
        Args:
            player: Player to find moves for
            side: Which side the player is on
            opponent_cards: Known opponent cards (if any)
            top_n: Number of top moves to return
            
        Returns:
            List of best moves, sorted by score (highest first)
        """
        # Generate all possible moves
        moves = self.generate_moves(player, side)
        
        if not moves:
            return []
        
        # Evaluate each move
        for move in moves:
            move.score = self.evaluate_move(move, side, opponent_cards)
        
        # Sort by score (descending) and return top N
        moves.sort(reverse=True)
        return moves[:top_n]
    
    def analyze_position(
        self, 
        player: Player, 
        side: Side,
        opponent_cards: Optional[List[Card]] = None
    ) -> Dict[str, any]:
        """
        Analyze the current position and provide detailed analysis.
        
        Args:
            player: Player to analyze for
            side: Which side the player is on
            opponent_cards: Known opponent cards (if any)
            
        Returns:
            Dictionary with analysis results
        """
        best_moves = self.find_best_move(player, side, opponent_cards, top_n=5)
        
        analysis = {
            'player': player.name,
            'elixir': player.elixir,
            'playable_cards': len(player.get_playable_cards()),
            'hand': [str(card) for card in player.hand],
            'best_moves': [
                {
                    'card': move.card.name,
                    'position': f"({move.position.x:.0f}, {move.position.y:.0f})",
                    'score': round(move.score, 2),
                    'elixir_cost': move.card.elixir_cost
                }
                for move in best_moves
            ],
            'recommendation': str(best_moves[0]) if best_moves else "No moves available"
        }
        
        return analysis
