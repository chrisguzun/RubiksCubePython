# RubiksCubePython

An interactive 3D Rubik's Cube renderer and simulator built with Python and Pygame. Rotate faces with the keyboard, apply standard algorithms, shuffle the cube, and orbit the camera freely with the mouse.

## Features

- Fully rendered 3D cube with perspective projection (no external 3D library)
- Smooth animated face rotations
- Standard Rubik's Cube notation (U, D, R, L, F, B with `'` for counterclockwise)
- Built-in algorithms: Checker Board, Dot, Corner Twist, Cube-in-a-Cube, and more
- Shuffle with 50 random moves
- Undo via Reset (reverses all moves made this session)
- Resizable window

## Requirements

- Python 3.8+
- pygame

## Installation

```bash
git clone https://github.com/chrisguzun/RubiksCubePython.git
cd RubiksCubePython
pip install -r requirements.txt
```

## Usage

```bash
python rubikscube.py
```

### Controls

| Input | Action |
|---|---|
| Mouse drag | Orbit camera |
| `W` | Rotate **Top** face |
| `S` | Rotate **Bottom** face |
| `A` | Rotate **Front** face |
| `D` | Rotate **Back** face |
| `Q` | Rotate **Right** face |
| `E` | Rotate **Left** face |
| `M` | Toggle side menu |
| `Esc` | Release mouse |

### Menu Options (press `M`)

- **Shuffle** — apply 50 random moves
- **Reset** — reverse all moves made this session
- **Instant Move** — toggle between smooth animation and instant rotation
- Algorithm buttons — apply named algorithms directly
