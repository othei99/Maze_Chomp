"""
HUD (Head-Up Display) - käyttöliittymän näyttö.
Näyttää pisteet, elämät, tason numeron ja muut pelitiedot.
Päivitetty moodin ja ghost-ketjupisteiden näyttämiseen.
"""
import pygame
from typing import Optional, List, Tuple
from constants import WHITE, YELLOW, HUD_FONT_SIZE, WINDOW_WIDTH, GHOST_CHAIN_POINTS, GHOST_POINTS_DISPLAY_TIME


class GhostPointsDisplay:
    """Ghost-ketjupisteiden näyttö."""
    
    def __init__(self, x: int, y: int, points: int, chain_count: int):
        """
        Alustaa ghost-pisteiden näytön.
        
        Args:
            x: X-koordinaatti
            y: Y-koordinaatti
            points: Näytettävät pisteet
            chain_count: Ketjun numero (0-3)
        """
        self.x = x
        self.y = y
        self.points = points
        self.chain_count = chain_count
        self.timer = GHOST_POINTS_DISPLAY_TIME
        self.alpha = 255
    
    def update(self, dt: float) -> bool:
        """
        Päivittää näytön.
        
        Args:
            dt: Aikaerotus sekunteina
            
        Returns:
            True jos näyttö on vielä aktiivinen
        """
        self.timer -= dt
        if self.timer <= 0:
            return False
        
        # Fade out viimeisellä sekunnilla
        if self.timer <= 1.0:
            self.alpha = int(255 * (self.timer / 1.0))
        
        return True
    
    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """
        Piirtää ghost-pisteet.
        
        Args:
            surface: Pinta jolle piirretään
            font: Käytettävä fontti
        """
        if self.alpha <= 0:
            return
        
        text = f"{self.points}"
        text_surface = font.render(text, True, YELLOW)
        text_surface.set_alpha(self.alpha)
        
        # Keskitä teksti
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        surface.blit(text_surface, text_rect)


class HUD:
    """Pelin HUD-näyttö."""
    
    def __init__(self):
        """Alustaa HUD:in."""
        # Alusta fontti
        pygame.font.init()
        self.font: pygame.font.Font = pygame.font.Font(None, HUD_FONT_SIZE)
        
        # HUD:in korkeus
        self.height: int = 40
        
        # Tekstien värit
        self.text_color = WHITE
        self.score_color = YELLOW
        
        # Ghost-ketjupisteiden näytöt
        self.ghost_points_displays: List[GhostPointsDisplay] = []
    
    def add_ghost_points(self, x: int, y: int, chain_count: int) -> None:
        """
        Lisää ghost-ketjupisteiden näytön.
        
        Args:
            x: X-koordinaatti
            y: Y-koordinaatti
            chain_count: Ketjun numero (0-3)
        """
        if 0 <= chain_count < len(GHOST_CHAIN_POINTS):
            points = GHOST_CHAIN_POINTS[chain_count]
            display = GhostPointsDisplay(x, y, points, chain_count)
            self.ghost_points_displays.append(display)
    
    def update(self, dt: float) -> None:
        """
        Päivittää HUD:in.
        
        Args:
            dt: Aikaerotus sekunteina
        """
        # Päivitä ghost-pisteiden näytöt
        self.ghost_points_displays = [
            display for display in self.ghost_points_displays 
            if display.update(dt)
        ]
    
    def draw(self, surface: pygame.Surface, score: int, lives: int, level: int, 
             pellets_left: int = 0, current_mode: str = "SCATTER") -> None:
        """
        Piirtää HUD:in.
        
        Args:
            surface: Pinta jolle piirretään
            score: Nykyiset pisteet
            lives: Jäljellä olevat elämät
            level: Nykyinen taso
            pellets_left: Jäljellä olevien pellettien määrä
            current_mode: Nykyinen moodi (SCATTER/CHASE/FRIGHT)
        """
        # Piirrä HUD:in tausta
        hud_rect = pygame.Rect(0, 0, WINDOW_WIDTH, self.height)
        pygame.draw.rect(surface, (0, 0, 0), hud_rect)
        
        # Piirrä raja-viiva HUD:in alle
        pygame.draw.line(surface, WHITE, (0, self.height), (WINDOW_WIDTH, self.height), 2)
        
        # Score (left)
        score_text = f"SCORE: {score:06d}"
        score_surface = self.font.render(score_text, True, self.score_color)
        surface.blit(score_surface, (10, 10))
        
        # Lives (center left)
        lives_text = f"LIVES: {lives}"
        lives_surface = self.font.render(lives_text, True, self.text_color)
        lives_x = 200
        surface.blit(lives_surface, (lives_x, 10))
        
        # Level (center)
        level_text = f"LEVEL: {level}"
        level_surface = self.font.render(level_text, True, self.text_color)
        level_x = WINDOW_WIDTH // 2 - level_surface.get_width() // 2
        surface.blit(level_surface, (level_x, 10))
        
        # Pellets remaining (right top)
        if pellets_left > 0:
            pellets_text = f"PELLETS: {pellets_left}"
            pellets_surface = self.font.render(pellets_text, True, self.text_color)
            pellets_x = WINDOW_WIDTH - pellets_surface.get_width() - 10
            surface.blit(pellets_surface, (pellets_x, 10))
        
        # Mode (right bottom)
        mode_text = f"MODE: {current_mode}"
        mode_surface = self.font.render(mode_text, True, self.text_color)
        mode_x = WINDOW_WIDTH - mode_surface.get_width() - 10
        mode_y = 25  # Lower row
        surface.blit(mode_surface, (mode_x, mode_y))
        
        # Ghost-ketjupisteet piirretään nyt suoraan pelialueelle game_state.py:ssä
    
    def draw_game_over(self, surface: pygame.Surface, final_score: int) -> None:
        """
        Piirtää game over -näytön.
        
        Args:
            surface: Pinta jolle piirretään
            final_score: Lopulliset pisteet
        """
        # Suurempi fontti otsikkolle
        big_font = pygame.font.Font(None, 48)
        
        # Game Over text
        game_over_text = "GAME OVER"
        game_over_surface = big_font.render(game_over_text, True, WHITE)
        game_over_x = WINDOW_WIDTH // 2 - game_over_surface.get_width() // 2
        game_over_y = 200
        surface.blit(game_over_surface, (game_over_x, game_over_y))
        
        # Final score
        score_text = f"Final Score: {final_score:06d}"
        score_surface = self.font.render(score_text, True, self.score_color)
        score_x = WINDOW_WIDTH // 2 - score_surface.get_width() // 2
        score_y = game_over_y + 60
        surface.blit(score_surface, (score_x, score_y))
        
        # Instructions
        restart_text = "Press ENTER to restart or ESC to exit"
        restart_surface = self.font.render(restart_text, True, self.text_color)
        restart_x = WINDOW_WIDTH // 2 - restart_surface.get_width() // 2
        restart_y = score_y + 40
        surface.blit(restart_surface, (restart_x, restart_y))
    
    def draw_victory(self, surface: pygame.Surface, score: int, level: int) -> None:
        """
        Piirtää voittonäytön (taso läpäisty).
        
        Args:
            surface: Pinta jolle piirretään
            score: Nykyiset pisteet
            level: Läpäisty taso
        """
        # Suurempi fontti otsikkolle
        big_font = pygame.font.Font(None, 48)
        
        # Victory text
        victory_text = f"LEVEL {level} COMPLETE!"
        victory_surface = big_font.render(victory_text, True, YELLOW)
        victory_x = WINDOW_WIDTH // 2 - victory_surface.get_width() // 2
        victory_y = 200
        surface.blit(victory_surface, (victory_x, victory_y))
        
        # Score
        score_text = f"Score: {score:06d}"
        score_surface = self.font.render(score_text, True, self.score_color)
        score_x = WINDOW_WIDTH // 2 - score_surface.get_width() // 2
        score_y = victory_y + 60
        surface.blit(score_surface, (score_x, score_y))
        
        # Instructions
        continue_text = "Press ENTER to continue to next level"
        continue_surface = self.font.render(continue_text, True, self.text_color)
        continue_x = WINDOW_WIDTH // 2 - continue_surface.get_width() // 2
        continue_y = score_y + 40
        surface.blit(continue_surface, (continue_x, continue_y))
    
    def draw_complete_victory(self, surface: pygame.Surface, final_score: int) -> None:
        """
        Piirtää koko pelin läpäisemisen näytön.
        
        Args:
            surface: Pinta jolle piirretään
            final_score: Lopulliset pisteet
        """
        # Suurempi fontti otsikkolle
        big_font = pygame.font.Font(None, 64)
        
        # Game completion text
        victory_text = "CONGRATULATIONS!"
        victory_surface = big_font.render(victory_text, True, YELLOW)
        victory_x = WINDOW_WIDTH // 2 - victory_surface.get_width() // 2
        victory_y = 150
        surface.blit(victory_surface, (victory_x, victory_y))
        
        # Lower text
        complete_text = "YOU COMPLETED ALL 6 LEVELS!"
        complete_surface = self.font.render(complete_text, True, WHITE)
        complete_x = WINDOW_WIDTH // 2 - complete_surface.get_width() // 2
        complete_y = victory_y + 80
        surface.blit(complete_surface, (complete_x, complete_y))
        
        # Final score
        score_text = f"Final Score: {final_score:06d}"
        score_surface = self.font.render(score_text, True, self.score_color)
        score_x = WINDOW_WIDTH // 2 - score_surface.get_width() // 2
        score_y = complete_y + 60
        surface.blit(score_surface, (score_x, score_y))
        
        # Instructions
        restart_text = "Press ENTER to restart or ESC to return to menu"
        restart_surface = self.font.render(restart_text, True, self.text_color)
        restart_x = WINDOW_WIDTH // 2 - restart_surface.get_width() // 2
        restart_y = score_y + 60
        surface.blit(restart_surface, (restart_x, restart_y))
    
    def draw_menu(self, surface: pygame.Surface) -> None:
        """
        Piirtää päävalikon.
        
        Args:
            surface: Pinta jolle piirretään
        """
        # Suurempi fontti otsikkolle
        big_font = pygame.font.Font(None, 72)
        
        # Pelin nimi
        title_text = "MAZE CHOMP"
        title_surface = big_font.render(title_text, True, YELLOW)
        title_x = WINDOW_WIDTH // 2 - title_surface.get_width() // 2
        title_y = 150
        surface.blit(title_surface, (title_x, title_y))
        
        # Start instruction
        start_text = "Press ENTER to start"
        start_surface = self.font.render(start_text, True, WHITE)
        start_x = WINDOW_WIDTH // 2 - start_surface.get_width() // 2
        start_y = title_y + 100
        surface.blit(start_surface, (start_x, start_y))
        
        # Controls
        controls_title = "CONTROLS:"
        controls_surface = self.font.render(controls_title, True, WHITE)
        controls_x = WINDOW_WIDTH // 2 - controls_surface.get_width() // 2
        controls_y = start_y + 60
        surface.blit(controls_surface, (controls_x, controls_y))
        
        # Controls list
        controls = [
            "Arrow keys or WASD - Move",
            "ESC - Exit game"
        ]
        
        for i, control in enumerate(controls):
            control_surface = self.font.render(control, True, WHITE)
            control_x = WINDOW_WIDTH // 2 - control_surface.get_width() // 2
            control_y = controls_y + 30 + (i * 25)
            surface.blit(control_surface, (control_x, control_y))
    
    def draw_pause(self, surface: pygame.Surface) -> None:
        """
        Piirtää taukonäytön.
        
        Args:
            surface: Pinta jolle piirretään
        """
        # Läpinäkyvä tausta
        pause_overlay = pygame.Surface((WINDOW_WIDTH, surface.get_height()))
        pause_overlay.set_alpha(128)
        pause_overlay.fill((0, 0, 0))
        surface.blit(pause_overlay, (0, 0))
        
        # Pause text
        big_font = pygame.font.Font(None, 48)
        pause_text = "PAUSED"
        pause_surface = big_font.render(pause_text, True, WHITE)
        pause_x = WINDOW_WIDTH // 2 - pause_surface.get_width() // 2
        pause_y = 250
        surface.blit(pause_surface, (pause_x, pause_y))
        
        # Continue instruction
        continue_text = "Press SPACE to continue"
        continue_surface = self.font.render(continue_text, True, WHITE)
        continue_x = WINDOW_WIDTH // 2 - continue_surface.get_width() // 2
        continue_y = pause_y + 50
        surface.blit(continue_surface, (continue_x, continue_y))
    
    def get_height(self) -> int:
        """
        Palauttaa HUD:in korkeuden.
        
        Returns:
            HUD:in korkeus pikseleinä
        """
        return self.height