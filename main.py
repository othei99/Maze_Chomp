"""
Maze Chomp - Pac-Man-tyylinen peli Pygame:lla.
Pääsilmukka ja pelin alustus.
"""
import pygame
import sys
import os
from typing import Optional

# Lisää projektin juurihakemisto polkuun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BLACK
from game_state import GameStateManager


class Game:
    """Pelin pääluokka."""
    
    def __init__(self):
        """Alustaa pelin."""
        # Alusta Pygame
        pygame.init()
        
        # macOS-yhteensopivuus
        import os
        os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
        
        # Luo ikkuna
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Maze Chomp")
        
        # Varmista että ikkuna tulee näkyviin
        pygame.display.flip()
        
        # Kello FPS:n hallintaan
        self.clock = pygame.time.Clock()
        
        # Tilamanageri
        self.state_manager = GameStateManager()
        
        # Pelin tila
        self.running = True
        
        print("Maze Chomp started!")
        print("Controls:")
        print("- Arrow keys or WASD: Move")
        print("- SPACE: Pause")
        print("- ESC: Back to menu/exit")
        print("- ENTER: Select/continue")
        print(f"Window size: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        print("Game ready, press ENTER to start!")
    
    def handle_events(self) -> None:
        """Käsittelee Pygame-tapahtumat."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                # Anna tilamanagerin käsitellä tapahtumat
                self.state_manager.handle_event(event)
    
    def update(self, dt: float) -> None:
        """
        Päivittää pelin tilan.
        
        Args:
            dt: Aikaerotus sekunteina
        """
        self.state_manager.update(dt)
    
    def render(self) -> None:
        """Renderöi pelin."""
        # Tyhjennä ruutu
        self.screen.fill(BLACK)
        
        # Anna tilamanagerin renderöidä
        self.state_manager.render(self.screen)
        
        # Päivitä näyttö
        pygame.display.flip()
    
    def run(self) -> None:
        """Pelin pääsilmukka."""
        try:
            while self.running:
                # Laske delta-aika
                dt = self.clock.tick(FPS) / 1000.0  # Muunna millisekunneista sekunneiksi
                
                # Pelin päivittäminen
                self.handle_events()
                self.update(dt)
                self.render()
                
        except KeyboardInterrupt:
            print("\nPeli keskeytetty käyttäjän toimesta")
        except Exception as e:
            print(f"Virhe pelissä: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.quit()
    
    def quit(self) -> None:
        """Lopettaa pelin ja vapauttaa resurssit."""
        print("Closing Maze Chomp...")
        pygame.quit()
        sys.exit()


def main() -> None:
    """Pelin käynnistysfunktio."""
    try:
        # Tarkista että level1-hakemisto löytyy
        level1_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "level1")
        level_file = os.path.join(level1_dir, "level1.txt")
        
        if not os.path.exists(level_file):
            print(f"Error: Level file not found: {level_file}")
            print("Make sure level1/level1.txt file exists")
            return
        
        # Luo ja käynnistä peli
        game = Game()
        game.run()
        
    except Exception as e:
        print(f"Error starting game: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
