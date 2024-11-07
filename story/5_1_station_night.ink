=== 5_1_station_night ===

The storm continues to rage outside as your group settles in for an unexpected night in the maintenance station.
The old fluorescent lights are long dead, but your flashlights cast enough light to work by.

@Airi: *brushing cobwebs away* We should try to make this place a bit more... habitable.

@Haruto: Good idea. Let's see what we can find.

{has_snacks:
    @{player_name}: Well, at least we won't go hungry. *pulling out snacks* 
    
    You spread out the food on a cleared workbench, creating an impromptu picnic.
    
    @Kanae: *smiling* It's like a midnight feast! Just... with more dust and old machinery.
}

As you work to clear some floor space, Ryu discovers some old emergency blankets in a utility closet.

@Ryu: They're a bit musty, but they'll keep us warm.

While moving some boxes to create sleeping areas, you bump into an old metal shelf.
A dusty cardboard box tumbles from the top, spilling its contents across the floor.

@{player_name}: Sorry! I'll clean that up...

@Haruto: *picking up papers* Wait... these look like maintenance documents!

Among the scattered papers, a large folded blueprint catches your eye.
As you carefully unfold it, your flashlight reveals detailed route maps of the shrine grounds.

@Kaori: *leaning in* What's that marking there?

@Haruto: *studying the map* This is interesting... Look at this: "Bridge collapsed during typhoon season. Emergency zip-line system implemented for maintenance access."

@Ryu: *excited* A zip-line? That means the original route was a dead end all along..?

@Airi: But that was years ago... Would it even still be there?

* [Study the map carefully]
    ~ curiosity += 1
    @{player_name}: These markings show the zip-line route... they are actually quite detailed.
    
    @Haruto: *tracing the path* If it's still intact, it could save us hours of hiking.
    
    @Kanae: But is it safe? After all this time?

* [Express concern]
    ~ caution += 1
    @{player_name}: An incredibly old emergency zip-line? That sounds incredibly dangerous.
    
    @Kanae: We don't have to decide now. Let's sleep on it.

It's almost as if decicing to stay back paid off silently.

- As the night deepens, your group arranges the emergency blankets on the cleared floor.
The storm's fury seems to have lessened somewhat, but rain still drums steadily on the metal roof.

@Airi: *wrapping herself in a blanket* Should we take turns keeping watch?

@Kaori: Good idea. I'll take first shift.

{has_flashlight: 
    You position your flashlight to create a makeshift lantern, casting a warm glow over your makeshift camp.
}

After a few hours, it's your turn to keep watch. 
As your friends settle in for the night, you can't help but wonder about the zip-line.
Could it really offer a way to reach the shrine? And more importantly - should you risk it?
But the original route is a dead end, so it's not like you have a lot of options.

The maintenance map rests nearby, its secrets waiting to be explored in the morning light.

$jump silent_morning
-> 6_silent_morning
