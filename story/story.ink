INCLUDE 1_summer_break_choice.ink
INCLUDE 2_packing.ink

// Details
VAR player_name = "Aie"
// Attributes
VAR curiosity = 0
VAR social = 0
VAR caution = 0
VAR agnostic = 0
VAR supernatural = 0
// Items
VAR has_talisman = false
VAR has_snacks = false

-> summer_break_choice_tunnel -> 2_packing

=== summer_break_choice_tunnel ===
-> 1_summer_break_choice ->->

=== packing ===
-> 2_packing
