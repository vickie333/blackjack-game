from .deck import Deck
from .hand import Hand

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Hand()
        self.dealer = Hand()
        self.state = "start" 
        self.result = ""
        # configuración simple: rebarajar cuando queden menos del 25% del shoe
        self.penetration_threshold = 0.25
        self.initial_deck_size = self.deck.remaining()

    def reshuffle_if_needed(self):
        # Si las cartas restantes son menos que el umbral, rebarajamos el shoe completo
        if self.deck.remaining() <= int(self.initial_deck_size * self.penetration_threshold):
            self.deck.reset(shuffle=True)

    def deal_initial(self):
        self.player.clear()
        self.dealer.clear()
        self.reshuffle_if_needed()
       
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
        self.reshuffle_if_needed()
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
        # Dealer se planta en cualquier 17 (no hit on soft 17)
        while True:
            dealer_total = self.dealer.total()
            if dealer_total < 17:
                self.reshuffle_if_needed()
                self.dealer.add(self.deck.deal())
                continue
            if dealer_total == 17 and self.dealer.is_soft():
                # Plantarse en soft 17 (cambiar a 'hit' si prefieres H17)
                break
            break
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
