"""
Polunetsintäalgoritmit haamujen AI:ta varten.
BFS-toteutus next_step-funktiolla ja tunnel-wrap-tuki.
"""
from typing import List, Tuple, Optional, Set
from collections import deque

from level import Level
from constants import ALL_DIRECTIONS, TILE


def next_step(level: Level, start_tile: Tuple[int, int], goal_tile: Tuple[int, int], 
              forbid_reverse_dir: Optional[Tuple[int, int]] = None) -> Optional[Tuple[int, int]]:
    """
    BFS-reitinhaku joka palauttaa seuraavan askeleen kohti kohdetta.
    
    Args:
        level: Taso jossa liikutaan
        start_tile: Aloitusruutu (x, y)
        goal_tile: Kohderuutu (x, y)
        forbid_reverse_dir: Kielletyt suunta (dx, dy) - ei U-käännöstä
        
    Returns:
        Seuraava suunta (dx, dy) tai None jos polkua ei löydy
    """
    if start_tile == goal_tile:
        return None
    
    # BFS-queue: (position, path)
    queue = deque([(start_tile, [start_tile])])
    visited: Set[Tuple[int, int]] = {start_tile}
    
    while queue:
        current, path = queue.popleft()
        
        # Tarkista naapurit prioriteettijärjestyksessä: Up, Left, Down, Right
        for direction in ALL_DIRECTIONS:
            next_tile = (current[0] + direction[0], current[1] + direction[1])
            
            # Tarkista wrap-tunneli
            next_tile = _wrap_tunnel_position(next_tile, level.width, level.height)
            
            if next_tile == goal_tile:
                # Löytyi polku - palauta ensimmäinen suunta
                if len(path) >= 2:
                    first_step = path[1]
                    return (first_step[0] - start_tile[0], first_step[1] - start_tile[1])
                return direction
            
            # Tarkista onko ruutu läpikuljettava
            if (_is_traversable(next_tile, level) and 
                next_tile not in visited and
                (forbid_reverse_dir is None or direction != forbid_reverse_dir)):
                
                visited.add(next_tile)
                queue.append((next_tile, path + [next_tile]))
    
    return None


def _is_traversable(tile: Tuple[int, int], level: Level) -> bool:
    """
    Tarkistaa onko ruutu läpikuljettava (ei seinä).
    
    Args:
        tile: Ruutu (x, y)
        level: Taso
        
    Returns:
        True jos ruutu on läpikuljettava
    """
    x, y = tile
    return level.is_valid_position(x, y)


def _wrap_tunnel_position(tile: Tuple[int, int], width: int, height: int) -> Tuple[int, int]:
    """
    Käsittelee tunnel-wrap:in (vasen/oikea tyhjän läpi).
    
    Args:
        tile: Ruutu (x, y)
        width: Tason leveys
        height: Tason korkeus
        
    Returns:
        Wrapattu positio
    """
    x, y = tile
    
    # Wrap vasemmasta oikealle
    if x < 0:
        x = width - 1
    # Wrap oikealta vasemmalle
    elif x >= width:
        x = 0
    
    return (x, y)


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """
    Laskee Manhattan-etäisyyden kahden pisteen välillä.
    
    Args:
        pos1: Ensimmäinen piste (x, y)
        pos2: Toinen piste (x, y)
        
    Returns:
        Manhattan-etäisyys
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def get_neighbors(pos: Tuple[int, int], level: Level) -> List[Tuple[int, int]]:
    """
    Palauttaa kaikki kelvolliset naapurit annetulle positiolle.
    
    Args:
        pos: Nykyinen positio (x, y)
        level: Taso jossa liikutaan
        
    Returns:
        Lista kelvollisista naapureista
    """
    neighbors = []
    x, y = pos
    
    for dx, dy in ALL_DIRECTIONS:
        new_x, new_y = x + dx, y + dy
        new_pos = _wrap_tunnel_position((new_x, new_y), level.width, level.height)
        if _is_traversable(new_pos, level):
            neighbors.append(new_pos)
    
    return neighbors


def bfs_shortest_path(start: Tuple[int, int], goal: Tuple[int, int], 
                     level: Level) -> Optional[List[Tuple[int, int]]]:
    """
    Breadth-First Search -polunetsintä.
    Löytää lyhimmän polun kahden pisteen välillä.
    
    Args:
        start: Aloituspiste (x, y)
        goal: Maali (x, y)
        level: Taso jossa etsitään polkua
        
    Returns:
        Polku listana koordinaatteja tai None jos polkua ei löydy
    """
    if start == goal:
        return [start]
    
    queue = deque([(start, [start])])
    visited: Set[Tuple[int, int]] = {start}
    
    while queue:
        current, path = queue.popleft()
        
        for neighbor in get_neighbors(current, level):
            if neighbor == goal:
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None  # Polkua ei löytynyt


def get_scatter_direction(current: Tuple[int, int], home_corner: Tuple[int, int], 
                        level: Level) -> Optional[Tuple[int, int]]:
    """
    Palauttaa suunnan hajautumiskulmaa kohti.
    Käytetään haamujen scatter-tilassa.
    
    Args:
        current: Nykyinen positio (x, y)
        home_corner: Haamun kotikulma (x, y)
        level: Taso
        
    Returns:
        Suunta kotikulmaa kohti tai None
    """
    return next_step(level, current, home_corner)


def get_flee_direction(ghost_pos: Tuple[int, int], player_pos: Tuple[int, int], 
                      level: Level) -> Optional[Tuple[int, int]]:
    """
    Palauttaa pakenemissuunnan (vastakkaiseen suuntaan pelaajasta).
    Käytetään frightened-tilassa.
    
    Args:
        ghost_pos: Haamun positio (x, y)
        player_pos: Pelaajan positio (x, y)
        level: Taso
        
    Returns:
        Pakenemissuunta tai None
    """
    # Etsi suunta joka vie kauimmaksi pelaajasta
    best_direction = None
    best_distance = -1
    
    for direction in ALL_DIRECTIONS:
        new_x = ghost_pos[0] + direction[0]
        new_y = ghost_pos[1] + direction[1]
        new_pos = _wrap_tunnel_position((new_x, new_y), level.width, level.height)
        
        if _is_traversable(new_pos, level):
            distance = manhattan_distance(new_pos, player_pos)
            if distance > best_distance:
                best_distance = distance
                best_direction = direction
    
    return best_direction


def is_path_clear(start: Tuple[int, int], end: Tuple[int, int], 
                 level: Level) -> bool:
    """
    Tarkistaa onko suora polku kahden pisteen välillä vapaa.
    
    Args:
        start: Aloituspiste (x, y)
        end: Päätepiste (x, y)
        level: Taso
        
    Returns:
        True jos polku on vapaa
    """
    # Yksinkertainen tarkistus: onko suora linja mahdollinen
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    
    # Tarkista vain suorat linjat (vaakasuora tai pystysuora)
    if dx != 0 and dy != 0:
        return False  # Ei suora linja
    
    if dx == 0 and dy == 0:
        return True  # Sama piste
    
    # Tarkista kaikki väliruudut
    if dx != 0:
        # Vaakasuora liike
        step = 1 if dx > 0 else -1
        for x in range(start[0] + step, end[0] + step, step):
            if not _is_traversable((x, start[1]), level):
                return False
    else:
        # Pystysuora liike
        step = 1 if dy > 0 else -1
        for y in range(start[1] + step, end[1] + step, step):
            if not _is_traversable((start[0], y), level):
                return False
    
    return True