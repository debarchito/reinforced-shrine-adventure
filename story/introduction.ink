VAR player_name = "Aie"
VAR courage = 0
VAR has_talisman = false

-> introduction

=== introduction ===

# Introduction

The final bell of the semester rings, signaling the start of summer vacation. As your classmates burst into excited chatter, you, {player_name}, quietly pack your bag, ready to slip away unnoticed.

Kaori: "Hey, everyone! I've got an awesome idea!"

Kaori bursts into the classroom, her eyes sparkling with excitement, a newspaper clutched tightly in her hand.

* [Look up curiously]
    You raise your head, curiosity getting the better of your usual reserve.
    ~ courage += 1
* [Pretend not to hear]
    You keep your head down, hoping to avoid whatever scheme Kaori's cooked up this time.
    ~ courage -= 1

- Kaori's gaze sweeps the room, landing on you and your friends: Airi, Kanae, Ryu, and Haruto.

Kaori: "Why don't we visit this shrine for a test of courage? It's rumored that there's some treasure hidden somewhere around the shrine!"

Airi: "A shrine? Where?"

Kaori: "It's in that old abandoned amusement park by the sea. You know, the one up on the hill surrounded by that creepy forest?"

* [Speak up]
    {player_name}: "Isn't that place off-limits?"
    ~ courage += 1
    Kaori: "That's what makes it exciting, Aie!"
* [Stay silent]
~ courage -= 1
    You shrink in your seat, hoping to avoid being dragged into this.

- Ryu: "A test of courage, huh? Sounds like fun!"

Haruto: "I'm in! What about you, Kanae?"

Kanae: "Well... okay. But we should be careful, right?"

All eyes turn to you.

Kaori: "Come on, Aie! It'll be fun. We can't do this without you!"

* [Reluctantly agree]
    {player_name}: "I... I guess I could come along."
    ~ courage += 2
    Kaori: "Great! It's decided then!"
    -> group_planning
* [Try to back out]
    {player_name}: "I don't know... It sounds dangerous."
    ~ courage -= 2
    Haruto: "Don't worry, we'll all be there together. Safety in numbers, right?"
    -> convince_player

=== convince_player ===

Airi: "It would mean a lot if you came, Aie. We're all friends here."

Ryu: "Yeah, and think of the stories we'll have to tell when school starts again!"

* [Give in]
    {player_name}: "Alright, alright. I'll come."
    ~ courage += 1
    Kaori: "Yes! This is going to be awesome!"
    -> group_planning
* [Stand firm]
    {player_name}: "I really don't think it's a good idea."
    Kaori: "What if we bring talismans for protection? Would that help?"
    -> talisman_option

=== talisman_option ===

* [Accept the talisman]
    {player_name}: "Well... if we have talismans, I guess it might be okay."
    ~ has_talisman = true
    ~ courage += 1
    Kaori: "Perfect! I'll make sure we all have talismans."
    -> group_planning
* [Refuse]
    {player_name}: "I don't think a talisman will make much difference."
    Kaori: "I understand. But please, think about it? We really want you there."
    -> final_decision

=== final_decision ===

The group looks at you expectantly. This is your last chance to decide.

* [Join the group]
    {player_name}: "Okay, I'll come. But promise we'll be careful?"
    ~ courage += 3
    Kaori: "Of course! We'll stick together and watch out for each other."
    Everyone nods enthusiastically.
    -> group_planning
* [Refuse to go]
    {player_name}: "I'm sorry, but I really can't. Have fun without me."
    ~ courage -= 3
    Airi: "We'll miss you, Aie."
    The group looks disappointed, but they respect your decision.
    -> solo_ending

=== group_planning ===

Kaori: "Alright! Let's meet at the old park entrance tomorrow at dusk. Don't forget to bring flashlights!"

As your friends chatter excitedly about tomorrow's adventure, you feel a mix of anticipation and anxiety. What awaits you at the abandoned shrine?

Ryu: "Hey, Aie, you okay? You look a bit pale."

* [Admit your nervousness]
    {player_name}: "Just a little nervous, I guess. This is pretty out of my comfort zone."
    Airi: "Don't worry, we'll all look out for each other. Right, everyone?"
    The group nods reassuringly.
    ~ courage += 1
* [Put on a brave face]
    {player_name}: "I'm fine. Just thinking about what to pack."
    Haruto: "That's the spirit! Maybe bring some snacks to share?"
    ~ courage += 2

- Kanae: "Should we bring anything else? First aid kit maybe?"

Kaori: "Good thinking, Kanae! Aie, since you're good at planning, why don't you make a list of things we should bring?"

* [Accept the responsibility]
    {player_name}: "Sure, I can do that. Better to be prepared, I suppose."
    ~ courage += 2
    You start jotting down items: flashlights, first aid kit, snacks, water...
* [Deflect the task]
    {player_name}: "Uh, maybe someone else should do it? I'm not sure what we'd need."
    ~ courage -= 1
    Airi: "No problem, I can handle it. But feel free to add any ideas, Aie!"

- As the group continues to plan, you can't help but wonder if you've made the right decision. But seeing your friends' excitement, a small part of you starts to look forward to the adventure.

Kaori: "This is going to be the best summer break ever! See you all tomorrow!"

The group disperses, leaving you with your thoughts about the upcoming test of courage.

-> group_ending

=== group_ending ===

# Group Ending

{courage >= 5:
    Despite your initial reservations, you feel a spark of excitement about the adventure ahead. Maybe this test of courage is just what you need to come out of your shell. You head home, already thinking about what to pack for tomorrow.
- else:
    You head home, a knot of worry in your stomach. As night falls, you wonder about things that could go wrong... but it's too late to back out now. You'll just have to face whatever comes tomorrow.
}

-> DONE

=== solo_ending ===

# Solo Ending

You head home alone, feeling a mix of relief and regret. As you settle in for a quiet evening, your phone buzzes with messages from your friends.

Kaori: "We'll miss you tomorrow, Aie! But we understand. Maybe next time?"
Airi: "Take care, Aie. We'll tell you all about it when we get back."
Ryu: "Your loss, buddy! But hey, if you change your mind, you know where to find us!"

* [Reply with encouragement]
    {player_name}: "Have fun, guys. Be safe out there."
    ~ courage += 1
* [Don't reply]
    You set your phone aside, trying to ignore the pang of regret.
    ~ courage -= 1

- As night falls, you wonder if you've made the right decision. Part of you wishes you were brave enough to join them, while another part is glad to be safe at home.

-> DONE
