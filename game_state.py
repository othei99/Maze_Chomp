"""
Pelin tilakone.
Hallitsee eri pelitiloja: menu, pelaaminen, game over.
Integroitu kaikki uudet ominaisuudet: power-pelletit, haamujen tilakone, törmäykset.
"""
import pygame
import math
from abc import ABC, abstractmethod
from typing import Optional, Tuple
from enum import Enum

from constants import (
    BLACK, INITIAL_LIVES, SPEED_INCREASE_PER_LEVEL, COLLISION_DISTANCE,
    WINDOW_WIDTH, WINDOW_HEIGHT, MODE_SCHEDULE_LEVEL_1, FRIGHTENED_DURATION
)
from level import Level
from player import Player
from ghost import Ghost, GhostMode
from hud import HUD
from audio import AudioManager


class GameStateType(Enum):
    """Pelitilat."""
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    VICTORY = "victory"
    COMPLETE_VICTORY = "complete_victory"
    PAUSED = "paused"


class GameState(ABC):
    """Abstrakti pelitilaluokka."""
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> Optional[GameStateType]:
        """
        Käsittelee tapahtumat.
        
        Args:
            event: Pygame-tapahtuma
            
        Returns:
            Uusi pelitila tai None jos ei muutosta
        """
        pass
    
    @abstractmethod
    def update(self, dt: float) -> Optional[GameStateType]:
        """
        Päivittää tilan.
        
        Args:
            dt: Aikaerotus sekunteina
            
        Returns:
            Uusi pelitila tai None jos ei muutosta
        """
        pass
    
    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """
        Renderöi tilan.
        
        Args:
            surface: Pinta jolle renderöidään
        """
        pass


class MenuState(GameState):
    """Päävalikkotila."""
    
    def __init__(self, hud: HUD, audio: AudioManager):
        """
        Alustaa valikkotilan.
        
        Args:
            hud: HUD-objekti
            audio: Audiomanageri
        """
        self.hud = hud
        self.audio = audio
    
    def handle_event(self, event: pygame.event.Event) -> Optional[GameStateType]:
        """Käsittelee valikon tapahtumat."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.audio.play_menu_select()
                return GameStateType.PLAYING
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        
        return None
    
    def update(self, dt: float) -> Optional[GameStateType]:
        """Päivittää valikkotilaa."""
        return None
    
    def render(self, surface: pygame.Surface) -> None:
        """Renderöi valikon."""
        surface.fill(BLACK)
        self.hud.draw_menu(surface)


class PlayState(GameState):
    """Pelaamistila."""
    
    def __init__(self, hud: HUD, audio: AudioManager):
        """
        Alustaa pelitilan.
        
        Args:
            hud: HUD-objekti
            audio: Audiomanageri
        """
        self.hud = hud
        self.audio = audio
        self.level: Optional[Level] = None
        self.player: Optional[Player] = None
        self.ghosts: list[Ghost] = []
        
        # Pelitiedot
        self.score: int = 0
        self.lives: int = INITIAL_LIVES
        self.current_level: int = 1
        
        # Tauon tila
        self.paused: bool = False
        
        # Globaali moodiajastin
        self.mode_timer: float = 0.0
        self.mode_schedule: list[Tuple[str, float]] = MODE_SCHEDULE_LEVEL_1.copy()
        self.current_mode: str = "SCATTER"
        self.mode_index: int = 0
        
        # Ghost-ketjupisteet
        self.ghost_chain_count: int = 0
        
        # Lataa ensimmäinen taso
        self._load_level()
    
    def _load_level(self) -> None:
        """Lataa nykyisen tason."""
        try:
            # Lataa taso (tässä MVP:ssä aina sama taso)
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            level_file = os.path.join(script_dir, "level1", "level1.txt")
            self.level = Level(level_file)
            
            # Luo pelaaja
            spawn_x, spawn_y = self.level.get_player_spawn()
            self.player = Player(spawn_x, spawn_y)
            
            # Aseta power-pelletin signaalifunktio
            self.player.set_power_pellet_callback(self._on_power_pellet_eaten)
            
            # Aseta nopeus tason mukaan
            speed_multiplier = 1.0 + (self.current_level - 1) * SPEED_INCREASE_PER_LEVEL
            self.player.set_speed_multiplier(speed_multiplier)
            
            # Luo haamut (määrä kasvaa tason mukaan)
            self.ghosts = []
            ghost_spawns = self.level.get_ghost_spawns()
            personalities = ["blinky", "pinky", "clyde", "inky"]
            
            # Haamujen määrä: Level 1 = 1 haamu, Level 2 = 2 haamua, jne.
            # Maksimissaan niin monta kuin spawn-paikkoja on
            max_ghosts = min(self.current_level, len(ghost_spawns))
            
            for i in range(max_ghosts):
                ghost_x, ghost_y = ghost_spawns[i]
                personality = personalities[i % len(personalities)]
                ghost = Ghost(ghost_x, ghost_y, i, personality)
                ghost.set_speed_multiplier(speed_multiplier)
                self.ghosts.append(ghost)
            
            print(f"Level {self.current_level}: Created {len(self.ghosts)} ghosts")
            
            # Aseta aktiivisten haamujen määrä (ylimääräiset spawn-paikat muuttuvat pelleteiksi)
            self.level.set_active_ghosts(len(self.ghosts))
            
            # Nollaa moodiajastin
            self.mode_timer = 0.0
            self.mode_index = 0
            self.current_mode = self.mode_schedule[0][0]
            self.ghost_chain_count = 0
                
        except Exception as e:
            print(f"Error loading level: {e}")
            # Return to menu if loading fails
            return
    
    def _on_power_pellet_eaten(self) -> None:
        """Kutsutaan kun power-pellet syödään."""
        # Toista power-pellet ääni
        self.audio.play_power_pellet()
        self.audio.play_frightened()
        
        # Aseta kaikki haamut FRIGHTENED-tilaan
        for ghost in self.ghosts:
            if ghost.mode != GhostMode.EATEN:
                ghost.set_frightened()
        
        # Nollaa ghost-ketjupisteet
        self.ghost_chain_count = 0
    
    def _update_mode_timer(self, dt: float) -> None:
        """Päivittää globaalin moodiajastimen."""
        self.mode_timer += dt
        
        # Tarkista pitääkö vaihtaa moodia
        if self.mode_index < len(self.mode_schedule):
            current_duration = self.mode_schedule[self.mode_index][1]
            
            if self.mode_timer >= current_duration:
                # Vaihda moodia
                self.mode_timer = 0.0
                self.mode_index += 1
                
                if self.mode_index < len(self.mode_schedule):
                    new_mode = self.mode_schedule[self.mode_index][0]
                    if new_mode != self.current_mode:
                        self.current_mode = new_mode
                        # Käännä kaikkien haamujen suunta
                        for ghost in self.ghosts:
                            if ghost.mode in [GhostMode.SCATTER, GhostMode.CHASE]:
                                ghost.set_mode(GhostMode.SCATTER if new_mode == "SCATTER" else GhostMode.CHASE)
    
    def _check_collisions(self) -> Optional[GameStateType]:
        """Tarkistaa törmäykset pelaajan ja haamujen välillä."""
        if not self.player:
            return None
        
        player_pos = self.player.get_position()
        
        for ghost in self.ghosts:
            ghost_pos = ghost.get_position()
            
            # Laske etäisyys
            distance = math.sqrt(
                (player_pos[0] - ghost_pos[0])**2 + 
                (player_pos[1] - ghost_pos[1])**2
            )
            
            if distance < COLLISION_DISTANCE:
                if ghost.mode == GhostMode.FRIGHTENED:
                    # Syö haamu
                    self._eat_ghost(ghost)
                elif ghost.mode not in [GhostMode.EATEN]:
                    # Pelaaja kuolee
                    game_over = self._player_die()
                    if game_over == GameStateType.GAME_OVER:
                        return game_over
        
        return None
    
    def _eat_ghost(self, ghost: Ghost) -> None:
        """Syö haamun ja anna pisteet."""
        # Toista haamun syömisen ääni
        self.audio.play_eat_ghost(self.ghost_chain_count + 1)
        
        # Aseta haamu EATEN-tilaan
        ghost.set_eaten()
        
        # Anna ketjupisteet
        if self.ghost_chain_count < len([200, 400, 800, 1600]):
            points = [200, 400, 800, 1600][self.ghost_chain_count]
            self.score += points
            
            # Lisää ghost-pisteiden näyttö
            ghost_tile = ghost.get_tile_position()
            from utils import tile_center_pixels, scale_for_rendering
            center_x, center_y = tile_center_pixels(ghost_tile[0], ghost_tile[1])
            render_x, render_y = scale_for_rendering(center_x, center_y)
            self.hud.add_ghost_points(render_x, render_y, self.ghost_chain_count)
            
            self.ghost_chain_count += 1
    
    def _player_die(self) -> GameStateType:
        """Pelaaja kuolee."""
        # Toista kuoleman ääni
        self.audio.play_death()
        
        self.lives -= 1
        
        if self.lives <= 0:
            # Game over
            return GameStateType.GAME_OVER
        
        # Respawn pelaaja ja haamut
        if self.level and self.player:
            spawn_x, spawn_y = self.level.get_player_spawn()
            self.player.reset_position(spawn_x, spawn_y)
            
            # Resetoi haamut
            for ghost in self.ghosts:
                ghost.reset_position()
            
            # Nollaa FRIGHTENED ja ketjupisteet
            self.ghost_chain_count = 0
            for ghost in self.ghosts:
                if ghost.mode == GhostMode.FRIGHTENED:
                    ghost.mode = GhostMode.SCATTER
                    ghost.fright_timer = 0.0
            
            # Resetoi moodiajastin
            self.mode_timer = 0.0
            self.mode_index = 0
            self.current_mode = self.mode_schedule[0][0]
        
        return None
    
    def handle_event(self, event: pygame.event.Event) -> Optional[GameStateType]:
        """Käsittelee pelitilan tapahtumat."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return GameStateType.MENU
            elif event.key == pygame.K_SPACE:
                self.paused = not self.paused
        
        return None
    
    def update(self, dt: float) -> Optional[GameStateType]:
        """Päivittää pelitilaa."""
        if self.paused or not self.level or not self.player:
            return None
        
        # Päivitä HUD
        self.hud.update(dt)
        
        # Päivitä moodiajastin
        self._update_mode_timer(dt)
        
        # Käsittele pelaajan syöte
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        # Päivitä pelaaja
        points_earned, pellet_type = self.player.update(dt, self.level)
        
        # Toista ääni jos pelletti syötiin
        if points_earned > 0 and pellet_type == "normal":
            self.audio.play_pellet()
        
        self.score += points_earned
        
        # Päivitä haamut
        player_pos = self.player.get_position()
        player_direction = self.player.get_direction()
        for ghost in self.ghosts:
            ghost.update(dt, self.level, player_pos, player_direction, self.current_mode)
        
        # Tarkista törmäykset
        collision_result = self._check_collisions()
        if collision_result == GameStateType.GAME_OVER:
            return collision_result
        
        # Tarkista voittoehdot
        if self.level.pellets_left() == 0:
            # Taso läpäisty!
            self.audio.play_level_complete()
            
            if self.current_level >= 6:
                # Peli läpäisty kokonaan!
                return GameStateType.COMPLETE_VICTORY
            else:
                # Siirry seuraavaan tasoon
                self.current_level += 1
                self._load_level()  # Lataa seuraava taso
                return GameStateType.VICTORY
        
        return None
    
    def render(self, surface: pygame.Surface) -> None:
        """Renderöi pelitilan."""
        # Tyhjennä tausta
        surface.fill(BLACK)
        
        if not self.level or not self.player:
            return
        
        # Piirrä taso HUD:in alapuolelle
        # Luo väliaikainen surface pelialueelle
        game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - 40))
        game_surface.fill(BLACK)
        
        # Piirrä kaikki pelielementit game_surface:lle
        self.level.draw(game_surface)
        self.player.draw(game_surface)
        for ghost in self.ghosts:
            ghost.draw(game_surface)
        
        # Piirrä ghost-pisteet game_surface:lle (pelialueella)
        for display in self.hud.ghost_points_displays:
            display.draw(game_surface, self.hud.font)
        
        # Siirrä game_surface pääsurfacelle HUD:in alapuolelle
        surface.blit(game_surface, (0, 40))
        
        # Piirrä HUD (ilman ghost-pisteitä, koska ne piirrettiin jo)
        self.hud.draw(surface, self.score, self.lives, self.current_level, 
                     self.level.pellets_left(), self.current_mode)
        
        # Piirrä tauko-overlay tarvittaessa
        if self.paused:
            self.hud.draw_pause(surface)
    
    
    def reset_game(self) -> None:
        """Nollaa pelin alkutilaan."""
        self.score = 0
        self.lives = INITIAL_LIVES
        self.current_level = 1
        self.paused = False
        self.ghost_chain_count = 0
        self._load_level()


class GameOverState(GameState):
    """Game over -tila."""
    
    def __init__(self, hud: HUD, audio: AudioManager, final_score: int):
        """
        Alustaa game over -tilan.
        
        Args:
            hud: HUD-objekti
            audio: Audiomanageri
            final_score: Lopulliset pisteet
        """
        self.hud = hud
        self.audio = audio
        self.final_score = final_score
    
    def handle_event(self, event: pygame.event.Event) -> Optional[GameStateType]:
        """Käsittelee game over -tilan tapahtumat."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.audio.play_menu_select()
                return GameStateType.PLAYING
            elif event.key == pygame.K_ESCAPE:
                self.audio.play_menu_select()
                return GameStateType.MENU
        
        return None
    
    def update(self, dt: float) -> Optional[GameStateType]:
        """Päivittää game over -tilaa."""
        return None
    
    def render(self, surface: pygame.Surface) -> None:
        """Renderöi game over -näytön."""
        surface.fill(BLACK)
        self.hud.draw_game_over(surface, self.final_score)


class VictoryState(GameState):
    """Voittonäytön tila."""
    
    def __init__(self, hud: HUD, audio: AudioManager, score: int, level: int):
        """
        Alustaa voittotilan.
        
        Args:
            hud: HUD-objekti
            audio: Audiomanageri
            score: Nykyiset pisteet
            level: Läpäisty taso
        """
        self.hud = hud
        self.audio = audio
        self.score = score
        self.level = level
        self.display_time = 0.0
        self.min_display_time = 2.0  # Näytä vähintään 2 sekuntia
    
    def handle_event(self, event: pygame.event.Event) -> Optional[GameStateType]:
        """Käsittelee voittotilan tapahtumat."""
        if (event.type == pygame.KEYDOWN and 
            event.key == pygame.K_RETURN and 
            self.display_time >= self.min_display_time):
            return GameStateType.PLAYING
        
        return None
    
    def update(self, dt: float) -> Optional[GameStateType]:
        """Päivittää voittotilaa."""
        self.display_time += dt
        
        # Automaattinen siirtyminen jos tarpeeksi aikaa kulunut
        if self.display_time >= 5.0:  # 5 sekunnin jälkeen automaattisesti
            return GameStateType.PLAYING
        
        return None
    
    def render(self, surface: pygame.Surface) -> None:
        """Renderöi voittonäytön."""
        surface.fill(BLACK)
        self.hud.draw_victory(surface, self.score, self.level)


class CompleteVictoryState(GameState):
    """Koko pelin läpäisemisen tila."""
    
    def __init__(self, hud: HUD, audio: AudioManager, final_score: int):
        """
        Alustaa koko pelin voittotilan.
        
        Args:
            hud: HUD-objekti
            audio: Audiomanageri
            final_score: Lopulliset pisteet
        """
        self.hud = hud
        self.audio = audio
        self.final_score = final_score
    
    def handle_event(self, event: pygame.event.Event) -> Optional[GameStateType]:
        """Käsittelee koko pelin voittotilan tapahtumat."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return GameStateType.PLAYING
            elif event.key == pygame.K_ESCAPE:
                return GameStateType.MENU
        
        return None
    
    def update(self, dt: float) -> Optional[GameStateType]:
        """Päivittää koko pelin voittotilaa."""
        return None
    
    def render(self, surface: pygame.Surface) -> None:
        """Renderöi koko pelin voittonäytön."""
        surface.fill(BLACK)
        self.hud.draw_complete_victory(surface, self.final_score)


class GameStateManager:
    """Pelitilojen hallinta."""
    
    def __init__(self):
        """Alustaa tilamanagerin."""
        self.hud = HUD()
        self.audio = AudioManager()
        self.current_state: GameState = MenuState(self.hud, self.audio)
        self.play_state: Optional[PlayState] = None
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Käsittelee tapahtumat.
        
        Args:
            event: Pygame-tapahtuma
        """
        new_state_type = self.current_state.handle_event(event)
        if new_state_type:
            self._change_state(new_state_type)
    
    def update(self, dt: float) -> None:
        """
        Päivittää nykyisen tilan.
        
        Args:
            dt: Aikaerotus sekunteina
        """
        new_state_type = self.current_state.update(dt)
        if new_state_type:
            self._change_state(new_state_type)
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Renderöi nykyisen tilan.
        
        Args:
            surface: Pinta jolle renderöidään
        """
        self.current_state.render(surface)
    
    def _change_state(self, new_state_type: GameStateType) -> None:
        """
        Vaihtaa pelitilaa.
        
        Args:
            new_state_type: Uusi pelitila
        """
        if new_state_type == GameStateType.MENU:
            self.current_state = MenuState(self.hud, self.audio)
            
        elif new_state_type == GameStateType.PLAYING:
            if isinstance(self.current_state, MenuState):
                # Uusi peli
                self.play_state = PlayState(self.hud, self.audio)
                self.current_state = self.play_state
            elif isinstance(self.current_state, (GameOverState, CompleteVictoryState)):
                # Uudelleenaloitus
                if self.play_state:
                    self.play_state.reset_game()
                    self.current_state = self.play_state
                else:
                    self.play_state = PlayState(self.hud, self.audio)
                    self.current_state = self.play_state
            elif isinstance(self.current_state, VictoryState):
                # Jatka samaa peliä
                if self.play_state:
                    self.current_state = self.play_state
                    
        elif new_state_type == GameStateType.GAME_OVER:
            if self.play_state:
                self.current_state = GameOverState(self.hud, self.audio, self.play_state.score)
                
        elif new_state_type == GameStateType.VICTORY:
            if self.play_state:
                self.current_state = VictoryState(
                    self.hud, self.audio, self.play_state.score, self.play_state.current_level - 1
                )
                
        elif new_state_type == GameStateType.COMPLETE_VICTORY:
            if self.play_state:
                self.current_state = CompleteVictoryState(self.hud, self.audio, self.play_state.score)