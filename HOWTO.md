## 1. Structure

The project is structured as follows:

- `assets`: Contains all of the game's assets.
- `game`: Contains all of the game's code.
- `playground`: Contains all the code for the `RL` environment and agents.
- `story`: Contains the story written in `Ink` (also contains the compiled artifact under `story/json`).

## 2. (game) Writing new surfaces

> **NOTE regarding HMR:**
>
> Files in the `game/surfaces` directory receive comprehensive hot-patching during HMR:
> - All code and state within these files is hot-patched, regardless of whether it exists inside or outside the game loop.
> - For files outside of `game/surfaces`:
>   - Methods executed within the game loop are hot-patched.
>   - State updates stay stagnant during hot-patching. A restart is required to update the state.

[game/surface.py](game/surface.py) contains the base class `Surface` which all surfaces should inherit from. It expects a blank surface to be passed as an argument during initialization. The class provides a set of abstract methods that must be implemented by all surfaces. They are:

- `on_event(event: pygame.event.Event)`: This method is how the surface listens to and handles events.
- `update()`: This method is called every frame. It is used to update the state of the surface.
- `draw()`: This method is also called every frame. It is used to draw necessary changes to the surface.

Additionally, the `Surface` class also provides some pre-defined methods (inherited by all surfaces) that are intrinsically linked to the surface's lifecycle:

- `activate()`: This method is used to activate the surface.
- `deactivate()`: This method is used to deactivate the surface. On deactivation, the surface pauses its on_event/update/draw cycles.
- `hook()`: This method is called every time the surface is activated. It is used to run any necessary setup code for the surface. By default, this method does nothing; override it accordingly. This is not an abstract method as it's expected to be present in all surfaces.

e.g.

```python
# game/surfaces/_1_my_custom.py
# HMR hot-patching class resolution rules:
# 1. Converts snake_case to PascalCase (e.g. _1_my_custom -> _1_MyCustom)
# 2. Removes leading _<number>_; good for order (e.g. _1_my_custom -> MyCustom)
# 3. Appends "Surface" to the class name (e.g. _1_my_custom -> MyCustomSurface)
# 4. Looks for the class "MyCustomSurface" to patch.
# So, name your surfaces like this: _<number>_<snake_case>.py and leave the rest to the parser magic.
import pygame
from game.surface import Surface

class MyCustomSurface(Surface):
    def __init__(self, surface: pygame.Surface, **kwargs):
        super().__init__(surface)
        # State goes here
        self.frame_count = 0
        self.component = MyTextComponent()
    
    def hook(self) -> None:
        print("MyCustomSurface has been activated! Let's play some music!")
        pygame.mixer.music.load("/path/to/soothing/music.mp3")
        pygame.mixer.music.play(-1) # Loop indefinitely

    def on_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space key pressed!")
        self.component.on_event(event) # Passes the event to the component

    def update(self) -> None:
        self.frame_count += 1
        print(f"MyCustomSurface is updating! Frame count: {self.frame_count}")
        self.component.update() # Updates the component

    def draw(self) -> None:
        self.component.draw(self.surface) # Draws the component to the surface
```
