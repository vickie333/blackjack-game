import pygame
import os
from typing import Optional
from .game_logic import Game
from .deck import Card

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "cards")

CARD_W, CARD_H = 96, 132

class PygameUI:
    def __init__(self, width=900, height=600):
        pygame.init()
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Blackjack - Pygame (Repo structure)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 20)
        self.bigfont = pygame.font.SysFont("arial", 28, bold=True)
        self.game = Game()
        self.card_images = {}  
        self.load_card_images()

    def load_card_images(self):
        if not os.path.isdir(ASSETS_DIR):
            return
        for fname in os.listdir(ASSETS_DIR):
            if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                key = os.path.splitext(fname)[0]  
                path = os.path.join(ASSETS_DIR, fname)
                try:
                    img = pygame.image.load(path).convert_alpha()
                    img = pygame.transform.smoothscale(img, (CARD_W, CARD_H))
                    self.card_images[key] = img
                except Exception as e:
                    print("Error cargando imagen", path, e)

    def card_surface(self, card: Card) -> Optional[pygame.Surface]:
        key = card.code()
        return self.card_images.get(key)

    def draw_card(self, card: Card, x: int, y: int, face_up=True):
        surf = self.card_surface(card)
        if surf and face_up:
            self.screen.blit(surf, (x, y))
        else:
            pygame.draw.rect(self.screen, (255,255,255), (x,y,CARD_W,CARD_H), border_radius=8)
            pygame.draw.rect(self.screen, (0,0,0), (x,y,CARD_W,CARD_H), 2, border_radius=8)
            if face_up:
                txt = self.font.render(str(card), True, (0,0,0))
                self.screen.blit(txt, (x+8, y+8))
            else:
                pygame.draw.rect(self.screen, (180,0,0), (x+6,y+6,CARD_W-12,CARD_H-12), border_radius=6)

    def draw(self):
        self.screen.fill((34,139,34))
        self.screen.blit(self.bigfont.render("Crupier", True, (255,255,255)), (50, 20))
        for i, c in enumerate(self.game.dealer.cards):
            face_up = not (self.game.state == "player_turn" and i == 1)
            self.draw_card(c, 50 + i*(CARD_W+12), 60, face_up=face_up)

        self.screen.blit(self.bigfont.render("Jugador", True, (255,255,255)), (50, 220))
        for i, c in enumerate(self.game.player.cards):
            self.draw_card(c, 50 + i*(CARD_W+12), 260, face_up=True)

        player_total = f"Jugador: {self.game.player.total()}"
        dealer_total = f"Crupier: {'?' if self.game.state=='player_turn' else self.game.dealer.total()}"
        self.screen.blit(self.font.render(player_total, True, (255,255,255)), (50, 420))
        self.screen.blit(self.font.render(dealer_total, True, (255,255,255)), (50, 450))

        self.hit_rect = pygame.Rect(50, self.height-80, 120, 40)
        self.stand_rect = pygame.Rect(190, self.height-80, 120, 40)
        self.restart_rect = pygame.Rect(330, self.height-80, 120, 40)
        self.draw_button(self.hit_rect, "Pedir (H)")
        self.draw_button(self.stand_rect, "Plantarse (S)")
        self.draw_button(self.restart_rect, "Reiniciar (R)")

        if self.game.state == "result":
            self.screen.blit(self.bigfont.render(self.game.result, True, (255,255,255)), (500, 300))

        pygame.display.flip()

    def draw_button(self, rect, text):
        pygame.draw.rect(self.screen, (200,200,200), rect, border_radius=6)
        pygame.draw.rect(self.screen, (0,0,0), rect, 2, border_radius=6)
        txt = self.font.render(text, True, (0,0,0))
        self.screen.blit(txt, (rect.x + 8, rect.y + 8))

    def run(self):
        self.game.deal_initial()
        running = True
        while running:
            self.clock.tick(30)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_h and self.game.state == "player_turn":
                        self.game.player_hit()
                    elif ev.key == pygame.K_s and self.game.state == "player_turn":
                        self.game.player_stand()
                    elif ev.key == pygame.K_r:
                        self.game.deal_initial()
                elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    mx,my = ev.pos
                    if self.hit_rect.collidepoint(mx,my) and self.game.state=="player_turn":
                        self.game.player_hit()
                    elif self.stand_rect.collidepoint(mx,my) and self.game.state=="player_turn":
                        self.game.player_stand()
                    elif self.restart_rect.collidepoint(mx,my):
                        self.game.deal_initial()
            self.draw()
        pygame.quit()
