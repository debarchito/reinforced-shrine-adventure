=== 3_1_beach_path ===
The beach path stretches before you, a thin line against the restless surf.
Waves creep higher with each surge, already lapping unusually close to the path.

@Kanae: *voice tense* This isn't right... The water shouldn't be this high yet.

@Ryu: *checking phone with shaking hands* There's a coastal flood warning… a spring tide combined with a storm surge.

@Aie: *face paling* A flood warning? But I checked the weather… wait, how could I have missed it?

The realization hits hard — this was the crucial detail everyone overlooked.

@Haruto: *grabbing Aie's shoulder* Focus, Aie! We don't have time for this! Move, everyone — RUN!

* [Get to higher ground immediately]
    ~ caution += 2
    @{player_name}: *urgently* We need to move, NOW! Head for the cliffs!
    @Airi: *voice trembling* What's happening?
    @{player_name}: Spring tides combined with a storm can raise water levels by several meters, fast. We shouldn't have come this way… damn it.

* [Look for escape routes]
    ~ curiosity += 1
    ~ caution += 1
    @{player_name}: Everyone, look for a path up the cliffs! We can't stay here!
    @Ryu: *pointing* The waves are already cutting off our way back!

- Water swirls around your foot, and the first drops of rain begin to fall, forming a misty curtain that limits visibility.

A deafening crack of thunder overhead coincides with another massive wave, spraying saltwater in your faces. The intensifying rain and rising tide are creating a perilous situation.

@Kanae: *shouting over the wind* The water's rising too fast! We need to get to higher ground now!

@Ryu: *stumbling* There might be a path up the cliffs, just ahead!

* [Try to reach the cliff path]
    ~ caution += 2
    @{player_name}: Everyone, link arms! We'll make it if we stick together!
    The group forms a human chain, but the strengthening current pulls at your legs, the water now up to your waists.

    ** [Push forward]
        ~ curiosity += 1
    @{player_name}: Just a little further! I think I see a path!
        @Airi: *voice breaking* The current… it's too strong, I can't…

    ** [Turn back]
        ~ caution += 1
        @{player_name}: It's too dangerous. We need to find another way!
        @Haruto: *gritting teeth* There IS no other way!

- Before anyone can react, a massive wave crashes over the group, breaking your chain and scattering everyone. The roar of the water drowns out all other sound.

@Ryu: *surfacing, coughing* Help! I… I can't swim against this. GASP...
@{player_name}: Hold on! Grab onto anything solid!

{has_flashlight: Your flashlight beam cuts through the chaos, catching terrifying glimpses of your friends struggling in the water.}

* [Attempt a rescue]
    ~ social += 2
    ~ caution += 1
    @{player_name}: *fighting against the current* Everyone...GASP...swim towards my voice! We need to stay together!
    With desperate strokes, you manage to reach Ryu first, pulling him towards a partially submerged rock formation; waves so strong that your grip is slipping slowly..

* [Search for higher ground]
    ~ caution += 2
    @{player_name}: GASP...There's a ledge over there! Everyone swim towards it!
    The waves crash against you as you guide your friends toward what looks like a stable outcropping.

- Through sheer determination, you manage to gather everyone onto a small rocky platform. The water swirls menacingly below, but for now, you're above the worst of it.

@Airi: *sobbing* My leg... I hit it on the rocks...
@Kanae: *clutching her arm* The current slammed me against something...
@Ryu: *coughing up water* I think I swallowed half the ocean...*cough*

{has_first_aid_kit: 
    @{player_name}: *pulling out the first aid kit* Thank goodness, I brought this. Let me patch you up.
    You quickly assess the injuries. Airi has a nasty gash on her leg, while Kanae's arm shows signs of bruising.
    @{player_name}: *working efficiently* This might sting, but it'll prevent infection.
    @Airi: *wincing* Thank you, Aie...
    The group's spirits lift slightly as you tend to their wounds.
    @Kanae: *head down, eyes filled with tears* Sorry guys it's all my fault....
    @{player_name}: Don't blame yourself kanae.. you nobody knew the situation will get this bad.
    @kanae: But-
    @Airi: Aie is right it was all unexpected and.... it's partially everyone's fault for not checking the weather, right? everyone.
    
    - else:
    @{player_name}: *helplessly* I... I should have brought the first aid kit...
    @Haruto: *tearing strips from his shirt* We'll have to make do with makeshift bandages.
    @Kanae: *head down, eyes filled with tears* Sorry guys it's all my fault....

}

@Kaori: *shivering* The rescue lights... they're so far away...
@Ryu: *voice weak* My phone's dead... we can't even call for help...

- The group huddles together for warmth, the adrenaline wearing off to reveal exhaustion and fear.

@Haruto: *squinting through the rain* Wait... do you hear that?

A distant mechanical whirring cuts through the storm's chaos - the unmistakable sound of rescue boats.

@{player_name}: *waving frantically* Over here! We're over here!

- The searchlight from a coast guard vessel sweeps across the cliffs, finally finding your group.

@Coast Guard: *through megaphone* Hold your position! We're coming to get you!

@Airi: *crying with relief* We're... we're going to make it...

- As the rescue boat carefully approaches, you look at your battered and exhausted friends. You've survived, but it was far too close.

-> DONE
