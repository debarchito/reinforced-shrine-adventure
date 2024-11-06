"""Provide type-safe access to game assets including images, fonts, sounds and story."""

import pygame
from bink.story import story_from_file


class Fonts:
    """Load and provide type-safe access to fonts."""

    __slots__ = ()

    def monogram_extended(self, size: int) -> pygame.font.Font:
        """Load monogram extended font at specified size."""
        return pygame.font.Font("assets/fonts/truetype/monogram_extended.ttf", size)

    def monogram_extended_italic(self, size: int) -> pygame.font.Font:
        """Load monogram extended italic font at specified size."""
        return pygame.font.Font(
            "assets/fonts/truetype/monogram_extended_italic.ttf", size
        )


class Backgrounds:
    """Load and provide type-safe access to background images."""

    __slots__ = ()

    def moon_sky(self, namehint: str = "") -> pygame.Surface:
        """Load moon sky background."""
        return pygame.image.load("assets/images/backgrounds/moon_sky.png", namehint)

    def empty_classroom(self, namehint: str = "") -> pygame.Surface:
        """Load empty classroom background."""
        return pygame.image.load(
            "assets/images/backgrounds/empty_classroom.jpg", namehint
        )

    def bedroom(self, namehint: str = "") -> pygame.Surface:
        """Load bedroom background."""
        return pygame.image.load("assets/images/backgrounds/bedroom.jpg", namehint)

    def abandoned_amusement_park(self, namehint: str = "") -> pygame.Surface:
        """Load abandoned amusement park background."""
        return pygame.image.load(
            "assets/images/backgrounds/abandoned_amusement_park.jpg", namehint
        )

    def maintenance_station(self, namehint: str = "") -> pygame.Surface:
        """Load maintenance station background."""
        return pygame.image.load("assets/images/backgrounds/maintenance_station.jpg", namehint)

    def beach(self, namehint: str = "") -> pygame.Surface:
        """Load beach house background."""
        return pygame.image.load("assets/images/backgrounds/beach.jpg", namehint)

class UI:
    """Load and provide type-safe access to UI elements."""

    __slots__ = ()

    def button_start(self, namehint: str = "") -> pygame.Surface:
        """Load start button."""
        return pygame.image.load("assets/images/ui/button_start.png", namehint)

    def button_start_hover(self, namehint: str = "") -> pygame.Surface:
        """Load start button hover state."""
        return pygame.image.load("assets/images/ui/button_start_hover.png", namehint)

    def button_start_active(self, namehint: str = "") -> pygame.Surface:
        """Load start button active state."""
        return pygame.image.load("assets/images/ui/button_start_active.png", namehint)

    def button_cog(self, namehint: str = "") -> pygame.Surface:
        """Load cog button."""
        return pygame.image.load("assets/images/ui/button_cog.png", namehint)

    def button_cog_hover(self, namehint: str = "") -> pygame.Surface:
        """Load cog button hover state."""
        return pygame.image.load("assets/images/ui/button_cog_hover.png", namehint)

    def button_cog_active(self, namehint: str = "") -> pygame.Surface:
        """Load cog button active state."""
        return pygame.image.load("assets/images/ui/button_cog_active.png", namehint)

    def button_quit(self, namehint: str = "") -> pygame.Surface:
        """Load quit button."""
        return pygame.image.load("assets/images/ui/button_quit.png", namehint)

    def button_quit_hover(self, namehint: str = "") -> pygame.Surface:
        """Load quit button hover state."""
        return pygame.image.load("assets/images/ui/button_quit_hover.png", namehint)

    def button_quit_active(self, namehint: str = "") -> pygame.Surface:
        """Load quit button active state."""
        return pygame.image.load("assets/images/ui/button_quit_active.png", namehint)

    def button_home(self, namehint: str = "") -> pygame.Surface:
        """Load home button."""
        return pygame.image.load("assets/images/ui/button_home.png", namehint)

    def button_home_hover(self, namehint: str = "") -> pygame.Surface:
        """Load home button hover state."""
        return pygame.image.load("assets/images/ui/button_home_hover.png", namehint)

    def button_home_active(self, namehint: str = "") -> pygame.Surface:
        """Load home button active state."""
        return pygame.image.load("assets/images/ui/button_home_active.png", namehint)

    def button_arrow_left(self, namehint: str = "") -> pygame.Surface:
        """Load left arrow button."""
        return pygame.image.load("assets/images/ui/button_arrow_left.png", namehint)

    def button_arrow_left_hover(self, namehint: str = "") -> pygame.Surface:
        """Load left arrow button hover state."""
        return pygame.image.load(
            "assets/images/ui/button_arrow_left_hover.png", namehint
        )

    def button_arrow_left_active(self, namehint: str = "") -> pygame.Surface:
        """Load left arrow button active state."""
        return pygame.image.load(
            "assets/images/ui/button_arrow_left_active.png", namehint
        )

    def button_play(self, namehint: str = "") -> pygame.Surface:
        """Load play button."""
        return pygame.image.load("assets/images/ui/button_play.png", namehint)

    def button_play_hover(self, namehint: str = "") -> pygame.Surface:
        """Load play button hover state."""
        return pygame.image.load("assets/images/ui/button_play_hover.png", namehint)

    def button_play_active(self, namehint: str = "") -> pygame.Surface:
        """Load play button active state."""
        return pygame.image.load("assets/images/ui/button_play_active.png", namehint)

    def button_question(self, namehint: str = "") -> pygame.Surface:
        """Load question button."""
        return pygame.image.load("assets/images/ui/button_question.png", namehint)

    def button_question_hover(self, namehint: str = "") -> pygame.Surface:
        """Load question button hover state."""
        return pygame.image.load("assets/images/ui/button_question_hover.png", namehint)

    def button_question_active(self, namehint: str = "") -> pygame.Surface:
        """Load question button active state."""
        return pygame.image.load(
            "assets/images/ui/button_question_active.png", namehint
        )

    def banner_dialogue_wood(self, namehint: str = "") -> pygame.Surface:
        """Load wooden dialogue banner."""
        return pygame.image.load("assets/images/ui/banner_dialogue_wood.png", namehint)

    def banner_choice_wood(self, namehint: str = "") -> pygame.Surface:
        """Load wooden choice banner."""
        return pygame.image.load("assets/images/ui/banner_choice_wood.png", namehint)

    def border_character_wood(self, namehint: str = "") -> pygame.Surface:
        """Load wooden character border."""
        return pygame.image.load("assets/images/ui/border_character_wood.png", namehint)

    def border_dialogue_wood(self, namehint: str = "") -> pygame.Surface:
        """Load wooden dialogue border."""
        return pygame.image.load("assets/images/ui/border_dialogue_wood.png", namehint)

    def border_choice_wood(self, namehint: str = "") -> pygame.Surface:
        """Load wooden choice border."""
        return pygame.image.load("assets/images/ui/border_choice_wood.png", namehint)


class Characters:
    """Load and provide type-safe access to character sprites."""

    __slots__ = ()

    def aie(self, namehint: str = "") -> pygame.Surface:
        """Load Aie character sprite."""
        return pygame.image.load("assets/images/characters/aie.png", namehint)

    def haruto(self, namehint: str = "") -> pygame.Surface:
        """Load Haruto character sprite."""
        return pygame.image.load("assets/images/characters/haruto.png", namehint)

    def ryu(self, namehint: str = "") -> pygame.Surface:
        """Load Ryu character sprite."""
        return pygame.image.load("assets/images/characters/ryu.png", namehint)

    def airi(self, namehint: str = "") -> pygame.Surface:
        """Load Airi character sprite."""
        return pygame.image.load("assets/images/characters/airi.png", namehint)

    def kanae(self, namehint: str = "") -> pygame.Surface:
        """Load Kanae character sprite."""
        return pygame.image.load("assets/images/characters/kanae.png", namehint)

    def kaori(self, namehint: str = "") -> pygame.Surface:
        """Load Kaori character sprite."""
        return pygame.image.load("assets/images/characters/kaori.png", namehint)


class Images:
    """Provide type-safe access to all game images."""

    __slots__ = ("backgrounds", "ui", "characters")

    def __init__(self) -> None:
        self.backgrounds = Backgrounds()
        self.ui = UI()
        self.characters = Characters()


class Sounds:
    """Load and provide type-safe access to sound effects and music."""

    __slots__ = ()

    def ambient_evening(self) -> str:
        """Get ambient evening music path."""
        return "assets/sounds/music/ambient_evening.mp3"

    def empty_classroom(self) -> str:
        """Get empty classroom music path."""
        return "assets/sounds/music/empty_classroom.mp3"

    def cicada(self) -> str:
        """Get cicada music path."""
        return "assets/sounds/music/cicada.mp3"

    def button_click_1(self) -> str:
        """Get button click sound effect path."""
        return "assets/sounds/sfx/button_click_1.mp3"

    def button_click_2(self) -> str:
        """Get button click sound effect path."""
        return "assets/sounds/sfx/button_click_2.mp3"


class Assets:
    """Provide type-safe access to all game assets."""

    __slots__ = ("fonts", "images", "sounds", "story")

    def __init__(self) -> None:
        self.fonts = Fonts()
        self.images = Images()
        self.sounds = Sounds()
        self.story = story_from_file("story/json/story.ink.json")
