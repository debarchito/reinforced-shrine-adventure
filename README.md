## About

This project serves as a *text-based adventure game-ish environment* to train solo **RL agents**. I prepared this as a showcase for a `#BuildWithAI` event organized by `GDG on Campus | AdtU`. 

## Run

This project uses the [pixi](https://github.com/prefix-dev/pixi) package manager (written in *Rust* btw). To install `pixi`, run:

```sh
# Install pixi on Linux & macOS
curl -fsSL https://pixi.sh/install.sh | bash

# Install pixi on Windows (Powershell)
iwr -useb https://pixi.sh/install.ps1 | iex

# Linux & macOS autocompletions for pixi
echo 'pixi completion --shell fish | source' >> ~/.config/fish/config.fish # fish
echo 'eval "$(pixi completion --shell zsh)"' >> ~/.zshrc # zsh
echo 'eval "$(pixi completion --shell bash)"' >> ~/.bashrc # bash

# Windows (Powershell) autocompletions for pixi
Add-Content -Path $PROFILE -Value '(& pixi completion --shell powershell) | Out-String | Invoke-Expression'

# Clone the repo and cd into it
git clone https://github.com/debarchito/reinforced-shrine-adventure.git
cd reinforced-shrine-adventure

# If your system is avx2 capable, set this env variable to "1" before installing packages
set PYGAME_DETECT_AVX2 1 # fish
export PYGAME_DETECT_AVX2=1 # bash or zsh
$env:PYGAME_DETECT_AVX2="1" # powershell

# Install dependencies
pixi install

# Activate the virtual environment
pixi shell

# Run the game
pixi run game
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
