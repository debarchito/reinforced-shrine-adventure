import pygame
from game.assets import Assets
from game.components.choice_banner import ChoiceBanner
from game.components.dialogue_banner import DialogueBanner


class SceneDynamics:
    """
    Handles core scene dynamics like choices, dialogue and transitions.
    """

    def __init__(self, surface: pygame.Surface, assets: Assets):
        self.surface = surface
        self.assets = assets
        self.story = assets.story
        self.choice_banners: list[tuple[ChoiceBanner, int]] = []
        self.dialogue_banner: DialogueBanner | None = None
        self.character_sprite: pygame.Surface | None = None
        self.button_click_1 = pygame.mixer.Sound(assets.sounds.button_click_1())
        self.walking_frame = 0
        self.walking_timer = 0
        self.animation_state = "standing"
        self.state_timer = 0
        self.animation_sequence = [
            "standing",
            "walking",
            "standing",
            "standing_left",
            "walking_left",
            "standing_left",
            "standing_right",
            "walking_right",
            "standing_right",
        ]
        self.sequence_index = 0

    def get_next_dialogue(self) -> str:
        """
        Get next line of dialogue from story.
        """

        while self.story.can_continue():
            text = self.story.cont()
            if text.strip():
                return text
        return ""

    def parse_dialogue(self, text: str) -> tuple[str | None, str]:
        """
        Parse dialogue text to extract character name and content.
        """

        if not text.startswith("@"):
            return None, text

        parts = text.split(":", 1)
        if len(parts) != 2:
            return None, text

        return parts[0][1:].strip(), parts[1].strip()

    def create_dialogue_banner(
        self, text: str, char_name: str | None
    ) -> DialogueBanner:
        """
        Create a dialogue banner with the given parameters.
        """

        return DialogueBanner(
            surface=self.surface,
            banner_image=self.assets.images.ui.banner_dialogue_wood(),
            text_content=text,
            text_color=(42, 0, 30),
            font=self.assets.fonts.monogram_extended(50),
            character_name=char_name,
            character_name_color=(
                255,
                255,
                255,
            ),  # Pure white is very visible against wood
            on_advance=self.button_click_1,
        )

    def create_choice_banner(
        self, choice: str, index: int, y_offset: float
    ) -> ChoiceBanner:
        """
        Create a choice banner with the given parameters.
        """

        return ChoiceBanner(
            surface=self.surface,
            banner_image=self.assets.images.ui.banner_choice_wood(),
            text_content=f"{index+1}. {choice}",
            font=self.assets.fonts.monogram_extended(40),
            y_offset=y_offset,
            text_color=(42, 0, 30),
        )

    def get_character_sprite(self, char_name: str | None) -> pygame.Surface | None:
        """
        Get character sprite based on character name.
        """

        match char_name:
            case "Aie":
                if self.animation_state == "standing":
                    return self.assets.images.characters.boy_1_standing()
                elif self.walking_frame == 0:
                    return (
                        self.assets.images.characters.boy_1_walking_front_right_first()
                    )
                else:
                    return (
                        self.assets.images.characters.boy_1_walking_front_left_first()
                    )
            case "Haruto":
                if self.animation_state == "standing":
                    return self.assets.images.characters.boy_2_standing()
                elif self.walking_frame == 0:
                    return (
                        self.assets.images.characters.boy_2_walking_front_right_first()
                    )
                else:
                    return (
                        self.assets.images.characters.boy_2_walking_front_left_first()
                    )
            case "Ryu":
                if "standing" in self.animation_state:
                    if self.animation_state == "standing_left":
                        return self.assets.images.characters.boy_3_standing_left()
                    elif self.animation_state == "standing_right":
                        return self.assets.images.characters.boy_3_standing_right()
                    else:
                        return self.assets.images.characters.boy_3_standing()
                elif "walking" in self.animation_state:
                    if self.animation_state == "walking_left":
                        return (
                            self.assets.images.characters.boy_3_walking_left_right_first()
                            if self.walking_frame == 0
                            else self.assets.images.characters.boy_3_walking_left_left_first()
                        )
                    elif self.animation_state == "walking_right":
                        return (
                            self.assets.images.characters.boy_3_walking_right_right_first()
                            if self.walking_frame == 0
                            else self.assets.images.characters.boy_3_walking_right_left_first()
                        )
                    else:
                        return (
                            self.assets.images.characters.boy_3_walking_front_right_first()
                            if self.walking_frame == 0
                            else self.assets.images.characters.boy_3_walking_front_left_first()
                        )
            case "Kaori":
                if "standing" in self.animation_state:
                    if self.animation_state == "standing_left":
                        return self.assets.images.characters.girl_1_standing_left()
                    elif self.animation_state == "standing_right":
                        return self.assets.images.characters.girl_1_standing_right()
                    else:
                        return self.assets.images.characters.girl_1_standing()
                elif "walking" in self.animation_state:
                    if self.animation_state == "walking_left":
                        return (
                            self.assets.images.characters.girl_1_walking_left_right_first()
                            if self.walking_frame == 0
                            else self.assets.images.characters.girl_1_walking_left_left_first()
                        )
                    elif self.animation_state == "walking_right":
                        return (
                            self.assets.images.characters.girl_1_walking_right_right_first()
                            if self.walking_frame == 0
                            else self.assets.images.characters.girl_1_walking_right_left_first()
                        )
                    else:
                        return (
                            self.assets.images.characters.girl_1_walking_front_right_first()
                            if self.walking_frame == 0
                            else self.assets.images.characters.girl_1_walking_front_left_first()
                        )
            case "Airi":
                if self.animation_state == "standing":
                    return self.assets.images.characters.girl_2_standing()
                elif self.walking_frame == 0:
                    return (
                        self.assets.images.characters.girl_2_walking_front_right_first()
                    )
                else:
                    return (
                        self.assets.images.characters.girl_2_walking_front_left_first()
                    )
            case "Kanae":
                if self.animation_state == "standing":
                    return self.assets.images.characters.girl_3_standing()
                elif self.walking_frame == 0:
                    return (
                        self.assets.images.characters.girl_3_walking_front_right_first()
                    )
                else:
                    return (
                        self.assets.images.characters.girl_3_walking_front_left_first()
                    )
            case _:
                return None

    def update_choices(self) -> None:
        """
        Update available choice banners.
        """

        self.choice_banners.clear()

        if self.should_show_next_page():
            return

        choices = self.story.get_current_choices()
        for i, choice in enumerate(choices):  # type: ignore
            y_offset = 0.55 + (i * 0.08)
            banner = self.create_choice_banner(choice, i, y_offset)
            self.choice_banners.append((banner, i))

    def should_show_next_page(self) -> bool:
        """
        Check if there are more pages of dialogue to show.
        """

        if not self.dialogue_banner:
            return False

        next_page_start = (self.dialogue_banner.current_page + 1) * (
            self.dialogue_banner.max_lines - 1
            if self.dialogue_banner.character_name
            else self.dialogue_banner.max_lines
        )
        return next_page_start < len(self.dialogue_banner.full_text_lines)

    def handle_choice_selection(self, choice_idx: int) -> None:
        """
        Handle selection of a choice option.
        """

        self.story.choose_choice_index(choice_idx)
        if not self.story.can_continue():
            return

        next_text = self.get_next_dialogue()
        if not next_text:
            return

        char_name, dialogue_text = self.parse_dialogue(next_text)
        if self.dialogue_banner:
            self.dialogue_banner.update_text(dialogue_text, char_name)
        self.update_character_sprite(char_name)
        self.update_choices()

    def handle_dialogue_advance(self) -> None:
        """
        Handle advancing to next dialogue line.
        """

        if self.story.can_continue():
            next_text = self.get_next_dialogue()
            if next_text and self.dialogue_banner:
                char_name, dialogue_text = self.parse_dialogue(next_text)
                self.dialogue_banner.update_text(dialogue_text, char_name)
                self.update_character_sprite(char_name)
            self.update_choices()

    def update_character_sprite(self, char_name: str | None) -> None:
        """
        Update the character sprite based on who is speaking.
        """

        sprite = self.get_character_sprite(char_name)
        if sprite:
            self.character_sprite = pygame.transform.scale(sprite, (200, 270))
        else:
            self.character_sprite = None

    def update_character_animation(self) -> None:
        """
        Update character animation frames.
        """

        if self.dialogue_banner and self.dialogue_banner.character_name:
            current_time = pygame.time.get_ticks()

            # Generic animation sequence for all characters
            if current_time - self.state_timer > (
                1000 if "standing" in self.animation_state else 3000
            ):
                self.sequence_index = (self.sequence_index + 1) % len(
                    self.animation_sequence
                )
                self.animation_state = self.animation_sequence[self.sequence_index]
                self.state_timer = current_time
                self.walking_frame = 0
                self.walking_timer = current_time
                self.update_character_sprite(self.dialogue_banner.character_name)

            elif "walking" in self.animation_state:
                if current_time - self.walking_timer > 500:  # Animation frame timing
                    self.walking_frame = 1 - self.walking_frame
                    self.walking_timer = current_time
                    self.update_character_sprite(self.dialogue_banner.character_name)

    def setup_initial_dialogue(self) -> None:
        """
        Set up initial dialogue and character sprite.
        """

        initial_text = self.get_next_dialogue()
        char_name, dialogue_text = self.parse_dialogue(initial_text)
        self.dialogue_banner = self.create_dialogue_banner(dialogue_text, char_name)
        self.update_character_sprite(char_name)
