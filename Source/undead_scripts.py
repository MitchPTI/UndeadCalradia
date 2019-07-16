# -*- coding: cp1254 -*-
import collections

from header_common import *
from header_operations import *
from header_items import *
from header_troops import *
from module_constants import *
from ID_items import *

from module_troops import troops

class Script:
	def __init__(self, id, operations = []):
		self.id = id
		self.operations = operations
	
	def __str__(self):
		script_string = "(\"" + self.id + "\",\n[\n"
		for operation in self.operations:
			script_string += "\t" + str(operation) + ",\n"
		script_string += "])"
		return script_string
	
	def convert_to_tuple(self):
		return (self.id, self.operations)

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

new_start_operations = [
	# Give undead troops a morale bonus of 10000 so they always have perfect morale
	(faction_set_slot, "fac_undeads", slot_faction_morale_of_player_troops, 10000),
	#(party_add_members, "p_main_party", "trp_horseman_pestilence", 1),
	#(party_add_members, "p_main_party", "trp_horseman_war", 1),
	#(party_add_members, "p_main_party", "trp_horseman_famine", 1),
	#(party_add_members, "p_main_party", "trp_horseman_death", 1),
	#(party_add_members, "p_main_party", "trp_skeleton_death_knight", 100),
	(troop_add_item, "trp_player", "itm_spak_IceAxe"),
	(troop_add_item, "trp_player", "itm_kingslayer"),
	(troop_add_item, "trp_player", "itm_demonic_boots"),
	(troop_add_item, "trp_player", "itm_demonic_gauntlets"),
	(troop_add_item, "trp_player", "itm_helm07"),
	(troop_add_item, "trp_player", "itm_splate_armor2"),
]

for troop in troops[find_troop(troops, soldiers_begin[len("trp_"):]):find_troop(troops, soldiers_end[len("trp_"):])]:
	flags = troop[3]
	if (flags & tf_hero) == 0 and (flags & troop_type_mask) < tf_undead and not troop[0].startswith("undead_"):
		new_start_operations.append((troop_set_slot, "trp_" + troop[0], undead_slot_troop_undead, "trp_undead_" + troop[0]))
		#print((troop_set_slot, "trp_" + troop[0], undead_slot_troop_undead, "trp_undead_" + troop[0]))

party_encounter_operations = [
	(party_clear, "p_recruitable_undead"),
	#(display_message, "@Clearing recruitable undead"),
]

new_scripts = [
	
	("famine_consume_agent",
	[
		(store_script_param, ":agent", 1),
		
		(agent_get_troop_id, ":troop_type", ":agent"),
		
		(try_for_range, ":troop_attribute", 0, 4),
			(store_attribute_level, ":troop_attribute_level", ":troop_type", ":troop_attribute"),
			(store_attribute_level, ":famine_attribute_level", "trp_horseman_famine", ":troop_attribute"),
			
			(store_mul, ":increase", 30, ":troop_attribute_level"),
			(store_add, ":denominator", ":famine_attribute_level", 120),
			(val_div, ":increase", ":denominator"),
			
			(gt, ":increase", 0),
			
			(troop_raise_attribute, "trp_horseman_famine", ":troop_attribute", ":increase"),
		(try_end),
		
		(try_for_range, ":troop_skill", skl_horse_archery, skl_reserved_14),
			(store_skill_level, ":troop_skill_level", ":troop_skill", ":troop_type"),
			(store_skill_level, ":famine_skill_level", ":troop_skill", "trp_horseman_famine"),
			
			(store_add, ":skill_slot", undead_slot_famine_skill_points_start, ":troop_skill"),
			(troop_get_slot, ":skill_point_accumulation", "trp_horseman_famine", ":skill_slot"),
			(val_add, ":skill_point_accumulation", ":troop_skill_level"),
			(troop_set_slot, "trp_horseman_famine", ":skill_slot", ":skill_point_accumulation"),
			
			(assign, ":skill_point_threshold", 4),
			
			(assign, ":skill_levels_end", 10),
			(try_for_range, ":skill_level", 0, ":skill_levels_end"),
				(try_begin),
					(ge, ":skill_point_accumulation", ":skill_point_threshold"),
					
					(try_begin),
						(eq, ":famine_skill_level", ":skill_level"),
						
						(troop_raise_skill, "trp_horseman_famine", ":troop_skill", 1),
						(val_add, ":famine_skill_level", 1),
					(try_end),
					
					(val_mul, ":skill_point_threshold", 2),
				(else_try),
					(assign, ":skill_levels_end", 0),
				(try_end),
			(try_end),
		(try_end),
		
		(try_for_range, ":troop_proficiency", 0, 7),
			(store_proficiency_level, ":troop_proficiency_level", ":troop_type", ":troop_proficiency"),
			
			(troop_raise_proficiency, "trp_horseman_famine", ":troop_proficiency", ":troop_proficiency_level"),
		(try_end),
		
		(try_for_range, ":armour_slot", 4, 8),
			(agent_get_item_slot, ":new_armour", ":agent", ":armour_slot"),
			(troop_get_inventory_slot, ":current_armour", "trp_horseman_famine", ":armour_slot"),
			
			(gt, ":new_armour", 0),
			
			(item_get_difficulty, ":str_requirement", ":new_armour"),
			(store_attribute_level, ":strength", "trp_horseman_famine", ca_strength),
			(gt, ":strength", ":str_requirement"),
			
			(assign, ":current_armour_value", 0),
			(try_begin),
				(gt, ":current_armour", 0),
				
				(item_get_value, ":current_armour_value", ":current_armour"),
			(try_end),
			
			(item_get_value, ":new_armour_value", ":new_armour"),
			(gt, ":new_armour_value", ":current_armour_value"),
			
			(troop_set_inventory_slot, "trp_horseman_famine", ":armour_slot", ":new_armour"),
			(agent_equip_item, "$famine_agent", ":new_armour"),
			(agent_unequip_item, ":agent", ":new_armour"),
		(try_end),
	]),
	
	("print_kill_count_to_s0",
	[
		(assign, ":total_reported", 0),
		(str_clear, s0),
		(try_for_agents, ":cur_agent"),
			(agent_is_human, ":cur_agent"),
			
			(agent_get_troop_id, ":agent_troop_id", ":cur_agent"),
			(troop_is_hero, ":agent_troop_id"),
			
			(agent_get_kill_count, ":num_killed", ":cur_agent"),
			(agent_get_kill_count, ":num_wounded", ":cur_agent", 1),
			(try_begin),
				(eq, ":cur_agent", "$war_agent"),
				(val_add, ":num_killed", "$war_kills"),
				(val_add, ":num_wounded", "$war_wounded"),
			(try_end),
			
			(troop_get_slot, ":troop_kill_count", ":agent_troop_id", undead_slot_troop_kill_count),
			(troop_get_slot, ":troop_wound_count", ":agent_troop_id", undead_slot_troop_wound_count),
			(val_add, ":troop_kill_count", ":num_killed"),
			(val_add, ":troop_wound_count", ":num_wounded"),
			(troop_set_slot, ":agent_troop_id", undead_slot_troop_kill_count, ":troop_kill_count"),
			(troop_set_slot, ":agent_troop_id", undead_slot_troop_wound_count, ":troop_wound_count"),
			
			(this_or_next|gt, ":num_killed", 0),
			(gt, ":num_wounded", 0),
			
			(str_store_troop_name, s1, ":agent_troop_id"),
			(store_add, reg3, ":num_killed", ":num_wounded"),
			(assign, reg4, ":num_killed"),
			(assign, reg5, ":num_wounded"),
			(str_store_string, s2, "@{reg4} killed, {reg5} wounded"),
			
			(try_begin),
				(this_or_next|eq, ":agent_troop_id", "trp_player"),
				(this_or_next|is_between, ":agent_troop_id", companions_begin, companions_end),
				(is_between, ":agent_troop_id", four_horsemen_begin, four_horsemen_end),
				(str_store_string, s0, "@{s0}^{s1}: {reg3} ({s2})"),
			(else_try),
				(agent_is_ally, ":cur_agent"),
				(str_store_string, s0, "@{s0}^{s1} (ally): {reg3} ({s2})"),
			(else_try),
				(str_store_string, s0, "@{s0}^{s1} (enemy): {reg3} ({s2})"),
			(try_end),
			(val_add, ":total_reported", 1),
		(try_end),
		(try_begin),
			(eq, ":total_reported", 0),
			(str_store_string, s0, "@^None"),
		(try_end),
	]),
	
	#("check_friendly_kills",
	#	[(get_player_agent_own_troop_kill_count, ":count"),
	#	 (try_begin),
	#		 (neq, "$g_player_current_own_troop_kills", ":count"),
	#		 (val_sub, ":count", "$g_player_current_own_troop_kills"),
	#		 (val_add, "$g_player_current_own_troop_kills", ":count"),
	#		 (assign, reg0, ":count"),
	#		 (display_message, "@Friendly kills +{reg0}", 0xFF0000),
	#		 (val_mul, ":count", -1),
	#		 (call_script, "script_change_player_party_morale", ":count"),
	#	 (try_end),
	#]),
]

def add_operations(scripts, script, new_operations):
	script_list = list(script)
	operations = script_list[1]
	for operation in new_operations:
		operations.append(operation)
	
	replace_element(scripts, script, tuple(script_list))

def modmerge(var_set):
	try:
		var_name_1 = "scripts"
		orig_scripts = var_set[var_name_1]

		orig_scripts.extend(new_scripts)
		
		scripts = collections.OrderedDict()
		for script_tuple in orig_scripts:
			scripts[script_tuple[0]] = Script(*script_tuple)
		
		scripts["game_start"].operations.extend(new_start_operations)
		scripts["game_event_party_encounter"].operations.extend(party_encounter_operations)
		
		# Ensure undead troop wages are set to 0 just as with the player and kidnapped girl (though the game seems to round these to 1 anyway)
		index = scripts["game_get_troop_wage"].operations.index((eq, ":troop_id", "trp_kidnapped_girl"))
		scripts["game_get_troop_wage"].operations[index:index+1] = [
			(troop_get_type, ":troop_type", ":troop_id"),
			(this_or_next|eq, ":troop_id", "trp_kidnapped_girl"),
			(is_between, ":troop_type", tf_undead, tf_skeleton + 1),
		]
		
		# Ensure troops of the undead faction also get a morale modifier applied (which is set in the game_start script to be +1000 and is never changed)
		index = scripts["game_get_morale_of_troops_from_faction"].operations.index((set_trigger_result, reg0))
		scripts["game_get_morale_of_troops_from_faction"].operations[index:index] = [
			(try_begin),
				(eq, ":faction_no", "fac_undeads"),
				
				(assign, reg0, 1000),
			(try_end),
		]
		
		# Triple party size limit
		index = scripts["game_get_party_companion_limit"].operations.index((set_trigger_result, reg0))
		scripts["game_get_party_companion_limit"].operations[index:index] = [(val_mul, reg0, 3)]
		
		del orig_scripts[:]
		for script_id in scripts:
			orig_scripts.append(scripts[script_id].convert_to_tuple())
			
	except KeyError:
			errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
			raise ValueError(errstring)