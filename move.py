"""
Move class representing a card placement in Clash Royale.
"""

from typing import Optional
from card import Card
from board import Position


class Move:
    """
    Represents a move in Clash Royale (deploying a card at a position).
    """
    
    def __init__(self, card: Card, position: Position, score: float = 0.0):
        """
        Initialize a move.
        
        Args:
            card: The card being played
            position: Where the card is being placed
            score: Evaluation score for this move
        """
        self.card = card
        self.position = position
        self.score = score
    
    def __repr__(self) -> str:
        return f"Move({self.card.name} at {self.position}, score={self.score:.2f})"
    
    def __str__(self) -> str:
        return f"{self.card.name} at ({self.position.x:.0f}, {self.position.y:.0f})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Move):
            return False
        return (self.card.name == other.card.name and 
                self.position == other.position)
    
    def __hash__(self) -> int:
        return hash((self.card.name, self.position))
    
    def __lt__(self, other) -> bool:
        """Compare moves by score for sorting."""
        return self.score < other.score
