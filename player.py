"""
Player class managing deck, hand, and elixir.
"""

from typing import List
from card import Card


class Player:
    """Represents a Clash Royale player with their deck and resources."""
    
    MAX_ELIXIR = 10
    STARTING_ELIXIR = 5
    HAND_SIZE = 4
    
    def __init__(self, deck: List[Card], name: str = "Player"):
        """
        Initialize a player.
        
        Args:
            deck: List of 8 cards in the player's deck
            name: Player name
        """
        if len(deck) != 8:
            raise ValueError("Deck must contain exactly 8 cards")
        
        self.name = name
        self.deck = deck
        self.elixir = self.STARTING_ELIXIR
        
        # Initialize hand with first 4 cards
        self.hand = deck[:self.HAND_SIZE]
        self.next_card_index = self.HAND_SIZE
    
    def can_play_card(self, card: Card) -> bool:
        """
        Check if player has enough elixir to play a card.
        
        Args:
            card: Card to check
            
        Returns:
            True if card can be played
        """
        return self.elixir >= card.elixir_cost and card in self.hand
    
    def play_card(self, card: Card) -> bool:
        """
        Play a card from hand, spending elixir and cycling deck.
        
        Args:
            card: Card to play
            
        Returns:
            True if card was successfully played
        """
        if not self.can_play_card(card):
            return False
        
        # Spend elixir
        self.elixir -= card.elixir_cost
        
        # Remove card from hand and add next card from deck
        card_index = self.hand.index(card)
        self.hand[card_index] = self.deck[self.next_card_index % 8]
        self.next_card_index += 1
        
        return True
    
    def add_elixir(self, amount: float):
        """
        Add elixir, capping at max.
        
        Args:
            amount: Amount of elixir to add
        """
        self.elixir = min(self.elixir + amount, self.MAX_ELIXIR)
    
    def get_playable_cards(self) -> List[Card]:
        """
        Get list of cards in hand that can be played.
        
        Returns:
            List of playable cards
        """
        return [card for card in self.hand if self.elixir >= card.elixir_cost]
    
    def get_average_elixir(self) -> float:
        """
        Calculate average elixir cost of deck.
        
        Returns:
            Average elixir cost
        """
        return sum(card.elixir_cost for card in self.deck) / len(self.deck)
    
    def __repr__(self) -> str:
        return f"Player({self.name}, {self.elixir}/{self.MAX_ELIXIR} elixir)"
    
    def __str__(self) -> str:
        hand_str = ", ".join(str(card) for card in self.hand)
        return f"{self.name}: [{hand_str}] ({self.elixir:.1f} elixir)"
