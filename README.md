# Blackjack (Pygame)

Un juego simple de Blackjack construido con Python y Pygame, pensado para aprender y experimentar con la lógica del juego y una UI 2D básica.

## Requisitos

- Python 3.9+
- Pygame

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

Si no tienes `requirements.txt`, puedes instalar manualmente:

```bash
pip install pygame
```

## Ejecutar

Desde la raíz del repo:

```bash
python run_pygame.py
```

## Controles

- Botones en pantalla:
  - Pedir (H)
  - Plantarse (S)
  - Reiniciar (R)
- Atajos de teclado:
  - H: Pedir carta
  - S: Plantarse
  - R: Repartir nueva mano

## Reglas implementadas (resumen)

- Se reparten 2 cartas al jugador y 2 al crupier (una oculta durante el turno del jugador).
- El jugador puede pedir cartas hasta plantarse o pasarse (>21).
- El crupier roba hasta alcanzar 17 o más y se planta en cualquier 17 (incluye soft 17).
- Blackjack natural detectado (21 con 2 cartas). Mensajes de resultado: victoria, derrota, empate, bust del jugador o del crupier.

## Estructura

- `src/deck.py`: Cartas y mazo (shoe), barajado, reset, valores.
- `src/hand.py`: Mano, cálculo de total, blackjack, bust, soft.
- `src/game_logic.py`: Estados simples del juego y flujo de turnos.
- `src/pygame_ui.py`: Renderizado, botones, entrada de mouse y teclado.
- `run_pygame.py`: Punto de entrada.

## Assets (cartas)

Las imágenes de cartas, si las hay, se buscan en `data/cards`. El juego se ejecuta sin imágenes, mostrando cartas placeholder si faltan assets.


## Licencia

MIT (o la que prefieras).