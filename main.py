import tkinter as tk
from game import ShadowSwapGame

root = tk.Tk()

game = ShadowSwapGame(root)

# SAVE TRAINING DATA WHEN WINDOW CLOSES
def on_close():

    game.agent.save_q_table()

    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()