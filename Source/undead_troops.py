from header_troops import *
from header_skills import *
from ID_factions import *
from ID_items import *
from module_constants import *

TROOP_ID = 0
TROOP_NAME = 1
TROOP_PLURAL_NAME = 2
TROOP_FLAGS = 3
TROOP_SCENE = 4
TROOP_RESERVED = 5
TROOP_FACTION = 6
TROOP_INVENTORY = 7
TROOP_ATTRIBUTES = 8
TROOP_WEAPON_PROFICIENCIES = 9
TROOP_SKILLS = 10
TROOP_FACE_CODE_1 = 11
TROOP_FACE_CODE_2 = 12
TROOP_IMAGE = 13

undead_face1	= 0x00000000002000000000000000000000
undead_face2	= 0x000000000020010000001fffffffffff

knows_common = knows_riding_1|knows_trade_2|knows_inventory_management_2|knows_prisoner_management_1|knows_leadership_1
def_attrib = str_7 | agi_5 | int_4 | cha_4

ghouls_and_skellies = [
	["ghoul", "Ghoul", "Ghoul", tf_undead|tf_allways_fall_dead, no_scene, 0, fac_undeads,
	[itm_pickaxe_hand],
	str_21|agi_8|level(6), wp(120), knows_athletics_1|knows_power_draw_3|knows_power_strike_2|knows_ironflesh_10, 0, 0],
	["skeleton", "Skeleton", "Skeleton", tf_skeleton|tf_allways_fall_dead|tf_guarantee_ranged, no_scene, 0, fac_undeads,
	[itm_pickaxe_hand],
	str_6|agi_30|level(16), wp(120), knows_athletics_10|knows_power_draw_3|knows_power_strike_3|knows_ironflesh_8, 0, 0],
	["ghoul_warrior", "Ghoul Warrior", "Ghoul Warriors", tf_undead|tf_allways_fall_dead|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves, no_scene, 0, fac_undeads,
	[itm_scythe, itm_military_sickle_a, itm_military_cleaver_b, itm_military_scythe, itm_awlpike, itm_shield_heater_c, itm_leather_gloves, itm_leather_boots, itm_leather_armor, itm_leather_jacket, itm_leather_vest, itm_light_leather],
	str_25|agi_8|level(9), wp(120), knows_athletics_1|knows_power_strike_4|knows_ironflesh_10, 0, 0],
	["ghoul_crusher", "Ghoul Crusher", "Ghoul Crushers", tf_undead|tf_allways_fall_dead|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves, no_scene, 0, fac_undeads,
	[itm_nordic_armor, itm_mail_with_tunic_red, itm_mail_coat, itm_byrnie, itm_nordic_footman_helmet, itm_nordic_archer_helmet, itm_sarranid_helmet1, itm_sarranid_horseman_helmet, itm_morningstar, itm_scimitar, itm_scimitar_b, itm_great_sword, itm_arabian_sword_d, itm_axe, itm_voulge, itm_bardiche, itm_shield_heater_c, itm_steel_shield, itm_leather_covered_round_shield, itm_leather_boots, itm_mail_boots],
	str_30|agi_12|level(12), wp(160), knows_athletics_1|knows_power_strike_6|knows_ironflesh_10, 0, 0],
	["ghoul_hunter", "Ghoul Hunter", "Ghoul Hunter", tf_undead|tf_allways_fall_dead|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves|tf_guarantee_shield, no_scene, 0, fac_undeads,
	[itm_fur_hat, itm_mail_hauberk, itm_byrnie, itm_haubergeon, itm_mail_boots, itm_sword_medieval_d_long, itm_steel_shield, itm_throwing_axes, itm_light_throwing_axes, itm_heavy_throwing_axes],
	str_35|agi_20|level(15), wpe(190,190,190,300), knows_athletics_10|knows_power_throw_8|knows_power_strike_8|knows_ironflesh_10, 0, 0],
	["ghoul_hulk", "Ghoul Destoryer", "Ghoul Destoryer", tf_undead|tf_allways_fall_dead|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves, no_scene, 0, fac_undeads,
	[itm_helm07, itm_spak_coat_of_plates_a, itm_spak_black_boots, itm_spak_black_gauntlets, itm_2double_axe],
	str_50|agi_5|level(19), wp(200), knows_athletics_1|knows_power_strike_9|knows_ironflesh_10, 0, 0],
	["skeleton_footman", "Skeleton Footman", "Skeleton Footman", tf_skeleton|tf_allways_fall_dead|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves|tf_guarantee_shield, no_scene, 0, fac_undeads,
	[itm_ashwood_pike, itm_military_scythe, itm_spear, itm_glaive, itm_scythe, itm_battle_fork, itm_nordic_shield, itm_wooden_shield, itm_fur_covered_shield],
	str_12|agi_30|level(18), wp(120), knows_riding_2|knows_athletics_10|knows_shield_3|knows_power_draw_3|knows_power_strike_4|knows_ironflesh_10, 0, 0],
	["skeleton_infantry", "Skeleton Infantry", "Skeleton Infantry", tf_skeleton|tf_allways_fall_dead|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves|tf_guarantee_shield, no_scene, 0, fac_undeads,
	[itm_ashwood_pike, itm_military_scythe, itm_spear, itm_glaive, itm_scythe, itm_battle_fork, itm_nordic_shield, itm_wooden_shield, itm_fur_covered_shield, itm_nordic_fighter_helmet],
	str_12|agi_30|level(18), wp(140), knows_riding_4|knows_athletics_10|knows_shield_7|knows_power_draw_3|knows_power_strike_6|knows_ironflesh_10, 0, 0],
	["skeleton_rider", "War Rider", "War Riders", tf_skeleton|tf_allways_fall_dead|tf_mounted|tf_guarantee_all_wo_ranged, no_scene, 0, fac_undeads,
	[itm_zombi_horse, itm_zombi_horse2, itm_mail_shirt, itm_pickaxe_hand, itm_sp_shr1, itm_mail_mittens, itm_iron_greaves, itm_2kettle_hat_new],
	str_15|agi_30|level(18), wp(140), knows_riding_5|knows_athletics_10|knows_shield_5|knows_power_draw_3|knows_power_strike_6|knows_ironflesh_10, 0, 0],
	["skeleton_heavy_infantry", "Skeleton Heavy Infantry", "Skeleton Heavy Infantrys", tf_skeleton|tf_allways_fall_dead|tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_helmet|tf_guarantee_gloves|tf_guarantee_shield, no_scene, 0, fac_undeads,
	[itm_ashwood_pike, itm_military_scythe, itm_spear, itm_glaive, itm_scythe, itm_battle_fork, itm_nordic_shield, itm_wooden_shield, itm_fur_covered_shield, itm_nordic_fighter_helmet],
	str_20|agi_30|level(25), wp(140), knows_riding_4|knows_athletics_10|knows_shield_10|knows_power_draw_3|knows_power_strike_8|knows_ironflesh_10, 0, 0],
	["skeleton_horseman", "Death Rider", "Death Rider", tf_skeleton|tf_allways_fall_dead|tf_mounted|tf_guarantee_all_wo_ranged, no_scene, 0, fac_undeads,
	[itm_nibbler, itm_2kettle_hat_new, itm_shb2, itm_lightedge_spak, itm_mail_mittens, itm_iron_greaves, itm_byrnie, itm_mail_hauberk, itm_mail_shirt],
	str_19|agi_30|level(24), wp(180), knows_riding_7|knows_athletics_10|knows_shield_5|knows_power_draw_3|knows_power_strike_8|knows_ironflesh_10, 0, 0],
	["skeleton_knight", "Black Knight", "Black Knight", tf_undead|tf_allways_fall_dead|tf_mounted|tf_guarantee_all_wo_ranged, no_scene, 0, fac_undeads,
	[itm_riper, itm_spak_coat_of_plates_b, itm_plate_boots3, itm_gauntlets, itm_sp_helm1, itm_sp_2hsw, itm_sp_shr1],
	str_24|agi_30|level(30), wp(210), knows_riding_9|knows_athletics_10|knows_shield_5|knows_power_draw_3|knows_power_strike_10|knows_ironflesh_10, 0, 0],
	["skeleton_death_knight", "Demon Knight", "Demon Knight", tf_undead|tf_allways_fall_dead|tf_mounted|tf_guarantee_all_wo_ranged, no_scene, 0, fac_undeads,
	[itm_heavy_riper, itm_glowing_helmet, itm_glowing_armor, itm_demonic_boots, itm_demonic_gauntlets, itm_spak_iceaxe, itm_spider_shield2],
	str_35|agi_30|level(40), wp(270), knows_riding_10|knows_athletics_10|knows_shield_9|knows_power_draw_3|knows_power_strike_10|knows_ironflesh_10, 0, 0]
]

def modmerge(var_set):
	try:
		var_name_1 = "troops"
		orig_troops = var_set[var_name_1]
		
		undead_troops = []
		
		for troop in orig_troops[find_troop(orig_troops, soldiers_begin[len("trp_"):]):find_troop(orig_troops, soldiers_end[len("trp_"):])]:
			if (troop[TROOP_FLAGS] & tf_hero) != tf_hero and (troop[TROOP_FLAGS] & tf_undead) != tf_undead:
				undead_troop = list(troop[TROOP_ID:TROOP_IMAGE])
				undead_troop[TROOP_FLAGS] = (troop[TROOP_FLAGS] & (troop[TROOP_FLAGS] ^ troop_type_mask)) | tf_undead | tf_allways_fall_dead | tf_guarantee_gloves
				#undead_troop[TROOP_FLAGS] = (troop[TROOP_FLAGS] & (tf_guarantee_ranged | tf_guarantee_horse | tf_mounted | tf_guarantee_shield)) | tf_undead | tf_allways_fall_dead | tf_guarantee_gloves
				undead_troop[TROOP_ID] = "undead_" + troop[TROOP_ID]
				undead_troop[TROOP_NAME] = "Undead " + troop[TROOP_NAME]
				undead_troop[TROOP_PLURAL_NAME] = "Undead " + troop[TROOP_PLURAL_NAME]
				undead_troop[TROOP_FACTION] = fac_undeads
				undead_troop[TROOP_INVENTORY].append(itm_leather_gloves)
				undead_troop[TROOP_FACE_CODE_1] = undead_face1
				undead_troop[TROOP_FACE_CODE_2] = undead_face2
				undead_troops.append(undead_troop)
		
		undead_horsemen = [
			["horseman_pestilence", "Pestilence", "Pestilence", tf_hero|tf_undead|tf_guarantee_horse|tf_mounted, 0, reserved, fac_undeads, [itm_crowned_helm, itm_courtly_outfit, itm_leather_boots, itm_leather_gloves, itm_khergit_bow, itm_arrows, itm_courser], level(5)|str_12|agi_9|int_10|cha_6, wp(90), knows_ironflesh_4|knows_riding_4|knows_power_draw_3|knows_horse_archery_4|knows_weapon_master_4|knows_wound_treatment_3, 0],
			["horseman_war", "War", "War", tf_hero|tf_undead|tf_guarantee_horse|tf_mounted, 0, reserved, fac_undeads, [itm_mail_with_surcoat, itm_gauntlets, itm_sword_of_war, itm_war_bow, itm_bodkin_arrows, itm_hunter], level(10)|str_15|agi_9|int_12|cha_6, wp(120), knows_ironflesh_4|knows_riding_4|knows_power_strike_4|knows_power_draw_4|knows_horse_archery_4|knows_weapon_master_4|knows_tactics_5, 0],
			["horseman_famine", "Famine", "Famine", tf_hero|tf_undead|tf_guarantee_horse|tf_mounted, 0, reserved, fac_undeads, [itm_shirt, itm_leather_gloves, itm_butchering_knife, itm_saddle_horse], level(15)|def_attrib, wp(60), knows_riding_4|knows_trade_10|knows_inventory_management_10, 0],
			["horseman_death", "Death", "Death", tf_hero|tf_undead|tf_guarantee_horse|tf_mounted, 0, reserved, fac_undeads, [itm_robe, itm_black_hood, itm_leather_gloves, itm_scythe, itm_sickle, itm_sumpter_horse], level(20)|str_12|agi_18|int_16|cha_6, wp(150), knows_riding_4|knows_ironflesh_4|knows_athletics_10|knows_weapon_master_10|knows_power_draw_5|knows_horse_archery_5|knows_tracking_10, 0],
			["four_horsemen_end", "{!}Four Horsemen End", "{!}Four Horsemen End", tf_hero|tf_undead, 0, reserved,	fac_neutral, [], 0, 0, 0, 0]
		]
		
		#skeletons = [
		#	["skeleton_infantry", "Skeleton", "Skeletons", tf_skeleton|tf_allways_fall_dead, 0, 0, fac_undeads,	[],	str_15|agi_21|level(16), wp(120), knows_ironflesh_8|knows_power_strike_2|knows_athletics_10, undead_face1, undead_face2],
		#	["skeleton_archer", "Skeleton Archer", "Skeleton Archers", tf_skeleton|tf_allways_fall_dead|tf_guarantee_ranged, 0, 0, fac_undeads,	[],	str_6|agi_30|level(16), wp(120), knows_ironflesh_8|knows_power_draw_5|knows_athletics_10, undead_face1, undead_face2],
		#	["skeleton_cavalry", "Skeleton Horseman", "Skeleton Horsemen", tf_skeleton|tf_allways_fall_dead|tf_guarantee_horse|tf_mounted, 0, 0, fac_undeads, [itm_skeletal_horse], str_6|agi_30|level(16), wp(120), knows_ironflesh_8|knows_power_strike_2|knows_athletics_5|knows_riding_5, undead_face1, undead_face2],
		#	["skeleton_horse_archer", "Skeleton Horse Archer", "Skeleton Horse Archers", tf_skeleton|tf_allways_fall_dead|tf_guarantee_horse|tf_guarantee_ranged|tf_mounted, 0, 0, fac_undeads, [itm_skeletal_horse], str_6|agi_30|level(16), wp(120), knows_ironflesh_6|knows_power_draw_5|knows_athletics_4|knows_riding_4|knows_horse_archery_4, undead_face1, undead_face2],
		#]
		
		orig_troops.extend(undead_troops)
		orig_troops.extend(undead_horsemen)
		orig_troops.extend(ghouls_and_skellies)
		#orig_troops.extend(skeletons)
		orig_troops.append(["game_load_check", "{!}Game Load Check", "{!}Game Load Check", tf_hero|tf_inactive, 0, reserved, fac_neutral, [], 0, 0, knows_inventory_management_10, 0])
		
		upgrade(orig_troops, "ghoul", "ghoul_warrior")
		upgrade(orig_troops, "skeleton", "skeleton_footman")
		upgrade(orig_troops, "ghoul_warrior", "ghoul_crusher")
		upgrade2(orig_troops, "ghoul_crusher", "ghoul_hulk", "ghoul_hunter")
		upgrade(orig_troops, "skeleton_footman", "skeleton_infantry")
		upgrade2(orig_troops, "skeleton_infantry", "skeleton_heavy_infantry", "skeleton_rider")
		upgrade(orig_troops, "skeleton_rider", "skeleton_horseman")
		upgrade(orig_troops, "skeleton_horseman", "skeleton_knight")
		upgrade(orig_troops, "skeleton_knight", "skeleton_death_knight")
		
	except KeyError:
			errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
			raise ValueError(errstring)
