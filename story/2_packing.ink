=== 2_packing ===
{
    - supernatural >= 2:
        As night approaches, you find yourself drawn into research about ancient Shinto practices and sacred sites.
        The stories about the "Kagura Yume" ritual and its connection to the shrine fill you with a mix of excitement and reverence.
        Each account of supernatural encounters sends a peculiar thrill through you - equal parts fear and fascination.
    - else:
        You spend a large portion of the evening researching the shrine's history online, focusing on old newspaper articles and academic papers about its cultural significance.
        While skeptical of supernatural claims, you're intrigued by the documented architectural details and historical ceremonies.
        The logical part of your mind suggests there must be rational explanations behind the legends - perhaps clever engineering or natural phenomena.
}

{curiosity >= 3:
    The shrine's mysteries consume your thoughts. You sketch rough maps based on old photographs, marking points of interest.
    Every article leads to new questions, and you carefully note them all down, hoping to find answers tomorrow.
}

In your research, you discover there are two possible routes to the shrine - the longer beach path that follows the coastline, or an old maintenance path that winds up through the mountain.

The mountain route seems more direct but potentially treacherous, while the beach path is well-documented but takes considerably longer.

{social >= 4:
    Your phone lights up constantly with messages from the group chat.
    @Kaori: Don't forget your flashlights everyone! 
    @Ryu: Already packed mine! Anyone bringing extra batteries?
    @Airi: I've got spares! We can share!
    Their enthusiasm is contagious, making even the daunting aspects of tomorrow feel more like an exciting shared adventure.
}

{caution >= 7:
    You approach your preparation with methodical precision, creating detailed checklists and contingency plans.
    {has_talisman: The talisman sits on your desk, wrapped in a delicate cloth - a spiritual safeguard that brings comfort, even to skeptical minds.}
    In your excitement about the historical aspects.
}

The evening light filters through your window, casting amber shadows across your preparation space.
Each item you consider carries its own weight of possibility and purpose.

It's the time to pack. Will you go according to plan, or will you pack light?

* [Pack a flashlight?]
    ~ has_flashlight = true
    You add a flashlight to your bag. Essential for exploring in the dark.
    -> continue_packing

* [Skip]
    You decide against bringing a flashlight. Your phone light should be enough... right?
    -> continue_packing

=== continue_packing ===
* [Pack water?]
    ~ has_water = true 
    You add two water bottles. Staying hydrated is important.
    -> first_aid_choice
    
* [Skip]
    You decide not to bring water. There might be vending machines nearby.
    -> first_aid_choice

=== first_aid_choice ===
* [Pack a first aid kit?]
    ~ has_first_aid_kit = true
    Better safe than sorry. You add the first-aid kit.
    -> snacks_choice
    
* [Skip]
    You leave the first aid kit. What could possibly go wrong?
    -> snacks_choice

=== snacks_choice ===
* [Pack snacks?]
    ~ has_snacks = true
    You pack the planned snacks. Food always brings people together.
    -> final_check
    
* [Skip]
    Your stomach might regret this later, but you decide to travel light.
    -> final_check

=== final_check ===
{has_talisman: The talisman finds its place in a secure pocket.}

As you drift off to sleep, you're sure you've checked everything — though a nagging feeling suggests you might have overlooked something important.

Sleep proves elusive as your mind traces the path ahead - from the weathered steps at the shore's edge to the mysterious heights of the ancient shrine.

Any lingering questions might have answers tomorrow.

$jump walk_to_gate
-> 3_walk_to_gate
