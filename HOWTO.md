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

[game/surface.py](game/surface.py) contains the base class `Surface` which all surfaces should inherit from. The class provides a set of abstract methods that must be implemented by all surfaces. They are:

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
        super().__init__()
        # State goes here
        self.surface = surface
        self.assets = kwargs["assets"]
        self.frame_count = 0
        self.component = MyTextComponent()
    
    def hook(self) -> None:
        print("MyCustomSurface has been activated! Let's play some music!")
        pygame.mixer.music.load("/path/to/soothing/music.mp3")
        pygame.mixer.music.play(-1) # Loop indefinitely

    def on_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print("Space key pressed!")
        self.component.on_event(event) # Passes the event to the component, if required

    def update(self) -> None:
        self.frame_count += 1
        print(f"MyCustomSurface is updating! Frame count: {self.frame_count}")
        self.component.update() # Updates the component, if required

    def draw(self) -> None:
        self.component.draw(self.surface) # Draws the component to the surface, if required
```

You can also add custom methods to make code within the surface more organized and reusable. By conventions, all methods that are used internally within the surface should be prefixed with dunders (double-underscores aka "__"). e.g. `__some_private_method()`. Methods that are expected to be called from outside the surface should not have dunders. e.g. `some_public_method()`.

## 3. (game) Managing surfaces

This is where the `SurfaceManager` class in [game/surface.py](game/surface.py) comes in. This class is responsible for managing the surfaces in the game. It provides methods for activating, deactivating, and setting surfaces surfaces.

e.g.

```python
# game/main.py
import pygame
from game.assets import Assets
from game.surface import SurfaceManager
from game.surfaces._1_my_custom import MyCustomSurface

pygame.init() # Initialize pygame
surface = pygame.display.set_mode((800, 600)) # Create an empty 800x600 surface
assets = Assets() # Initialize the assets

manager = SurfaceManager(surface, assets) # The manager expects an initialized surface and assets

manager.surfaces["my_custom"] = MyCustomSurface(surface, assets=assets) # Add the surface to the manager
# for some, MyOtherCustomSurface
manager.surfaces["my_other_custom"] = MyOtherCustomSurface(surface, assets=assets) # Add the surface to the manager

manager.set_active_surface_by_name("my_custom") # Activates the surface
manager.set_active_surface_by_name("my_other_custom") # Activates the surface, and at the same time deactivates "my_custom"

print(manager.active_surface) # Prints the active surface
print(manager.active_surface_name) # Prints the name of the active surface
print(manager.last_active_surface_name) # Prints the name of the last active surface
```

All the pre-defined methods in the `Surface` class exist so it can be used by the manager to manage the surface's lifecycle. They can be overriden to modify the behaviour if necessary. Ideally, you should only be overriding the `hook()` method.

## 4. (game) Small notes on SFX audio

Volume controls for SFX (`pygame.mixer.Sound` objects) are also controlled by the manager. 

e.g.

```python
manager.set_global_sfx_volume(0.5) # Sets the volume to 50%

print(manager.current_global_sfx_volume) # Prints the current volume
print(manager.sfx_objects) # Prints the SFX objects
```

I couldn't find a unified way to control SFX volume using pygame's apis, so I ended up using a list to keep track of all the SFX objects. This way, I can iterate through the list and adjust the volume of each object. This is also decently efficient.

For sounds loaded using `pygame.mixer.music`, you can simply use the existing `set_volume()` and `get_volume()` methods. No need to reinvent the wheel here.

## 5. (game) Writing new components

Components are reusable building blocks that encapsulate specific UI elements and their behaviors. Unlike the `Surface` class which enforces a strict protocol, components are flexible and can implement only the methods they need. Common methods include:

- `on_event()` - Handle user input and interactions
- `update()` - Update internal state 
- `draw()` - Render the component visually

While there's no required interface, following these common patterns makes components more maintainable and easier to use consistently across the codebase. The goal is to break down complex UI into smaller, focused pieces that can be composed together.

e.g.

```python
import pygame

class MyCustomComponent:
    def __init__(self):
        # State goes here
        self.name = "My Custom Component"

    def on_event(self, event: pygame.event.Event) -> None:
        # Handle events here
        ...

    def update(self) -> None:
        # Update the component's state here
        ...

    def draw(self, surface: pygame.Surface) -> None:
        # Draw the component to the screen here
        # Unlike surfaces, components ideally should take in a surface parameter in the draw method only
        # This allows for more flexibility and reusability as a pre-defined component can be drawn on any surface
        # Surfaces do not typically need this flexibility as their fate is set in stone at the beginning of the program :)
        ...
```

Again, you can add custom methods just like in the `Surface` class. The same naming conventions apply.