## About

This project serves as a *text-based adventure game-ish environment* to train solo **RL agents**. I prepared this as a showcase for a `#BuildWithAI` event organized by `GDG on Campus | AdtU`. 

## Run

This project uses the [pixi](https://github.com/prefix-dev/pixi) package manager (written in *Rust* btw).

```sh
git clone https://github.com/debarchito/reinforced-shrine-adventure.git
cd reinforced-shrine-adventure

# If your system is avx2 capable, set this env variable to "1" before installing packages
# set PYGAME_DETECT_AVX2 1 # fish
# export PYGAME_DETECT_AVX2=1 # bash/zsh
# $env:PYGAME_DETECT_AVX2="1" # powershell

# Installs packages
pixi install

# Activate the shell
pixi shell

# Run the game
pixi run game
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
