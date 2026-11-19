# 🎮 The Great Heist

**The Great Heist** is a Python-based, turn-based museum stealth game developed using Pygame. Players control a thief attempting to steal a valuable artifact while avoiding a security guard.

## 🎯 Game Objective

The thief must:
1. Collect the golden key.
2. Unlock the museum vault.
3. Steal the artifact.
4. Escape through the exit without getting caught.

The guard must capture the thief before they escape.

## 🕹️ Game Modes

- **2 Player Mode:** One player controls the thief and another controls the guard.
- **AI Guard Mode:** The player controls the thief while an AI-controlled guard attempts to capture them.

## 🤖 AI Concepts

The project explores:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- A* Search
- Heuristic Search
- Procedural Map Generation
- Connectivity Validation
- Rule-based AI Decision Making

The current Medium AI Guard uses BFS for pathfinding, line-of-sight detection, last-known-position investigation and patrol behaviour.

## 🛠️ Technologies Used

- Python
- Pygame
- Git and GitHub

## 🎮 Controls

| Action | Controls |
|---|---|
| Move thief | W, A, S, D |
| Move human guard | Arrow keys |
| Return to menu | ESC |

## ⚙️ Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/the-great-heist.git
   ```

2. Navigate into the project:

   ```bash
   cd the-great-heist
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the game:

   ```bash
   python main.py
   ```

## 🗺️ Procedural Map Generation

A new museum layout is generated for each new game using randomized grid generation and connectivity validation. The positions of the players and mission objects also change.

## 👩‍💻 Project Status

Developed as an academic project to explore Artificial Intelligence concepts through interactive gameplay.
:::Replace your-username with your actual GitHub username.

After creating the README, commit and push it:
- Commit message: Add project documentation
- Click Commit and Push.