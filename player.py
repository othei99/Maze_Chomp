"""
Pelaajan liike ja logiikka.
Käsittelee syötteet, liikkeen ruudukossa ja törmäykset.
Päivitetty power-pelletin syöminen ja signaali varten.
"""
import pygame
from typing import Tuple, Optional, Callable
from constants import (
    PLAYER_COLOR, PLAYER_SPEED, TILE, SCALE,
    DIRECTION_NONE, DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT
)
from utils import (
    pixels_to_tile, tile_center_pixels, is_near_tile_center, 
    snap_to_tile_center, scale_for_rendering, wrap_position
)
from level import Level


class Player:
    """Pelaajan hahmo ja sen toiminnallisuus."""
    
    def __init__(self, start_x: int, start_y: int):
        """
        Alustaa pelaajan.
        
        Args:
            start_x: Aloitus x-koordinaatti ruutuina
            start_y: Aloitus y-koordinaatti ruutuina
        """
        # Sijoita pelaaja ruudun keskelle
        center_x, center_y = tile_center_pixels(start_x, start_y)
        self.x: float = center_x
        self.y: float = center_y
        
        # Nykyinen ja haluttu liikkumissuunta
        self.current_direction: Tuple[int, int] = DIRECTION_NONE
        self.desired_direction: Tuple[int, int] = DIRECTION_NONE
        
        # Nopeus
        self.speed: float = PLAYER_SPEED
        
        # Pelaajan koko renderöintiä varten
        self.radius: int = 6
        
        # Power-pelletin signaalifunktio
        self.power_pellet_callback: Optional[Callable[[], None]] = None
    
    def set_power_pellet_callback(self, callback: Callable[[], None]) -> None:
        """
        Asettaa power-pelletin signaalifunktion.
        
        Args:
            callback: Funktio joka kutsutaan kun power-pellet syödään
        """
        self.power_pellet_callback = callback
    
    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """
        Käsittelee pelaajan syötteet.
        
        Args:
            keys: Pygame:n näppäimistön tila
        """
        # Tallenna haluttu suunta syötteen perusteella
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.desired_direction = DIRECTION_UP
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.desired_direction = DIRECTION_DOWN
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.desired_direction = DIRECTION_LEFT
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.desired_direction = DIRECTION_RIGHT
    
    def update(self, dt: float, level: Level) -> Tuple[int, str]:
        """
        Päivittää pelaajan tilan.
        
        Args:
            dt: Aikaerotus sekunteina
            level: Nykyinen taso
            
        Returns:
            Tuple (pisteet, pellet_tyyppi) - (0, "") jos ei pellettejä syöty
        """
        points_earned = 0
        pellet_type = ""
        
        # Tarkista nykyinen ruutu
        current_tile_x, current_tile_y = pixels_to_tile(self.x, self.y)
        
        # Tarkista voiko vaihtaa suuntaa
        if (self.desired_direction != DIRECTION_NONE and 
            self.desired_direction != self.current_direction):
            
            # Jos ollaan lähellä ruudun keskustaa, tarkista voiko vaihtaa suuntaa
            if is_near_tile_center(self.x, self.y, current_tile_x, current_tile_y):
                next_tile_x = current_tile_x + self.desired_direction[0]
                next_tile_y = current_tile_y + self.desired_direction[1]
                
                if level.is_valid_position(next_tile_x, next_tile_y):
                    # Keskitä position ja vaihda suuntaa
                    self.x, self.y = tile_center_pixels(current_tile_x, current_tile_y)
                    self.current_direction = self.desired_direction
        
        # Liiku nykyiseen suuntaan
        if self.current_direction != DIRECTION_NONE:
            # Laske uusi positio
            move_x = self.current_direction[0] * self.speed * dt
            move_y = self.current_direction[1] * self.speed * dt
            
            new_x = self.x + move_x
            new_y = self.y + move_y
            
            # Tarkista törmäys seinään - tarkista myös ruudun rajat
            new_tile_x, new_tile_y = pixels_to_tile(new_x, new_y)
            
            # Tarkista että kohderuutu on kelvollinen
            can_move = level.is_valid_position(new_tile_x, new_tile_y)
            
            # Jos liikutaan ruudun rajojen yli, tarkista myös kohderuutu
            if can_move and (new_tile_x != current_tile_x or new_tile_y != current_tile_y):
                # Varmista että kohderuutu on todella kelvollinen
                can_move = level.is_valid_position(new_tile_x, new_tile_y)
            
            if can_move:
                # Liike on laillinen
                self.x = new_x
                self.y = new_y
                
                # Käsittele tunneli (wrap around)
                self.x, self.y = wrap_position(self.x, self.y, level.width, level.height)
                
            else:
                # Törmäys seinään - keskitä nykyiseen ruutuun ja pysähdy
                current_center_x, current_center_y = tile_center_pixels(current_tile_x, current_tile_y)
                self.x = current_center_x
                self.y = current_center_y
                self.current_direction = DIRECTION_NONE
        
        # Tarkista onko pelaaja ruudun keskellä ja syö pelletti
        final_tile_x, final_tile_y = pixels_to_tile(self.x, self.y)
        if is_near_tile_center(self.x, self.y, final_tile_x, final_tile_y):
            points_earned, pellet_type = level.eat_pellet_at(final_tile_x, final_tile_y)
            
            # Jos power-pellet syöty, kutsu signaalifunktio
            if pellet_type == "power" and self.power_pellet_callback:
                self.power_pellet_callback()
        
        return (points_earned, pellet_type)
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Piirtää pelaajan.
        
        Args:
            surface: Pinta jolle piirretään
        """
        # Skaalaa positio renderöintiä varten
        render_x, render_y = scale_for_rendering(self.x, self.y)
        
        # Piirrä pelaaja ympyränä
        pygame.draw.circle(
            surface, PLAYER_COLOR,
            (render_x, render_y),
            self.radius * SCALE
        )
        
        # Lisää "suu" osoittamaan liikkumissuuntaan
        if self.current_direction != DIRECTION_NONE:
            # Laske suun positio
            mouth_offset = 4 * SCALE
            mouth_x = render_x + self.current_direction[0] * mouth_offset
            mouth_y = render_y + self.current_direction[1] * mouth_offset
            
            # Piirrä pieni musta ympyrä suuksi
            pygame.draw.circle(
                surface, (0, 0, 0),
                (mouth_x, mouth_y),
                2 * SCALE
            )
    
    def get_position(self) -> Tuple[float, float]:
        """
        Palauttaa pelaajan nykyisen position.
        
        Returns:
            Position (x, y) pikseleinä
        """
        return (self.x, self.y)
    
    def get_tile_position(self) -> Tuple[int, int]:
        """
        Palauttaa pelaajan nykyisen ruutuposition.
        
        Returns:
            Position (tile_x, tile_y) ruutuina
        """
        return pixels_to_tile(self.x, self.y)
    
    def get_direction(self) -> Tuple[int, int]:
        """
        Palauttaa pelaajan nykyisen liikkumissuunnan.
        
        Returns:
            Liikkumissuunta (dx, dy)
        """
        return self.current_direction
    
    def reset_position(self, start_x: int, start_y: int) -> None:
        """
        Palauttaa pelaajan aloituspaikkaan.
        
        Args:
            start_x: Aloitus x-koordinaatti ruutuina
            start_y: Aloitus y-koordinaatti ruutuina
        """
        center_x, center_y = tile_center_pixels(start_x, start_y)
        self.x = center_x
        self.y = center_y
        self.current_direction = DIRECTION_NONE
        self.desired_direction = DIRECTION_NONE
    
    def set_speed_multiplier(self, multiplier: float) -> None:
        """
        Asettaa nopeuskertoimem (esim. tason mukaan).
        
        Args:
            multiplier: Nopeuskerroin (1.0 = normaali)
        """
        self.speed = PLAYER_SPEED * multiplier
    
    def is_moving(self) -> bool:
        """
        Tarkistaa liikkuuko pelaaja.
        
        Returns:
            True jos pelaaja liikkuu
        """
        return self.current_direction != DIRECTION_NONE