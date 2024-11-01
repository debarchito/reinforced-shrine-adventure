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

{caution >= 2:
    Your supplies are arranged with tactical consideration: flashlight with backup batteries, a detailed map of the area marked with potential hazards{has_first_aid_kit:, comprehensive first-aid supplies}.
    Each item has been chosen based on careful risk assessment and practical necessity.
}

{curiosity >= 2:
    Your research materials spread across your desk tell their own story - printouts of historical photographs, notes about local legends, and carefully marked topographical maps.
    You've even found old maintenance records from the shrine's active years, offering potential insights into its layout.
}

* [Pack light]
    ~ caution -= 1
    After careful consideration, you opt for minimalist efficiency: a reliable flashlight, your fully-charged phone, and a small water bottle.
    Sometimes, you reason, mobility and simplicity are their own forms of preparation.
* [Pack extensively]
    ~ caution += 1
    Your backpack gradually fills with carefully considered items: flashlight with spare batteries{has_first_aid_kit:, comprehensive first-aid kit}, backup power bank, water supplies, weather-appropriate gear.
    Each addition represents a calculated response to potential scenarios.

- {has_snacks:
    The thermal flask and selection of snacks are packed strategically at the top for easy access.
    You remember to include enough to share - food has a way of bringing people together in uncertain situations.
}

{has_talisman:
    The talisman receives special consideration. You wrap it carefully in traditional cloth before placing it in a secure pocket.
    Its presence provides a curious comfort - a bridge between rational preparation and spiritual protection.
}

As darkness settles, you perform one final inventory check, mentally walking through various scenarios.

{
- supernatural >= 2:
    The evening shadows seem to hold new meaning now, dancing at the edge of your vision like playful spirits.
    You catch yourself wondering if the shrine's ancient guardians are aware of tomorrow's visitors, and what welcome they might prepare.
- supernatural <= -2:
    You ground yourself in facts and probabilities, reviewing structural safety concerns and weather forecasts.
    Ghost stories may be fiction, but abandoned structures pose real challenges that demand respect and preparation.
- else:
    The night brings a mix of practical concerns and imaginative wonderings about what tomorrow might hold.
    Whether the shrine's mysteries are natural or supernatural, they deserve careful consideration.
}

Sleep proves elusive as your mind traces the path you'll take tomorrow - from the weathered steps at the shore's edge to the mysterious heights of the ancient shrine.

$jump
-> 3_walk_to_gate
