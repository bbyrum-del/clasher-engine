"""
Clash Royale Engine - A chess-like engine for Clash Royale card game.

This package provides a strategic engine for analyzing Clash Royale gameplay,
similar to how chess engines work. It evaluates card placements and suggests
optimal moves based on game state.
"""

__version__ = "1.0.0"
__author__ = "Clasher Engine Team"

from card import Card, CardType, Rarity, TargetType, CARD_POOL
from board import Board, Position, Side
from move import Move
from player import Player
from engine import ClashRoyaleEngine

__all__ = [
    'Card',
    'CardType',
    'Rarity',
    'TargetType',
    'Board',
    'Position',
    'Side',
    'Move',
    'Player',
    'ClashRoyaleEngine',
    'CARD_POOL'
]
