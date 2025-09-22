# 🎮 Maze Chomp

A complete PacMan-style game built with Python and Pygame. Features full game mechanics including power-pellets, ghost AI with state machines, pathfinding, and collision detection.

![Game Status](https://img.shields.io/badge/Status-Playable-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-orange)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/maze_chomp.git
cd maze_chomp

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## 🎯 Game Preview

**Maze Chomp** is a fully functional Pac-Man clone featuring:
- 🟡 Classic Pac-Man gameplay with modern Python implementation
- 👻 Smart ghost AI with 4 different personalities (Blinky, Pinky, Clyde, Inky)
- ⚡ Power-pellets that turn ghosts blue and edible
- 🎵 Sound effects and smooth animations
- 📈 Progressive difficulty across 6 levels
- 🏆 Complete scoring system with bonus points

## ✨ Features

### 🎮 Core Gameplay
- **Grid-based Movement**: Player moves on a 16x16 pixel grid system
- **Wall Collision**: Cannot move through walls, smooth grid-snapping
- **Pellet Collection**: Collect pellets (10 points) and power-pellets (50 points)
- **Tunnel System**: Wrap around screen edges for strategic gameplay
- **Progressive Levels**: 6 levels with increasing difficulty and speed

### 👻 Advanced Ghost AI
- **Smart Ghost Behavior**: 4 unique ghost personalities
  - **Blinky** (Red): Direct aggressive pursuit
  - **Pinky** (Pink): Ambush tactics, targets 4 tiles ahead
  - **Clyde** (Orange): Unpredictable switching behavior
  - **Inky** (Cyan): Complex positioning strategy
- **State Machine**: SCATTER ↔ CHASE ↔ FRIGHTENED ↔ EATEN
- **Pathfinding**: BFS algorithm for optimal ghost movement
- **Mode Scheduling**: Timed global mode switches

### ⚡ Power-Pellet Mechanics
- **Ghost Frightening**: Turn all ghosts blue and edible
- **Chain Scoring**: 200 → 400 → 800 → 1600 points per ghost
- **Strategic Timing**: Limited frightened duration creates tension

### 🎵 Audio & Visual
- **Sound Effects**: Pellet eating, power-pellet activation, ghost consumption
- **Dynamic HUD**: Score, lives, level, pellets remaining, current mode
- **Smooth Animations**: Responsive character movement
- **Game States**: Menu, playing, game over, victory screens

## 📦 Installation

### Method 1: Quick Start (Recommended)
```bash
git clone https://github.com/othei99/Maze_Chomp.git
cd Maze_Chomp
pip install -r requirements.txt
python main.py
```

### Method 2: With Virtual Environment
```bash
git clone https://github.com/othei99/Maze_Chomp.git
cd Maze_Chomp

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## 🎮 Getting Started

Ready to play? Check out our comprehensive **[How to Play Guide](HOW_TO_PLAY.md)** for detailed instructions, strategies, and tips to master the game!

**Quick Controls:**
- **Movement**: Arrow keys or WASD  
- **Pause**: SPACE
- **Menu**: ESC

## 🏗️ Project Structure

```
maze_chomp/
├── main.py              # Main game loop and initialization
├── constants.py         # Game constants (colors, dimensions, speeds)
├── game_state.py        # State machine (menu, playing, game over)
├── level.py             # Level loading and management
├── player.py            # Player movement and logic
├── ghost.py             # Advanced ghost AI with personalities
├── hud.py               # User interface display
├── audio.py             # Sound effects management
├── pathfinding.py       # BFS pathfinding for ghost AI
├── utils.py             # Grid handling utilities
├── level1/
│   └── level1.txt       # ASCII level map
├── requirements.txt     # Python dependencies
├── README.md           # Project overview and setup
├── HOW_TO_PLAY.md      # Comprehensive gameplay guide
└── TESTING_GUIDE.md    # Testing instructions
```

## 🧠 Code Architecture

### 🔧 Core Modules

- **main.py**: Game loop, Pygame initialization, event handling
- **game_state.py**: State machine for different game states (menu, playing, game over, victory)
- **constants.py**: All game constants (colors, dimensions, speeds, scoring)
- **utils.py**: Coordinate conversion and vector calculation utilities

### 🎮 Game Logic

- **level.py**: ASCII map loading, wall collision detection, pellet management
- **player.py**: Input handling, grid-based movement with smooth interpolation
- **ghost.py**: Advanced AI with 4 distinct personalities and state machines
- **pathfinding.py**: BFS algorithm for optimal ghost pathfinding

### 🎨 Presentation Layer

- **hud.py**: Score display, lives counter, level information, game UI
- **audio.py**: Sound effect management and audio playback

### ⚙️ Technical Details

- **Grid System**: 16x16 pixel tiles, scaled 4x for rendering (64x64 pixels on screen)
- **Delta Time**: All movement uses delta time for consistent gameplay
- **Coordinate Systems**: Both tile coordinates (logic) and pixel coordinates (rendering)
- **Direction Changes**: Only occur at tile centers with snap-to-grid functionality
- **Collision Detection**: Checks next tile before movement execution

## 🗺️ Level Map Legend (level1/level1.txt)

- `#` = Wall
- `.` = Pellet (10 points)
- `o` = Power-pellet (50 points)
- `P` = Player spawn point
- `G` = Ghost spawn point
- ` ` = Empty space

## 🚀 Future Development Ideas

Potential enhancements for future versions:

1. **Additional Levels**: More diverse maze layouts and challenges
2. **Enhanced Graphics**: Sprite-based graphics instead of simple shapes
3. **Bonus Items**: Fruits and special items for extra points
4. **Animations**: Character movement animations and effects
5. **Difficulty Modes**: Easy, Normal, Hard with different ghost behaviors
6. **High Score System**: Persistent leaderboard functionality
7. **Multiplayer Mode**: Local co-op or competitive gameplay
8. **Custom Level Editor**: Allow users to create their own mazes

## 📋 Requirements

- **Python**: 3.9+ (3.11+ recommended)
- **Pygame**: 2.6+
- **NumPy**: 1.21+
- **Operating System**: Windows, macOS, or Linux

## 🤝 Contributing

This is an educational project, but contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is created for educational purposes. Feel free to use, modify, and distribute for learning and development purposes.

---

**Enjoy playing Maze Chomp!** 🎮✨
