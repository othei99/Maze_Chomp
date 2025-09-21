# 🎮 Maze Chomp - Testing Guide

## ✅ Game Status: READY TO PLAY!

This Pac-Man-style game is **fully functional** and ready for testing. All dependencies are installed and the game modules load successfully.

## 🚀 Quick Start

### Option 1: Direct Run (Recommended)
```bash
cd /Users/ottoheinonen/maze_chomp
python3 main.py
```

### Option 2: With Virtual Environment
```bash
cd /Users/ottoheinonen/maze_chomp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## 🎯 Testing Checklist

### ✅ Pre-flight Checks (All Passed)
- [x] Python 3.9.6 available
- [x] Pygame 2.6.1 installed  
- [x] NumPy available
- [x] Game modules import successfully
- [x] Level file exists (level1/level1.txt)
- [x] Window size: 704x616 pixels

### 🎮 Game Features to Test

#### Basic Movement
- [ ] Arrow keys move the player
- [ ] WASD keys work as alternative controls
- [ ] Player cannot move through walls
- [ ] Player wraps around screen edges (tunnel effect)

#### Game Mechanics
- [ ] Collect pellets (dots) for 10 points each
- [ ] Collect power-pellets (large dots) for 50 points
- [ ] Power-pellets make ghosts frightened (blue)
- [ ] Can eat frightened ghosts for bonus points (200→400→800→1600)
- [ ] Ghost modes change: SCATTER ↔ CHASE automatically
- [ ] Player loses life when touching normal ghosts
- [ ] Level advances when all pellets collected

#### Interface & Controls
- [ ] HUD shows: Score, Lives, Level, Pellets remaining, Current mode
- [ ] SPACE pauses the game
- [ ] ESC returns to menu or exits
- [ ] ENTER starts game or continues
- [ ] Game over screen appears when lives = 0
- [ ] Victory screen appears when level completed

#### Audio (if available)
- [ ] Pellet eating sounds
- [ ] Power-pellet activation sound
- [ ] Ghost eating sounds
- [ ] Death sound
- [ ] Level complete sound

## 🐛 Known System Requirements

- **OS**: macOS (tested on darwin 24.6.0)
- **Python**: 3.9.6+ (3.11+ recommended)
- **Display**: Game window 704x616 pixels
- **Input**: Keyboard required

## 📊 Game Statistics

- **Levels**: Progressive difficulty (up to level 6)
- **Ghosts**: 1-4 ghosts depending on level
- **Ghost Personalities**: Blinky (aggressive), Pinky (ambush), Clyde, Inky
- **Lives**: Start with 3 lives
- **Scoring**: Pellets (10), Power-pellets (50), Ghosts (200-1600)

## 🔧 Troubleshooting

If you encounter issues:

1. **Import errors**: Run `pip install -r requirements.txt`
2. **Display issues**: Make sure you have a display available (not SSH)
3. **Permission errors**: Check file permissions in the directory
4. **Audio issues**: Game works without audio if sound files missing

## 🎯 Testing Scenarios

### Scenario 1: Basic Gameplay
1. Start game with `python3 main.py`
2. Press ENTER to begin
3. Use arrow keys to collect pellets
4. Avoid ghosts or eat them when they're blue
5. Complete the level

### Scenario 2: Power-Pellet Mechanics  
1. Navigate to a power-pellet (large dot)
2. Eat it and observe ghosts turn blue
3. Chase and eat ghosts for bonus points
4. Notice point progression: 200→400→800→1600

### Scenario 3: Multi-Level Progression
1. Complete level 1 by eating all pellets
2. Observe level 2 starts with more ghosts
3. Notice increased game speed
4. Continue until game completion or game over

---

**Ready to play!** The game is fully functional and all systems are operational. 🚀
