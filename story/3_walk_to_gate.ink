=== 3_walk_to_gate ===
The next evening arrives with an ethereal glow, the setting sun painting the sky in shades of amber and rose.
Dark clouds gather on the horizon, barely noticeable in the twilight.

{social >= 4:
    You arrive at the park entrance to find your friends already gathered, their excitement palpable in the twilight air.
    @Kaori: THERE YOU ARE! We were starting to worry!
    @Airi: We just got here too, don't listen to her.
- else:
    You arrive at the park entrance right on time. The others trickle in gradually, their usual energy somewhat subdued by the approaching darkness.
}

{caution >= 7:
    You double-check your supplies one last time, ensuring everything is secure and accessible.
    @Kanae: Always the prepared one, aren't you?
    {has_first_aid_kit: The weight of the first-aid kit provides a reassuring presence against your back. You'll be grateful for this foresight later.}
}

The abandoned amusement park looms before you, its rusted gates standing sentinel against the darkening sky.
Beyond them, barely visible, the mountain's silhouette rises against the horizon.

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

- The gate creaks open with a sound that seems to echo through the empty park.
Your flashlight beams cut through the growing darkness, creating dancing shadows among the abandoned attractions.

{
    - supernatural >= 2:
        The air feels different here - heavier somehow, charged with an energy that makes the hair on your arms stand up. The ocean breeze carries an unusual chill.
        {has_talisman: You touch the talisman in your pocket, drawing comfort from its presence.}
    - else:
        You focus on practical concerns - watching for loose ground, rusty metal, anything that could pose a real danger.
        The "spooky" atmosphere is just your mind playing tricks in the low light.
}

@Haruto: The beach access should be this way, past the old carousel.

* [Suggest taking the mountain coaster path]
    ~ curiosity += 2
    @{player_name}: What about following the mountain coaster track? It might be a more direct route to the shrine.
    @Kanae: Through the maintenance paths? That's... actually not a bad idea.
    @Ryu: It's probably overgrown though... and less safe.
    @Airi: I vote we stick to the plan. The beach route is longer but we know it's passable.
    
    ** [Insist on the mountain path]
        ~ curiosity += 1
        @{player_name}: Think about it - the maintenance paths were designed for quick access. They have to be more direct.
        @Kanae: Plus, the workers would have needed them to be reliable.
        @Haruto: The paths might be better maintained too - they were built to last.
        @Ryu: I don't know... what if we run into locked gates or something?
        @{player_name}: The locks are probably rusted through by now.
        @Airi: Or we could get completely lost up there...
        @Kanae: We have our phones for light. And maps.

        *** [Appeal to their sense of adventure]
            @{player_name}: Where's your sense of adventure? This could be our chance to see parts of the park no one has in years!
            @Ryu: You know what? I'm in. Could be interesting.
            @Airi: *sighs* Fine, but if we get stuck, I'm blaming you both.
            @{player_name}: We could always turn back if it gets too difficult.
            
            **** [Take the mountain path]
                ~ took_beach_path = false
                @Ryu: Let's do this!
                @Airi: Just... be careful, okay?
                
            **** [Play it safe]
                ~ took_beach_path = true
                ~ caution += 1
                @{player_name}: On second thought, maybe we should stick to the beach route.
                @Airi: *relieved sigh* Thank you.
                @Ryu: Probably for the best.

        *** [Express concern about safety]
            ~ caution += 2
            @{player_name}: Actually... those maintenance paths haven't been used in years. Who knows what condition they're in?
            @Airi: That's exactly what I was thinking! And in the dark...
            @Ryu: Yeah, when you put it that way...
            @Kanae: The beach route is longer, but at least we know what we're getting into.
            ~ took_beach_path = true
            @{player_name}: Let's stick to the original plan. Better safe than sorry.
            @Airi: *nodding vigorously* Definitely the right call.
            
    ** [Back down gracefully]
        ~ caution += 1
        @{player_name}: You're right, better safe than sorry. Beach route it is.
        ~ took_beach_path = true
* [Follow the original beach route]
    ~ caution += 1
    ~ took_beach_path = true
    @{player_name}: Let's stick to the beach path. We know it's safer.
    The others nod in agreement.

- {has_snacks:
    @{player_name}: Anyone want a snack before we head down?
    @Airi: Maybe later? I'm too nervous to eat right now.
    @Ryu: Save them for when we reach the shrine!
}

As you make your way through the park, the night air grows thick with anticipation.
The distant sound of waves seems unusually loud tonight.

{took_beach_path:
    @Ryu: Hey Aie, didn't you mention something about caves during your research?
    
    @{player_name}: Actually...yes! I found some old maps while researching. There used to be a hidden prayer spot carved into the cliffs.
    
    @Kanae: A hidden shrine within the cliffs? That's amazing!
    
    @{player_name}: The monks would use it during low tide. They'd walk through a narrow path to perform meditation rituals.
    
    @Airi: I've lived here my whole life and never heard about this...

    @{player_name}: The beach path was actually considered sacred. Only monks and shrine maidens were allowed to use it for special ceremonies.
    
    @Ryu: Really? What made it so special?
    
    @{player_name}: There's a natural cave formation that aligns perfectly with the moon during certain times of the year. The monks believed it had spiritual significance.
    
    @Kanae: That's fascinating! I wonder if we'll be able to see it.
    
    @{player_name}: Maybe. The cave entrance should still be there, even if no one's used it in decades.
    
    @Airi: How long has it been abandoned?
    
    @{player_name}: Around 1987, I think?. That's when they closed the shrine and stopped all ceremonies.
    
    @Kaori: Anyway, hungry...? Maybe we should take a break soon.
    
    @Ryu: I'm more excited than hungry! Can't believe we're actually doing this.
    
    @{player_name}: Look at all these cool rock formations. The monks really picked an amazing spot.
    
    @Airi: *giggling* The waves sound like they're whispering secrets...
    
    The group walks along the beach path, their excited chatter mixing with the gentle sound of waves in the distance.

    @Ryu: Hey guys... isn't the water a bit too close?

    $jump beach_path
    -> 4_1_beach_path
}

{not took_beach_path:
    @Ryu: Hey Aie, how did you know about this path anyway?
    
    @{player_name}: I actually did some research before coming. This used to be a maintenance route that at some point was also open to the public.
    
    @Kanae: Really? Didn't know.
    
    @{player_name}: Well, back when the shrine was active, workers would use this path daily. They'd carry supplies, perform repairs, even help elderly visitors sometimes.
    
    @Airi: I can't imagine anyone working here now... it's so creepy.
    
    @{player_name}: It wasn't always like this. The shrine used to be really popular - there were festivals, ceremonies, all sorts of events.
    
    @Ryu: What happened to make everyone stop coming?
    
    @{player_name}: That's the interesting part. Nobody really knows. The records just... stopped around 1987.
    
    @Kanae: Just stop? Nothing about why?
    
    @{player_name}: Nothing official. Though I found some old newspaper clippings about strange incidents...
    
    @Airi: What kind of incidents? *nervous laugh*
    
    @{player_name}: Well...
    
    @Kaori: Maybe we should save the ghost stories for when we actually reach the shrine?
    
    @Ryu: Kaori's right. We should focus on getting there first.
    
    @{player_name}: Fair enough. But remind me to tell you about the missing maintenance worker later.
    
    @Airi: Aie! Stop teasing!
    
    Everyone laughs, but there's a nervous edge to it. The path ahead seems to grow darker.
    
    @Haruto: Well, no turning back now...

    $jump mountain_path
    -> 4_2_mountain_path
}
