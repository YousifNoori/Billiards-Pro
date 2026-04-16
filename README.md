# Billiards Pro

A browser-based billiards game with realistic physics simulation. Built using a C physics library for performance-critical calculations, a Python backend for game logic and HTTP serving, and SVG rendering for the table and ball animations in the browser.

---

## Features

- **Physics simulation in C** — ball movement, drag, collision detection, and cushion bouncing implemented in `phylib.c` with real-world constants (ball radius, drag coefficient, table dimensions)
- **Python/C integration** — `phylib.c` is wrapped with SWIG (`phylib.i`) and imported directly into Python, bridging low-level physics with high-level game logic
- **SVG rendering** — each frame of the simulation is rendered as an SVG file and served to the browser, producing smooth animated ball movement
- **HTTP game server** — a custom Python HTTP server handles GET and POST requests, manages game state, and serves pages and SVG frames
- **Shot input** — players specify the cue ball position, rolling ball, and shot direction via a web form; the server simulates the full shot and streams the result back as an animation
- **SQLite game state** — ball positions and game state are persisted to a SQLite database between shots

---

## Requirements

- Python 3
- GCC
- SWIG (`swig` on PATH)
- SQLite3

---

## Build

```bash
make
```

This compiles `phylib.c` into a shared library and generates the SWIG Python bindings.

To clean:

```bash
make clean
```

---

## Usage

**Start the server:**
```bash
python3 server.py <port>
```

Example:
```bash
python3 server.py 8080
```

**Open the game in your browser:**
```
http://localhost:8080/homePage.html
```

From there, navigate to the shot page and enter your shot parameters to play.

---

## Project Structure

```
billiards-pro/
├── phylib.c        C physics library — ball movement, drag, collision detection
├── phylib.h        Physics constants and type definitions
├── phylib.i        SWIG interface file — exposes C library to Python
├── Physics.py      Python game logic — wraps phylib, manages SVG generation and SQLite
├── server.py       Custom HTTP server — handles GET/POST, serves pages and SVG frames
├── homePage.html   Landing page
├── shoot.html      Shot input form
└── makefile        Builds shared library and SWIG bindings
```

---

## Design Notes

**Physics engine** — `phylib.c` models each object on the table (still balls, rolling balls, holes, cushions) as a tagged union. The simulation steps forward at `0.0001s` intervals, applying drag to rolling balls, detecting collisions between balls, and stopping balls that fall below the velocity threshold (`0.01 mm/s`). Constants reflect real billiards table dimensions (2700mm × 1350mm) and ball radius (28.5mm).

**Python/C bridge** — SWIG generates a Python module from `phylib.i`, allowing `Physics.py` to call the C simulation functions directly. This keeps performance-critical physics in C while game logic, database management, and HTTP handling stay in Python.

**SVG animation** — After a shot is submitted, the server runs the full physics simulation and writes each frame as an SVG file to disk. The browser receives these frames sequentially, producing a smooth animation of the shot.

**HTTP server** — Built on Python's `http.server` module. GET requests serve HTML pages and SVG frames. POST requests to `/display.html` accept shot parameters, validate input, run the simulation, and return the animated result.

**SQLite persistence** — Ball positions and game state are stored in a SQLite database via `Physics.py`, allowing state to persist between shots without keeping everything in memory.

---

## Known Limitations

- Single player / no multiplayer support
- SVG frames are written to disk rather than streamed in memory
- No win condition detection implemented
