# 🎮 Maze Chomp - Testing Guide

## ✅ Game Status: READY TO PLAY!

This Pac-Man-style game is **fully functional** and ready for testing by anyone on any system.

## 📋 Prerequisites

Before testing, make sure you have:
- **Python 3.9+** installed ([Download here](https://python.org))
- **Git** installed ([Download here](https://git-scm.com))
- **Working display** (GUI environment, not SSH terminal)
- **Keyboard** for game controls

## 🚀 Step-by-Step Setup

### Step 1: Download the Game
```bash
git clone https://github.com/othei99/Maze_Chomp.git
cd Maze_Chomp
```

### Step 2: Install Dependencies
```bash
# On macOS/Linux:
pip3 install -r requirements.txt

# On Windows:
pip install -r requirements.txt

# If pip not found, try:
python3 -m pip install -r requirements.txt
```

### Step 3: Run the Game
```bash
# On macOS/Linux:
python3 main.py

# On Windows:
python main.py
```

**That's it!** The game should start immediately.

## 🖥️ System Compatibility

### ✅ Supported Operating Systems
- **Windows** 10/11
- **macOS** 10.14+
- **Linux** (Ubuntu, Debian, Fedora, etc.)

### ✅ Python Versions
- **Python 3.9** ✅
- **Python 3.10** ✅
- **Python 3.11** ✅ (Recommended)
- **Python 3.12** ✅

## 🧪 Quick Verification

### Test Installation Success
```bash
# On macOS/Linux:
python3 -c "import pygame; print('✅ Pygame installed:', pygame.version.ver)"
python3 -c "import numpy; print('✅ NumPy installed:', numpy.__version__)"

# On Windows:
python -c "import pygame; print('✅ Pygame installed:', pygame.version.ver)"
python -c "import numpy; print('✅ NumPy installed:', numpy.__version__)"
```

If both commands work without errors, you're ready to play!

## 🎯 Complete Testing Checklist

### 📦 Installation Verification
- [ ] Game downloads successfully from GitHub
- [ ] Dependencies install without errors  
- [ ] Game starts without import errors
- [ ] Game window opens (704x616 pixels)
- [ ] No error messages in terminal

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

## 🔧 Troubleshooting Common Issues

### ❌ "python: command not found"
**Solution:** On macOS/Linux, use `python3` instead:
```bash
python3 main.py
```

### ❌ "pip: command not found"  
**Solutions:**
- **macOS/Linux:** Try `pip3` or `python3 -m pip`:
```bash
pip3 install -r requirements.txt
# OR
python3 -m pip install -r requirements.txt
```
- **Windows:** Try `python -m pip install -r requirements.txt`

### ❌ "ModuleNotFoundError: No module named 'pygame'"
**Solution:** Install dependencies with `pip install -r requirements.txt`

### ❌ "Permission denied" errors
**Solution:** Try `pip install --user -r requirements.txt`

### ❌ Game window doesn't appear
**Solutions:**
- Make sure you're not running in SSH/terminal-only environment
- Try running from a GUI terminal (Terminal.app, Command Prompt, etc.)
- Check if display is available: `echo $DISPLAY` (Linux)

### ❌ "destination path 'Maze_Chomp' already exists"
**Solutions:**
- **Use existing directory:** `cd Maze_Chomp` (if you already cloned it)
- **Delete and re-clone:** `rm -rf Maze_Chomp` then clone again
- **Clone to different name:** `git clone https://github.com/othei99/Maze_Chomp.git Maze_Chomp_Test`

### ❌ "fatal: repository does not exist"
**Solution:** Make sure the GitHub URL is correct:
```bash
git clone https://github.com/othei99/Maze_Chomp.git
```

## 📊 What You're Testing

- **Complete Pac-Man Game**: 6 levels with progressive difficulty
- **Smart Ghost AI**: 4 different ghost personalities and behaviors  
- **Full Game Mechanics**: Pellets, power-pellets, scoring, lives system
- **Professional Code**: Modular architecture, clean documentation
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🎯 Testing Scenarios

### Scenario 1: First Time Setup
1. **Clone repository:** `git clone https://github.com/othei99/Maze_Chomp.git`
2. **Enter directory:** `cd Maze_Chomp`  
3. **Install dependencies:** 
   - macOS/Linux: `pip3 install -r requirements.txt`
   - Windows: `pip install -r requirements.txt`
4. **Start game:** 
   - macOS/Linux: `python3 main.py`
   - Windows: `python main.py`
5. **Verify:** Game window opens, menu appears

### Scenario 2: Basic Gameplay Test
1. **Start game:** Press ENTER at menu
2. **Movement:** Use arrow keys to move around
3. **Collect pellets:** Eat small dots for 10 points each
4. **Avoid ghosts:** Don't touch colored ghosts
5. **Verify:** Score increases, movement is smooth

### Scenario 3: Power-Pellet Test  
1. **Find power-pellet:** Large dot in maze corner
2. **Eat power-pellet:** Walk into it
3. **Observe:** All ghosts turn blue
4. **Chase ghosts:** Eat blue ghosts for bonus points
5. **Verify:** Points increase: 200→400→800→1600

### Scenario 4: Complete Level Test
1. **Collect all pellets:** Clear entire maze
2. **Observe:** Level complete screen appears
3. **Continue:** Press ENTER for next level
4. **Verify:** Level 2 starts with more ghosts

## ✅ Success Criteria

The game passes testing if:
- ✅ Downloads and installs without errors
- ✅ Game window opens correctly
- ✅ All controls respond properly
- ✅ Graphics display correctly
- ✅ Sound effects play (if audio available)
- ✅ Game mechanics work as expected
- ✅ No crashes or error messages

## 📞 Getting Help

If you encounter issues:
1. **Check this troubleshooting guide** above
2. **Review the [HOW_TO_PLAY.md](HOW_TO_PLAY.md)** for gameplay help
3. **Open an issue** on GitHub: https://github.com/othei99/Maze_Chomp/issues

---

**The game is ready for testing by anyone, anywhere!** 🚀🎮

*This guide ensures successful testing on Windows, macOS, and Linux systems.*
