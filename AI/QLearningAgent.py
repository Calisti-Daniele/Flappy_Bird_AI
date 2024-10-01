import os

import numpy as np


class QLearningAgent:
    def __init__(self, actions, state_size, learning_rate=0.1, discount_factor=0.95, exploration_rate=1.0, exploration_decay=0.99, min_exploration_rate=0.01):
        self.actions = actions
        self.state_size = state_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        self.q_table_file = 'q_table/q_table.npy'  # Nome del file per salvare la Q-table

        # Inizializza la Q-table con zero o carica dal file se esiste
        if os.path.exists(self.q_table_file):
            self.q_table = np.load(self.q_table_file)  # Carica la Q-table esistente
        else:
            self.q_table = np.zeros((10, 10, 10, len(actions)))  # Inizializza la Q-table con zero

    def choose_action(self, state):
        # Epsilon-greedy action selection
        if np.random.rand() < self.exploration_rate:
            return np.random.choice(self.actions)  # Esplora
        else:
            state_index = self.state_to_index(state)  # Converti lo stato in indice
            return np.argmax(self.q_table[state_index])  # Scegli l'azione migliore

    def update(self, state, action, reward, next_state):
        # Aggiorna la Q-table
        state_index = self.state_to_index(state)
        next_state_index = self.state_to_index(next_state)
        best_next_action = np.argmax(self.q_table[next_state_index])  # Migliore azione per il prossimo stato

        # Q-learning formula
        td_target = reward + self.discount_factor * self.q_table[next_state_index][best_next_action]
        td_error = td_target - self.q_table[state_index][action]
        self.q_table[state_index][action] += self.learning_rate * td_error  # Aggiorna Q-value

        # Decay exploration rate
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)

    def state_to_index(self, state):
        # Mappa lo stato a un indice della Q-table
        # Qui è necessario normalizzare lo stato, personalizzare secondo il tuo gioco
        y_bird, y_pipe, x_pipe = state
        return (min(max(y_bird // 10, 0), 9),  # Normalizza posizione dell'uccello
                min(max((y_pipe - y_bird) // 10, 0), 9),  # Distanza tra l'uccello e la pipe
                min(max(x_pipe // 10, 0), 9))  # Normalizza la posizione della pipe

    def save_q_table(self):
        np.save(self.q_table_file, self.q_table)  # Salva la Q-table in un file

    def load_q_table(self):
        if os.path.exists(self.q_table_file):
            self.q_table = np.load(self.q_table_file)  # Carica la Q-table esistente

    def state_to_index(self, state):
        # Mappa lo stato a un indice della Q-table
        # Qui è necessario normalizzare lo stato, personalizzare secondo il tuo gioco
        y_bird, y_pipe, x_pipe = state
        return (min(max(y_bird // 10, 0), 9),  # Normalizza posizione dell'uccello
                min(max((y_pipe - y_bird) // 10, 0), 9),  # Distanza tra l'uccello e la pipe
                min(max(x_pipe // 10, 0), 9))  # Normalizza la posizione della pipe