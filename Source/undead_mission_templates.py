import collections

from header_common import *
from header_operations import *
from header_mission_templates import *
from module_constants import *

class MissionTemplate:
	def __init__(self, id, flags, type, text, spawn_records, triggers):
		self.id = id
		self.flags = flags
		self.type = type
		self.text = text
		self.spawn_records = spawn_records
		self.triggers = triggers
	
	def convert_to_tuple(self):
		return (self.id, self.flags, self.type, self.text, self.spawn_records, self.triggers)
	
	def has_flag(self, flag):
		return (self.flags & flag) == flag
	
	def spawn_records_have_alter_flag(self, flag):
		have_flag = True
		for spawn_record in self.spawn_records:
			if (spawn_record[2] & flag) == 0:
				have_flag = False
				break
		
		return have_flag


pilgrim_disguise = [itm_pilgrim_hood,itm_pilgrim_disguise,itm_practice_staff, itm_throwing_daggers]
af_castle_lord = af_override_horse | af_override_weapons| af_require_civilian
	
process_casualty = (
	# Add enemy troops killed by members of player party to recruitable undead
	ti_on_agent_killed_or_wounded, 0, 0, [],
	[
		(store_trigger_param, ":dead_agent", 1),
		(store_trigger_param, ":killer_agent", 2),
		(store_trigger_param, ":wounded", 3),
		
		(try_begin),
			(agent_is_human, ":dead_agent"),	# Just makes sure it's not a horse, would not exclude troops of different skin types
			
			(agent_get_party_id, ":dead_agent_party", ":dead_agent"),
			(agent_get_party_id, ":killer_agent_party", ":killer_agent"),
			
			(try_begin),
				(eq, ":wounded", 1),
				
				(this_or_next|eq, ":killer_agent_party", "p_main_party"),
				(agent_slot_eq, ":killer_agent", undead_slot_agent_afflicted_by_war, 1), # account for team kills from War's effects
				(neq, ":dead_agent_party", "p_main_party"),
				
				(agent_get_troop_id, ":troop", ":dead_agent"),
				(party_add_prisoners, "p_recruitable_undead", ":troop", 1),
			(else_try),
				(agent_get_troop_id, ":killer_troop", ":killer_agent"),
				(neq, ":killer_troop", "trp_horseman_famine"),
				
				(this_or_next|eq, ":killer_agent_party", "p_main_party"),
				(agent_slot_eq, ":killer_agent", undead_slot_agent_afflicted_by_war, 1), # account for team kills from War's effects
				(neq, ":dead_agent_party", "p_main_party"),
				
				#(display_message, "@Processing dead enemy"),
				
				(try_begin),
					# If troop killed by player or horseman, make undead troop recruitable
					(this_or_next|eq, ":killer_troop", "trp_player"),
					(this_or_next|is_between, ":killer_troop", four_horsemen_begin, four_horsemen_end),
					(agent_slot_eq, ":killer_agent", undead_slot_agent_afflicted_by_war, 1),
					
					(agent_get_troop_id, ":troop", ":dead_agent"),
					(troop_get_slot, ":undead", ":troop", undead_slot_troop_undead),
					(party_add_members, "p_recruitable_undead", ":undead", 1),
					
					#(str_store_troop_name, s0, ":undead"),
					#(display_message, "@Adding {s0}"),
				(else_try),
					# Otherwise make skeleton or ghoul recruitable
					(store_random_in_range, ":rand", 0, 2),
					(eq, ":rand", 0),
					
					(party_add_members, "p_recruitable_undead", "trp_skeleton_footman", 1),
					#(display_message, "@Adding skeleton"),
				(else_try),
					(party_add_members, "p_recruitable_undead", "trp_ghoul", 1),
					#(display_message, "@Adding ghoul"),
				(try_end),
				(assign, "$undead_recruitable", 1),
			(try_end),
		(try_end),
	])

horseman_effect_triggers = [
	
	# Initialise some variables
	(ti_before_mission_start, 0, 0, [],
	[
		(assign, "$enemies_unafflicted_by_war", 0),
		
		(assign, "$pestilence_agent", 0),
		(assign, "$war_agent", 0),
		(assign, "$famine_agent", 0),
		(assign, "$death_agent", 0),
		
		(assign, "$war_kills", 0),
		(assign, "$war_wounded", 0),
	]),
	
	# Set global variables for the agent ID of each horseman (and initialise enemy unafflicted by War count)
	(ti_on_agent_spawn, 0, 0, [],
	[
		(store_trigger_param, ":agent", 1),
		
		(try_begin),
			(agent_is_human, ":agent"),
			
			(agent_get_troop_id, ":troop_type", ":agent"),
			(try_begin),
				(eq, ":troop_type", "trp_horseman_pestilence"),
				
				(assign, "$pestilence_agent", ":agent"),
			(else_try),
				(eq, ":troop_type", "trp_horseman_war"),
				
				(assign, "$war_agent", ":agent"),
				(try_for_agents, ":agent"),
					(agent_is_human, ":agent"),
					(agent_get_team, ":agent_team", ":agent"),
					(agent_get_team, ":war_team", "$war_agent"),
					(teams_are_enemies, ":agent_team", ":war_team"),
					
					(val_add, "$enemies_unafflicted_by_war", 1),
				(try_end),
			(else_try),
				(gt, "$war_agent", 0),
				(agent_get_team, ":agent_team", ":agent"),
				(agent_get_team, ":war_team", "$war_agent"),
				(teams_are_enemies, ":agent_team", ":war_team"),
				
				(val_add, "$enemies_unafflicted_by_war", 1),
			(else_try),
				(eq, ":troop_type", "trp_horseman_famine"),
				
				(assign, "$famine_agent", ":agent"),
			(else_try),
				(eq, ":troop_type", "trp_horseman_death"),
				
				(assign, "$death_agent", ":agent"),
			(try_end),
		(try_end),
	]),
	
	# Make enemies struck by Death discontinue living
	(ti_on_agent_hit, 0, 0, [],
	[
		(store_trigger_param, ":hit_agent", 1),
		(store_trigger_param, ":attacking_agent", 2),
		
		(try_begin),
			(gt, "$death_agent", 0),
			(eq, ":attacking_agent", "$death_agent"),
			
			(agent_set_hit_points, ":hit_agent", 1, 1),
			(set_trigger_result, 1),
		(try_end),
	]),
	
	# Make enemies struck by Pestilence become afflicted with draining health
	(ti_on_agent_hit, 0, 0, [],
	[
		(store_trigger_param, ":hit_agent", 1),
		(store_trigger_param, ":attacking_agent", 2),
		(store_trigger_param, ":raw_damage", 4),
		(store_trigger_param, ":weapon", 6),
		
		(try_begin),
			(gt, "$pestilence_agent", 0),
			(eq, ":attacking_agent", "$pestilence_agent"),
			
			# Display message about affliction
			#(try_begin),
			#	(agent_slot_eq, ":hit_agent", undead_slot_agent_afflicted_by_pestilence, 0),
			#	
			#	(agent_get_troop_id, ":hit_troop", ":hit_agent"),
			#	(str_store_troop_name, s0, ":hit_troop"),
			#	(display_message, "@{s0} afflicted with pestilence"),
			#(try_end),
			
			# Set affliction
			(assign, "$pestilence_agent", ":attacking_agent"),
			(agent_set_slot, ":hit_agent", undead_slot_agent_afflicted_by_pestilence, 1),
			
			#(assign, reg0, ":weapon"),
			#(display_message, "@Weapon: {reg0}"),
			
			# If no weapon used, this "hit" was a health drain from proximity to Pestilence, so use raw damage to prevent damage reduction due to armour
			(eq, ":weapon", -1),
			(set_trigger_result, ":raw_damage"),
		(try_end),
	]),
	
	# Make enemies struck by War turn on their allies
	(ti_on_agent_hit, 0, 0, [],
	[
		(store_trigger_param, ":hit_agent", 1),
		(store_trigger_param, ":attacking_agent", 2),
		
		(try_begin),
			(gt, "$war_agent", 0),
			#(get_player_agent_no, ":player_agent"),
			#(this_or_next|eq, ":attacking_agent", ":player_agent"),	# For easy testing
			(eq, ":attacking_agent", "$war_agent"),
			(gt, "$enemies_unafflicted_by_war", 1),
			(agent_slot_eq, ":hit_agent", undead_slot_agent_afflicted_by_war, 0),
			
			# Make the agent friendly to all on War's team and hostile to all of War's enemies
			(agent_get_team, ":war_team", "$war_agent"),
			(get_player_agent_no, ":player_agent"),
			(try_for_agents, ":agent"),
				(agent_is_human, ":agent"),
				
				(try_begin),
					(agent_get_team, ":agent_team", ":agent"),
					(teams_are_enemies, ":agent_team", ":war_team"),
					
					(agent_add_relation_with_agent, ":hit_agent", ":agent", -1),
				(else_try),
					(neq, ":agent", ":player_agent"),
					
					(agent_add_relation_with_agent, ":hit_agent", ":agent", 1),
				(try_end),
			(try_end),
			
			(agent_force_rethink, ":hit_agent"),
			
			# Mark the agent as afflicted by war and set damage dealt by War's blow to 0
			(agent_set_slot, ":hit_agent", undead_slot_agent_afflicted_by_war, 1),
			(val_sub, "$enemies_unafflicted_by_war", 1),
			(set_trigger_result, 0),
		(try_end),
	]),
	
	# Let War gain XP for troops killed thanks to its affliction
	(ti_on_agent_killed_or_wounded, 0, 0, [],
	[
		(store_trigger_param, ":dead_agent", 1),
		(store_trigger_param, ":killer_agent", 2),
		(store_trigger_param, ":wounded", 3),
		
		(try_begin),
			(gt, "$war_agent", 0),
			(agent_is_human, ":dead_agent"),
			
			(agent_get_team, ":dead_agent_team", ":dead_agent"),
			(agent_get_team, ":killer_agent_team", ":killer_agent"),
			(agent_get_team, ":war_team", "$war_agent"),
			
			(assign, ":war_gets_xp", 0),
			(try_begin),
				# Afflicted enemy kills another enemy
				(agent_slot_eq, ":killer_agent", undead_slot_agent_afflicted_by_war, 1),
				(teams_are_enemies, ":dead_agent_team", ":war_team"),
				
				(assign, ":war_gets_xp", 1),
			(else_try),
				# Enemy has to kill an afflicted enemy
				(agent_slot_eq, ":dead_agent", undead_slot_agent_afflicted_by_war, 1),
				(teams_are_enemies, ":killer_agent_team", ":war_team"),
				
				(assign, ":war_gets_xp", 1),
			(try_end),
			
			(eq, ":war_gets_xp", 1),
			
			# Couldn't find an exact formula for XP but (level + 10)^2 / 5 seems to be a pretty good approximation
			(agent_get_troop_id, ":dead_troop", ":dead_agent"),
			(store_character_level, ":xp", ":dead_troop"),
			(val_add, ":xp", 10),
			(val_mul, ":xp", ":xp"),
			(val_div, ":xp", 5),
			
			(add_xp_to_troop, ":xp", "trp_horseman_war"),
			#(assign, reg0, ":xp"),
			#(display_message, "@War got {reg0} experience."),
			
			(try_begin),
				(eq, ":wounded", 0),
				(val_add, "$war_kills", 1),
			(else_try),
				(val_add, "$war_wounded", 1),
			(try_end),
		(try_end),
	]),
	
	# If the last enemy not afflicted by war is killed and afflicted enemies remain, switch them back to hostile with War and allies (though still hostile with each other)
	(ti_on_agent_killed_or_wounded, 0, 0, [],
	[
		(store_trigger_param, ":dead_agent", 1),
		
		(try_begin),
			(gt, "$war_agent", 0),
			(agent_is_human, ":dead_agent"),
			(agent_get_team, ":dead_agent_team", ":dead_agent"),
			(agent_get_team, ":war_team", "$war_agent"),
			(teams_are_enemies, ":dead_agent_team", ":war_team"),
			(agent_slot_eq, ":dead_agent", undead_slot_agent_afflicted_by_war, 0),
			
			(val_sub, "$enemies_unafflicted_by_war", 1),
			
			(eq, "$enemies_unafflicted_by_war", 0),
			
			(try_for_agents, ":agent"),
				(agent_slot_eq, ":agent", undead_slot_agent_afflicted_by_war, 1),
				
				# Just let them be hostile with everyone
				(try_for_agents, ":agent_2"),
					(neq, ":agent", ":agent_2"),
					(agent_add_relation_with_agent, ":agent", ":agent_2", -1),
				(try_end),
			(try_end),
		(try_end),
	]),
	
	# Ensure enemies taken down by Death are never wounded
	(ti_on_agent_killed_or_wounded, 0, 0, [],
	[
		(store_trigger_param, ":killer_agent", 2),
		(store_trigger_param, ":wounded", 3),
		
		(try_begin),
			(gt, "$death_agent", 0),
			(eq, ":wounded", 1),
			(agent_is_human, ":killer_agent"),
			(eq, ":killer_agent", "$death_agent"),
			
			(set_trigger_result, 1),
		(try_end),
	]),
	
	# Have Famine consume the enemies it kills
	(ti_on_agent_killed_or_wounded, 0, 0, [],
	[
		(store_trigger_param, ":dead_agent", 1),
		(store_trigger_param, ":killer_agent", 2),
		(store_trigger_param, ":wounded", 3),
		
		(try_begin),
			(gt, "$famine_agent", 0),
			(eq, ":wounded", 0),
			(agent_is_human, ":dead_agent"),
			(eq, ":killer_agent", "$famine_agent"),
			
			(call_script, "script_famine_consume_agent", ":dead_agent"),
		(try_end),
	]),
	
	# Every 2 seconds, enemies close to pestilence lose health depending on how close they are
	#(2, 0, 0, [],
	#[
	#	(try_for_agents, ":agent"),
	#		(gt, "$pestilence_agent", 0),
	#		(agent_get_team, ":agent_team", ":agent"),
	#		(agent_get_team, ":pestilence_team", "$pestilence_agent"),
	#		(teams_are_enemies, ":agent_team", ":pestilence_team"),
	#		
	#		(agent_get_position, pos1, ":agent"),
	#		(agent_get_position, pos2, "$pestilence_agent"),
	#		(get_distance_between_positions, ":distance", pos1, pos2),
	#		(val_max, ":distance", 1),	# Avoid division by 0
	#		
	#		(store_character_level, ":level", "trp_horseman_pestilence"),
	#		(val_mul, ":level", 50),
	#		
	#		(store_add, ":damage", 1000, ":level"),
	#		(val_div, ":damage", ":distance"),
	#		(gt, ":damage", 0),
	#		
	#		(store_agent_hit_points, ":hp", ":agent", 1),
	#		(try_begin),
	#			(le, ":hp", 2),
	#			
	#			(agent_deliver_damage_to_agent, "$pestilence_agent", ":agent", ":damage"),
	#		(else_try),
	#			(val_sub, ":hp", ":damage"),
	#			(agent_set_hit_points, ":agent", ":hp", 1),
	#		(try_end),
	#	(try_end),
	#]),
	
	# Every second, enemies struck by pestilence lose health
	(1, 0, 0, [],
	[
		(try_for_agents, ":agent"),
			(agent_slot_eq, ":agent", undead_slot_agent_afflicted_by_pestilence, 1),
			
			(store_agent_hit_points, ":hp", ":agent", 1),
			(try_begin),
				(le, ":hp", 2),
				
				(agent_deliver_damage_to_agent, "$pestilence_agent", ":agent", 2),
			(else_try),
				(val_sub, ":hp", 2),
				(agent_set_hit_points, ":agent", ":hp", 1),
			(try_end),
		(try_end),
	]),
	
	# Every second, enemies within a certain radius of Death drop dead
	#(1, 0, 0, [],
	#[
	#	(try_begin),
	#		(gt, "$death_agent", 0),
	#		(neg|agent_is_wounded, "$death_agent"),
	#		
	#		(agent_get_position, pos1, "$death_agent"),
	#		(agent_get_team, ":death_team", "$death_agent"),
	#		(store_character_level, ":death_radius", "trp_horseman_death"),
	#		(val_mul, ":death_radius", 3),
	#		
	#		(try_for_agents, ":agent"),
	#			(agent_get_team, ":agent_team", ":agent"),
	#			(teams_are_enemies, ":agent_team", ":death_team"),
	#			
	#			(agent_get_position, pos2, ":agent"),
	#			(get_distance_between_positions, ":distance", pos1, pos2),
	#			(lt, ":distance", ":death_radius"),
	#			
	#			(agent_deliver_damage_to_agent, "$death_agent", ":agent", 1),
	#		(try_end),
	#	(try_end),
	#]),
	
	# Every 3 seconds, pestilence is transmitted by afflicted enemies to those close to them
	(3, 0, 0, [],
	[
		(try_for_agents, ":agent"),
			(gt, "$pestilence_agent", 0),
			
			(agent_is_human, ":agent"),
			(agent_is_alive, ":agent"),
			(neg|agent_is_wounded, ":agent"),
			(agent_slot_eq, ":agent", undead_slot_agent_afflicted_by_pestilence, 1),
			
			(agent_get_team, ":agent_team", ":agent"),
			(agent_get_position, pos1, ":agent"),
			
			(try_for_agents, ":other_agent"),
				(agent_is_human, ":other_agent"),
				(agent_is_alive, ":other_agent"),
				(neg|agent_is_wounded, ":other_agent"),
				(agent_slot_eq, ":other_agent", undead_slot_agent_afflicted_by_pestilence, 0),
				
				# Only transmit to agents on the same team or an allied team
				(agent_get_team, ":other_agent_team", ":other_agent"),
				(neg|teams_are_enemies, ":agent_team", ":other_agent_team"),
				
				# Only transmit to agents within a radius of 150
				(agent_get_position, pos2, ":other_agent"),
				(get_distance_between_positions, ":distance", pos1, pos2),
				(lt, ":distance", 150),
				
				(agent_set_slot, ":other_agent", undead_slot_agent_afflicted_by_pestilence, 1),
				
				#(agent_get_troop_id, reg0, ":agent"),
				#(agent_get_troop_id, reg1, ":other_agent"),
				
				#(str_store_troop_name, s0, reg0),
				#(str_store_troop_name, s1, reg1),
				#(display_message, "@Pestilence transmitted from {s0} to {s1}"),
			(try_end),
		(try_end),
	]),
]

def modmerge(var_set):
	try:
		var_name_1 = "mission_templates"
		orig_mission_templates = var_set[var_name_1]
		
		templates = collections.OrderedDict()
		for template_tuple in orig_mission_templates:
			templates[template_tuple[0]] = MissionTemplate(*template_tuple)
		
		for template_id in templates:
			template = templates[template_id]
			if template.has_flag(mtf_battle_mode): 
				template.triggers.append(process_casualty)
				template.triggers.extend(horseman_effect_triggers)
		
		del orig_mission_templates[:]
		for template_id in templates:
			orig_mission_templates.append(templates[template_id].convert_to_tuple())
			
	except KeyError:
			errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
			raise ValueError(errstring)