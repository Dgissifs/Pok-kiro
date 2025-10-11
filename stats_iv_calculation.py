import random
import math
from pokémon import NATURE_EFFECTS
def calculate_official_stats(base_stats, ivs, level, nature, evs=None):
    if evs is None:
        evs = {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0}
    nature_lower = nature.lower()
    nature_multipliers = NATURE_EFFECTS.get(nature_lower, {})
    calculated_stats = {}
    for stat_name in ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]:
        base = base_stats.get(stat_name, 50)
        iv = ivs.get(stat_name, 0)
        ev = evs.get(stat_name, 0)
        if stat_name == "hp":
            stat_value = math.floor(((2 * base + iv + math.floor(ev / 4)) * level) / 100) + level + 10
        else:
            stat_value = math.floor(((2 * base + iv + math.floor(ev / 4)) * level) / 100) + 5
            if stat_name in nature_multipliers:
                stat_value = math.floor(stat_value * nature_multipliers[stat_name])
        calculated_stats[stat_name] = stat_value
    return calculated_stats
def calculate_iv_percentage(ivs):
    total_ivs = sum(ivs.values())
    iv_percentage = round((total_ivs / 186) * 100, 2)
    return iv_percentage
def generate_pokemon_ivs():
    return {
        "hp": random.randint(0, 31),
        "attack": random.randint(0, 31),
        "defense": random.randint(0, 31),
        "sp_attack": random.randint(0, 31),
        "sp_defense": random.randint(0, 31),
        "speed": random.randint(0, 31)
    }
def get_stat_range(base_stat, level, nature_multiplier=1.0):
    min_hp = math.floor(((2 * base_stat + 0 + 0) * level) / 100) + level + 10
    min_other = math.floor(((2 * base_stat + 0 + 0) * level) / 100) + 5
    max_hp = math.floor(((2 * base_stat + 31 + 63) * level) / 100) + level + 10
    max_other = math.floor(((2 * base_stat + 31 + 63) * level) / 100) + 5
    if base_stat == "hp":
        return min_hp, max_hp
    else:
        min_stat = math.floor(min_other * nature_multiplier)
        max_stat = math.floor(max_other * nature_multiplier)
        return min_stat, max_stat