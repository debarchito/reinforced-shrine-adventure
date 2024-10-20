=== 1_summer_break_choice ===
The final bell of the semester rings, signaling the start of summer break. As your classmates burst into excited chatter, you, {player_name}, quietly pack your bag, ready to slip away unnoticed.

GUUUUYYYYYS! YOU WON'T BELIEVE WHAT I FOUND! IT'S THE PERFECT OF THE PERFECT-EST (?) PLACE! # @Kaori

Kaori bursts into the classroom, her eyes sparkling with excitement, and a newspaper clutched tightly in her hand.

* [Look up curiously] You raise your head, curiosity getting the better of your usual reserve.
    ~ courage += 1
* [Pretend not to hear] You keep your head down, hoping to avoid whatever scheme Kaori's cooked up this time.
    ~ courage -= 1

- Kaori's gaze sweeps the room, landing on you and your friends: Airi, Kanae, Ryu, and Haruto.

Why don't we visit this shrine for a test of courage? It's rumored that there's some treasure, hidden somewhere in this shrine! # @Kaori

A shrine...a treasure? Wha- can you take it slow? # @Airi

Breathe Kaori, breathe. # @Haruto

I'm breathing just fine... but that’s not why I’m here for! # @Kaori

Ya'll remember that abandoned amusement park by the ocean in Ukiyo, right? Well, there’s a huge beach on the northern side. # @Kaori

It’s this amazing spot where the mountains meet the ocean... and there’s an old, crumbling shrine at the top of a hill! The best part? It’s rumored to be haunted! # @Kaori

* [Show interest] You lean in, intrigued by Kaori's description.
    ~ courage += 1
    Tell me more. # @{player_name}
    Finally showing some interest, eh? Get this- # @Kaori
* [Remain skeptical] You raise an eyebrow, not entirely convinced.
    ~ courage -= 1
    An abandoned amusement park? Sounds dangerous... # @{player_name}
    That's the real fun! Get this- # @Kaori

- The stairs leading up to the shrine start right near the shore. You’re practically walking from the beach straight up to the shrine. It’s like something out of a storybook! # @Kaori

Dial down... jeez. Don't know where you get this energy from. # @Kanae

* [Agree with Kanae] You nod in agreement with Kanae's sentiment.
    ~ courage -= 1
    Yeah, Kaori, maybe take it down a notch? # @{player_name}
* [Defend Kaori's enthusiasm] You smile at Kaori's enthusiasm.
    ~ courage += 1
    Come on, Kanae. Let her finish. It sounds interesting! # @{player_name}

- Just listen! That's your only job here! # @Kaori

Back in the day, it was a major tourist attraction. A special miko, chosen by the elders, would perform the legendary "Kagura Yume" ritual, an event that occurred only once every hundred years. # @Kaori

It's said that the chosen miko, blessed by the spirits of the shrine, gains the ability to walk on water during the ritual. # @Kaori

As she gracefully steps across the surface, the water shimmers with a celestial glow, creating an enchanting spectacle that draws people from all over, eager to witness this miraculous event at least once in their lives. # @Kaori"

* [Speak up] Isn't that place off-limits? # @{player_name}
    ~ courage += 1
    That's what makes it exciting, Aie! # @Kaori
* [Stay silent] You shrink in your seat, hoping to avoid being dragged into this.
    ~ courage -= 1
    
- So here is the plan: Lets's hold a test of courage in that shrine! # @Kaori

A test of courage, huh? Interesting. Not like we have anything better to do in the break. # @Ryu

Yeah, this actually sounds like a lot of fun! What about you, Kanae? # @Haruto

Well... okay. But we should be careful, right? Airi, any input? # @Kanae

I mean, sounds ok but I am not that good with spooky places... you know. # @Airi

All eyes turn to you.

Come on, Aie! It'll be fun. What do you think? # @Kaori

* [Reluctantly agree] I... I guess I could come along. # @{player_name}
    ~ courage += 2
    Great! It's decided then! # @Kaori
    -> group_planning
* [Try to back out] I don't know... It sounds dangerous. # @{player_name}
    ~ courage -= 2
    Don't worry, we'll all be there together. Safety in numbers, right? # @Haruto
    -> convince_player

=== convince_player ===
See, I'm not very good with these things, but I'm still joining. # @Airi

Yeah, and think of the stories we'll have to tell when school starts again! # @Ryu

* [Give in] Alright, alright. I'll come. # @{player_name}
    ~ courage += 1
    LESS GO! This is going to be super awesome! # @Kaori
    -> group_planning
* [Stand firm] I really don't think it's a good idea. # @{player_name}
    What if we bring talismans for protection? Would that help? # @Kaori
    -> talisman_option

=== talisman_option ===
* [Accept the talisman] Well... if we have talismans, I guess it might be okay. # @{player_name}
    ~ has_talisman = true
    ~ courage += 1
    Perfect! I'll make sure we all have talismans. # @Kaori
    -> group_planning
* [Refuse] I don't think a talisman will make much difference. # @{player_name}
    I understand. But please, think about it? We really want you there. # @Kaori
    -> final_decision

=== final_decision ===
The group looks at you expectantly. This is your last chance to decide.

* [Join the group] Okay, I'll come. But promise we'll be careful? # @{player_name}
    ~ courage += 3
    Of course! We'll stick together and watch out for each other. # @Kaori
    Everyone nods enthusiastically.
    -> group_planning
* [Refuse to go] I'm sorry, but I really can't. Have fun without me. # @{player_name}
    ~ courage -= 3
    We'll miss you, Aie. # @Airi
    The group looks disappointed, but they respect your decision.
    -> solo_ending

=== group_planning ===
Alright! Let's meet at the entrance of the park tomorrow at dusk. Don't forget to bring your flashlights! # @Kaori

As your friends chatter excitedly about tomorrow's adventure, you feel a mix of anticipation and anxiety. What awaits you at the shrine?

Hey, Aie, you okay? You look a bit pale. # @Ryu

* [Admit your nervousness] Just a little nervous, I guess. This is pretty out of my comfort zone. # @{player_name}
    Don't worry, we'll all look out for each other. Right, everyone? # @Airi
    The group nods reassuringly.
    ~ courage += 1
* [Put on a brave face] I'm fine. Just thinking about what to pack. # @{player_name}
    - That's the spirit! Maybe bring some snacks to share? # @Haruto
    ~ courage += 2
    * [Agree to pack snacks] You decide to pack some instant ramen and hot water before you leave tomorrow.
        ~ took_snacks = true
        ~ courage += 2
    * [Politely decline] I don't think we need snacks as we won't be there for long? # @{player_name}
        You decide to skip on packing snacks.
        ~ courage -= 1

- Should we bring anything else? First aid kit maybe? # @Kanae

Good thinking, Kanae! Aie, since you're good at planning, why don't you make a list of things we should bring? # @Kaori

* [Accept the responsibility] Sure, I can do that. Better to be prepared, I suppose. # @{player_name}
    ~ courage += 2
    You start listing down items.
* [Deflect the task] Uh, maybe someone else should do it? I'm not sure what we'd need. # @{player_name}
    ~ courage -= 1
    No problem, I can handle it. But feel free to add any ideas, Aie! # @Airi

- As the group continues to plan, you can't help but wonder if you've made the right decision. But seeing your friends' excitement, a small part of you starts to look forward to the adventure.

This is going to be the best summer break ever! See you all tomorrow! # @Kaori

The group disperses, leaving you with your thoughts about the upcoming test of courage.

-> group_ending

=== group_ending ===
# Group Ending

{courage >= 7:
    Despite your initial reservations, you feel a spark of excitement about the adventure ahead. Maybe this test of courage is just what you need to come out of your shell. You head home, already thinking about what to pack for tomorrow.
- else:
    You head home, a knot of worry in your stomach. As night falls, you wonder about things that could go wrong... but it's too late to back out now. You'll just have to face whatever comes tomorrow.
}

->->

=== solo_ending ===
# Solo Ending

You head home alone, feeling a mix of relief and regret. As you settle in for a quiet evening, your phone buzzes with messages from your friends.

We'll miss you tomorrow, Aie! But we understand. Maybe next time? # @Kaori
Take care, Aie. We'll tell you all about it when we get back. # @Airi
Your loss, buddy! But hey, if you change your mind, you know where to find us! # @Ryu

* [Reply with encouragement] Have fun, guys. Be safe out there. # @{player_name}
    ~ courage += 1
* [Don't reply]
    You set your phone aside, trying to ignore the pang of regret.
    ~ courage -= 1

- As night falls, you wonder if you've made the right decision. Part of you wishes you were brave enough to join them, while another part is glad to be safe at home.

-> END
