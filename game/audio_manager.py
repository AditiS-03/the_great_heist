
import pygame
from pathlib import Path


class AudioManager:

    def __init__(self):

        self.sound_dir = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "sounds"
        )

        self.sounds = {}

        self.enabled = True

        self.music_volume = 0.35
        self.sound_volume = 0.65

        # Initialise mixer safely
        if not pygame.mixer.get_init():

            try:
                pygame.mixer.init()

            except pygame.error as error:

                print("Audio unavailable:", error)

                self.enabled = False
                return

        self.load_sounds()

    def load_sounds(self):

        sound_files = {

            "move": "move.wav",
            "collect": "collect.wav",
            "door_open": "door_open.wav",
            "alert": "alert.wav",
            "capture": "capture.wav",
            "escape": "escape.wav",
            "button_click": "button_click.wav",
            "victory": "victory.wav",
            "defeat": "defeat.wav"

        }

        for name, filename in sound_files.items():

            path = self.sound_dir / filename

            if not path.exists():

                print("Missing sound:", filename)
                continue

            try:

                sound = pygame.mixer.Sound(str(path))

                sound.set_volume(self.sound_volume)

                self.sounds[name] = sound

            except pygame.error as error:

                print("Could not load", filename, error)

    def play(self, name):

        if not self.enabled:
            return

        sound = self.sounds.get(name)

        if sound:

            sound.play()

    def play_music(self, filename, loop=True):

        if not self.enabled:
            return

        path = self.sound_dir / filename

        if not path.exists():

            print("Music not found:", filename)
            return

        try:

            pygame.mixer.music.load(str(path))

            pygame.mixer.music.set_volume(
                self.music_volume
            )

            pygame.mixer.music.play(
                -1 if loop else 0
            )

        except pygame.error as error:

            print("Could not play music:", error)

    def stop_music(self):

        if self.enabled:
            pygame.mixer.music.stop()

    def set_music_volume(self, volume):

        self.music_volume = max(
            0.0,
            min(1.0, volume)
        )

        if self.enabled:
            pygame.mixer.music.set_volume(
                self.music_volume
            )

    def set_sound_volume(self, volume):

        self.sound_volume = max(
            0.0,
            min(1.0, volume)
        )

        for sound in self.sounds.values():

            sound.set_volume(
                self.sound_volume
            )

    def toggle(self):

        self.enabled = not self.enabled

        if not self.enabled:
            self.stop_music()
