"""
Board/Arena class representing the Clash Royale playing field.
"""

from typing import List, Tuple, Optional
from enum import Enum


class Side(Enum):
    """Which side of the arena."""
    FRIENDLY = "friendly"
    ENEMY = "enemy"


class Position:
    """Represents a position on the arena."""
    
    def __init__(self, x: float, y: float, side: Side):
        """
        Initialize a position.
        
        Args:
            x: X coordinate (0-18, representing tiles across)
            y: Y coordinate (0-32, representing tiles from bottom to top)
            side: Which side of the arena (friendly or enemy)
        """
        self.x = x
        self.y = y
        self.side = side
    
    def __repr__(self) -> str:
        return f"Position(x={self.x}, y={self.y}, {self.side.value})"
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y}) {self.side.value}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return False
        return (self.x == other.x and self.y == other.y and 
                self.side == other.side)
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.side))
    
    def distance_to(self, other: 'Position') -> float:
        """Calculate Euclidean distance to another position."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


class Board:
    """
    Represents the Clash Royale arena/board.
    
    The arena is divided into two halves:
    - Friendly side (bottom): y = 0 to 16
    - Enemy side (top): y = 16 to 32
    
    Width: 18 tiles (x = 0 to 18)
    """
    
    # Standard arena dimensions
    WIDTH = 18
    HEIGHT = 32
    MIDLINE = 16
    
    # Common deployment zones
    FRIENDLY_DEPLOYMENT_ZONES = [
        # Left lane
        (4, 4), (4, 6), (4, 8),
        # Center
        (9, 4), (9, 6), (9, 8),
        # Right lane
        (14, 4), (14, 6), (14, 8),
        # Bridge positions
        (4, 14), (9, 14), (14, 14)
    ]
    
    ENEMY_DEPLOYMENT_ZONES = [
        # Left lane
        (4, 18), (4, 20), (4, 22),
        # Center
        (9, 18), (9, 20), (9, 22),
        # Right lane
        (14, 18), (14, 20), (14, 22),
        # Bridge positions
        (4, 18), (9, 18), (14, 18)
    ]
    
    # Tower positions
    FRIENDLY_KING_TOWER = Position(9, 2, Side.FRIENDLY)
    FRIENDLY_LEFT_TOWER = Position(4, 10, Side.FRIENDLY)
    FRIENDLY_RIGHT_TOWER = Position(14, 10, Side.FRIENDLY)
    
    ENEMY_KING_TOWER = Position(9, 30, Side.ENEMY)
    ENEMY_LEFT_TOWER = Position(4, 22, Side.ENEMY)
    ENEMY_RIGHT_TOWER = Position(14, 22, Side.ENEMY)
    
    def __init__(self):
        """Initialize the board."""
        # Track destroyed towers
        self.friendly_towers = {
            'king': True,
            'left': True,
            'right': True
        }
        self.enemy_towers = {
            'king': True,
            'left': True,
            'right': True
        }
    
    def get_deployment_positions(self, side: Side) -> List[Position]:
        """
        Get valid deployment positions for a side.
        
        Args:
            side: Which side to get positions for
            
        Returns:
            List of valid deployment positions
        """
        if side == Side.FRIENDLY:
            zones = self.FRIENDLY_DEPLOYMENT_ZONES
        else:
            zones = self.ENEMY_DEPLOYMENT_ZONES
        
        return [Position(x, y, side) for x, y in zones]
    
    def is_valid_position(self, position: Position) -> bool:
        """
        Check if a position is valid on the board.
        
        Args:
            position: Position to check
            
        Returns:
            True if position is valid
        """
        if position.x < 0 or position.x > self.WIDTH:
            return False
        if position.y < 0 or position.y > self.HEIGHT:
            return False
        
        # Check deployment restrictions
        if position.side == Side.FRIENDLY and position.y > self.MIDLINE:
            return False
        if position.side == Side.ENEMY and position.y < self.MIDLINE:
            return False
        
        return True
    
    def get_nearest_tower(self, position: Position, side: Side) -> Optional[Position]:
        """
        Get the nearest tower position for a given side.
        
        Args:
            position: Position to check from
            side: Which side's towers to consider
            
        Returns:
            Nearest tower position or None
        """
        towers = []
        
        if side == Side.FRIENDLY:
            if self.friendly_towers['left']:
                towers.append(self.FRIENDLY_LEFT_TOWER)
            if self.friendly_towers['right']:
                towers.append(self.FRIENDLY_RIGHT_TOWER)
            if self.friendly_towers['king']:
                towers.append(self.FRIENDLY_KING_TOWER)
        else:
            if self.enemy_towers['left']:
                towers.append(self.ENEMY_LEFT_TOWER)
            if self.enemy_towers['right']:
                towers.append(self.ENEMY_RIGHT_TOWER)
            if self.enemy_towers['king']:
                towers.append(self.ENEMY_KING_TOWER)
        
        if not towers:
            return None
        
        return min(towers, key=lambda t: position.distance_to(t))
    
    def __repr__(self) -> str:
        return f"Board({self.WIDTH}x{self.HEIGHT})"
