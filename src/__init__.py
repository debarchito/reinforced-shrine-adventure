from .game import main
from .init import Assets
from .surface import Surface, SurfaceManager
from .surfaces.root import RootSurface
from .surfaces.settings import SettingsSurface
from .components.text import Text
from .components.button import Button

__all__ = [
    "main",
    "Assets",
    "Surface",
    "SurfaceManager",
    "RootSurface",
    "SettingsSurface",
    "Text",
    "Button",
]
