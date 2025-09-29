import random
from dataclasses import dataclass
from typing import List

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
VALUE_MAP = {**{str(i): i for i in range(2, 11)}, "J":10, "Q":10, "K":10, "A":1}

@dataclass
class Card:
    rank: str
    suit: str

    def value(self) -> int:
        return VALUE_MAP[self.rank]

    def code(self) -> str:
        """Código identificador útil para mapear a una imagen, ej: 'A_spades'"""
        suit_map = {"♠":"spades","♥":"hearts","♦":"diamonds","♣":"clubs"}
        return f"{self.rank}_{suit_map[self.suit]}"

    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self, shuffle: bool = True, num_decks: int = 1):
        self.cards: List[Card] = []
        for _ in range(num_decks):
            for s in SUITS:
                for r in RANKS:
                    self.cards.append(Card(r, s))
        if shuffle:
            self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self) -> Card:
        if not self.cards:
            self.__init__(shuffle=True)
        return self.cards.pop()
