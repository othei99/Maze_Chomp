"""
Pelin vakiot ja asetukset.
Sisältää värit, mitat, nopeudet ja muut pelimekaniikan vakiot.
"""
from typing import Tuple

# Ikkunan ja ruudukon mitat
TILE: int = 16  # Logiikan ruutukoko pikseleinä
SCALE: int = 2  # Skaalauskerroin renderöintiin (pienennetty)
HUD_HEIGHT: int = 40  # HUD:in korkeus
WINDOW_WIDTH: int = 22 * TILE * SCALE  # 704 pikseliä
WINDOW_HEIGHT: int = 18 * TILE * SCALE + HUD_HEIGHT  # 576 + 40 = 616 pikseliä
FPS: int = 60

# Värit (RGB)
BLACK: Tuple[int, int, int] = (0, 0, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
YELLOW: Tuple[int, int, int] = (255, 255, 0)
BLUE: Tuple[int, int, int] = (0, 0, 255)
RED: Tuple[int, int, int] = (255, 0, 0)
PINK: Tuple[int, int, int] = (255, 184, 255)
CYAN: Tuple[int, int, int] = (0, 255, 255)
ORANGE: Tuple[int, int, int] = (255, 165, 0)
GREEN: Tuple[int, int, int] = (0, 255, 0)

# Seinien väri
WALL_COLOR: Tuple[int, int, int] = BLUE

# Pellettien värit ja koot
PELLET_COLOR: Tuple[int, int, int] = WHITE
POWER_PELLET_COLOR: Tuple[int, int, int] = WHITE
PELLET_SIZE: int = 2
POWER_PELLET_SIZE: int = 8

# Hahmojen värit
PLAYER_COLOR: Tuple[int, int, int] = YELLOW
GHOST_COLORS: list[Tuple[int, int, int]] = [RED, PINK, CYAN, ORANGE]

# FRIGHTENED-tilan värit
FRIGHTENED_BLUE: Tuple[int, int, int] = (0, 0, 255)
FRIGHTENED_BLINK: Tuple[int, int, int] = (255, 255, 255)

# Nopeudet (pikseliä sekunnissa skaalaamattomassa avaruudessa)
PLAYER_SPEED: float = 60.0
GHOST_SPEED_CHASE: float = 55.0
GHOST_SPEED_SCATTER: float = 55.0
GHOST_SPEED_FRIGHT: float = 40.0
GHOST_SPEED_EATEN: float = 100.0
SPEED_INCREASE_PER_LEVEL: float = 0.05  # 5% nopeuslisäys per taso

# Tilakestot (sekunteina)
FRIGHTENED_DURATION: float = 6.0
FRIGHTENED_BLINK_LAST: float = 2.0

# Globaali moodi-aikataulu Level 1
MODE_SCHEDULE_LEVEL_1: list[Tuple[str, float]] = [
    ("SCATTER", 7.0),
    ("CHASE", 20.0),
    ("SCATTER", 7.0),
    ("CHASE", 20.0),
    ("SCATTER", 5.0),
    ("CHASE", 20.0),
    ("SCATTER", 5.0),
    ("CHASE", 9999.0)
]

# Pisteet
PELLET_POINTS: int = 10
POWER_PELLET_POINTS: int = 50
GHOST_CHAIN_POINTS: list[int] = [200, 400, 800, 1600]

# Pelaajan aloitusarvot
INITIAL_LIVES: int = 3

# Fonttikoko
FONT_SIZE: int = 24
HUD_FONT_SIZE: int = 20

# Suunnat (dx, dy)
DIRECTION_NONE: Tuple[int, int] = (0, 0)
DIRECTION_UP: Tuple[int, int] = (0, -1)
DIRECTION_DOWN: Tuple[int, int] = (0, 1)
DIRECTION_LEFT: Tuple[int, int] = (-1, 0)
DIRECTION_RIGHT: Tuple[int, int] = (1, 0)

# Kaikki suunnat listana
ALL_DIRECTIONS: list[Tuple[int, int]] = [
    DIRECTION_UP, DIRECTION_LEFT, DIRECTION_DOWN, DIRECTION_RIGHT
]

# Tunnelin sijainnit (y-koordinaatti)
TUNNEL_Y: int = 10

# Tarkkuus liikkeen keskittämiseen
SNAP_THRESHOLD: float = 2.0  # Pikseliä

# Kartan merkit
WALL_CHAR: str = '#'
PELLET_CHAR: str = '.'
POWER_PELLET_CHAR: str = 'o'
PLAYER_SPAWN_CHAR: str = 'P'
GHOST_SPAWN_CHAR: str = 'G'
EMPTY_CHAR: str = ' '

# Törmäysetäisyys
COLLISION_DISTANCE: float = TILE * 0.6

# Ghost-ketjupisteiden näyttöaika
GHOST_POINTS_DISPLAY_TIME: float = 1.0