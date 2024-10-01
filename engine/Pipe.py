import pygame
import random


class Pipe:
    def __init__(self, pipe_image, screen_width, screen_height, gap_height=100):  # Puoi regolare questo valore
        self.gap_height = gap_height
        self.image = pipe_image  # Solo pipe normale, non flippabile
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.screen_height = screen_height

        # Posizione y della pipe sotto la base
        #Il range ottimale è 200, 270
        self.rect.y = screen_height - self.image.get_height() - gap_height + random.randint(200,270)  # Aggiungi un valore per spostarla più in basso

    def update(self):
        # Aggiorna la posizione della pipe
        self.rect.x -= 5  # Velocità di movimento della pipe
        if self.rect.right < 0:  # Se la pipe esce dallo schermo
            self.rect.x = 288  # Riposiziona la pipe all'estrema destra dello schermo
            # Ripristina la posizione y della pipe
            self.rect.y = self.screen_height - self.image.get_height() - self.gap_height + random.randint(200,270)  # Rimane appoggiata alla base

    def draw(self, screen):
        # Disegna la pipe sullo schermo
        screen.blit(self.image, self.rect)
