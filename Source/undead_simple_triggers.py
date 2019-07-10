from header_common import *
from header_operations import *
from header_troops import *
from header_triggers import *

from module_constants import *

class SimpleTrigger:
  def __init__(self, check_interval, operations = []):
    self.check_interval = check_interval
    self.operations = operations
  
  def __str__(self):
    script_string = "(" + self.check_interval + ",\n[\n"
    for operation in self.operations:
      script_string += "\t" + str(operation) + ",\n"
    script_string += "])"
    return script_string
  
  def convert_to_tuple(self):
    return (self.check_interval, self.operations)

new_simple_triggers = [
	
	# This trigger will activate upon the game being loaded
	(0,
	[
		(try_begin),
			(store_item_kind_count, reg0, "itm_no_item", "trp_game_load_check"),
			(eq, reg0, 0),
			
			# Ensure undead and skeleton troops have perfect morale
			(faction_set_slot, "fac_undeads", slot_faction_morale_of_player_troops, 10000),
			
			(troop_add_item, "trp_game_load_check", "itm_no_item"),
		(try_end),
	]),
	
	# Cheat option: Immediately add next horseman to party by pressing ctrl+H
	(0,
	[
		(try_begin),
			(eq, "$cheat_mode", 1),
			(this_or_next|key_is_down, key_left_control),
			(key_is_down, key_right_control),
			(key_clicked, key_h),
			
			(lt, "$horseman_to_add_index", 4),
			
			(store_add, ":horseman", four_horsemen_begin, "$horseman_to_add_index"),
			(store_add, ":horseman_intro", four_horsemen_intros_begin, "$horseman_to_add_index"),
			(dialog_box, ":horseman_intro"),
			(party_force_add_members, "p_main_party", ":horseman", 1),
			
			(val_add, "$horseman_to_add_index", 1),
		(else_try),
			(eq, "$cheat_mode", 1),
			(this_or_next|key_is_down, key_left_control),
			(key_is_down, key_right_control),
			(key_clicked, key_x),
			
			(party_add_members, "p_main_party", "trp_ghoul_hunter", 10),
			(party_add_members, "p_main_party", "trp_ghoul_hulk", 10),
			(party_add_members, "p_main_party", "trp_skeleton_heavy_infantry", 10),
			(party_add_members, "p_main_party", "trp_skeleton_knight", 10),
			(party_add_members, "p_main_party", "trp_skeleton_death_knight", 10),
			(display_message, "@Added ghouls and skeletons to party"),
		(try_end),
	]),
	
	# Every 30 days, flag that the next horseman should be added at midnight
	(30 * 24,
	[
		(try_begin),
			(lt, "$horseman_to_add_index", 4),
			
			(assign, "$add_horseman_to_party", 1),
		(try_end),
	]),
	
	# At midnight, the next horseman joins the player's party if flagged, or a lost horseman can join
	(1,
	[
		(try_begin),
			(store_time_of_day, ":hour"),
			(eq, ":hour", 0),
			
			(try_begin),
				(eq, "$add_horseman_to_party", 1),
				
				(store_add, ":horseman", four_horsemen_begin, "$horseman_to_add_index"),
				(store_add, ":horseman_intro", four_horsemen_intros_begin, "$horseman_to_add_index"),
				(dialog_box, ":horseman_intro"),
				(party_force_add_members, "p_main_party", ":horseman", 1),
				
				(val_add, "$horseman_to_add_index", 1),
				(assign, "$add_horseman_to_party", 0),
			(else_try),
				# Horsemen lost from party rejoin one day at a time
				(assign, ":horseman_indexes_end", "$horseman_to_add_index"),
				(try_for_range, ":horseman_index", 0, ":horseman_indexes_end"),
					(store_add, ":horseman", four_horsemen_begin, ":horseman_index"),
					(neg|main_party_has_troop, ":horseman"),
					
					(str_store_troop_name, s0, ":horseman"),
					(display_message, "@{s0} rejoined your party"),
					(party_force_add_members, "p_main_party", ":horseman", 1),
					
					(assign, ":horseman_indexes_end", 0),
				(try_end),
			(try_end),
		(try_end),
	]),
	
	(24,
	[
	
	]),
  
]

def modmerge(var_set):
  try:
    var_name_1 = "simple_triggers"
    orig_simple_triggers = var_set[var_name_1]
    
    orig_simple_triggers.extend(new_simple_triggers)
    
    simple_triggers = []
    for st_tuple in orig_simple_triggers:
      simple_triggers.append(SimpleTrigger(*st_tuple))
    
    # Edit the food consumption trigger to skip over undead troops (the undead do not need to eat)
    for simple_trigger in simple_triggers:
      if (call_script, "script_consume_food", ":selected_food") in simple_trigger.operations:
        index = simple_trigger.operations.index((party_stack_get_size, ":stack_size","p_main_party",":i_stack"))
        simple_trigger.operations[index:index] = [
          (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
					(troop_get_type, ":troop_type", ":stack_troop"),
          (neg|is_between, ":troop_type", tf_undead, tf_skeleton + 1),
        ]
    
    del orig_simple_triggers[:]
    for simple_trigger in simple_triggers:
      orig_simple_triggers.append(simple_trigger.convert_to_tuple())
    
    #print var_name_1 + " done"
    
  except KeyError:
      errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
      raise ValueError(errstring)