from header_common import *
from header_game_menus import *
from header_game_menus_class import *
from header_operations import *
from header_troops import *
from header_items import *
from module_constants import *

def modmerge(var_set):
	try:
		var_name_1 = "game_menus"
		orig_menus = var_set[var_name_1]
		
		menus = collections.OrderedDict()
		for menu_tuple in orig_menus:
			menus[menu_tuple[0]] = Menu(*menu_tuple)
		
		menus["start_game_0"].text = "Welcome to Undead Calradia. In this mod, you play an undead necromancer of mysterious origins who shows up in the land of Calradia, ready to bring all the land under your rule.\
		Those who fall before you soon rise back up as loyal members of your army, so every battle has the potential to end with your forces being even stronger than when you started. As time goes on, you may also find\
		mysterious figures join your party with peculiar abilities."
		menus["start_game_0"].options["continue"].consequences = [
			(set_show_messages, 0),
			
			(troop_set_type, "trp_player", tf_undead),
			(troop_raise_attribute, "trp_player", ca_strength, 5),
			(troop_raise_attribute, "trp_player", ca_agility, 5),
			(troop_raise_attribute, "trp_player", ca_intelligence, 2),
			(troop_raise_attribute, "trp_player", ca_charisma, 2),
			
			(troop_raise_skill, "trp_player", "skl_leadership", 1),
			(troop_raise_skill, "trp_player", "skl_riding", 1),
			
			(try_for_range, ":proficiency", wpt_one_handed_weapon, wpt_firearm),
				(troop_raise_proficiency_linear, "trp_player", ":proficiency", 45),
			(try_end),
			
			(troop_add_item, "trp_player", "itm_red_gambeson", imod_plain),
			(troop_add_item, "trp_player", "itm_leather_boots", imod_plain),
			(troop_add_item, "trp_player", "itm_sword_medieval_a", imod_plain),
			(troop_add_item, "trp_player", "itm_tab_shield_round_a", imod_battered),
			(troop_add_item, "trp_player", "itm_saddle_horse", imod_plain),
			
			(assign, "$current_town", "p_town_6"),
			(assign, "$g_starting_town", "$current_town"),
			(party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
			
			(set_show_messages, 1),
			
			(change_screen_return, 0),
		]
		
		menus["start_phase_2"].text = "You arrive near the town of Praven, ready to begin your conquest."
		for option_id in menus["start_phase_2"].options.keys():
			del menus["start_phase_2"].options[option_id]
		menus["start_phase_2"].options["continue"] = MenuOption("continue", [], "Continue...", [(change_screen_return, 0)])
		
		del menus["village"].options["recruit_volunteers"]
		
		index = menus["total_victory"].operations.index((party_get_num_companions, ":num_rescued_prisoners", "p_temp_party"))
		menus["total_victory"].operations[index:index+5] = [
			(eq, "$undead_recruitable", 1),
			#(call_script, "script_party_prisoners_add_party_prisoners", "p_recruitable_undead", "p_temp_party"),
			(change_screen_exchange_with_party, "p_recruitable_undead"),
		]
		
		menus["battle_debrief"].text += "^^Kill count:{s12}"
		menus["battle_debrief"].operations.extend([
			(call_script, "script_print_kill_count_to_s0"),
			(str_store_string_reg, s12, s0),
		])
		
		#menus["battle_debrief"].options["continue"].consequences[0:0] = [(change_screen_exchange_with_party, "p_recruitable_undead")]
		
		menus["village_hostile_action"].options["village_slaughter"] = MenuOption("village_slaughter",
		[
			(call_script, "script_party_count_members_with_full_health", "p_main_party"),
			(assign, ":player_party_size", reg0),
			(call_script, "script_party_count_members_with_full_health", "$current_town"),
			(assign, ":villagers_party_size", reg0),
			
			(gt, ":player_party_size", 0),
			(gt, ":villagers_party_size", 0),
		],
		"Slaughter the peasants for your army",
		[
			(jump_to_menu, "mnu_village_slaughter_confirm"),
		])
		menus["village_hostile_action"].move_option_to_end("forget_it")
		
		menus["village_slaughter_confirm"] = Menu(
			"village_slaughter_confirm",mnf_disable_all_keys|mnf_scale_picture,
			"{s5} has {reg5} inhabitant{reg6?s:} remaining.^^You have {reg10} troops against {reg11} defenders.^^Are you sure you want to continue?",
			"none",
			[
				(str_store_party_name, s5, "$current_town"),
				
				(assign, "$g_enemy_party", "$current_town"),
				(call_script, "script_encounter_calculate_fit"),
				(call_script, "script_party_count_members_with_full_health", "$current_town"),
				(assign, reg5, reg0),
				(store_sub, reg6, reg5, 1),
				
				(set_background_mesh, "mesh_pic_villageriot"),
				
				(try_begin),
					(eq, "$g_battle_result", 1),
					
					(call_script, "script_change_player_relation_with_center", "$current_town", -15),
					(party_get_slot, ":town_lord", "$current_town", slot_town_lord),
					(try_begin),
						(gt, ":town_lord", 0),
						
						(call_script, "script_change_player_relation_with_troop", ":town_lord", -5),
					(try_end),
					
					(eq, "$undead_recruitable", 1),
					
					(assign, "$undead_recruitable", 0),
					(jump_to_menu, "mnu_camp"),
					(change_screen_exchange_with_party, "p_recruitable_undead"),
				(else_try),
					(eq, "$g_battle_result", -1),
					
					(jump_to_menu, "mnu_village_loot_defeat"),
				(else_try),
					(eq, reg5, 0),
					
					(change_screen_return),
				(try_end),
			],
			[
				("village_slaughter_yes",[],"Yes, charge them.",
				[
					(call_script, "script_change_player_relation_with_center", "$current_town", -25),
					
					(try_begin),
						(party_get_slot, ":town_lord", "$current_town", slot_town_lord),
						(gt, ":town_lord", 0),
						
						(call_script, "script_change_player_relation_with_troop", ":town_lord", -5),
					(try_end),
					
					(call_script, "script_calculate_battle_advantage"),
					(set_battle_advantage, reg0),
					(set_party_battle_mode),
					(assign, "$g_battle_result", 0),
					(assign, "$g_village_raid_evil", 1),
					(set_jump_mission,"mt_village_raid"),
					(party_get_slot, ":scene_to_use", "$current_town", slot_castle_exterior),
					(jump_to_scene, ":scene_to_use"),
					(assign, "$g_next_menu", "mnu_village_slaughter_confirm"),

					(call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$g_encountered_party"),
					###NPC companion changes begin
					(call_script, "script_objectionable_action", tmt_humanitarian, "str_loot_village"),
					#NPC companion changes end

					(jump_to_menu, "mnu_battle_debrief"),
					(change_screen_mission),
				]),
				("village_slaughter_no",[],"No, leave this village alone.",[(change_screen_return)]),
			],
		)
		
		del orig_menus[:]
		for menu_id in menus:
			orig_menus.append(menus[menu_id].convert_to_tuple())
		
		#print var_name_1
		
	except KeyError:
			errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
			raise ValueError(errstring)