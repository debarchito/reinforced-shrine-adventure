## About

This project serves as a *text-based adventure game-ish environment* to train solo **RL agents**. I prepared this as a showcase for a `#BuildWithAI` event organized by `GDG on Campus | AdtU`. 

## Run

This project uses the [uv](https://github.com/astral-sh/uv) package manager (written in *Rust* btw). **uv** automatically creates and manages a **.venv** for you. Ensure you are using **Python 3.12+**.

```sh
git clone https://github.com/debarchito/reinforced-shrine-adventure.git
cd reinforced-shrine-adventure

# Creates .venv and installs packages
uv sync

# Activate the .venv (fish shell e.g.)
source .venv/bin/activate.fish

# Run the game
python src/main.py
```
