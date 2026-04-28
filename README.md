<img width="668" height="896" alt="screenshot" src="https://github.com/user-attachments/assets/8c216268-6c90-4b53-839d-400ad6c4c662" />




# Dodge the Balls

Dodge the Balls is a small, charming arcade-style Python game, using the knowledge from 15-110 (CMU), where you control a player sprite and try to survive as long as possible while colorful balls fall from the sky. With a cozy snowfall effect, responsive controls, and an ever-increasing challenge, this little game is perfect for quick breaks, demos, or learning how simple game mechanics work with Pygame.

## Features

- Simple, addictive gameplay: survive as long as possible while balls fall.
- Smooth, responsive controls using the left/right arrow keys.
- Gradually increasing difficulty — balls fall faster over time.
- Decorative snowfall effect for atmosphere.
- Lightweight: a single-folder project using only Python and Pygame.

## Requirements

- Python 3.8+ (likely any modern Python 3 release)
- Pygame

## Install

Open a terminal (zsh on macOS) and run:

```bash
python3 -m pip install --user pygame
```

If you use a virtual environment, activate it first, then install without `--user`.

## Run

Make sure `player.png` is present in the same folder as the game scripts. Then run the game from the project directory:

```bash
cd DodgeBalls
python3 RUN.py
```

Notes:
- The main loop and entry point are in `RUN.py`.
- If the window is too large or small, edit the `WIDTH` and `HEIGHT` variables at the top of `RUN.py`.

## Controls

- Left Arrow: move left
- Right Arrow: move right
- Close window or press the window close button to quit
- When you collide with a ball, the game shows "GAME OVER" and press any key to restart

## How it works (quick dev notes)

- `RUN.py`: bootstraps Pygame, sets up the window, spawns falling `Ball` objects, tracks time-based score, and contains the main game loop.
- `Sprite.py`: defines `Player`, `Ball`, and `SnowFlake` classes. The `Player` uses `player.png` as its sprite.
- `Window.py`: creates the Pygame window, the clock, and a shared font for on-screen text.

If you'd like to tinker:
- Change `move_speed` in `RUN.py` to make the player faster/slower.
- Adjust spawn timing or `fall_speed` growth to tune difficulty.
- Replace `player.png` with your own 60×60 image to change the player look.

## Contributing

All contributions are welcome — bug fixes, polish, or creative features. A few ideas:

- Add sound effects for collisions and scoring.
- Add multiple ball types or power-ups.
- Add high score persistence or a menu screen.

To contribute, fork the repo, make changes, and open a pull request with a brief description of your change.

## License

Unlicense

## Credits

Built with Pygame. Thanks to the Python and Pygame communities for great learning resources.

---

Enjoy the game — how long can you survive?
