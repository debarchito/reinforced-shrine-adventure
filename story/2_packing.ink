=== 2_packing ===
{
    - supernatural <= -2:
        You spend a large portion of the evening researching the shrine's history online, focusing on old newspaper articles and academic papers about its cultural significance.
        While skeptical of supernatural claims, you're intrigued by the documented architectural details and historical ceremonies.
        The logical part of your mind suggests there must be rational explanations behind the legends - perhaps clever engineering or natural phenomena.
    - supernatural >= 2:
        As night approaches, you find yourself drawn into research about ancient Shinto practices and sacred sites.
        The stories about the "Kagura Yume" ritual and its connection to the shrine fill you with a mix of excitement and reverence.
        Each account of supernatural encounters sends a peculiar thrill through you - equal parts fear and fascination.
    - else:
        You spend the evening doing general research about the shrine, trying to separate fact from fiction.
        While the supernatural stories are intriguing, you're more interested in understanding its historical significance.
}

{curiosity >= 2:
    The shrine's mysteries consume your thoughts. You sketch rough maps based on old photographs, marking points of interest.
    Every article leads to new questions, and you carefully note them all down, hoping to find answers tomorrow.
}

In your research, you discover there are two possible routes to the shrine - the longer beach path that follows the coastline, or an old maintenance path that winds up through the mountain.

The mountain route seems more direct but potentially treacherous, while the beach path is well-documented but takes considerably longer.

{social >= 2:
    Your phone lights up constantly with messages from the group chat.
    @Kaori: Don't forget your flashlights everyone! 
    @Ryu: Already packed mine! Anyone bringing extra batteries?
    @Airi: I've got spares! We can share!
    Their enthusiasm is contagious, making even the daunting aspects of tomorrow feel more like an exciting shared adventure.
}

{caution >= 2:
    You approach your preparation with methodical precision, creating detailed checklists and contingency plans.
    {has_talisman: The talisman rests carefully wrapped on your desk - a spiritual safeguard, regardless of your beliefs.}
    Your research into the area's terrain and weather patterns helps you pack appropriately.
}

{has_snacks: The carefully chosen snacks and thermal supplies are arranged nearby - you've read enough adventure stories to know that shared food can lift spirits in tense moments.}

The evening light filters through your window, casting amber shadows across your preparation space. Each item you consider carries its own weight of possibility and purpose.

It's the time to pack. Will you go according to plan, or will you pack light?

* [Pack a flashlight?]
    ~ has_flashlight = true
    You add a flashlight to your bag. Essential for exploring in the dark.
    -> continue_packing

* [Skip the flashlight]
    You decide against bringing a flashlight. Your phone light should be enough... right?
    -> continue_packing

=== continue_packing ===
* [Pack water?]
    ~ has_water = true 
    You add a water bottle. Staying hydrated is important.
    -> first_aid_choice
    
* [Skip water]
    You decide not to bring water. There might be vending machines nearby.
    -> first_aid_choice

=== first_aid_choice ===
* [Pack a first aid kit?]
    ~ has_first_aid_kit = true
    Better safe than sorry. You add the small medical kit.
    -> snacks_choice
    
* [Skip first aid]
    You leave the first aid kit. What could possibly go wrong?
    -> snacks_choice

=== snacks_choice ===
* [Pack some snacks?]
    ~ has_snacks = true
    You pack some sharing-friendly snacks. Food always brings people together.
    -> final_check
    
* [Skip snacks]
    Your stomach might regret this later, but you decide to travel light.
    -> final_check

=== final_check ===
{has_talisman:
    The talisman finds its place in a secure pocket, carefully wrapped in cloth. Its presence offers a strange comfort.
}

As you drift off to sleep, you're sure you've checked everything — but did you miss something? 

Sleep proves elusive as your mind traces the path ahead - from the weathered steps at the shore's edge to the mysterious heights of the ancient shrine.

Any lingering questions might have answers tomorrow.

$jump
-> 3_walk_to_gate
