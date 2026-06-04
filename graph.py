# =====================================================
# SHADOW SWAP DX
# ADVANCED TRAINING ANALYTICS
# =====================================================

import matplotlib.pyplot as plt

episodes = []
wins = []
rewards = []
steps = []
epsilons = []

# =====================================================
# LOAD DATA
# =====================================================

try:

    with open("training_stats.txt", "r") as file:

        for line in file:

            data = line.strip().split(",")

            if len(data) != 5:
                continue

            episodes.append(int(data[0]))
            wins.append(int(data[1]))
            rewards.append(float(data[2]))
            steps.append(int(data[3]))
            epsilons.append(float(data[4]))

except FileNotFoundError:

    print("training_stats.txt not found.")
    exit()

# =====================================================
# CHECK DATA
# =====================================================

if len(episodes) == 0:

    print("No training data available.")
    exit()

# =====================================================
# TRAINING SUMMARY CALCULATIONS
# =====================================================

total_episodes = len(episodes)

total_wins = sum(wins)

win_rate = (total_wins / total_episodes) * 100

average_reward = sum(rewards) / total_episodes

average_steps = sum(steps) / total_episodes

final_epsilon = epsilons[-1]

# =====================================================
# CREATE FIGURE
# =====================================================

fig = plt.figure(figsize=(16, 12))

# =====================================================
# GRAPH 1 — WIN HISTORY
# =====================================================

ax1 = plt.subplot(3, 2, 1)

ax1.plot(episodes, wins, linewidth=2)

ax1.set_title("AI Win History")

ax1.set_xlabel("Episode")

ax1.set_ylabel("Win")

ax1.set_ylim(-0.1, 1.1)

ax1.grid(True)

# =====================================================
# GRAPH 2 — REWARDS
# =====================================================

ax2 = plt.subplot(3, 2, 2)

ax2.plot(episodes, rewards, linewidth=2)

ax2.set_title("Reward Improvement")

ax2.set_xlabel("Episode")

ax2.set_ylabel("Reward")

ax2.grid(True)

# =====================================================
# GRAPH 3 — STEPS
# =====================================================

ax3 = plt.subplot(3, 2, 3)

ax3.plot(episodes, steps, linewidth=2)

ax3.set_title("Steps Per Episode")

ax3.set_xlabel("Episode")

ax3.set_ylabel("Steps")

ax3.grid(True)

# =====================================================
# GRAPH 4 — EPSILON DECAY
# =====================================================

ax4 = plt.subplot(3, 2, 4)

ax4.plot(episodes, epsilons, linewidth=2)

ax4.set_title("Exploration Rate (Epsilon Decay)")

ax4.set_xlabel("Episode")

ax4.set_ylabel("Epsilon")

ax4.grid(True)

# =====================================================
# TRAINING SUMMARY PANEL
# =====================================================

ax5 = plt.subplot(3, 1, 3)

ax5.axis("off")

summary_text = f"""
SHADOW SWAP DX — TRAINING SUMMARY

Total Episodes: {total_episodes}            Average Reward: {average_reward:.2f}

Total Wins: {total_wins}                         Average Steps: {average_steps:.2f}

Win Rate: {win_rate:.2f}%                     Final Epsilon: {final_epsilon:.4f}
"""

ax5.text(
    0.02,
    0.95,
    summary_text,
    fontsize=14,
    verticalalignment="top",
    family="monospace"
)

# =====================================================
# WINDOW TITLE
# =====================================================

fig.suptitle(
    "SHADOW SWAP DX — Reinforcement Learning Analytics",
    fontsize=18,
    fontweight="bold"
)

plt.tight_layout()

plt.show()