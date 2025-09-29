from .deck import Deck
from .hand import Hand

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Hand()
        self.dealer = Hand()
        self.state = "start" 
        self.result = ""

    def deal_initial(self):
        self.player.clear()
        self.dealer.clear()
        if len(self.deck.cards) < 10:
            self.deck = Deck()
       
        self.player.add(self.deck.deal())
        self.dealer.add(self.deck.deal())
        self.player.add(self.deck.deal())
        self.dealer.add(self.deck.deal())
        self.state = "player_turn"
        self.result = ""
       
        if self.player.is_blackjack() and self.dealer.is_blackjack():
            self.state = "result"
            self.result = "Push: ambos blackjack."
        elif self.player.is_blackjack():
            self.state = "result"
            self.result = "Blackjack! Ganas 1.5x."
        elif self.dealer.is_blackjack():
            self.state = "result"
            self.result = "Dealer tiene Blackjack. Pierdes."

    def player_hit(self):
        if self.state != "player_turn":
            return
        self.player.add(self.deck.deal())
        if self.player.is_bust():
            self.state = "result"
            self.result = "Player busts. Dealer gana."

    def player_stand(self):
        if self.state != "player_turn":
            return
        self.state = "dealer_turn"
        self.dealer_play()

    def dealer_play(self):
        while self.dealer.total() < 17:
            self.dealer.add(self.deck.deal())
        self.evaluate()

    def evaluate(self):
        p, d = self.player.total(), self.dealer.total()
        if d > 21:
            self.result = "Dealer busts. Ganas."
        elif p > d:
            self.result = "Ganas."
        elif p < d:
            self.result = "Dealer gana."
        else:
            self.result = "Push (empate)."
        self.state = "result"
