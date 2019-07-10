from header_common import *
from header_animations import *

####################################################################################################################
#  There are two animation arrays (one for human and one for horse). Each animation in these arrays contains the following fields:
#  1) Animation id (string): used for referencing animations in other files. The prefix anim_ is automatically added before each animation-id .
#  2) Animation flags: could be anything beginning with acf_ defined in header_animations.py
#  3) Animation master flags: could be anything beginning with amf_ defined in header_animations.py
#  4) Animation sequences (list).
#  4.1) Duration of the sequence.
#  4.2) Name of the animation resource.
#  4.3) Beginning frame of the sequence within the animation resource.
#  4.4) Ending frame of the sequence within the animation resource.
#  4.5) Sequence flags: could be anything beginning with arf_ defined in header_animations.py
# 
####################################################################################################################

#plan : 
# basic movement : walk ride etc. 0 -20000
#  on_foot  : 0     - 10000
#  horse    : 10000 - 20000
# combat         :                20000 - 40000
# fall           :                4000 - 70000
# act            : misc.          70000 - ...

amf_priority_jump           = 2
amf_priority_ride           = 2
amf_priority_continue       = 1
amf_priority_attack         = 10
amf_priority_cancel         = 12
amf_priority_defend         = 14
amf_priority_defend_parry   = amf_priority_defend + 1
amf_priority_throw          = amf_priority_defend + 1
amf_priority_blocked        = amf_priority_defend_parry
amf_priority_parried        = amf_priority_defend_parry
amf_priority_kick           = 33
amf_priority_jump_end       = 33
amf_priority_reload         = 60
amf_priority_mount          = 64
amf_priority_equip          = 70
amf_priority_rear           = 74
amf_priority_striked        = 80
amf_priority_fall_from_horse= 81
amf_priority_die            = 95

horse_move = 10000
combat     = 20000
defend     = 35000
blow       = 40000

attack_parried_duration = 0.6
attack_blocked_duration = 0.3
attack_blocked_duration_thrust = attack_blocked_duration + 0.3
attack_parried_duration_thrust = attack_parried_duration + 0.1
defend_parry_duration_1 = 0.6
defend_parry_duration_2 = 0.6
defend_parry_duration_3 = 0.8
ready_durn     = 0.35
defend_duration = 0.75
defend_keep_duration = 2.0
cancel_duration = 0.25

blend_in_defense = arf_blend_in_3
blend_in_ready = arf_blend_in_6
blend_in_release = arf_blend_in_5
blend_in_parry = arf_blend_in_5
blend_in_parried = arf_blend_in_3

blend_in_walk = arf_blend_in_3
blend_in_continue = arf_blend_in_1

animations = [
  ["ready_overswing_spear", acf_thrust|acf_rot_vertical_bow|acf_anim_length(100), amf_priority_attack|amf_use_weapon_speed|amf_use_inertia|amf_keep|amf_client_owner_prediction,
    [ready_durn, "attacks_staff_thrust_overhead", 0, 21, blend_in_ready],
  ],
  ["release_overswing_spear", acf_thrust|acf_rot_vertical_bow|acf_anim_length(100), amf_priority_attack|amf_use_weapon_speed|amf_play|amf_continue_to_next,
    [0.6, "attacks_staff_thrust_overhead", 21, 43, blend_in_release],
  ],
  ["release_overswing_spear_continue", acf_thrust|acf_rot_vertical_bow|acf_anim_length(100), amf_priority_continue|amf_use_weapon_speed|amf_play|amf_client_owner_prediction,
    [0.3, "attacks_staff_thrust_overhead", 43, 50, arf_blend_in_2],
  ],
  ["parried_overswing_spear", acf_rot_vertical_bow|acf_anim_length(100), amf_priority_parried|amf_use_weapon_speed|amf_play,
    [0.3, "attacks_staff_thrust_overhead", 50, 43, arf_blend_in_2],
  ],
  ["blocked_overswing_spear", acf_rot_vertical_bow|acf_anim_length(100), amf_priority_blocked|amf_use_weapon_speed|amf_play,
    [0.3, "attacks_staff_thrust_overhead", 50, 43, arf_blend_in_2],
  ],
  
  ["ready_overswing_musket", acf_thrust|acf_rot_vertical_bow|acf_anim_length(100), amf_priority_attack|amf_use_weapon_speed|amf_use_inertia|amf_keep|amf_client_owner_prediction,
    [ready_durn, "javelin_thrust_overhead", 0, 35, blend_in_ready],
  ],
  ["release_overswing_musket", acf_thrust|acf_rot_vertical_bow|acf_anim_length(100), amf_priority_attack|amf_use_weapon_speed|amf_play|amf_continue_to_next,
    [0.55, "javelin_thrust_overhead", 35, 81, blend_in_release],
  ],
  ["release_overswing_musket_continue", acf_thrust|acf_rot_vertical_bow|acf_anim_length(100), amf_priority_continue|amf_use_weapon_speed|amf_play|amf_client_owner_prediction,
    [0.4, "javelin_thrust_overhead", 81, 100, arf_blend_in_2],
  ],
  ["parried_overswing_musket", acf_rot_vertical_bow|acf_anim_length(100), amf_priority_parried|amf_use_weapon_speed|amf_play,
    [attack_parried_duration, "javelin_thrust_overhead", 81, 70, blend_in_parry],
  ],
  ["blocked_overswing_musket", acf_rot_vertical_bow|acf_anim_length(100), amf_priority_blocked|amf_use_weapon_speed|amf_play,
    [attack_blocked_duration, "javelin_thrust_overhead", 81, 70, blend_in_parry],
  ],
  
  ["crouch_pike", 0, amf_client_prediction,
    [3.3, "crouch_staff_cstance_attack", 0, 100, arf_use_stand_progress|arf_cyclic, 0, (0, 0, 0), 0.0], 
  ],
  ["crouch_pike_recover", 0, amf_priority_parried|amf_use_weapon_speed|amf_play,
    [1.2, "crouch_staff_cstance_attack", 105, 137, arf_blend_in_3, 0, (0, 0, 0), 0.0], 
  ],
]