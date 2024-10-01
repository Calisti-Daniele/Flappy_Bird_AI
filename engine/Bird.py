import pygame
from pygame import Surface


# Definisci la classe Bird
class Bird:
    def __init__(self, bird_image: Surface, screen_width: int, screen_height: int):
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 4, screen_height // 2)
        self.gravity = 0
        self.lift = -10
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, screen_height: int):
        self.gravity += 1  # Simula la gravità
        self.rect.y += self.gravity
        if self.rect.y > screen_height:
            self.rect.y = screen_height

    def flap(self):
        self.gravity = self.lift

    def reset(self):
        # Ripristina la posizione iniziale dell'uccellino
        self.rect.center = (50, self.screen_height // 2)  # Imposta la posizione iniziale