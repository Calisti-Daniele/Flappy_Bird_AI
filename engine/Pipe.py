import pygame
import random


class Pipe:
    def __init__(self, image, screen_width, screen_height, flipped=False, gap_height=150):
        self.image = image
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.flipped = flipped
        self.gap_height = gap_height

        # Dimensione della pipe
        self.pipe_width = self.image.get_width()
        self.pipe_height = self.image.get_height()

        # Posizione iniziale
        self.x = screen_width + self.pipe_width + random.randint(100, 300)  # Distanziare le pipe
        self.y = self.get_random_pipe_y()

        # Se la pipe è capovolta, la ruota
        if self.flipped:
            self.image = pygame.transform.flip(self.image, False, True)
            self.y = self.y - self.gap_height - self.pipe_height  # Posizione pipe superiore

        # Rect della pipe per il rilevamento delle collisioni
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def get_random_pipe_y(self):
        """Genera una posizione Y casuale per le pipe."""
        return random.randint(50, self.screen_height - self.gap_height - 50)

    def update(self):
        """Aggiorna la posizione della pipe."""
        self.x -= 3  # La velocità con cui la pipe si muove a sinistra
        self.rect.topleft = (self.x, self.y)

        if self.x < -self.pipe_width:
            self.x = self.screen_width + self.pipe_width
            self.y = self.get_random_pipe_y()  # Nuova posizione Y per la pipe
            if self.flipped:
                self.y = self.y - self.gap_height - self.pipe_height
