"""
Pelin ääniefektit.
Luo retro-tyylisiä ääniä Pygame:n sisäänrakennetulla syntetisaattorilla.
"""
import pygame
import numpy as np
from typing import Optional


class AudioManager:
    """Hallinnoi pelin ääniefektit."""
    
    def __init__(self):
        """Alustaa äänimanagerin."""
        # Alusta pygame mixer
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        self.sample_rate = 22050
        self.sounds = {}
        self.enabled = True
        
        # Luo ääniefektit
        self._create_sounds()
    
    def _create_sounds(self) -> None:
        """Luo kaikki ääniefektit."""
        # Pelletin syömisen ääni (lyhyt "pip")
        self.sounds['pellet'] = self._create_pellet_sound()
        
        # Power-pelletin syömisen ääni (syvempi "bom")
        self.sounds['power_pellet'] = self._create_power_pellet_sound()
        
        # Haamun syömisen ääni (nouseva "wooop")
        self.sounds['eat_ghost'] = self._create_eat_ghost_sound()
        
        # Pelaajan kuoleman ääni (laskeva "awww")
        self.sounds['death'] = self._create_death_sound()
        
        # Tason valmistumisen ääni (voittomelodi)
        self.sounds['level_complete'] = self._create_level_complete_sound()
        
        # Frightened-tilan ääni (syvä hälytys)
        self.sounds['frightened'] = self._create_frightened_sound()
        
        # Valikkoääni (valinta)
        self.sounds['menu_select'] = self._create_menu_select_sound()
    
    def _create_pellet_sound(self) -> pygame.mixer.Sound:
        """Luo pelletin syömisen ääni."""
        duration = 0.1
        frequency = 800
        samples = int(self.sample_rate * duration)
        
        # Lyhyt siniaalto
        wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration, samples))
        
        # Fade out
        fade = np.linspace(1, 0, samples)
        wave *= fade
        
        # Stereo
        stereo = np.array([wave, wave]).T
        audio_data = (stereo * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.ascontiguousarray(audio_data))
    
    def _create_power_pellet_sound(self) -> pygame.mixer.Sound:
        """Luo power-pelletin syömisen ääni."""
        duration = 0.3
        base_freq = 400
        samples = int(self.sample_rate * duration)
        
        # Moduloitu ääni
        t = np.linspace(0, duration, samples)
        modulation = np.sin(2 * np.pi * 15 * t)  # 15 Hz modulaatio
        frequency = base_freq + 100 * modulation
        
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Envelope
        envelope = np.exp(-t * 3)  # Eksponentiaalinen fade
        wave *= envelope
        
        # Stereo
        stereo = np.array([wave, wave]).T
        audio_data = (stereo * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.ascontiguousarray(audio_data))
    
    def _create_eat_ghost_sound(self) -> pygame.mixer.Sound:
        """Luo haamun syömisen ääni."""
        duration = 0.4
        samples = int(self.sample_rate * duration)
        
        # Nouseva frequenssi
        start_freq = 200
        end_freq = 800
        t = np.linspace(0, duration, samples)
        frequency = start_freq + (end_freq - start_freq) * (t / duration)
        
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Envelope
        envelope = np.exp(-t * 2)
        wave *= envelope
        
        # Stereo
        stereo = np.array([wave, wave]).T
        audio_data = (stereo * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.ascontiguousarray(audio_data))
    
    def _create_death_sound(self) -> pygame.mixer.Sound:
        """Luo pelaajan kuoleman ääni."""
        duration = 1.0
        samples = int(self.sample_rate * duration)
        
        # Laskeva frequenssi
        start_freq = 600
        end_freq = 100
        t = np.linspace(0, duration, samples)
        frequency = start_freq - (start_freq - end_freq) * (t / duration)
        
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Hitaasti häipyvä envelope
        envelope = np.exp(-t * 1.5)
        wave *= envelope
        
        # Stereo
        stereo = np.array([wave, wave]).T
        audio_data = (stereo * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.ascontiguousarray(audio_data))
    
    def _create_level_complete_sound(self) -> pygame.mixer.Sound:
        """Luo tason valmistumisen ääni."""
        duration = 1.5
        samples = int(self.sample_rate * duration)
        
        # Yksinkertainen voittomelodi: C-E-G-C
        notes = [261.63, 329.63, 392.00, 523.25]  # C4, E4, G4, C5
        note_duration = duration / len(notes)
        
        wave = np.array([])
        for note_freq in notes:
            note_samples = int(self.sample_rate * note_duration)
            t = np.linspace(0, note_duration, note_samples)
            note_wave = np.sin(2 * np.pi * note_freq * t)
            
            # Envelope jokaiselle nuotille
            envelope = np.exp(-t * 2)
            note_wave *= envelope
            
            wave = np.concatenate([wave, note_wave])
        
        # Stereo
        stereo = np.array([wave, wave]).T
        audio_data = (stereo * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.ascontiguousarray(audio_data))
    
    def _create_frightened_sound(self) -> pygame.mixer.Sound:
        """Luo frightened-tilan ääni."""
        duration = 0.5
        samples = int(self.sample_rate * duration)
        
        # Matala hälytysääni
        base_freq = 150
        t = np.linspace(0, duration, samples)
        
        # Tremolo-efekti
        tremolo = 1 + 0.3 * np.sin(2 * np.pi * 8 * t)  # 8 Hz tremolo
        wave = np.sin(2 * np.pi * base_freq * t) * tremolo
        
        # Envelope
        envelope = np.exp(-t * 1)
        wave *= envelope
        
        # Stereo
        stereo = np.array([wave, wave]).T
        audio_data = (stereo * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.ascontiguousarray(audio_data))
    
    def _create_menu_select_sound(self) -> pygame.mixer.Sound:
        """Luo valikkoääni."""
        duration = 0.15
        frequency = 600
        samples = int(self.sample_rate * duration)
        
        # Nopea "beep"
        t = np.linspace(0, duration, samples)
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Nopea fade
        envelope = np.exp(-t * 8)
        wave *= envelope
        
        # Stereo
        stereo = np.array([wave, wave]).T
        audio_data = (stereo * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.ascontiguousarray(audio_data))
    
    def play_sound(self, sound_name: str, volume: float = 1.0) -> None:
        """
        Toistaa ääniefektin.
        
        Args:
            sound_name: Äänen nimi
            volume: Äänenvoimakkuus (0.0-1.0)
        """
        if not self.enabled or sound_name not in self.sounds:
            return
        
        sound = self.sounds[sound_name]
        sound.set_volume(volume)
        sound.play()
    
    def play_pellet(self) -> None:
        """Toistaa pelletin syömisen ääni."""
        self.play_sound('pellet', 0.3)
    
    def play_power_pellet(self) -> None:
        """Toistaa power-pelletin syömisen ääni."""
        self.play_sound('power_pellet', 0.5)
    
    def play_eat_ghost(self, chain_count: int = 1) -> None:
        """
        Toistaa haamun syömisen ääni.
        
        Args:
            chain_count: Ketjun pituus (korkeampi pitch)
        """
        volume = min(0.6, 0.3 + chain_count * 0.1)
        self.play_sound('eat_ghost', volume)
    
    def play_death(self) -> None:
        """Toistaa pelaajan kuoleman ääni."""
        self.play_sound('death', 0.7)
    
    def play_level_complete(self) -> None:
        """Toistaa tason valmistumisen ääni."""
        self.play_sound('level_complete', 0.6)
    
    def play_frightened(self) -> None:
        """Toistaa frightened-tilan ääni."""
        self.play_sound('frightened', 0.4)
    
    def play_menu_select(self) -> None:
        """Toistaa valikkoääni."""
        self.play_sound('menu_select', 0.5)
    
    def set_enabled(self, enabled: bool) -> None:
        """
        Asettaa äänien päälle/pois.
        
        Args:
            enabled: True = äänet päällä, False = äänet pois
        """
        self.enabled = enabled
    
    def stop_all(self) -> None:
        """Pysäyttää kaikki äänet."""
        pygame.mixer.stop()
