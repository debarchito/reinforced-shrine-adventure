=== 6_silent_morning ===

Dawn breaks with an eerie stillness. The storm that raged through the night has passed, leaving behind a landscape transformed by its fury.

@Ryu: *stretching* Everyone made it through okay?

Your group slowly stirs from their makeshift beds, muscles stiff from sleeping on the hard floor.
The maintenance map you discovered last night lies where you left it, its markings holding the key to your path forward.

@Haruto: *spreading out map* According to this, the zip-line station should be just up that service trail.

@Kanae: *peering at markings* They kept using it for years after the bridge collapsed.

@Airi: But how do we even find it? Everything's probably overgrown by now...

* [Study the technical details]
    ~ curiosity += 1
    @{player_name}: Look at these specifications - steel cable rated for maintenance carts. This wasn't just some temporary solution.
    
    @Haruto: *tracing route* The platform should be built right into the mountainside. Something that sturdy doesn't just disappear.
    
    @Ryu: These coordinates and landmarks... we can work with this.

- After a quick breakfast, your group follows the maintenance map's guidance.
The service trail is overgrown but still visible, switching back and forth up the mountainside.

@Kaori: *pushing through vegetation* Wait - I see something metal!

Breaking through a curtain of vines, you discover a sturdy platform extending from the cliff face.
Years of exposure haven't weakened its heavy-duty construction.

@Airi: *looking down* Oh... that's... that's quite a drop...

Through gaps in the morning mist, you catch glimpses of the shrine's distinctive roof across the chasm.
A thick steel cable, weathered but intact, stretches into the fog.

@Haruto: *examining equipment locker* Look at this - they kept everything sealed properly. Harnesses, pulleys, all the safety gear...

{has_talisman:
    The talisman in your pocket seems to warm slightly, as if responding to the shrine's proximity.
}

* [Inspect the mechanism]
    ~ curiosity += 2
    @{player_name}: The winch system looks solid. They built this to last.
    
    @Ryu: *testing cable* No rust... they used marine-grade steel.
    
    @Haruto: These maintenance logs in the locker... they checked it monthly.

* [Test safety equipment]
    ~ caution += 2
    @{player_name}: Let's check every piece of gear thoroughly. We can't risk anything.
    
    Your group methodically inspects each component, comparing them against the maintenance diagrams.
    
    @Kanae: The backup brake system still works. They really thought of everything.

- One by one, your group prepares for the crossing.
Haruto goes first, double-checking his harness before pushing off.
The zip-line hums with tension as he glides through the mist, becoming a silhouette against the clouded sky.
Ryu follows, then Kanae, then Kaori, each disappearing briefly in the fog before emerging safely on the other side.
Airi's hands shake as she grips the handles, but her determination shows in her set jaw as she takes the plunge.
Finally, it's your turn. The old cable holds steady as you slide across the chasm, wind whipping past your ears.
Through breaks in the mist, you catch dizzying glimpses of the forested valley far below.
The shrine's curved roof grows larger, its weathered tiles and ancient timber drawing closer with each passing second.

@Airi: *feet touching platform* I can't believe that worked...

@Ryu: *unhooking harness* The engineers who built this... they knew what they were doing.

@{player_name}: The shrine should be just ahead.

@Kaori: *voice hushed* After everything we went through to get here...

@Haruto: *smiling* Sometimes the hardest path leads to exactly where you need to be.

$jump shrine
-> 7_shrine
