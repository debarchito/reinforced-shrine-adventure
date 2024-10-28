=== 1_summer_break_choice ===
The final bell of the semester rings, signaling the start of summer break. As your classmates burst into excited chatter, you, {player_name}, quietly pack your bag, ready to slip away unnoticed.

@Kaori: GUUUUYYYYYS! YOU WON'T BELIEVE WHAT I FOUND! IT'S THE PERFECT OF THE PERFECT-EST (?) PLACE!

Kaori bursts into the classroom, her eyes sparkling with excitement, and a newspaper clutched tightly in her hand.

* [Look up curiously] You raise your head, curiosity getting the better of your usual reserve.
    ~ courage += 1
* [Pretend not to hear] You keep your head down, hoping to avoid whatever scheme Kaori's cooked up this time.
    ~ courage -= 1

- Kaori's gaze sweeps the room, landing on you and your friends: Airi, Kanae, Ryu, and Haruto.

@Kaori: Why don't we visit this shrine for a test of courage? It's rumored that there's some treasure, hidden somewhere in this shrine!

@Airi: A shrine...a treasure? Wha- can you take it slow?

@Haruto: Breathe Kaori, breathe.

@Kaori: I'm breathing just fine... but that’s not why I’m here for!

@Kaori: Ya'll remember that abandoned amusement park by the ocean in Ukiyo, right? Well, there’s a huge beach on the northern side.

@Kaori: It’s this amazing spot where the mountains meet the ocean... and there’s an old, crumbling shrine at the top of a hill! The best part? It’s rumored to be haunted!

* [Show interest] You lean in, intrigued by Kaori's description.
    ~ courage += 1
    @{player_name}: Tell me more. 
    @Kaori: Finally showing some interest, eh? Get this-
* [Remain skeptical] You raise an eyebrow, not entirely convinced.
    ~ courage -= 1
    @{player_name}: An abandoned amusement park? Sounds dangerous...
    @Kaori: That's the real fun! Get this-

- @Kaori: The stairs leading up to the shrine start right near the shore. You’re practically walking from the beach straight up to the shrine. It’s like something out of a storybook!

@Kanae: Dial down... jeez. Don't know where you get this energy from.

* [Agree with Kanae] You nod in agreement with Kanae's sentiment.
    ~ courage -= 1
    @{player_name}: Yeah, Kaori, maybe take it down a notch?
* [Defend Kaori's enthusiasm] You smile at Kaori's enthusiasm.
    ~ courage += 1
    @{player_name}: Come on, Kanae. Let her finish. It sounds interesting!

- @Kaori: Just listen! That's your only job here!

@Kaori: Back in the day, it was a major tourist attraction. A special miko, chosen by the elders, would perform the legendary "Kagura Yume" ritual, an event that occurred only once every hundred years.

@Kaori: It's said that the chosen miko, blessed by the spirits of the shrine, gains the ability to walk on water during the ritual.

@Kaori: As she gracefully steps across the surface, the water shimmers with a celestial glow, creating an enchanting spectacle that draws people from all over, eager to witness this miraculous event at least once in their lives.

* [Speak up] @{player_name}: Isn't that place off-limits?
    ~ courage += 1
    @Kaori: That's what makes it exciting, Aie!
* [Stay silent] You shrink in your seat, hoping to avoid being dragged into this.
    ~ courage -= 1
    
- @Kaori: So here is the plan: Lets's hold a test of courage in that shrine!

@Ryu: A test of courage, huh? Interesting. Not like we have anything better to do in the break.

@Haruto: Yeah, this actually sounds like a lot of fun! What about you, Kanae?

@Kanae: Well... okay. But we should be careful, right? Airi, any input?

@Airi: I mean, sounds ok but I am not that good with spooky places... you know.

All eyes turn to you.

@Kaori: Come on, Aie! It'll be fun. What do you think?

* [Reluctantly agree] @{player_name}: I... I guess I could come along.
    ~ courage += 2
    @Kaori: Great! It's decided then!
    -> group_planning
* [Try to back out] @{player_name}: I don't know... It sounds dangerous.
    ~ courage -= 2
    @Haruto: Don't worry, we'll all be there together. Safety in numbers, right?
    -> convince_player

=== convince_player ===
@Airi: See, I'm not very good with these things, but I'm still joining.

@Ryu: Yeah, and think of the stories we'll have to tell when school starts again!

* [Give in] @{player_name}: Alright, alright. I'll come.
    ~ courage += 1
    @Kaori: LESS GO! This is going to be super awesome!
    -> group_planning
* [Stand firm] @{player_name}: I really don't think it's a good idea.
    @Kaori: What if we bring talismans for protection? Would that help?
    -> talisman_option

=== talisman_option ===
* [Accept the talisman] @{player_name}: Well... if we have talismans, I guess it might be okay.
    ~ has_talisman = true
    ~ courage += 1
    @Kaori: Perfect! I'll make sure we all have talismans.
    -> group_planning
* [Refuse] @{player_name}: I don't think a talisman will make much difference.
    @Kaori: I understand. But please, think about it? We really want you there.
    -> final_decision

=== final_decision ===
The group looks at you expectantly. This is your last chance to decide.

* [Join the group] @{player_name}: Okay, I'll come. But promise we'll be careful?
    ~ courage += 3
    @Kaori: Of course! We'll stick together and watch out for each other.
    Everyone nods enthusiastically.
    -> group_planning
* [Refuse to go] @{player_name}: I'm sorry, but I really can't. Have fun without me.
    ~ courage -= 3
    @Airi: We'll miss you, Aie.
    The group looks disappointed, but they respect your decision.
    -> solo_ending

=== group_planning ===
@Kaori: Alright! Let's meet at the entrance of the park tomorrow at dusk. Don't forget to bring your flashlights!

As your friends chatter excitedly about tomorrow's adventure, you feel a mix of anticipation and anxiety. What awaits you at the shrine?

@Ryu: Hey, Aie, you okay? You look a bit pale.

* [Admit your nervousness] @{player_name}: Just a little nervous, I guess. This is pretty out of my comfort zone.
    @Airi: Don't worry, we'll all look out for each other. Right, everyone?
    The group nods reassuringly.
    ~ courage += 1
* [Put on a brave face] @{player_name}: I'm fine. Just thinking about what to pack.
    - @Haruto: That's the spirit! Maybe bring some snacks to share?
    ~ courage += 2
    * [Agree to pack snacks] You decide to pack some instant ramen and hot water before you leave tomorrow.
        ~ took_snacks = true
        ~ courage += 2
    * [Politely decline] @{player_name}: I don't think we need snacks as we won't be there for long?
        You decide to skip on packing snacks.
        ~ courage -= 1

- @Kanae: Should we bring anything else? First aid kit maybe?

@Kaori: Good thinking, Kanae! Aie, since you're good at planning, why don't you make a list of things we should bring?

* [Accept the responsibility] @{player_name}: Sure, I can do that. Better to be prepared, I suppose.
    ~ courage += 2
    You start listing down items.
* [Deflect the task] @{player_name}: Uh, maybe someone else should do it? I'm not sure what we'd need.
    ~ courage -= 1
    @Airi: No problem, I can handle it. But feel free to add any ideas, Aie!

- As the group continues to plan, you can't help but wonder if you've made the right decision. But seeing your friends' excitement, a small part of you starts to look forward to the adventure.

@Kaori: This is going to be the best summer break ever! See you all tomorrow!

The group disperses, leaving you with your thoughts about the upcoming test of courage.

-> group_ending

=== group_ending ===
{courage >= 7:
    Despite your initial reservations, you feel a spark of excitement about the adventure ahead. Maybe this test of courage is just what you need to come out of your shell. You head home, already thinking about what to pack for tomorrow.
- else:
    You head home, a knot of worry in your stomach. As night falls, you wonder about things that could go wrong... but it's too late to back out now. You'll just have to face whatever comes tomorrow.
}

->->

=== solo_ending ===
You head home alone, feeling a mix of relief and regret. As you settle in for a quiet evening, your phone buzzes with messages from your friends.

@Kaori: We'll miss you tomorrow, Aie! But we understand. Maybe next time?
@Airi: Take care, Aie. We'll tell you all about it when we get back.
@Ryu: Your loss, buddy! But hey, if you change your mind, you know where to find us!

* [Reply with encouragement] @{player_name}: Have fun, guys. Be safe out there.
    ~ courage += 1
* [Don't reply]
    You set your phone aside, trying to ignore the pang of regret.
    ~ courage -= 1

- As night falls, you wonder if you've made the right decision. Part of you wishes you were brave enough to join them, while another part is glad to be safe at home.

-> END
