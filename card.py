"""
Card class representing Clash Royale cards with their properties.
"""

from enum import Enum
from typing import Optional


class CardType(Enum):
    """Types of cards in Clash Royale."""
    TROOP = "troop"
    SPELL = "spell"
    BUILDING = "building"


class Rarity(Enum):
    """Card rarity levels."""
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class TargetType(Enum):
    """What the card can target."""
    GROUND = "ground"
    AIR = "air"
    BOTH = "both"
    BUILDINGS = "buildings"


class Card:
    """Represents a Clash Royale card with its properties."""
    
    def __init__(
        self,
        name: str,
        card_type: CardType,
        elixir_cost: int,
        rarity: Rarity,
        target_type: TargetType,
        damage: int = 0,
        hit_speed: float = 0.0,
        range_: float = 0.0,
        area_damage: bool = False,
        splash_radius: float = 0.0
    ):
        """
        Initialize a card.
        
        Args:
            name: Card name
            card_type: Type of card (troop, spell, building)
            elixir_cost: Elixir cost to deploy
            rarity: Card rarity
            target_type: What the card can target
            damage: Damage per hit/use
            hit_speed: Time between attacks
            range_: Attack/effect range
            area_damage: Whether card does area damage
            splash_radius: Radius of splash damage
        """
        self.name = name
        self.card_type = card_type
        self.elixir_cost = elixir_cost
        self.rarity = rarity
        self.target_type = target_type
        self.damage = damage
        self.hit_speed = hit_speed
        self.range = range_
        self.area_damage = area_damage
        self.splash_radius = splash_radius
    
    def __repr__(self) -> str:
        return f"Card({self.name}, {self.elixir_cost} elixir, {self.card_type.value})"
    
    def __str__(self) -> str:
        return f"{self.name} ({self.elixir_cost})"


# Predefined common Clash Royale cards
KNIGHT = Card("Knight", CardType.TROOP, 3, Rarity.COMMON, TargetType.GROUND, 
              damage=100, hit_speed=1.1, range_=0.5)
ARCHERS = Card("Archers", CardType.TROOP, 3, Rarity.COMMON, TargetType.BOTH,
               damage=60, hit_speed=1.2, range_=5.0)
GIANT = Card("Giant", CardType.TROOP, 5, Rarity.RARE, TargetType.BUILDINGS,
             damage=120, hit_speed=1.5, range_=0.5)
FIREBALL = Card("Fireball", CardType.SPELL, 4, Rarity.RARE, TargetType.BOTH,
                damage=325, area_damage=True, splash_radius=2.5)
MUSKETEER = Card("Musketeer", CardType.TROOP, 4, Rarity.RARE, TargetType.BOTH,
                 damage=100, hit_speed=1.0, range_=6.0)
MINI_PEKKA = Card("Mini P.E.K.K.A", CardType.TROOP, 4, Rarity.RARE, TargetType.GROUND,
                  damage=400, hit_speed=1.8, range_=0.5)
HOG_RIDER = Card("Hog Rider", CardType.TROOP, 4, Rarity.RARE, TargetType.BUILDINGS,
                 damage=150, hit_speed=1.6, range_=0.5)
WIZARD = Card("Wizard", CardType.TROOP, 5, Rarity.RARE, TargetType.BOTH,
              damage=130, hit_speed=1.4, range_=5.5, area_damage=True, splash_radius=1.5)
CANNON = Card("Cannon", CardType.BUILDING, 3, Rarity.COMMON, TargetType.GROUND,
              damage=60, hit_speed=0.8, range_=5.5)
INFERNO_TOWER = Card("Inferno Tower", CardType.BUILDING, 5, Rarity.RARE, TargetType.BOTH,
                     damage=50, hit_speed=0.4, range_=6.0)

# Card pool for easy access
CARD_POOL = [KNIGHT, ARCHERS, GIANT, FIREBALL, MUSKETEER, MINI_PEKKA, 
             HOG_RIDER, WIZARD, CANNON, INFERNO_TOWER]
