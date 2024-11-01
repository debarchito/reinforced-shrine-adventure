=== 3_walk_to_gate ===
The next evening arrives with an ethereal glow, the setting sun painting the sky in shades of amber and rose.

{social >= 2:
    You arrive at the park entrance to find your friends already gathered, their excitement palpable in the twilight air.
    @Kaori: THERE YOU ARE! We were starting to worry!
    @Airi: We just got here too, don't listen to her.
- else:
    You arrive at the park entrance right on time. The others trickle in gradually, their usual energy somewhat subdued by the approaching darkness.
}

{caution >= 2:
    You double-check your supplies one last time, ensuring everything is secure and accessible.
    @Kanae: Always the prepared one, aren't you?
    {has_first_aid_kit: The weight of the first-aid kit provides a reassuring presence against your back.}
}

The abandoned amusement park looms before you, its rusted gates standing sentinel against the darkening sky. Beyond them, barely visible, the mountain's silhouette rises against the horizon.

@Ryu: So... we're really doing this?

* [Take the lead]
    ~ social += 1
    ~ curiosity += 1
    @{player_name}: No point standing here. Let's go.
    You step forward, pushing gently against the old gate.
* [Hang back]
    ~ caution += 1
    @{player_name}: Maybe we should review the plan one more time?
    @Kaori: The plan is simple - we follow the path to the beach, then take the shrine stairs up!

- The gate creaks open with a sound that seems to echo through the empty park. Your flashlight beams cut through the growing darkness, creating dancing shadows among the abandoned attractions.

{
    - supernatural >= 2:
        The air feels different here - heavier somehow, charged with an energy that makes the hair on your arms stand up.
        {has_talisman: You touch the talisman in your pocket, drawing comfort from its presence.}
    - supernatural <= -2:
        You focus on practical concerns - watching for loose ground, rusty metal, anything that could pose a real danger.
        The "spooky" atmosphere is just your mind playing tricks in the low light.
    - else:
        The air feels different here - heavier somehow, charged with an energy that makes the hair on your arms stand up.
        {has_talisman: You touch the talisman in your pocket, drawing comfort from its presence.}
}

@Haruto: The beach access should be this way, past the old carousel.

{has_snacks:
    @{player_name}: Anyone want a snack before we head down?
    @Airi: Maybe later? I'm too nervous to eat right now.
    @Ryu: Save them for when we reach the shrine!
}

As you make your way through the park, the sound of waves grows steadily louder, a rhythmic pulse that seems to match your heartbeat.

{curiosity >= 2:
    Your research comes flooding back as you pass each landmark. The carousel, installed in 1952, was once the pride of the park. The rusted tracks of the mountain coaster snake up into the darkness, their path to the shrine now overgrown.
    @{player_name}: Did you know this place used to attract thousands of visitors every summer?
    @Kanae: Really? It's hard to imagine now...
}

* [Focus on the path ahead]
    ~ caution += 1
    You keep your attention on the ground, watching for hazards in the beam of your flashlight.
    The beach stairs should be just ahead, beyond the old gift shop.
* [Take in the atmosphere]
    ~ supernatural += 1
    The abandoned park holds a strange beauty in the twilight. Moonlight glints off broken windows and rusted metal, creating an otherworldly scene.
    You can almost imagine echoes of past laughter carried on the sea breeze.

- The group falls quiet as you approach the beach access point. Ancient wooden stairs, weathered by decades of salt air, descend into darkness.

@Airi: Those steps don't look very stable...

{caution >= 3:
    @{player_name}: We should test each step before putting our full weight on it. And stay close to the railing.
    The others nod, appreciating your practical approach.
}

The shrine's presence feels stronger now, though it remains hidden in the darkness above. Only the first few stairs are visible in your flashlight beams, the rest disappearing into the night like a path into another world.

-> DONE
