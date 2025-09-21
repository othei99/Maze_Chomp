"""
Apufunktiot ruudukkokäsittelyyn ja vektorilaskentaan.
Sisältää koordinaattimuunnokset ja liikkeen apufunktiot.
"""
import math
from typing import Tuple
from constants import TILE, SCALE, SNAP_THRESHOLD


def tile_to_pixels(tile_x: int, tile_y: int) -> Tuple[float, float]:
    """
    Muuntaa ruutukoordinaatit pikselikoordinaateiksi.
    
    Args:
        tile_x: Ruudun x-koordinaatti
        tile_y: Ruudun y-koordinaatti
        
    Returns:
        Pikselikoordinaatit (x, y)
    """
    return (tile_x * TILE, tile_y * TILE)


def pixels_to_tile(pixel_x: float, pixel_y: float) -> Tuple[int, int]:
    """
    Muuntaa pikselikoordinaatit ruutukoordinaateiksi.
    
    Args:
        pixel_x: Pikselin x-koordinaatti
        pixel_y: Pikselin y-koordinaatti
        
    Returns:
        Ruutukoordinaatit (tile_x, tile_y)
    """
    return (int(pixel_x // TILE), int(pixel_y // TILE))


def tile_center_pixels(tile_x: int, tile_y: int) -> Tuple[float, float]:
    """
    Palauttaa ruudun keskipisteen pikselikoordinaateissa.
    
    Args:
        tile_x: Ruudun x-koordinaatti
        tile_y: Ruudun y-koordinaatti
        
    Returns:
        Ruudun keskipisteen koordinaatit (x, y)
    """
    center_x = tile_x * TILE + TILE // 2
    center_y = tile_y * TILE + TILE // 2
    return (float(center_x), float(center_y))


def is_near_tile_center(pixel_x: float, pixel_y: float, tile_x: int, tile_y: int) -> bool:
    """
    Tarkistaa onko pikselipositio lähellä ruudun keskustaa.
    
    Args:
        pixel_x: Nykyinen x-koordinaatti
        pixel_y: Nykyinen y-koordinaatti
        tile_x: Kohderuudun x-koordinaatti
        tile_y: Kohderuudun y-koordinaatti
        
    Returns:
        True jos lähellä keskustaa
    """
    center_x, center_y = tile_center_pixels(tile_x, tile_y)
    distance = math.sqrt((pixel_x - center_x) ** 2 + (pixel_y - center_y) ** 2)
    return distance <= SNAP_THRESHOLD


def snap_to_tile_center(pixel_x: float, pixel_y: float) -> Tuple[float, float]:
    """
    Keskittää position lähimpään ruudun keskustaan.
    
    Args:
        pixel_x: Nykyinen x-koordinaatti
        pixel_y: Nykyinen y-koordinaatti
        
    Returns:
        Keskitetyt koordinaatit (x, y)
    """
    tile_x, tile_y = pixels_to_tile(pixel_x, pixel_y)
    return tile_center_pixels(tile_x, tile_y)


def distance_to_tile_center(pixel_x: float, pixel_y: float) -> float:
    """
    Laskee etäisyyden lähimpään ruudun keskustaan.
    
    Args:
        pixel_x: Nykyinen x-koordinaatti
        pixel_y: Nykyinen y-koordinaatti
        
    Returns:
        Etäisyys pikseleinä
    """
    center_x, center_y = snap_to_tile_center(pixel_x, pixel_y)
    return math.sqrt((pixel_x - center_x) ** 2 + (pixel_y - center_y) ** 2)


def add_vectors(v1: Tuple[float, float], v2: Tuple[float, float]) -> Tuple[float, float]:
    """
    Laskee kahden vektorin summan.
    
    Args:
        v1: Ensimmäinen vektori (x, y)
        v2: Toinen vektori (x, y)
        
    Returns:
        Vektorien summa (x, y)
    """
    return (v1[0] + v2[0], v1[1] + v2[1])


def scale_vector(vector: Tuple[float, float], scale: float) -> Tuple[float, float]:
    """
    Skaalaa vektorin annetulla kertoimella.
    
    Args:
        vector: Skaalattava vektori (x, y)
        scale: Skaalaustekijä
        
    Returns:
        Skaalattu vektori (x, y)
    """
    return (vector[0] * scale, vector[1] * scale)


def normalize_vector(vector: Tuple[float, float]) -> Tuple[float, float]:
    """
    Normalisoi vektorin pituudeksi 1.
    
    Args:
        vector: Normalisoitava vektori (x, y)
        
    Returns:
        Normalisoitu vektori (x, y), tai (0, 0) jos alkuperäinen oli nollavektori
    """
    length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    if length == 0:
        return (0.0, 0.0)
    return (vector[0] / length, vector[1] / length)


def get_opposite_direction(direction: Tuple[int, int]) -> Tuple[int, int]:
    """
    Palauttaa vastakkaisen suunnan.
    
    Args:
        direction: Alkuperäinen suunta (dx, dy)
        
    Returns:
        Vastakkainen suunta (-dx, -dy)
    """
    return (-direction[0], -direction[1])


def scale_for_rendering(x: float, y: float) -> Tuple[int, int]:
    """
    Skaalaa koordinaatit renderöintiä varten.
    
    Args:
        x: X-koordinaatti skaalaamattomassa avaruudessa
        y: Y-koordinaatti skaalaamattomassa avaruudessa
        
    Returns:
        Skaalatut koordinaatit renderöintiä varten
    """
    return (int(x * SCALE), int(y * SCALE))


def wrap_position(x: float, y: float, level_width: int, level_height: int) -> Tuple[float, float]:
    """
    Käärii position tunnelin läpi tarvittaessa.
    
    Args:
        x: X-koordinaatti
        y: Y-koordinaatti  
        level_width: Tason leveys ruutuina
        level_height: Tason korkeus ruutuina
        
    Returns:
        Käärittyt koordinaatit (x, y)
    """
    # Vain horisontaalinen kääriminen tunnelissa
    if x < 0:
        x = (level_width - 1) * TILE + TILE // 2
    elif x >= level_width * TILE:
        x = TILE // 2
    
    return (x, y)
