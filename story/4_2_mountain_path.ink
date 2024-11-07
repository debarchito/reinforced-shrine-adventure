=== 4_2_mountain_path ===
The maintenance path winds upward through the dense foliage, your flashlight beams cutting through the darkness.
Old service rails, now rusted and overgrown, guide your ascent along the mountain's face.

@Kanae: *breathing heavily* The air feels different up here... it's difficult to breathe...*cough*

{has_first_aid_kit: @{player_name}: Are you alright, Kanae? I have an emergency oxygen mask if you need it.}
    
{caution >= 10:
    @Haruto: *concerned* Kanae, maybe we should take a break? The altitude change can be rough.
}
{social >= 5:
    @Airi: *putting a supportive hand on Kanae's shoulder* Hey, take it easy. We can rest if you need to.
}

@Ryu: *checking phone* The barometric pressu-... wait, what? That can't be right. The pressure just plummeted.

A distant rumble of thunder echoes across the mountain, and the first drops of rain begin to fall.

@Airi: *nervously* Maybe we should head back...
@Haruto: *studying the path ahead* Wait - look there. Is that a maintenance station?

Through the growing rain, a squat concrete structure comes into view, partially hidden by vegetation.

* [Take shelter in the structure]
    ~ curiosity += 1
    @{player_name}: This might be our best option as the storm is getting worse.
    @Kanae: *examining the door* The lock's completely rusted through...
    
    With some effort, you manage to force the old door open.
    The interior is dusty but surprisingly intact.
    
    @Ryu: *sweeping flashlight around* Look at all this old equipment...
    @Airi: At least it's dry in here.

* [Press on despite weather]
    ~ caution += 1
    @{player_name}: We should try to reach the shrine before the storm hits full force.
    @Haruto: *pointing at sky* Those clouds are moving too fast. We won't make it.
    
    A brilliant flash of lightning illuminates the mountain, followed immediately by deafening thunder.
    
    @Kanae: *grabbing your arm* No time to argue - we need shelter NOW!

- The storm breaks with sudden fury. Rain pounds against the mountain as wind howls through the old coaster track.
Safe inside the maintenance station, your group catches their breath.

The maintenance station, though old and dusty, provides a welcome refuge from the raging storm outside.

Haruto's flashlight beams dance across walls covered in faded safety posters and old maintenance schedules.

@Haruto: *eyes widening* Whoa... these old control panels... This must've been their command center for the whole coaster system. Look at all these switches and gauges!

@Kanae: *shivering* The temperature's dropping fast...

{has_snacks:
    @{player_name}: Good thing I packed some snacks. Anyone hungry?
    @Haruto: *grateful smile* Always prepared, aren't you?
    
    You share the food, the simple act of eating together somehow making the situation feel less dire.
}

A particularly violent gust of wind rattles the station's metal door, making everyone jump.

@Airi: *huddling closer* Do... do you think this place is really safe?

{has_talisman:
    You instinctively clutch the talisman in your pocket, its presence somehow reassuring.
    @{player_name}: Stay away from the door. It'll all be fine.
}

@Ryu: *checking phone again* Still no signal. And these pressure readings are getting weirder...

{supernatural >= 2:
    The wind outside seems to carry whispers, almost like distant voices calling out in the storm.
    @{player_name}: Does anyone else... hear that?
}

@Haruto: *looking through window* This storm... it's not natural. The clouds are moving in patterns I've never seen before.

* [Suggest waiting it out]
    ~ caution += 2
    @{player_name}: Maybe we should just camp here for the night. Better safe than sorry.
    
    @Kanae: Spend the night? Here?
    
    @Haruto: *nodding* {player_name}'s right. We've got shelter, we're dry...
    
    {has_water: @{player_name}: And we have water. We can make it through the night.}
    
    @Ryu: *settling down* We still need to keep an eye on the path.

    $jump station_night
    -> 5_1_station_night

* [Propose watching for a break]
    ~ curiosity += 1
    ~ stayed_at_station = true
    @{player_name}: Let's watch the storm. If it lets up even a little, we can make a run for it.
    
    @Airi: The shrine can't be too much further...
    
    @Ryu: *studying old route maps on wall* According to this, we're more than halfway there.

    $jump watch_storm
    -> 5_2_watch_storm
