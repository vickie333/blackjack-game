class Card:
    def __init__(self,rank):
        self.rank = rank

    def obtener_valor(self):
        if self.rank in range(2,11):
            return self.rank
        elif self.rank in ["J","Q","K"]:
            return 10
        elif self.rank == "A":
            return 1

class Hand:
    def __init__(self):
        self.hand = []

    def add_card(self,card):
        self.hand.append(card)

    def calculate_score(self):
        total = 0
        num_aces = 0
        for card in self.hand:
            value = card.obtener_valor()

            total += value
            if card.rank == "A":
                num_aces += 1

        if num_aces > 0 and total + 10 <= 21:
            return total + 10
        return total

    def is_blackjack(self):
        return len(self.hand) == 2 and self.calculate_score() == 21

    def is_bust(self):
        return self.calculate_score() > 21
        

class Deck:
    def __init__(self):
        self.deck = []

    def shuffle(self):
        