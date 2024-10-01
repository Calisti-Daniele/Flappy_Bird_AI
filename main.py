import pygame
import random
import numpy as np
import os

from matplotlib import pyplot as plt

from engine.Bird import Bird
from engine.Pipe import Pipe
from AI.QLearningAgent import QLearningAgent

# Inizializza pygame
pygame.init()

# Inizializza il mixer audio
pygame.mixer.init()

# Carica gli audio
hit_sound = pygame.mixer.Sound('audio/hit.wav')
die_sound = pygame.mixer.Sound('audio/die.wav')
point_sound = pygame.mixer.Sound('audio/point.wav')

# Definisci i colori
WHITE = (255, 255, 255)

# Imposta la larghezza e l'altezza dello schermo
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Carica gli sprite
bird_image = pygame.image.load('sprites/bluebird-midflap.png')
pipe_image = pygame.image.load('sprites/pipe-green.png')
background_image = pygame.image.load('sprites/background-day.png')
game_over_image = pygame.image.load('sprites/gameover.png')
base_image = pygame.image.load('sprites/base.png')
message_image = pygame.image.load('sprites/message.png')

# Carica le immagini per le cifre del punteggio
score_images = [pygame.image.load(f'sprites/{i}.png') for i in range(10)]

# Crea l'uccellino e le pipe
bird = Bird(bird_image, SCREEN_WIDTH, SCREEN_HEIGHT)
pipes = [Pipe(pipe_image, SCREEN_WIDTH, SCREEN_HEIGHT),
         Pipe(pipe_image, SCREEN_WIDTH, SCREEN_HEIGHT, flipped=True)]

# Definisci le azioni
actions = [0, 1]  # 0 = non flap, 1 = flap
state_size = 4  # (posizione_y_bird, posizione_y_pipe, distanza_x_pipe, velocità_y_bird)

# Crea l'agente Q-learning
agent = QLearningAgent(actions, state_size)

# Variabili per gestire lo stato del gioco
game_over = False
game_started = False

# Timer per la generazione delle pipe
pipe_timer = 0
pipe_interval = 1500  # Genera pipe ogni 1500 ms (1.5 secondi)

# Carica la Q-table dell'agente
agent.load_q_table()

# Variabili per punteggio e apprendimento
score = 0
scores = []  # Lista per salvare i punteggi
punteggio_learning = []  # Lista per tracciare l'apprendimento
tentativi = 0  # Lista per tracciare l'apprendimento


# Funzione per ottenere lo stato attuale
def get_state(bird, pipes):
    if pipes:
        nearest_pipe = pipes[0]
        distance_to_pipe = nearest_pipe.rect.x - bird.rect.x
        return (bird.rect.y, nearest_pipe.rect.y, distance_to_pipe)
    return (bird.rect.y, 0, 0, 0)


# Ottieni lo stato attuale
state = get_state(bird, pipes)

# Scegli un'azione dall'agente e aggiornalo
action = agent.choose_action(state)
next_state = get_state(bird, pipes)

# Loop principale del gioco
running = True
while running:
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_started:
        screen.blit(message_image, (
            SCREEN_WIDTH // 2 - message_image.get_width() // 2,
            SCREEN_HEIGHT // 2 - message_image.get_height() // 2))
    else:
        if not game_over:
            # Aggiorna e mostra l'uccellino
            bird.update(SCREEN_HEIGHT)
            screen.blit(bird.image, bird.rect)

            reward = 0

            # Aggiorna e mostra le pipe
            for pipe in pipes:
                pipe.update()
                screen.blit(pipe.image, pipe.rect)

                # Controlla se l'uccello ha superato la pipe
                if not pipe.passed and bird.rect.x > pipe.rect.x + pipe.rect.width:
                    # point_sound.play()
                    pipe.passed = True
                    if not pipe.flipped:
                        score += 1

                if pipe.passed:
                    reward = 1

                # Controllo collisioni
                if bird.rect.colliderect(pipe.rect):
                    # hit_sound.play()
                    game_over = True

            if bird.rect.bottom >= SCREEN_HEIGHT - base_image.get_height():
                # hit_sound.play()
                game_over = True

            # Ottieni lo stato attuale
            state = get_state(bird, pipes)

            # Scegli un'azione dall'agente e aggiornalo
            action = agent.choose_action(state)
            next_state = get_state(bird, pipes)
            agent.update(state, action, reward, next_state)

            # Aggiungi al punteggio di apprendimento
            punteggio_learning.append(reward)

            if action == 1:
                bird.flap()

            # Aggiungi l'immagine della base
            screen.blit(base_image, (0, SCREEN_HEIGHT - base_image.get_height()))

            # Timer per generare nuove pipe
            pipe_timer += 1
            if pipe_timer >= random.randint(30, 50):
                pipes.append(Pipe(pipe_image, SCREEN_WIDTH, SCREEN_HEIGHT))
                pipes.append(Pipe(pipe_image, SCREEN_WIDTH, SCREEN_HEIGHT, flipped=True))
                pipe_timer = 0

            # Mostra il punteggio
            scores.append(score)
            score_str = str(score)
            score_width = len(score_str) * score_images[0].get_width()
            score_x = (SCREEN_WIDTH - score_width) // 2
            for i, digit in enumerate(score_str):
                screen.blit(score_images[int(digit)], (score_x + i * score_images[0].get_width(), 20))

        else:
            tentativi += 1

            print(f"Tentativ: {tentativi}")
            print(f"Score: {score}")

            screen.blit(game_over_image, (SCREEN_WIDTH // 2 - game_over_image.get_width() // 2,
                                          SCREEN_HEIGHT // 2 - game_over_image.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(1000)
            game_over = False
            pipes.clear()
            pipes.append(Pipe(pipe_image, SCREEN_WIDTH, SCREEN_HEIGHT))
            pipes.append(Pipe(pipe_image, SCREEN_WIDTH, SCREEN_HEIGHT, flipped=True))
            score = 0
            bird.reset()

    pygame.display.flip()
    pygame.time.Clock().tick(30)

# Salva la Q-table al termine del gioco
agent.save_q_table()

# Visualizza i grafici dei punteggi e del punteggio di apprendimento
plt.figure(figsize=(12, 6))

# Grafico del punteggio
plt.subplot(1, 2, 1)
plt.plot(scores)
plt.title('Punteggio nel tempo')
plt.xlabel('Gioco')
plt.ylabel('Punteggio')
plt.grid()

# Grafico del punteggio di apprendimento
plt.subplot(1, 2, 2)
plt.plot(punteggio_learning)
plt.title('Punteggio di apprendimento nel tempo')
plt.xlabel('Passi di gioco')
plt.ylabel('Ricompensa')
plt.grid()

plt.tight_layout()
plt.show()

pygame.quit()
