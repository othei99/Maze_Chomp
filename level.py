"""
Tason lataus ja hallinta.
Lukee ASCII-kartan, hallitsee ruudukkoa, pellettejä ja aloituspaikkoja.
Päivitetty power-pellettejä, ghost_home_tile ja wrap-tunneli varten.
"""
import pygame
from typing import List, Tuple, Optional, Set
import os
from constants import (
    TILE, SCALE, WALL_CHAR, PELLET_CHAR, POWER_PELLET_CHAR,
    PLAYER_SPAWN_CHAR, GHOST_SPAWN_CHAR, EMPTY_CHAR, WALL_COLOR,
    PELLET_COLOR, POWER_PELLET_COLOR, PELLET_SIZE, POWER_PELLET_SIZE,
    PELLET_POINTS, POWER_PELLET_POINTS
)
from utils import tile_to_pixels, tile_center_pixels, scale_for_rendering


class Level:
    """Tason tiedot ja toiminnallisuus."""
    
    def __init__(self, level_file: str):
        """
        Alustaa tason lataamalla sen tiedostosta.
        
        Args:
            level_file: Tason tiedoston polku
        """
        self.grid: List[List[str]] = []
        self.width: int = 0
        self.height: int = 0
        self.pellets: Set[Tuple[int, int]] = set()
        self.power_pellets: Set[Tuple[int, int]] = set()
        self.player_spawn: Tuple[int, int] = (0, 0)
        self.ghost_spawns: List[Tuple[int, int]] = []
        
        self._load_level(level_file)
    
    def _load_level(self, level_file: str) -> None:
        """
        Lataa tason tiedostosta.
        
        Args:
            level_file: Tason tiedoston polku
            
        Raises:
            FileNotFoundError: Jos tiedostoa ei löydy
            ValueError: Jos taso on virheellinen
        """
        if not os.path.exists(level_file):
            raise FileNotFoundError(f"Tasotiedostoa ei löydy: {level_file}")
        
        with open(level_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Poista rivinvaihdot ja tyhjät rivit
        lines = [line.rstrip() for line in lines if line.strip()]
        
        if not lines:
            raise ValueError("Taso on tyhjä")
        
        self.height = len(lines)
        self.width = max(len(line) for line in lines)
        
        # Täytä grid ja kerää erikoisruudut
        self.grid = []
        for y, line in enumerate(lines):
            row = []
            # Täytä rivi oikeaan pituuteen
            padded_line = line.ljust(self.width)
            
            for x, char in enumerate(padded_line):
                if char == PLAYER_SPAWN_CHAR:
                    self.player_spawn = (x, y)
                    row.append(EMPTY_CHAR)  # Pelaajan spawn-kohta on tyhjä
                elif char == GHOST_SPAWN_CHAR:
                    self.ghost_spawns.append((x, y))
                    row.append(EMPTY_CHAR)  # Haamun spawn-kohta on tyhjä
                elif char == PELLET_CHAR:
                    self.pellets.add((x, y))
                    row.append(char)
                elif char == POWER_PELLET_CHAR:
                    self.power_pellets.add((x, y))
                    row.append(char)
                else:
                    row.append(char)
            
            self.grid.append(row)
        
        # Validoi taso
        self._validate_level()
    
    def _validate_level(self) -> None:
        """
        Validoi että taso on pelattava.
        
        Raises:
            ValueError: Jos taso on virheellinen
        """
        if not self.player_spawn:
            raise ValueError("Pelaajan aloituspaikkaa ei löydy (P)")
        
        if not self.ghost_spawns:
            raise ValueError("Haamujen aloituspaikkoja ei löydy (G)")
        
        if not self.pellets and not self.power_pellets:
            raise ValueError("Ei pellettejä tasossa")
    
    def is_wall(self, tile_x: int, tile_y: int) -> bool:
        """
        Tarkistaa onko annettu ruutu seinä.
        
        Args:
            tile_x: Ruudun x-koordinaatti
            tile_y: Ruudun y-koordinaatti
            
        Returns:
            True jos ruutu on seinä
        """
        if (tile_x < 0 or tile_x >= self.width or 
            tile_y < 0 or tile_y >= self.height):
            return True
        
        return self.grid[tile_y][tile_x] == WALL_CHAR
    
    def is_valid_position(self, tile_x: int, tile_y: int) -> bool:
        """
        Tarkistaa onko annettu ruutu kelvollinen sijainti (ei seinä).
        
        Args:
            tile_x: Ruudun x-koordinaatti
            tile_y: Ruudun y-koordinaatti
            
        Returns:
            True jos ruutu on kelvollinen
        """
        return not self.is_wall(tile_x, tile_y)
    
    def eat_pellet_at(self, tile_x: int, tile_y: int) -> Tuple[int, str]:
        """
        Syö pelletin annetusta ruudusta.
        
        Args:
            tile_x: Ruudun x-koordinaatti
            tile_y: Ruudun y-koordinaatti
            
        Returns:
            Tuple (pisteet, tyyppi) - (0, "") jos ei pellettejä
        """
        pos = (tile_x, tile_y)
        
        if pos in self.pellets:
            self.pellets.remove(pos)
            self.grid[tile_y][tile_x] = EMPTY_CHAR
            return (PELLET_POINTS, "pellet")
        
        if pos in self.power_pellets:
            self.power_pellets.remove(pos)
            self.grid[tile_y][tile_x] = EMPTY_CHAR
            return (POWER_PELLET_POINTS, "power")
        
        return (0, "")
    
    def pellets_left(self) -> int:
        """
        Palauttaa jäljellä olevien pellettien määrän.
        
        Returns:
            Pellettien määrä
        """
        return len(self.pellets) + len(self.power_pellets)
    
    def get_player_spawn(self) -> Tuple[int, int]:
        """
        Palauttaa pelaajan aloituspaikan.
        
        Returns:
            Aloituspaikka ruutukoordinaateissa (x, y)
        """
        return self.player_spawn
    
    def get_ghost_spawns(self) -> List[Tuple[int, int]]:
        """
        Palauttaa haamujen aloituspaikat.
        
        Returns:
            Lista aloituspaikoista ruutukoordinaateissa
        """
        return self.ghost_spawns.copy()
    
    def ghost_home_tile(self) -> Tuple[int, int]:
        """
        Palauttaa haamujen kotiruudun (ghost house).
        Käytetään EATEN-tilassa palaamiseen.
        
        Returns:
            Kotiruutu (x, y)
        """
        # Etsi keskihuoneen keskipiste
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Jos keskiruutu on seinä, etsi lähin tyhjä ruutu
        if self.is_wall(center_x, center_y):
            # Etsi ympyrässä lähin tyhjä ruutu
            for radius in range(1, max(self.width, self.height)):
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        if abs(dx) == radius or abs(dy) == radius:  # Ympyrän kehä
                            x, y = center_x + dx, center_y + dy
                            if (0 <= x < self.width and 0 <= y < self.height and 
                                not self.is_wall(x, y)):
                                return (x, y)
        
        return (center_x, center_y)
    
    def to_pixels(self, tile_x: int, tile_y: int) -> Tuple[float, float]:
        """
        Muuntaa ruutukoordinaatit pikselikoordinaateiksi.
        
        Args:
            tile_x: Ruudun x-koordinaatti
            tile_y: Ruudun y-koordinaatti
            
        Returns:
            Pikselikoordinaatit (x, y)
        """
        return tile_to_pixels(tile_x, tile_y)
    
    def draw_walls(self, surface: pygame.Surface) -> None:
        """
        Piirtää tason seinät.
        
        Args:
            surface: Pinta jolle piirretään
        """
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == WALL_CHAR:
                    # Laske piirtopositio
                    pixel_x, pixel_y = tile_to_pixels(x, y)
                    render_x, render_y = scale_for_rendering(pixel_x, pixel_y)
                    
                    # Piirrä seinä
                    wall_rect = pygame.Rect(
                        render_x, render_y,
                        TILE * SCALE, TILE * SCALE
                    )
                    pygame.draw.rect(surface, WALL_COLOR, wall_rect)
    
    def draw_pellets(self, surface: pygame.Surface) -> None:
        """
        Piirtää tason pelletit.
        
        Args:
            surface: Pinta jolle piirretään
        """
        # Piirrä tavalliset pelletit
        for x, y in self.pellets:
            center_x, center_y = tile_center_pixels(x, y)
            render_x, render_y = scale_for_rendering(center_x, center_y)
            
            pygame.draw.circle(
                surface, PELLET_COLOR, 
                (render_x, render_y), 
                PELLET_SIZE * SCALE
            )
        
        # Piirrä power-pelletit
        for x, y in self.power_pellets:
            center_x, center_y = tile_center_pixels(x, y)
            render_x, render_y = scale_for_rendering(center_x, center_y)
            
            pygame.draw.circle(
                surface, POWER_PELLET_COLOR,
                (render_x, render_y),
                POWER_PELLET_SIZE * SCALE
            )
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Piirtää koko tason.
        
        Args:
            surface: Pinta jolle piirretään
        """
        self.draw_walls(surface)
        self.draw_pellets(surface)
    
    def set_active_ghosts(self, num_ghosts: int) -> None:
        """
        Asettaa aktiivisten haamujen määrän ja muuttaa ylimääräiset spawn-paikat pelleteiksi.
        
        Args:
            num_ghosts: Aktiivisten haamujen määrä
        """
        # Muuta ylimääräiset ghost-spawn-paikat pelleteiksi
        for i in range(num_ghosts, len(self.ghost_spawns)):
            ghost_x, ghost_y = self.ghost_spawns[i]
            # Vaihda grid-merkki pelletiksi
            self.grid[ghost_y][ghost_x] = PELLET_CHAR
            # Lisää pelletit-settiin
            self.pellets.add((ghost_x, ghost_y))
    
    def reset_pellets(self) -> None:
        """
        Palauttaa kaikki pelletit takaisin tasoon.
        Käytetään uuden tason aloittamisessa.
        """
        self.pellets.clear()
        self.power_pellets.clear()
        
        # Käy läpi grid ja kerää pelletit uudelleen
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == PELLET_CHAR:
                    self.pellets.add((x, y))
                elif self.grid[y][x] == POWER_PELLET_CHAR:
                    self.power_pellets.add((x, y))