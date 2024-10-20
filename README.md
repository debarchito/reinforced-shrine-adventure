## About

This project serves as a *text-based adventure game-ish environment* to train solo **RL agents**. I prepared this as a showcase for a `#BuildWithAI` event organized by `GDG on Campus | AdtU`. But, this is not a solo effort. Contributions from `GDG on Campus | AdtU` team and community members have made this possible.

## Usage and development

This project uses the [pixi](https://github.com/prefix-dev/pixi) package manager (written in *Rust* btw). Follow the instructions below to install `pixi`, setup autocompletions and run the game:

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

# Run the game. Hot-Module-Replacement (HMR) is enabled
pixi run game
```

## How do I work on the story?

The story is written using the [Ink](https://github.com/inkle/ink) scripting language and [Inky](https://github.com/inkle/inky) editor for real-time feedback. You can find the story in the [story](story) directory. To load the story in the game, you need to export it as `JSON` (functionality available in the `Inky` editor). Check [story.ink.json](story/json/story.ink.json) for the exported version of the complete story (as it stands).

> You can get started with `Ink` using the official documentation: [WritingWithInk](https://github.com/inkle/ink/blob/master/Documentation/WritingWithInk.md). It covers everything you need to write succesful stories in `Ink`. If you want a video tutorial, I recommend [Learn Ink (video game dialogue language) in 15 minutes | Ink tutorial](https://youtu.be/KSRpcftVyKg?si=h3jSHifFc-Qa-kCR) by [Shaped By Rain Studios](https://www.youtube.com/@ShapedByRainStudios). I personally found it quite helpful.

[story.ink](story/story.ink) serves as the entry point for the story in the game. Put seperate scenes in separate files inside the [story](story) directory. Afterwards, import them in [story.ink](story/story.ink) and use them in appropriate places.

## Credits for assets used?

Please check the [assets/Credits.md](assets/Credits.md) file. It contains the credits for all the assets used in this project.

## License

This project is licensed under the `MIT License`. See the [LICENSE](LICENSE) file for more details.
