import pygame
from engine.Bird import Bird
from engine.Pipe import Pipe

# Inizializza pygame
pygame.init()

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
message_image = pygame.image.load('sprites/message.png')  # Immagine di messaggio

# Crea l'uccellino e le pipe
bird = Bird(bird_image, SCREEN_WIDTH, SCREEN_HEIGHT)
pipes = [Pipe(pipe_image, SCREEN_WIDTH, SCREEN_HEIGHT, gap_height=150)]

# Variabili per gestire il "game over"
game_over = False
game_started = False  # Variabile per gestire l'inizio del gioco

# Variabili per la generazione delle pipe
last_pipe_generation_time = pygame.time.get_ticks()  # Tempo dell'ultima generazione
pipe_generation_interval = 5000  # 5 secondi in millisecondi

# Definisci il loop principale del gioco
running = True
while running:
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over:
            bird.flap()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_started:  # Avvio del gioco al clic
            game_started = True

    if not game_started:
        # Mostra l'immagine di messaggio prima dell'inizio del gioco
        screen.blit(message_image, (
            SCREEN_WIDTH // 2 - message_image.get_width() // 2, SCREEN_HEIGHT // 2 - message_image.get_height() // 2))
    else:
        if not game_over:
            # Aggiorna e mostra l'uccellino
            bird.update(SCREEN_HEIGHT)
            screen.blit(bird.image, bird.rect)

            # Aggiorna e mostra le pipe
            for pipe in pipes:
                pipe.update()
                screen.blit(pipe.image, pipe.rect)

                # Controllo delle collisioni
                if bird.rect.colliderect(pipe.rect):
                    game_over = True  # Imposta il "game over"

            # Controllo per il "game over" quando l'uccello tocca la base
            if bird.rect.bottom >= SCREEN_HEIGHT - base_image.get_height():
                game_over = True

            # Aggiungi l'immagine di base
            screen.blit(base_image, (0, SCREEN_HEIGHT - base_image.get_height()))

            # Gestisci la generazione delle pipe
            current_time = pygame.time.get_ticks()  # Ottieni il tempo corrente
            if current_time - last_pipe_generation_time > pipe_generation_interval:
                pipes.append(Pipe(pipe_image, SCREEN_WIDTH, SCREEN_HEIGHT, gap_height=150))
                last_pipe_generation_time = current_time  # Aggiorna il tempo dell'ultima generazione

        else:
            # Mostra l'immagine di Game Over
            screen.blit(game_over_image, (SCREEN_WIDTH // 2 - game_over_image.get_width() // 2,
                                          SCREEN_HEIGHT // 2 - game_over_image.get_height() // 2))

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
