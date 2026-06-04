Shadow Swap DX

Shadow Swap DX is a Reinforcement Learning strategy game developed for the ITRI 616 Artificial Intelligence Mini Project.

The game demonstrates how a Q-Learning agent can learn through experience, improve performance over time, and adapt its behaviour using rewards and penalties.

Features
Q-Learning Reinforcement Learning Agent
Persistent AI Learning
Q-Table Storage using Pickle
AI vs AI Training Mode
Human vs AI Mode
Dynamic Goal Placement
Trap Tiles
Swap Tiles
Goal Lock Mechanic
Energy Management System
Training Analytics Dashboard
Win Rate Tracking
Reward Tracking
Epsilon Decay Visualization
Technologies Used
Python
Tkinter
Matplotlib
Pickle
Files
game.py

Contains:

Game Environment
Reinforcement Learning Agent
Reward System
Training Statistics Collection
main.py

Launches the game and saves AI learning progress.

graph.py

Generates training analytics and performance visualizations.

Running the Project

Install dependencies:

pip install matplotlib

Launch the game:

python main.py

Generate analytics:

python graph.py
Machine Learning Approach

The project uses Reinforcement Learning through the Q-Learning algorithm.

The AI agent learns by:

Exploring the environment
Receiving rewards and penalties
Updating Q-values
Reducing exploration through epsilon decay
Improving decision-making across training episodes
Project Outcomes

The project demonstrates:

Autonomous learning
Decision-making under constraints
Reward-based optimization
Exploration vs exploitation strategies
Performance evaluation using analytics
