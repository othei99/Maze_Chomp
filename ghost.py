"""
Haamujen AI ja liike.
Toteutettu tilakone ja persoonat (Blinky, Pinky).
"""
import pygame
import random
from enum import Enum
from typing import Tuple, List, Optional
from constants import (
    GHOST_COLORS, TILE, SCALE, FRIGHTENED_BLUE, FRIGHTENED_BLINK,
    GHOST_SPEED_CHASE, GHOST_SPEED_SCATTER, GHOST_SPEED_FRIGHT, GHOST_SPEED_EATEN,
    DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT, ALL_DIRECTIONS,
    FRIGHTENED_DURATION, FRIGHTENED_BLINK_LAST
)
from utils import (
    pixels_to_tile, tile_center_pixels, is_near_tile_center,
    get_opposite_direction, scale_for_rendering
)
from level import Level
from pathfinding import next_step, get_flee_direction


class GhostMode(Enum):
    """Haamun käyttäytymistilat."""
    SCATTER = "scatter"      # Hajautuva liike
    CHASE = "chase"          # Jahtaa pelaajaa
    FRIGHTENED = "frightened"  # Pelkää (power-pelletin jälkeen)
    EATEN = "eaten"          # Syöty, palaa kotiin


class Ghost:
    """Haamun hahmo ja sen AI."""
    
    def __init__(self, start_x: int, start_y: int, color_index: int = 0, personality: str = "blinky"):
        """
        Alustaa haamun.
        
        Args:
            start_x: Aloitus x-koordinaatti ruutuina
            start_y: Aloitus y-koordinaatti ruutuina
            color_index: Värin indeksi GHOST_COLORS-listasta
            personality: Haamun persoona ("blinky", "pinky", "clyde", "inky")
        """
        # Sijoita haamun ruudun keskelle
        center_x, center_y = tile_center_pixels(start_x, start_y)
        self.x: float = center_x
        self.y: float = center_y
        
        # Aloituspaikka (respawn-kohtaa varten)
        self.spawn_x: int = start_x
        self.spawn_y: int = start_y
        
        # Liikkumissuunta
        self.direction: Tuple[int, int] = random.choice(ALL_DIRECTIONS)
        self.desired_direction: Tuple[int, int] = self.direction
        
        # Väri ja persoona
        self.color = GHOST_COLORS[color_index % len(GHOST_COLORS)]
        self.personality = personality
        
        # AI-tila
        self.mode: GhostMode = GhostMode.SCATTER
        
        # Nopeuskerroin
        self.speed_multiplier: float = 1.0
        
        # Ajastimet
        self.fright_timer: float = 0.0
        self.eaten_home_timer: float = 0.0
        
        # Haamun koko renderöintiä varten
        self.radius: int = 6
        
        # Suunnanvaihtoajastin (estää liian tiheät käännökset)
        self.direction_change_timer: float = 0.0
        self.min_direction_change_interval: float = 0.1  # sekuntia
    
    def current_speed(self) -> float:
        """
        Palauttaa nykyisen nopeuden tilan mukaan.
        
        Returns:
            Nopeus pikseleinä sekunnissa
        """
        base_speed = 0.0
        if self.mode == GhostMode.FRIGHTENED:
            base_speed = GHOST_SPEED_FRIGHT
        elif self.mode == GhostMode.EATEN:
            base_speed = GHOST_SPEED_EATEN
        elif self.mode == GhostMode.SCATTER:
            base_speed = GHOST_SPEED_SCATTER
        else:  # CHASE
            base_speed = GHOST_SPEED_CHASE
        
        return base_speed * self.speed_multiplier
    
    def update(self, dt: float, level: Level, player_pos: Tuple[float, float], 
               player_direction: Tuple[int, int], global_mode: str) -> None:
        """
        Päivittää haamun tilan ja liikkeen.
        
        Args:
            dt: Aikaerotus sekunteina
            level: Nykyinen taso
            player_pos: Pelaajan positio (x, y)
            player_direction: Pelaajan liikkumissuunta (dx, dy)
            global_mode: Globaali moodi ("SCATTER" tai "CHASE")
        """
        # Päivitä ajastimet
        self.direction_change_timer -= dt
        
        if self.mode == GhostMode.FRIGHTENED:
            self.fright_timer -= dt
            if self.fright_timer <= 0:
                # FRIGHTENED loppuu - palaa SCATTER/CHASE
                self.mode = GhostMode.SCATTER if global_mode == "SCATTER" else GhostMode.CHASE
                self.fright_timer = 0.0
        
        if self.mode == GhostMode.EATEN:
            self.eaten_home_timer -= dt
            if self.eaten_home_timer <= 0:
                # Palauta haamu
                self.mode = GhostMode.SCATTER if global_mode == "SCATTER" else GhostMode.CHASE
                self.eaten_home_timer = 0.0
        
        # Tarkista nykyinen ruutu
        current_tile_x, current_tile_y = pixels_to_tile(self.x, self.y)
        
        # Jos ollaan lähellä ruudun keskustaa, voi vaihtaa suuntaa
        if (is_near_tile_center(self.x, self.y, current_tile_x, current_tile_y) and
            self.direction_change_timer <= 0):
            
            new_direction = self._choose_direction(level, current_tile_x, current_tile_y, 
                                                 player_pos, player_direction, global_mode)
            if new_direction != self.direction:
                # Keskitä positio ja vaihda suuntaa
                self.x, self.y = tile_center_pixels(current_tile_x, current_tile_y)
                self.direction = new_direction
                self.direction_change_timer = self.min_direction_change_interval
        
        # Liiku nykyiseen suuntaan
        speed = self.current_speed()
        move_x = self.direction[0] * speed * dt
        move_y = self.direction[1] * speed * dt
        
        new_x = self.x + move_x
        new_y = self.y + move_y
        
        # Tarkista törmäys seinään
        new_tile_x, new_tile_y = pixels_to_tile(new_x, new_y)
        
        if level.is_valid_position(new_tile_x, new_tile_y):
            # Liike on laillinen
            self.x = new_x
            self.y = new_y
        else:
            # Törmäys seinään - pakota suunnanvaihto
            self.x, self.y = tile_center_pixels(current_tile_x, current_tile_y)
            self.direction_change_timer = 0  # Salli välitön suunnanvaihto
    
    def _choose_direction(self, level: Level, tile_x: int, tile_y: int, 
                         player_pos: Tuple[float, float], player_direction: Tuple[int, int],
                         global_mode: str) -> Tuple[int, int]:
        """
        Valitsee haamulle uuden suunnan tilan mukaan.
        
        Args:
            level: Nykyinen taso
            tile_x: Haamun nykyinen x-ruutu
            tile_y: Haamun nykyinen y-ruutu
            player_pos: Pelaajan positio
            player_direction: Pelaajan liikkumissuunta
            global_mode: Globaali moodi
            
        Returns:
            Uusi liikkumissuunta (dx, dy)
        """
        current_pos = (tile_x, tile_y)
        
        if self.mode == GhostMode.FRIGHTENED:
            return self._frightened_behavior(level, current_pos, player_pos)
        elif self.mode == GhostMode.EATEN:
            return self._eaten_behavior(level, current_pos)
        elif self.mode == GhostMode.SCATTER:
            return self._scatter_behavior(level, current_pos)
        else:  # CHASE
            return self._chase_behavior(level, current_pos, player_pos, player_direction)
    
    def _scatter_behavior(self, level: Level, current_pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Hajautumiskäyttäytyminen - liiku kotikulmaan.
        
        Args:
            level: Nykyinen taso
            current_pos: Nykyinen positio (x, y)
            
        Returns:
            Suositeltava suunta
        """
        # Haetaan kotikulma persoonan mukaan
        home_corner = self._get_home_corner(level)
        direction = next_step(level, current_pos, home_corner, 
                            get_opposite_direction(self.direction))
        
        if direction is None:
            # Jos ei löydy polkua, valitse satunnainen kelvollinen suunta
            return self._get_random_valid_direction(level, current_pos)
        
        return direction
    
    def _chase_behavior(self, level: Level, current_pos: Tuple[int, int], 
                       player_pos: Tuple[float, float], player_direction: Tuple[int, int]) -> Tuple[int, int]:
        """
        Jahtauskäyttäytyminen - liiku kohti kohdetta.
        
        Args:
            level: Nykyinen taso
            current_pos: Nykyinen positio (x, y)
            player_pos: Pelaajan positio
            player_direction: Pelaajan liikkumissuunta
            
        Returns:
            Suositeltava suunta
        """
        # Haetaan kohde persoonan mukaan
        target = self._get_chase_target(player_pos, player_direction, level)
        direction = next_step(level, current_pos, target, 
                            get_opposite_direction(self.direction))
        
        if direction is None:
            # Jos ei löydy polkua, valitse satunnainen kelvollinen suunta
            return self._get_random_valid_direction(level, current_pos)
        
        return direction
    
    def _frightened_behavior(self, level: Level, current_pos: Tuple[int, int], 
                           player_pos: Tuple[float, int]) -> Tuple[int, int]:
        """
        Pelkäävä käyttäytyminen - liiku satunnaisesti.
        
        Args:
            level: Nykyinen taso
            current_pos: Nykyinen positio (x, y)
            player_pos: Pelaajan positio
            
        Returns:
            Suositeltava suunta
        """
        # Yritä ensin pakenemissuuntaa
        flee_dir = get_flee_direction(current_pos, 
                                    (int(player_pos[0] // TILE), int(player_pos[1] // TILE)), 
                                    level)
        
        if flee_dir is not None:
            return flee_dir
        
        # Jos ei pakenemissuuntaa, valitse satunnainen
        return self._get_random_valid_direction(level, current_pos)
    
    def _eaten_behavior(self, level: Level, current_pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Syödyn haamun käyttäytyminen - liiku kotiin.
        
        Args:
            level: Nykyinen taso
            current_pos: Nykyinen positio (x, y)
            
        Returns:
            Suositeltava suunta
        """
        home_tile = level.ghost_home_tile()
        direction = next_step(level, current_pos, home_tile)
        
        if direction is None:
            # Jos ei löydy polkua, valitse satunnainen kelvollinen suunta
            return self._get_random_valid_direction(level, current_pos)
        
        return direction
    
    def _get_home_corner(self, level: Level) -> Tuple[int, int]:
        """
        Palauttaa haamun kotikulman persoonan mukaan.
        
        Args:
            level: Nykyinen taso
            
        Returns:
            Kotikulma (x, y)
        """
        if self.personality == "blinky":
            return (level.width - 1, 0)  # Ylä-oikea
        elif self.personality == "pinky":
            return (0, 0)  # Ylä-vasen
        else:
            return (0, level.height - 1)  # Alhaan-vasen (placeholder)
    
    def _get_chase_target(self, player_pos: Tuple[float, float], player_direction: Tuple[int, int], 
                         level: Level) -> Tuple[int, int]:
        """
        Palauttaa jahtauskohteen persoonan mukaan.
        
        Args:
            player_pos: Pelaajan positio
            player_direction: Pelaajan liikkumissuunta
            level: Nykyinen taso
            
        Returns:
            Jahtauskohde (x, y)
        """
        player_tile = (int(player_pos[0] // TILE), int(player_pos[1] // TILE))
        
        if self.personality == "blinky":
            # Blinky: suoraan pelaajan perässä
            return player_tile
        elif self.personality == "pinky":
            # Pinky: 4 ruutua pelaajan toivottuun suuntaan
            target_x = player_tile[0] + player_direction[0] * 4
            target_y = player_tile[1] + player_direction[1] * 4
            return (target_x, target_y)
        else:
            # Placeholder: satunnainen kohde
            return player_tile
    
    def _get_random_valid_direction(self, level: Level, current_pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Valitsee satunnaisen kelvollisen suunnan.
        
        Args:
            level: Nykyinen taso
            current_pos: Nykyinen positio (x, y)
            
        Returns:
            Satunnainen kelvollinen suunta
        """
        possible_directions = []
        
        for direction in ALL_DIRECTIONS:
            next_tile_x = current_pos[0] + direction[0]
            next_tile_y = current_pos[1] + direction[1]
            
            if level.is_valid_position(next_tile_x, next_tile_y):
                # Vältä U-käännöstä paitsi jos pakko
                if direction != get_opposite_direction(self.direction):
                    possible_directions.append(direction)
        
        # Jos ei muita vaihtoehtoja, salli U-käännös
        if not possible_directions:
            opposite = get_opposite_direction(self.direction)
            next_tile_x = current_pos[0] + opposite[0]
            next_tile_y = current_pos[1] + opposite[1]
            
            if level.is_valid_position(next_tile_x, next_tile_y):
                possible_directions.append(opposite)
        
        # Jos vieläkään ei vaihtoehtoja, pysy paikallaan
        if not possible_directions:
            return self.direction
        
        return random.choice(possible_directions)
    
    def set_frightened(self) -> None:
        """Asettaa haamun FRIGHTENED-tilaan."""
        if self.mode != GhostMode.EATEN:
            self.mode = GhostMode.FRIGHTENED
            self.fright_timer = FRIGHTENED_DURATION
            # Käännä suunta välittömästi
            self.direction = get_opposite_direction(self.direction)
            self.direction_change_timer = 0
    
    def set_eaten(self) -> None:
        """Asettaa haamun EATEN-tilaan."""
        self.mode = GhostMode.EATEN
        self.eaten_home_timer = 3.0  # 3 sekuntia kotiin palaamiseen
        self.fright_timer = 0.0
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Piirtää haamun.
        
        Args:
            surface: Pinta jolle piirretään
        """
        # Skaalaa positio renderöintiä varten
        render_x, render_y = scale_for_rendering(self.x, self.y)
        
        # Määritä väri tilan mukaan
        if self.mode == GhostMode.FRIGHTENED:
            # Vilkkuva sininen/valkoinen viimeisillä sekunneilla
            if self.fright_timer <= FRIGHTENED_BLINK_LAST:
                blink_speed = 0.2  # Vilkkuu 5 kertaa sekunnissa
                if int(self.fright_timer / blink_speed) % 2 == 0:
                    color = FRIGHTENED_BLUE
                else:
                    color = FRIGHTENED_BLINK
            else:
                color = FRIGHTENED_BLUE
        elif self.mode == GhostMode.EATEN:
            # Syödyn haamun väri (himmeä)
            color = (self.color[0] // 3, self.color[1] // 3, self.color[2] // 3)
        else:
            color = self.color
        
        # Piirrä haamun runko ympyränä
        pygame.draw.circle(
            surface, color,
            (render_x, render_y),
            self.radius * SCALE
        )
        
        # Piirrä silmät (ei EATEN-tilassa)
        if self.mode != GhostMode.EATEN:
            eye_size = 2 * SCALE
            eye_offset_x = 2 * SCALE
            eye_offset_y = 2 * SCALE
            
            # Vasen silmä
            pygame.draw.circle(
                surface, (255, 255, 255),
                (render_x - eye_offset_x, render_y - eye_offset_y),
                eye_size
            )
            
            # Oikea silmä
            pygame.draw.circle(
                surface, (255, 255, 255),
                (render_x + eye_offset_x, render_y - eye_offset_y),
                eye_size
            )
            
            # Piirrä silmämunat (pienet mustat pisteet)
            pupil_size = 1 * SCALE
            pygame.draw.circle(
                surface, (0, 0, 0),
                (render_x - eye_offset_x, render_y - eye_offset_y),
                pupil_size
            )
            pygame.draw.circle(
                surface, (0, 0, 0),
                (render_x + eye_offset_x, render_y - eye_offset_y),
                pupil_size
            )
    
    def get_position(self) -> Tuple[float, float]:
        """
        Palauttaa haamun nykyisen position.
        
        Returns:
            Positio (x, y) pikseleinä
        """
        return (self.x, self.y)
    
    def get_tile_position(self) -> Tuple[int, int]:
        """
        Palauttaa haamun nykyisen ruutuposition.
        
        Returns:
            Positio (tile_x, tile_y) ruutuina
        """
        return pixels_to_tile(self.x, self.y)
    
    def reset_position(self) -> None:
        """Palauttaa haamun aloituspaikkaan."""
        center_x, center_y = tile_center_pixels(self.spawn_x, self.spawn_y)
        self.x = center_x
        self.y = center_y
        self.direction = random.choice(ALL_DIRECTIONS)
        self.desired_direction = self.direction
        self.direction_change_timer = 0.0
        self.mode = GhostMode.SCATTER
        self.fright_timer = 0.0
        self.eaten_home_timer = 0.0
    
    def set_mode(self, mode: GhostMode) -> None:
        """
        Asettaa haamun käyttäytymistilan.
        
        Args:
            mode: Uusi käyttäytymistila
        """
        if mode != self.mode:
            self.mode = mode
            # Käännä suunta kun moodi vaihtuu
            self.direction = get_opposite_direction(self.direction)
            self.direction_change_timer = 0
    
    def set_speed_multiplier(self, multiplier: float) -> None:
        """
        Asettaa nopeuskertoimem (esim. tason mukaan).
        
        Args:
            multiplier: Nopeuskerroin (1.0 = normaali)
        """
        self.speed_multiplier = multiplier