# =====================================================
# SHADOW SWAP DX
# Reinforcement Learning Game
# ITRI 616 PROJECT VERSION
# =====================================================

import tkinter as tk
from tkinter import messagebox
import random
import csv
import os
import pickle

# =====================================================
# CONFIG
# =====================================================

GRID_SIZE = 8
CELL_SIZE = 80
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

STARTING_ENERGY = 50
LOCK_MOVES = 10

STATS_FILE = "training_stats.txt"
QTABLE_FILE = "q_table.pkl"

# =====================================================
# Q-LEARNING AGENT
# =====================================================

class QLearningAgent:

    def __init__(self):

        self.q_table = {}

        self.learning_rate = 0.1
        self.discount_factor = 0.9

        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.min_epsilon = 0.05

        self.actions = [
            "Up",
            "Down",
            "Left",
            "Right"
        ]

        self.load_q_table()

    # =================================================
    # LOAD Q TABLE
    # =================================================

    def load_q_table(self):

        if os.path.exists(QTABLE_FILE):

            with open(QTABLE_FILE, "rb") as file:

                self.q_table = pickle.load(file)

            print("Q-table loaded.")

    # =================================================
    # SAVE Q TABLE
    # =================================================

    def save_q_table(self):

        with open(QTABLE_FILE, "wb") as file:

            pickle.dump(self.q_table, file)

        print("Q-table saved.")

    # =================================================
    # GET Q VALUE
    # =================================================

    def get_q_value(self, state, action):

        if (state, action) not in self.q_table:
            return 0

        return self.q_table[(state, action)]

    # =================================================
    # CHOOSE ACTION
    # =================================================

    def choose_action(self, state):

        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)

        q_values = []

        for action in self.actions:

            q_values.append(
                self.get_q_value(state, action)
            )

        max_q = max(q_values)

        best_actions = []

        for action in self.actions:

            if self.get_q_value(state, action) == max_q:
                best_actions.append(action)

        return random.choice(best_actions)

    # =================================================
    # UPDATE Q TABLE
    # =================================================

    def update_q_table(
        self,
        state,
        action,
        reward,
        next_state
    ):

        current_q = self.get_q_value(state, action)

        future_q = max([
            self.get_q_value(next_state, a)
            for a in self.actions
        ])

        new_q = current_q + self.learning_rate * (
            reward +
            self.discount_factor * future_q -
            current_q
        )

        self.q_table[(state, action)] = new_q

        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay


# =====================================================
# MAIN GAME
# =====================================================

class ShadowSwapGame:

    def __init__(self, root):

        self.root = root

        self.root.title("Shadow Swap DX")

        self.root.geometry("1000x980")

        self.root.configure(bg="#111111")

        self.mode = tk.StringVar(value="human")

        self.agent = QLearningAgent()

        self.ai_running = False

        # =================================================
        # PERFORMANCE TRACKING
        # =================================================

        self.episode = self.load_episode_count()

        self.current_steps = 0
        self.total_reward = 0

        self.create_ui()

        self.reset_game()

    # =================================================
    # LOAD EPISODE COUNT
    # =================================================

    def load_episode_count(self):

        if not os.path.exists(STATS_FILE):
            return 0

        try:

            with open(STATS_FILE, "r") as file:

                lines = file.readlines()

                if len(lines) == 0:
                    return 0

                last_line = lines[-1].strip().split(",")

                return int(last_line[0]) + 1

        except:
            return 0

    # =================================================
    # USER INTERFACE
    # =================================================

    def create_ui(self):

        title = tk.Label(
            self.root,
            text="SHADOW SWAP DX",
            font=("Arial", 32, "bold"),
            fg="white",
            bg="#111111"
        )

        title.pack(pady=10)

        subtitle = tk.Label(
            self.root,
            text="Human vs Learning AI Strategy Game",
            font=("Arial", 14),
            fg="#bbbbbb",
            bg="#111111"
        )

        subtitle.pack()

        self.info_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#111111"
        )

        self.info_label.pack(pady=10)

        self.canvas = tk.Canvas(
            self.root,
            width=WINDOW_SIZE,
            height=WINDOW_SIZE,
            bg="#1f1f1f",
            highlightthickness=0
        )

        self.canvas.pack(pady=10)

        controls = tk.Frame(
            self.root,
            bg="#111111"
        )

        controls.pack(pady=10)

        tk.Button(
            controls,
            text="Restart",
            command=self.reset_game,
            width=12,
            bg="#00aaff",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            controls,
            text="Human vs AI",
            variable=self.mode,
            value="human",
            bg="#111111",
            fg="white",
            selectcolor="#333333"
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            controls,
            text="AI vs AI",
            variable=self.mode,
            value="ai",
            bg="#111111",
            fg="white",
            selectcolor="#333333"
        ).pack(side="left", padx=10)

        instructions = tk.Label(
            self.root,
            text="""
🔵 BLUE = Human / Random AI
🔴 RED = Learning AI

GOALS
• BOTH players must reach their goal
• First player locks their goal
• Second player gets 10 turns to finish

SPECIAL BLOCKS
🟣 Purple = Trap
• -5 Energy

🟦 Cyan = Swap positions
⬜ Gray = Walls

CONTROLS
Arrow Keys = Move
""",
            justify="left",
            font=("Arial", 11),
            fg="#cccccc",
            bg="#111111"
        )

        instructions.pack()

        self.root.bind("<Key>", self.key_press)

    # =================================================
    # RESET GAME
    # =================================================

    def reset_game(self):

        self.energy = STARTING_ENERGY
        self.game_over = False
        self.last_event = "Game Started"
        self.turn = "blue"

        self.current_steps = 0
        self.total_reward = 0

        self.lock_active = False
        self.locked_player = None
        self.lock_moves_left = LOCK_MOVES

        self.blue = [0, 0]
        self.red = [7, 7]

        # RANDOMIZED GOALS

        self.blue_goal = [3, 3]
        self.red_goal = [4, 1]

        if random.random() < 0.3:

            self.blue_goal = [2, 6]
            self.red_goal = [5, 1]

        # WALLS

        self.walls = [
            [2, 2], [2, 3], [2, 4],
            [5, 3], [5, 4], [5, 5]
        ]

        # TRAPS

        self.traps = [
            [1, 5],
            [4, 2],
            [6, 1]
        ]

        # SWAP TILES

        self.swap_tiles = [
            [3, 1],
            [4, 6]
        ]

        self.draw()

        if not self.ai_running:

            self.ai_running = True

            self.root.after(300, self.ai_loop)

    # =================================================
    # DRAW GAME
    # =================================================

    def draw(self):

        self.canvas.delete("all")

        for row in range(GRID_SIZE):

            for col in range(GRID_SIZE):

                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE

                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="#2a2a2a",
                    outline="#444444"
                )

        for wall in self.walls:
            self.draw_square(wall, "#666666")

        for trap in self.traps:
            self.draw_square(trap, "#aa00ff")

        for tile in self.swap_tiles:
            self.draw_square(tile, "#00ffff")

        self.draw_goal(self.blue_goal, "#0044ff")
        self.draw_goal(self.red_goal, "#cc0000")

        self.draw_player(self.blue, "#00aaff")
        self.draw_player(self.red, "#ff4444")

        lock_text = ""

        if self.lock_active:

            lock_text = (
                f" | LOCK MOVES LEFT: "
                f"{self.lock_moves_left}"
            )

        self.info_label.config(
            text=f"Episode: {self.episode} | "
                 f"{self.last_event} | "
                 f"Turn: {self.turn.upper()} | "
                 f"Energy: {self.energy} | "
                 f"Epsilon: {round(self.agent.epsilon, 3)}"
                 f"{lock_text}"
        )

    # =================================================
    # DRAW PLAYER
    # =================================================

    def draw_player(self, pos, color):

        r, c = pos

        self.canvas.create_oval(
            c * CELL_SIZE + 10,
            r * CELL_SIZE + 10,
            c * CELL_SIZE + CELL_SIZE - 10,
            r * CELL_SIZE + CELL_SIZE - 10,
            fill=color,
            outline=""
        )

    # =================================================
    # DRAW GOAL
    # =================================================

    def draw_goal(self, pos, color):

        r, c = pos

        self.canvas.create_rectangle(
            c * CELL_SIZE + 20,
            r * CELL_SIZE + 20,
            c * CELL_SIZE + CELL_SIZE - 20,
            r * CELL_SIZE + CELL_SIZE - 20,
            fill=color,
            outline=""
        )

    # =================================================
    # DRAW SQUARE
    # =================================================

    def draw_square(self, pos, color):

        r, c = pos

        self.canvas.create_rectangle(
            c * CELL_SIZE + 5,
            r * CELL_SIZE + 5,
            c * CELL_SIZE + CELL_SIZE - 5,
            r * CELL_SIZE + CELL_SIZE - 5,
            fill=color,
            outline=""
        )

    # =================================================
    # SWITCH TURN
    # =================================================

    def switch_turn(self):

        if self.turn == "blue":
            self.turn = "red"
        else:
            self.turn = "blue"

    # =================================================
    # GET STATE
    # =================================================

    def get_state(self):

        return (
            self.red[0],
            self.red[1],
            self.red_goal[0],
            self.red_goal[1]
        )

    # =================================================
    # SAVE TRAINING STATISTICS
    # =================================================

    def save_statistics(self, win):

        with open(STATS_FILE, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                self.episode,
                win,
                self.total_reward,
                self.current_steps,
                round(self.agent.epsilon, 4)
            ])

        self.agent.save_q_table()

        self.episode += 1

    # =================================================
    # MOVE CHARACTER
    # =================================================

    def move_character(self, direction):

        if self.game_over:
            return

        self.current_steps += 1

        if (
            self.lock_active and
            self.locked_player == self.turn
        ):

            self.switch_turn()

            self.draw()

            return

        current = (
            self.blue
            if self.turn == "blue"
            else self.red
        )

        row, col = current

        # BLUE MOVEMENT

        if self.turn == "blue":

            if direction == "Up":
                row -= 1

            elif direction == "Down":
                row += 1

            elif direction == "Left":
                col -= 1

            elif direction == "Right":
                col += 1

        # RED MOVEMENT

        else:

            if direction == "Up":
                row += 1

            elif direction == "Down":
                row -= 1

            elif direction == "Left":
                col += 1

            elif direction == "Right":
                col -= 1

        row = max(0, min(GRID_SIZE - 1, row))
        col = max(0, min(GRID_SIZE - 1, col))

        new_position = [row, col]

        # WALL COLLISION

        if new_position in self.walls:

            self.last_event = "⬜ WALL BLOCKED"

            if self.turn == "red":
                self.total_reward -= 10

            self.draw()

            return

        # APPLY MOVE

        if self.turn == "blue":
            self.blue = new_position
        else:
            self.red = new_position

        self.energy -= 1

        # TRAP

        if new_position in self.traps:

            self.energy -= 5

            self.last_event = "🟣 TRAP HIT"

        # SWAP TILE

        if new_position in self.swap_tiles:

            self.blue, self.red = self.red, self.blue

            self.last_event = "🔁 SWAP ACTIVATED"

        # GOAL EVENTS

        if (
            self.blue == self.blue_goal
            and not self.lock_active
        ):

            self.lock_active = True

            self.locked_player = "blue"

            self.lock_moves_left = LOCK_MOVES

            self.turn = "red"

            self.last_event = (
                "🔵 BLUE LOCKED GOAL | RED HAS 10 MOVES"
            )

            self.draw()

            return

        if (
            self.red == self.red_goal
            and not self.lock_active
        ):

            self.lock_active = True

            self.locked_player = "red"

            self.lock_moves_left = LOCK_MOVES

            self.turn = "blue"

            self.last_event = (
                "🔴 RED LOCKED GOAL | BLUE HAS 10 MOVES"
            )

            self.draw()

            return

        # BOTH WIN

        if (
            self.blue == self.blue_goal
            and self.red == self.red_goal
        ):

            self.game_over = True

            self.last_event = "🏆 BOTH PLAYERS WON!"

            self.save_statistics(1)

            self.draw()

            play_again = messagebox.askyesno(
                "Victory",
                "🏆 BOTH PLAYERS REACHED THEIR GOALS!\n\n"
                "Start a new game?"
            )

            if play_again:
                self.reset_game()
            else:
                self.root.destroy()

            return

        # LOCK COUNTDOWN

        if self.lock_active:

            self.lock_moves_left -= 1

            self.last_event = (
                f"⏳ MOVES LEFT: {self.lock_moves_left}"
            )

            if self.lock_moves_left <= 0:

                self.game_over = True

                self.save_statistics(0)

                self.draw()

                play_again = messagebox.askyesno(
                    "Game Over",
                    "❌ SECOND PLAYER FAILED.\n\nRestart?"
                )

                if play_again:
                    self.reset_game()
                else:
                    self.root.destroy()

                return

        # ENERGY OUT

        if self.energy <= 0:

            self.game_over = True

            self.last_event = "⚠ ENERGY DEPLETED"

            self.save_statistics(0)

            self.draw()

            play_again = messagebox.askyesno(
                "Out of Energy",
                "⚠ ENERGY HAS RUN OUT!\n\nRestart?"
            )

            if play_again:
                self.reset_game()
            else:
                self.root.destroy()

            return

        self.switch_turn()

        self.draw()

    # =================================================
    # HUMAN INPUT
    # =================================================

    def key_press(self, event):

        if self.mode.get() != "human":
            return

        if self.turn != "blue":
            return

        if event.keysym in [
            "Up",
            "Down",
            "Left",
            "Right"
        ]:

            self.move_character(event.keysym)

    # =================================================
    # AI MOVE
    # =================================================

    def ai_move(self):

        if self.game_over:
            return

        if self.turn != "red":
            return

        state = self.get_state()

        action = self.agent.choose_action(state)

        old_distance = (
            abs(self.red[0] - self.red_goal[0]) +
            abs(self.red[1] - self.red_goal[1])
        )

        self.move_character(action)

        next_state = self.get_state()

        new_distance = (
            abs(self.red[0] - self.red_goal[0]) +
            abs(self.red[1] - self.red_goal[1])
        )

        # =================================================
        # IMPROVED REWARD SYSTEM
        # =================================================

        reward = -1

        if new_distance < old_distance:
            reward += 10

        if new_distance > old_distance:
            reward -= 5

        if self.red in self.traps:
            reward -= 25

        if self.red in self.swap_tiles:
            reward -= 5

        if self.red == self.red_goal:
            reward += 150

        self.total_reward += reward

        self.agent.update_q_table(
            state,
            action,
            reward,
            next_state
        )

    # =================================================
    # AI LOOP
    # =================================================

    def ai_loop(self):

        if not self.game_over:

            if self.mode.get() == "ai":

                if self.turn == "red":

                    self.ai_move()

                elif self.turn == "blue":

                    move = random.choice([
                        "Up",
                        "Down",
                        "Left",
                        "Right"
                    ])

                    self.move_character(move)

            elif (
                self.mode.get() == "human"
                and self.turn == "red"
            ):

                self.ai_move()

        self.root.after(300, self.ai_loop)


# =====================================================
# START GAME
# =====================================================

root = tk.Tk()

game = ShadowSwapGame(root)

root.mainloop()