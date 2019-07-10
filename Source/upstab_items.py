import collections

from header_items import *

####################################################################################################################
#  Each item record contains the following fields:
#  1) Item id: used for referencing items in other files.
#     The prefix itm_ is automatically added before each item id.
#  2) Item name. Name of item as it'll appear in inventory window
#  3) List of meshes.  Each mesh record is a tuple containing the following fields:
#    3.1) Mesh name.
#    3.2) Modifier bits that this mesh matches.
#     Note that the first mesh record is the default.
#  4) Item flags. See header_items.py for a list of available flags.
#  5) Item capabilities. Used for which animations this item is used with. See header_items.py for a list of available flags.
#  6) Item value.
#  7) Item stats: Bitwise-or of various stats about the item such as:
#      weight, abundance, difficulty, head_armor, body_armor,leg_armor, etc...
#  8) Modifier bits: Modifiers that can be applied to this item.
#  9) [Optional] Triggers: List of simple triggers to be associated with the item.
#  10) [Optional] Factions: List of factions that item can be found as merchandise.
####################################################################################################################

class Item:
  def __init__(self, id, name = "", meshes = [], flags = 0, capabilities = 0, value = 0, stats = 0, modbits = 0, triggers = [], factions = []):
    self.id = id
    self.name = name
    self.meshes = meshes
    self.flags = flags
    self.capabilities = capabilities
    self.value = value
    
    self.stats = {}
    self.stats["weight"] = get_weight(stats)
    self.stats["head_armor"] = get_head_armor(stats)
    self.stats["body_armor"] = get_body_armor(stats)
    self.stats["leg_armor"] = get_leg_armor(stats)
    self.stats["difficulty"] = get_difficulty(stats)
    self.stats["hit_points"] = get_hit_points(stats)
    self.stats["max_ammo"] = get_max_ammo(stats)
    self.stats["abundance"] = get_abundance(stats)
    
    swing_damage_bits = get_swing_damage(stats)
    self.stats["swing_damage"] = swing_damage_bits & 0xff
    self.stats["swing_damage_type"] = swing_damage_bits >> iwf_damage_type_bits
    
    if self.get_type() == itp_type_horse:
      self.stats["horse_scale"] = get_weapon_length(stats)
      self.stats["horse_speed"] = get_missile_speed(stats)
      self.stats["horse_maneuver"] = get_speed_rating(stats)
      self.stats["horse_charge"] = get_thrust_damage(stats)
    else:
      self.stats["speed_rating"] = get_speed_rating(stats)
      thrust_damage_bits = get_thrust_damage(stats)
      self.stats["thrust_damage"] = thrust_damage_bits & 0xff
      self.stats["thrust_damage_type"] = thrust_damage_bits >> iwf_damage_type_bits
      if self.get_type() == itp_type_shield:
        self.stats["shield_width"] = get_weapon_length(stats)
        self.stats["shield_height"] = get_missile_speed(stats)
      else:
        self.stats["weapon_length"] = get_weapon_length(stats)
        self.stats["missile_speed"] = get_missile_speed(stats)
    
    self.modbits = modbits
    self.triggers = triggers
    self.factions = factions
  
  def convert_to_list(self):
    item_list = []
    item_list.append(self.id)
    item_list.append(self.name)
    item_list.append(self.meshes)
    item_list.append(self.flags)
    item_list.append(self.capabilities)
    item_list.append(self.value)
    
    stats = 0
    stats |= weight(self.stats["weight"])
    stats |= head_armor(self.stats["head_armor"])
    stats |= body_armor(self.stats["body_armor"])
    stats |= leg_armor(self.stats["leg_armor"])
    stats |= difficulty(self.stats["difficulty"])
    stats |= hit_points(self.stats["hit_points"])
    stats |= max_ammo(self.stats["max_ammo"])
    stats |= swing_damage(self.stats["swing_damage"], self.stats["swing_damage_type"])
    stats |= abundance(self.stats["abundance"])
    
    if self.get_type() == itp_type_horse:
      stats |= horse_scale(self.stats["horse_scale"])
      stats |= horse_speed(self.stats["horse_speed"])
      stats |= horse_maneuver(self.stats["horse_maneuver"])
      stats |= horse_charge(self.stats["horse_charge"])
    else:
      stats |= spd_rtng(self.stats["speed_rating"])
      stats |= thrust_damage(self.stats["thrust_damage"], self.stats["thrust_damage_type"])
      if self.get_type() == itp_type_shield:
        stats |= shield_width(self.stats["shield_width"])
        stats |= shield_height(self.stats["shield_height"])
      else:
        stats |= weapon_length(self.stats["weapon_length"])
        stats |= shoot_speed(self.stats["missile_speed"])
    
    item_list.append(stats)
    
    item_list.append(self.modbits)
    item_list.append(self.triggers)
    item_list.append(self.factions)
    
    return item_list
  
  def has_flag(self, flag):
    return (self.flags & flag) == flag
  
  def add_flag(self, flag):
    self.flags |= flag
  
  def remove_flag(self, flag):
    if self.has_flag(flag):
      self.flags ^= flag
  
  def get_type(self):
    return self.flags & 0xff
  
  def has_capability(self, capability):
    return (self.capabilities & capability) == capability
  
  def add_capability(self, capability):
    self.capabilities |= capability
  
  def remove_capability(self, capability):
    if self.has_capability(capability):
      self.capabilities ^= capability

def modmerge(var_set):
  try:
    var_name_1 = "items"
    orig_items = var_set[var_name_1]
    
    items = collections.OrderedDict()
    for item_list in orig_items:
      if item_list[0] not in items:
        items[item_list[0]] = Item(*item_list)
    
    for item_id in items:
      item = items[item_id]
      if item.has_capability(itc_pike):
        item.remove_capability(itcf_overswing_polearm)
        
        item.add_capability(itc_parry_polearm)
        item.add_capability(itcf_overswing_spear)
        item.add_capability(itcf_overswing_musket)
        
        item.add_flag(itp_is_pike)
        item.add_flag(itp_has_upper_stab)
        item.add_flag(itp_no_blur)
    
    del orig_items[:]
    for item_id in items:
      orig_items.append(items[item_id].convert_to_list())
      
  except KeyError:
      errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
      raise ValueError(errstring)