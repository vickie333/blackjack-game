from typing import List
from .deck import Card

class Hand:
    def __init__(self):
        self.cards: List[Card] = []

    def add(self, card: Card):
        self.cards.append(card)

    def clear(self):
        self.cards = []

    def total(self) -> int:
        total = sum(c.value() for c in self.cards)
        num_aces = sum(1 for c in self.cards if c.rank == "A")
        if num_aces > 0 and total + 10 <= 21:
            total += 10
        return total

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.total() == 21

    def is_bust(self) -> bool:
        return self.total() > 21
