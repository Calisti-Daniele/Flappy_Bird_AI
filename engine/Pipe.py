import pygame
import random

class Pipe:
    def __init__(self, pipe_image, screen_width, screen_height, gap_height=100, flipped=False):
        self.gap_height = gap_height
        self.image = pipe_image  # Solo pipe normale, non flippabile
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.screen_height = screen_height
        self.passed = False  # Variabile per controllare se la pipe è stata superata
        self.flipped = flipped

        if flipped:
            self.image = pygame.transform.flip(pipe_image, False, True)  # Flippa l'immagine
            self.rect.y = screen_height - self.image.get_height() - gap_height - random.randint(200, 260)  # Posizione y della pipe flippata
        else:
            # Posizione y della pipe sotto la base
            self.rect.y = screen_height - self.image.get_height() - gap_height + random.randint(200, 270)

    def update(self):
        # Aggiorna la posizione della pipe
        self.rect.x -= 5  # Velocità di movimento della pipe

    def draw(self, screen):
        # Disegna la pipe sullo schermo
        screen.blit(self.image, self.rect)

    def flipped(self):
        return self.flipped
