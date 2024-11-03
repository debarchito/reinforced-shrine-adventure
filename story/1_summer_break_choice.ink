=== 1_summer_break_choice ===
The final bell of the semester rings, signaling the start of summer break.

As your classmates burst into excited chatter, you, {player_name}, quietly pack your bag, ready to slip away unnoticed.

@Kaori: GUUUUYYYYYS! YOU WON'T BELIEVE WHAT I FOUND! IT'S THE PERFECT OF THE PERFECT-EST (?) PLACE!

Kaori bursts into the classroom like a whirlwind, her eyes practically sparkling like stars, and a crumpled newspaper clutched victoriously in her hand.

* [Look up curiously] 
    ~ curiosity += 1
    ~ social += 1
    You raise your head, wondering what chaos Kaori's bringing this time.
* [Pretend not to hear] 
    ~ caution += 1
    You keep your head down, but your ears perk up anyway - it's impossible not to hear Kaori.

- Kaori's gaze sweeps the room like a searchlight, landing on you and your usual squad: Airi (the worrier), Kanae (the voice of reason), Ryu (the adventurer), and Haruto (the peacekeeper).

@Kaori: Why don't we visit this SUPER AWESOME shrine for a test of courage? There might even be hidden treasure!

@Airi: A shrine... a treasure... what? Slow down!

@Haruto: Kaori, remember breathing? That thing humans need to do?

@Kaori: Pffft, breathing is overrated when you've got NEWS THIS BIG!

@Kaori: Ya'll know that spooky abandoned amusement park by the ocean in Ukiyo? Well, there's this HUGE beach on the northern side.

@Kaori: It's like, BOOM - mountains! SPLASH - ocean! And right there, this amazing old shrine just sitting at the top of this hill! And get this - it's TOTALLY haunted!

* [Share the enthusiasm] 
    ~ curiosity += 1
    ~ supernatural += 2
    You lean forward, completely hooked.
    @{player_name}: Haunted how? Tell me everything!
* [Raise an eyebrow] 
    ~ supernatural -= 1
    You give your best skeptical look.
    @{player_name}: Haunted? Really, Kaori?

- @Kaori: The stairs to the shrine? They start RIGHT AT THE BEACH! It's like something straight outta those magical girl animes!

@Kanae: Inside voice, Kaori. INSIDE. VOICE.

* [Join Kanae's side] 
    ~ caution += 1
    ~ social -= 1
    You mime covering your ears.
    @{player_name}: My eardrums agree with Kanae.
* [Defend Kaori's excitement]
    ~ social += 2
    You lean into the energy.
    @{player_name}: Let her be excited! This actually sounds super cool!

- @Kaori: ANYWAY! Here's the best part!

@Kaori: Back in ye olden days, this wasn't just any shrine - it was THE shrine! They had this super special miko who'd do this crazy ritual called "Kagura Yume" - but only once every hundred years!

@Kaori: Legend says the chosen miko could literally WALK ON WATER! Like, not just a little hop-skip - full-on water-walking!

@Kaori: And get this - the water would GLOW wherever she stepped! People came from EVERYWHERE to see it! How cool is that?!

* [Question safety] 
    ~ curiosity += 1
    ~ caution += 2
    @{player_name}: But isn't it, like, super off-limits?
    @Kaori: That's what makes it EXTRA exciting, Aie!
* [Shrink away] 
    ~ caution += 1
    ~ social -= 1
    You try to become one with your chair, hoping to avoid the incoming chaos.
    
- @Kaori: SO! Test of courage time! Who's in?!

@Ryu: Count me in! Better than sitting at home playing games all break!

@Haruto: Sounds like an adventure! Kanae?

@Kanae: *sigh* Someone needs to keep you all from doing anything TOO stupid...

@Airi: I-I mean... if everyone's going... I might as well join.

All eyes turn to you like spotlights.

@Kaori: C'mon Aie! It'll be the BEST THING EVER! Pretty please?

* [Give in with enthusiasm]
    ~ social += 2
    ~ curiosity += 1
    @{player_name}: You know what? Let's do this!
    @Kaori: YAAAAAAAY!
    -> group_planning
* [Express doubts]
    ~ caution += 2
    @{player_name}: I dunno... sounds kinda sketchy...
    @Haruto: Hey, we'll all be there together!
    -> convince_player

=== convince_player ===
@Airi: Look, I'm scared of my own shadow sometimes, but even I'm going!

@Ryu: Think of the STORIES we'll have! We'll be LEGENDS!

* [Join the fun]
    ~ social += 2
    ~ curiosity += 1
    @{player_name}: When you put it that way... okay!
    @Kaori: THIS IS GONNA BE EPIC!
    -> group_planning
* [Stay hesitant]
    ~ caution += 1
    @{player_name}: I still don't know...
    @Kaori: Wait wait! I have an idea!
    -> talisman_option

=== talisman_option ===
@Kaori: What if we bring lucky talismans? My grandma has these SUPER POWERFUL ones!

* [Accept talisman]
    ~ has_talisman = true
    ~ supernatural += 2
    ~ social += 1
    @{player_name}: Well... if they're SUPER powerful...
    @Kaori: They're the MOST powerful! Promise!
    -> group_planning
* [Decline offer]
    ~ supernatural -= 1
    @{player_name}: A piece of paper won't help if the floor collapses...
    @Kaori: Aww, please? We really want you there!
    -> final_decision

=== final_decision ===
The group looks at you expectantly. This is your last chance to decide.

* [Join the group] 
    ~ social += 2
    ~ curiosity += 1
    @{player_name}: Okay, I'll come. But promise we'll be careful?
    @Kaori: Of course! We'll stick together and watch out for each other.
    Everyone nods enthusiastically.
    -> group_planning
* [Refuse to go]
    ~ caution += 2
    ~ social -= 2
    @{player_name}: I'm sorry, but I really can't. Have fun without me.
    @Airi: We'll miss you, Aie.
    The group looks disappointed, but they respect your decision.
    -> solo_ending

=== group_planning ===
@Kaori: Alright! Let's meet at the entrance of the park tomorrow at dusk. Don't forget to bring your flashlights!

As your friends chatter excitedly about tomorrow's adventure, you feel a mix of anticipation and anxiety. What awaits you at the shrine?

@Ryu: Hey, Aie, you okay? You look a bit pale.

* [Admit your nervousness]
    ~ social += 1
    ~ caution += 1
    @{player_name}: Just a little nervous, I guess. This is pretty out of my comfort zone.
    @Airi: Don't worry, we'll all look out for each other. Right, everyone?
    The group nods reassuringly.
* [Put on a brave face]
    ~ social += 1
    @{player_name}: I'm fine. Just thinking about what to pack.
    - @Haruto: That's the spirit! Maybe bring some snacks to share?
    * [Agree to pack snacks]
        ~ has_snacks = true
        ~ social += 2
        You decide to pack some instant ramen and hot water before you leave tomorrow.
    * [Politely decline]
        ~ caution += 1
        ~ social -= 1
        @{player_name}: I don't think we need snacks as we won't be there for long?
        You decide to skip on packing snacks.

- @Kanae: Should we bring anything else? First aid kit maybe?

@Kaori: Good thinking, Kanae! Aie, since you're good at planning, why don't you make a list of things we should bring?

* [Accept the responsibility]
    ~ caution += 2
    ~ social += 1
    ~ has_first_aid_kit = true
    @{player_name}: Sure, I can do that. Better to be prepared, I suppose.
    You start listing down items.
* [Deflect the task]
    ~ social -= 1
    @{player_name}: Uh, maybe someone else should do it? I'm not sure what we'd need.
    @Airi: No problem, I can handle it. But feel free to add any ideas, Aie!

- As the group continues to plan, you can't help but wonder if you've made the right decision. But seeing your friends' excitement, a small part of you starts to look forward to the adventure.

@Kaori: This is going to be the best summer break ever! See you all tomorrow!

The group disperses, leaving you with your thoughts about the upcoming test of courage.

// Group ending leads to packing
$jump
-> 2_packing

=== solo_ending ===
You head home alone, feeling a mix of relief and regret. As you settle in for a quiet evening, your phone buzzes with messages from your friends.

@Kaori: We'll miss you tomorrow, Aie! But we understand. Maybe next time?
@Airi: Take care, Aie. We'll tell you all about it when we get back.
@Ryu: Your loss, buddy! But hey, if you change your mind, you know where to find us!

* [Reply with encouragement] 
    ~ social += 1
    @{player_name}: Have fun, guys. Be safe out there.
    {caution >= 3: You add some safety reminders about bringing first aid kits and checking the weather.}
    -> DONE
* [Don't reply]
    ~ social -= 2
    You set your phone aside, trying to ignore the pang of regret.

{
    - supernatural <= -2:
        As night falls, you feel confident in your decision. 
        Ghost stories are just stories, and abandoned buildings are genuinely dangerous. Better to be smart than sorry.
    - supernatural >= 2:
        You can't help but wonder if you're missing out on something extraordinary.
        What if the legends about the shrine are true? Still, some mysteries might be better left unexplored.
    - else:
        The stories about the shrine nag at your mind - whether true or not, they hold an undeniable allure.
}

{social >= 3:
    The thought of your friends experiencing this adventure without you leaves an empty feeling in your chest.
    Maybe next time you'll be braver.
}

{caution >= 3:
    You remind yourself that safety comes first.
    Abandoned buildings are dangerous, regardless of any supernatural elements.
}

{curiosity >= 3:
    You wonder if you've made the right choice. Part of you wishes you were braver, while another part is glad to be safe at home.
    Your mind keeps wandering back to the mysteries of the shrine. What secrets might it hold? What stories could be waiting to be discovered?
}

-> END
