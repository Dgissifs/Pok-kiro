import random
import math
NATURE_EFFECTS = {
    "hardy": {},
    "lonely": {"attack": 1.1, "defense": 0.9},
    "brave": {"attack": 1.1, "speed": 0.9},
    "adamant": {"attack": 1.1, "sp_attack": 0.9},
    "naughty": {"attack": 1.1, "sp_defense": 0.9},
    "bold": {"defense": 1.1, "attack": 0.9},
    "docile": {},
    "relaxed": {"defense": 1.1, "speed": 0.9},
    "impish": {"defense": 1.1, "sp_attack": 0.9},
    "lax": {"defense": 1.1, "sp_defense": 0.9},
    "timid": {"speed": 1.1, "attack": 0.9},
    "hasty": {"speed": 1.1, "defense": 0.9},
    "serious": {},
    "jolly": {"speed": 1.1, "sp_attack": 0.9},
    "naive": {"speed": 1.1, "sp_defense": 0.9},
    "modest": {"sp_attack": 1.1, "attack": 0.9},
    "mild": {"sp_attack": 1.1, "defense": 0.9},
    "quiet": {"sp_attack": 1.1, "speed": 0.9},
    "bashful": {},
    "rash": {"sp_attack": 1.1, "sp_defense": 0.9},
    "calm": {"sp_defense": 1.1, "attack": 0.9},
    "gentle": {"sp_defense": 1.1, "defense": 0.9},
    "sassy": {"sp_defense": 1.1, "speed": 0.9},
    "careful": {"sp_defense": 1.1, "sp_attack": 0.9},
    "quirky": {}
}
NATURES = [
    "Hardy", "Lonely", "Brave", "Adamant", "Naughty",
    "Bold", "Docile", "Relaxed", "Impish", "Lax",
    "Timid", "Hasty", "Serious", "Jolly", "Naive",
    "Modest", "Mild", "Quiet", "Bashful", "Rash",
    "Calm", "Gentle", "Sassy", "Careful", "Quirky"
]
POKEMON_GEN1 = [
    {
        "name": "Bulbasaur",
        "base_stats": {"hp": 45, "attack": 49, "defense": 49, "sp_attack": 65, "sp_defense": 65, "speed": 45},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Chlorophyll"]
    },
    {
        "name": "Ivysaur",
        "base_stats": {"hp": 60, "attack": 62, "defense": 63, "sp_attack": 80, "sp_defense": 80, "speed": 60},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Chlorophyll"]
    },
    {
        "name": "Venusaur",
        "base_stats": {"hp": 80, "attack": 82, "defense": 83, "sp_attack": 100, "sp_defense": 100, "speed": 80},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Chlorophyll"]
    },
    {
        "name": "Charmander",
        "base_stats": {"hp": 39, "attack": 52, "defense": 43, "sp_attack": 60, "sp_defense": 50, "speed": 65},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Solar Power"]
    },
    {
        "name": "Charmeleon",
        "base_stats": {"hp": 58, "attack": 64, "defense": 58, "sp_attack": 80, "sp_defense": 65, "speed": 80},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Solar Power"]
    },
    {
        "name": "Charizard",
        "base_stats": {"hp": 78, "attack": 84, "defense": 78, "sp_attack": 109, "sp_defense": 85, "speed": 100},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Solar Power"]
    },
    {
        "name": "Squirtle",
        "base_stats": {"hp": 44, "attack": 48, "defense": 65, "sp_attack": 50, "sp_defense": 64, "speed": 43},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Rain Dish"]
    },
    {
        "name": "Wartortle",
        "base_stats": {"hp": 59, "attack": 63, "defense": 80, "sp_attack": 65, "sp_defense": 80, "speed": 58},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Rain Dish"]
    },
    {
        "name": "Blastoise",
        "base_stats": {"hp": 79, "attack": 83, "defense": 100, "sp_attack": 85, "sp_defense": 105, "speed": 78},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Rain Dish"]
    },
    {
        "name": "Caterpie",
        "base_stats": {"hp": 45, "attack": 30, "defense": 35, "sp_attack": 20, "sp_defense": 20, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shield Dust"],
        "hidden_abilities": ["Run Away"]
    },
    {
        "name": "Metapod",
        "base_stats": {"hp": 50, "attack": 20, "defense": 55, "sp_attack": 25, "sp_defense": 25, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shed Skin"],
        "hidden_abilities": []
    },
    {
        "name": "Butterfree",
        "base_stats": {"hp": 60, "attack": 45, "defense": 50, "sp_attack": 90, "sp_defense": 80, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Compound Eyes"],
        "hidden_abilities": ["Tinted Lens"]
    },
    {
        "name": "Weedle",
        "base_stats": {"hp": 40, "attack": 35, "defense": 30, "sp_attack": 20, "sp_defense": 20, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shield Dust"],
        "hidden_abilities": ["Run Away"]
    },
    {
        "name": "Kakuna",
        "base_stats": {"hp": 45, "attack": 25, "defense": 50, "sp_attack": 25, "sp_defense": 25, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shed Skin"],
        "hidden_abilities": []
    },
    {
        "name": "Beedrill",
        "base_stats": {"hp": 65, "attack": 90, "defense": 40, "sp_attack": 45, "sp_defense": 80, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm"],
        "hidden_abilities": ["Sniper"]
    },
    {
        "name": "Pidgey",
        "base_stats": {"hp": 40, "attack": 45, "defense": 40, "sp_attack": 35, "sp_defense": 35, "speed": 56},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Tangled Feet"],
        "hidden_abilities": ["Big Pecks"]
    },
    {
        "name": "Pidgeotto",
        "base_stats": {"hp": 63, "attack": 60, "defense": 55, "sp_attack": 50, "sp_defense": 50, "speed": 71},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Tangled Feet"],
        "hidden_abilities": ["Big Pecks"]
    },
    {
        "name": "Pidgeot",
        "base_stats": {"hp": 83, "attack": 80, "defense": 75, "sp_attack": 70, "sp_defense": 70, "speed": 101},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Tangled Feet"],
        "hidden_abilities": ["Big Pecks"]
    },
    {
        "name": "Rattata",
        "base_stats": {"hp": 30, "attack": 56, "defense": 35, "sp_attack": 25, "sp_defense": 35, "speed": 72},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Guts"],
        "hidden_abilities": ["Hustle"]
    },
    {
        "name": "Raticate",
        "base_stats": {"hp": 55, "attack": 81, "defense": 60, "sp_attack": 50, "sp_defense": 70, "speed": 97},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Guts"],
        "hidden_abilities": ["Hustle"]
    },
    {
        "name": "Spearow",
        "base_stats": {"hp": 40, "attack": 60, "defense": 30, "sp_attack": 31, "sp_defense": 31, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye"],
        "hidden_abilities": ["Sniper"]
    },
    {
        "name": "Fearow",
        "base_stats": {"hp": 65, "attack": 90, "defense": 65, "sp_attack": 61, "sp_defense": 61, "speed": 100},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye"],
        "hidden_abilities": ["Sniper"]
    },
    {
        "name": "Ekans",
        "base_stats": {"hp": 35, "attack": 60, "defense": 44, "sp_attack": 40, "sp_defense": 54, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate", "Shed Skin"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Arbok",
        "base_stats": {"hp": 60, "attack": 95, "defense": 69, "sp_attack": 65, "sp_defense": 79, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate", "Shed Skin"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Pikachu",
        "base_stats": {"hp": 35, "attack": 55, "defense": 40, "sp_attack": 50, "sp_defense": 50, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Static"],
        "hidden_abilities": ["Lightning Rod"]
    },
    {
        "name": "Raichu",
        "base_stats": {"hp": 60, "attack": 90, "defense": 55, "sp_attack": 90, "sp_defense": 80, "speed": 110},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Static"],
        "hidden_abilities": ["Lightning Rod"]
    },
    {
        "name": "Sandshrew",
        "base_stats": {"hp": 50, "attack": 75, "defense": 85, "sp_attack": 20, "sp_defense": 30, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Veil"],
        "hidden_abilities": ["Sand Rush"]
    },
    {
        "name": "Sandslash",
        "base_stats": {"hp": 75, "attack": 100, "defense": 110, "sp_attack": 45, "sp_defense": 55, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Veil"],
        "hidden_abilities": ["Sand Rush"]
    },
    {
        "name": "Nidoran♀",
        "base_stats": {"hp": 55, "attack": 47, "defense": 52, "sp_attack": 40, "sp_defense": 40, "speed": 41},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Poison Point", "Rivalry"],
        "hidden_abilities": ["Hustle"]
    },
    {
        "name": "Nidorina",
        "base_stats": {"hp": 70, "attack": 62, "defense": 67, "sp_attack": 55, "sp_defense": 55, "speed": 56},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Poison Point", "Rivalry"],
        "hidden_abilities": ["Hustle"]
    },
    {
        "name": "Nidoqueen",
        "base_stats": {"hp": 90, "attack": 92, "defense": 87, "sp_attack": 75, "sp_defense": 85, "speed": 76},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Poison Point", "Rivalry"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Nidoran♂",
        "base_stats": {"hp": 46, "attack": 57, "defense": 40, "sp_attack": 40, "sp_defense": 40, "speed": 50},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Poison Point", "Rivalry"],
        "hidden_abilities": ["Hustle"]
    },
    {
        "name": "Nidorino",
        "base_stats": {"hp": 61, "attack": 72, "defense": 57, "sp_attack": 55, "sp_defense": 55, "speed": 65},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Poison Point", "Rivalry"],
        "hidden_abilities": ["Hustle"]
    },
    {
        "name": "Nidoking",
        "base_stats": {"hp": 81, "attack": 102, "defense": 77, "sp_attack": 85, "sp_defense": 75, "speed": 85},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Poison Point", "Rivalry"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Clefairy",
        "base_stats": {"hp": 70, "attack": 45, "defense": 48, "sp_attack": 60, "sp_defense": 65, "speed": 35},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Cute Charm", "Magic Guard"],
        "hidden_abilities": ["Friend Guard"]
    },
    {
        "name": "Clefable",
        "base_stats": {"hp": 95, "attack": 70, "defense": 73, "sp_attack": 95, "sp_defense": 90, "speed": 60},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Cute Charm", "Magic Guard"],
        "hidden_abilities": ["Unaware"]
    },
    {
        "name": "Vulpix",
        "base_stats": {"hp": 38, "attack": 41, "defense": 40, "sp_attack": 50, "sp_defense": 65, "speed": 65},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Flash Fire"],
        "hidden_abilities": ["Drought"]
    },
    {
        "name": "Ninetales",
        "base_stats": {"hp": 73, "attack": 76, "defense": 75, "sp_attack": 81, "sp_defense": 100, "speed": 100},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Flash Fire"],
        "hidden_abilities": ["Drought"]
    },
    {
        "name": "Jigglypuff",
        "base_stats": {"hp": 115, "attack": 45, "defense": 20, "sp_attack": 45, "sp_defense": 25, "speed": 20},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Cute Charm", "Competitive"],
        "hidden_abilities": ["Friend Guard"]
    },
    {
        "name": "Wigglytuff",
        "base_stats": {"hp": 140, "attack": 70, "defense": 45, "sp_attack": 85, "sp_defense": 50, "speed": 45},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Cute Charm", "Competitive"],
        "hidden_abilities": ["Frisk"]
    },
    {
        "name": "Zubat",
        "base_stats": {"hp": 40, "attack": 45, "defense": 35, "sp_attack": 30, "sp_defense": 40, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Inner Focus"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Golbat",
        "base_stats": {"hp": 75, "attack": 80, "defense": 70, "sp_attack": 65, "sp_defense": 75, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Inner Focus"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Oddish",
        "base_stats": {"hp": 45, "attack": 50, "defense": 55, "sp_attack": 75, "sp_defense": 65, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll"],
        "hidden_abilities": ["Run Away"]
    },
    {
        "name": "Gloom",
        "base_stats": {"hp": 60, "attack": 65, "defense": 70, "sp_attack": 85, "sp_defense": 75, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll"],
        "hidden_abilities": ["Stench"]
    },
    {
        "name": "Vileplume",
        "base_stats": {"hp": 75, "attack": 80, "defense": 85, "sp_attack": 110, "sp_defense": 90, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll"],
        "hidden_abilities": ["Effect Spore"]
    },
    {
        "name": "Paras",
        "base_stats": {"hp": 35, "attack": 70, "defense": 55, "sp_attack": 45, "sp_defense": 55, "speed": 25},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Effect Spore", "Dry Skin"],
        "hidden_abilities": ["Damp"]
    },
    {
        "name": "Parasect",
        "base_stats": {"hp": 60, "attack": 95, "defense": 80, "sp_attack": 60, "sp_defense": 80, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Effect Spore", "Dry Skin"],
        "hidden_abilities": ["Damp"]
    },
    {
        "name": "Venonat",
        "base_stats": {"hp": 60, "attack": 55, "defense": 50, "sp_attack": 40, "sp_defense": 55, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Compound Eyes", "Tinted Lens"],
        "hidden_abilities": ["Run Away"]
    },
    {
        "name": "Venomoth",
        "base_stats": {"hp": 70, "attack": 65, "defense": 60, "sp_attack": 90, "sp_defense": 75, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shield Dust", "Tinted Lens"],
        "hidden_abilities": ["Wonder Skin"]
    },
    {
        "name": "Diglett",
        "base_stats": {"hp": 10, "attack": 55, "defense": 25, "sp_attack": 35, "sp_defense": 45, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Veil", "Arena Trap"],
        "hidden_abilities": ["Sand Force"]
    },
    {
        "name": "Dugtrio",
        "base_stats": {"hp": 35, "attack": 100, "defense": 50, "sp_attack": 50, "sp_defense": 70, "speed": 120},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Veil", "Arena Trap"],
        "hidden_abilities": ["Sand Force"]
    },
    {
        "name": "Meowth",
        "base_stats": {"hp": 40, "attack": 45, "defense": 35, "sp_attack": 40, "sp_defense": 40, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pickup", "Technician"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Persian",
        "base_stats": {"hp": 65, "attack": 70, "defense": 60, "sp_attack": 65, "sp_defense": 65, "speed": 115},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Limber", "Technician"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Psyduck",
        "base_stats": {"hp": 50, "attack": 52, "defense": 48, "sp_attack": 65, "sp_defense": 50, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Damp", "Cloud Nine"],
        "hidden_abilities": ["Swift Swim"]
    },
    {
        "name": "Golduck",
        "base_stats": {"hp": 80, "attack": 82, "defense": 78, "sp_attack": 95, "sp_defense": 80, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Damp", "Cloud Nine"],
        "hidden_abilities": ["Swift Swim"]
    },
    {
        "name": "Mankey",
        "base_stats": {"hp": 40, "attack": 80, "defense": 35, "sp_attack": 35, "sp_defense": 45, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Vital Spirit", "Anger Point"],
        "hidden_abilities": ["Defiant"]
    },
    {
        "name": "Primeape",
        "base_stats": {"hp": 65, "attack": 105, "defense": 60, "sp_attack": 60, "sp_defense": 70, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Vital Spirit", "Anger Point"],
        "hidden_abilities": ["Defiant"]
    },
    {
        "name": "Growlithe",
        "base_stats": {"hp": 55, "attack": 70, "defense": 45, "sp_attack": 70, "sp_defense": 50, "speed": 60},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Intimidate", "Flash Fire"],
        "hidden_abilities": ["Justified"]
    },
    {
        "name": "Arcanine",
        "base_stats": {"hp": 90, "attack": 110, "defense": 80, "sp_attack": 100, "sp_defense": 80, "speed": 95},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Intimidate", "Flash Fire"],
        "hidden_abilities": ["Justified"]
    },
    {
        "name": "Poliwag",
        "base_stats": {"hp": 40, "attack": 50, "defense": 40, "sp_attack": 40, "sp_defense": 40, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Absorb", "Damp"],
        "hidden_abilities": ["Swift Swim"]
    },
    {
        "name": "Poliwhirl",
        "base_stats": {"hp": 65, "attack": 65, "defense": 65, "sp_attack": 50, "sp_defense": 50, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Absorb", "Damp"],
        "hidden_abilities": ["Swift Swim"]
    },
    {
        "name": "Poliwrath",
        "base_stats": {"hp": 90, "attack": 95, "defense": 95, "sp_attack": 70, "sp_defense": 90, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Absorb", "Damp"],
        "hidden_abilities": ["Swift Swim"]
    },
    {
        "name": "Abra",
        "base_stats": {"hp": 25, "attack": 20, "defense": 15, "sp_attack": 105, "sp_defense": 55, "speed": 90},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Synchronize", "Inner Focus"],
        "hidden_abilities": ["Magic Guard"]
    },
    {
        "name": "Kadabra",
        "base_stats": {"hp": 40, "attack": 35, "defense": 30, "sp_attack": 120, "sp_defense": 70, "speed": 105},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Synchronize", "Inner Focus"],
        "hidden_abilities": ["Magic Guard"]
    },
    {
        "name": "Alakazam",
        "base_stats": {"hp": 55, "attack": 50, "defense": 45, "sp_attack": 135, "sp_defense": 95, "speed": 120},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Synchronize", "Inner Focus"],
        "hidden_abilities": ["Magic Guard"]
    },
    {
        "name": "Machop",
        "base_stats": {"hp": 70, "attack": 80, "defense": 50, "sp_attack": 35, "sp_defense": 35, "speed": 35},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Guts", "No Guard"],
        "hidden_abilities": ["Steadfast"]
    },
    {
        "name": "Machoke",
        "base_stats": {"hp": 80, "attack": 100, "defense": 70, "sp_attack": 50, "sp_defense": 60, "speed": 45},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Guts", "No Guard"],
        "hidden_abilities": ["Steadfast"]
    },
    {
        "name": "Machamp",
        "base_stats": {"hp": 90, "attack": 130, "defense": 80, "sp_attack": 65, "sp_defense": 85, "speed": 55},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Guts", "No Guard"],
        "hidden_abilities": ["Steadfast"]
    },
    {
        "name": "Bellsprout",
        "base_stats": {"hp": 50, "attack": 75, "defense": 35, "sp_attack": 70, "sp_defense": 30, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll"],
        "hidden_abilities": ["Gluttony"]
    },
    {
        "name": "Weepinbell",
        "base_stats": {"hp": 65, "attack": 90, "defense": 50, "sp_attack": 85, "sp_defense": 45, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll"],
        "hidden_abilities": ["Gluttony"]
    },
    {
        "name": "Victreebel",
        "base_stats": {"hp": 80, "attack": 105, "defense": 65, "sp_attack": 100, "sp_defense": 70, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll"],
        "hidden_abilities": ["Gluttony"]
    },
    {
        "name": "Tentacool",
        "base_stats": {"hp": 40, "attack": 40, "defense": 35, "sp_attack": 50, "sp_defense": 100, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Clear Body", "Liquid Ooze"],
        "hidden_abilities": ["Rain Dish"]
    },
    {
        "name": "Tentacruel",
        "base_stats": {"hp": 80, "attack": 70, "defense": 65, "sp_attack": 80, "sp_defense": 120, "speed": 100},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Clear Body", "Liquid Ooze"],
        "hidden_abilities": ["Rain Dish"]
    },
    {
        "name": "Geodude",
        "base_stats": {"hp": 40, "attack": 80, "defense": 100, "sp_attack": 30, "sp_defense": 30, "speed": 20},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rock Head", "Sturdy"],
        "hidden_abilities": ["Sand Veil"]
    },
    {
        "name": "Graveler",
        "base_stats": {"hp": 55, "attack": 95, "defense": 115, "sp_attack": 45, "sp_defense": 45, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rock Head", "Sturdy"],
        "hidden_abilities": ["Sand Veil"]
    },
    {
        "name": "Golem",
        "base_stats": {"hp": 80, "attack": 120, "defense": 130, "sp_attack": 55, "sp_defense": 65, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rock Head", "Sturdy"],
        "hidden_abilities": ["Sand Veil"]
    },
    {
        "name": "Ponyta",
        "base_stats": {"hp": 50, "attack": 85, "defense": 55, "sp_attack": 65, "sp_defense": 65, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Flash Fire"],
        "hidden_abilities": ["Flame Body"]
    },
    {
        "name": "Rapidash",
        "base_stats": {"hp": 65, "attack": 100, "defense": 70, "sp_attack": 80, "sp_defense": 80, "speed": 105},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Flash Fire"],
        "hidden_abilities": ["Flame Body"]
    },
    {
        "name": "Slowpoke",
        "base_stats": {"hp": 90, "attack": 65, "defense": 65, "sp_attack": 40, "sp_defense": 40, "speed": 15},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Oblivious", "Own Tempo"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Slowbro",
        "base_stats": {"hp": 95, "attack": 75, "defense": 110, "sp_attack": 100, "sp_defense": 80, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Oblivious", "Own Tempo"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Magnemite",
        "base_stats": {"hp": 25, "attack": 35, "defense": 70, "sp_attack": 95, "sp_defense": 55, "speed": 45},
        "gender_ratio": None,
        "abilities": ["Magnet Pull", "Sturdy"],
        "hidden_abilities": ["Analytic"]
    },
    {
        "name": "Magneton",
        "base_stats": {"hp": 50, "attack": 60, "defense": 95, "sp_attack": 120, "sp_defense": 70, "speed": 70},
        "gender_ratio": None,
        "abilities": ["Magnet Pull", "Sturdy"],
        "hidden_abilities": ["Analytic"]
    },
    {
        "name": "Farfetch'd",
        "base_stats": {"hp": 52, "attack": 90, "defense": 55, "sp_attack": 58, "sp_defense": 62, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Inner Focus"],
        "hidden_abilities": ["Defiant"]
    },
    {
        "name": "Doduo",
        "base_stats": {"hp": 35, "attack": 85, "defense": 45, "sp_attack": 35, "sp_defense": 35, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Early Bird"],
        "hidden_abilities": ["Tangled Feet"]
    },
    {
        "name": "Dodrio",
        "base_stats": {"hp": 60, "attack": 110, "defense": 70, "sp_attack": 60, "sp_defense": 60, "speed": 110},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Early Bird"],
        "hidden_abilities": ["Tangled Feet"]
    },
    {
        "name": "Seel",
        "base_stats": {"hp": 65, "attack": 45, "defense": 55, "sp_attack": 45, "sp_defense": 70, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Thick Fat", "Hydration"],
        "hidden_abilities": ["Ice Body"]
    },
    {
        "name": "Dewgong",
        "base_stats": {"hp": 90, "attack": 70, "defense": 80, "sp_attack": 70, "sp_defense": 95, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Thick Fat", "Hydration"],
        "hidden_abilities": ["Ice Body"]
    },
    {
        "name": "Grimer",
        "base_stats": {"hp": 80, "attack": 80, "defense": 50, "sp_attack": 40, "sp_defense": 50, "speed": 25},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Stench", "Sticky Hold"],
        "hidden_abilities": ["Poison Touch"]
    },
    {
        "name": "Muk",
        "base_stats": {"hp": 105, "attack": 105, "defense": 75, "sp_attack": 65, "sp_defense": 100, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Stench", "Sticky Hold"],
        "hidden_abilities": ["Poison Touch"]
    },
    {
        "name": "Shellder",
        "base_stats": {"hp": 30, "attack": 65, "defense": 100, "sp_attack": 45, "sp_defense": 25, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shell Armor", "Skill Link"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Cloyster",
        "base_stats": {"hp": 50, "attack": 95, "defense": 180, "sp_attack": 85, "sp_defense": 45, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shell Armor", "Skill Link"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Gastly",
        "base_stats": {"hp": 30, "attack": 35, "defense": 30, "sp_attack": 100, "sp_defense": 35, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Haunter",
        "base_stats": {"hp": 45, "attack": 50, "defense": 45, "sp_attack": 115, "sp_defense": 55, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Gengar",
        "base_stats": {"hp": 60, "attack": 65, "defense": 60, "sp_attack": 130, "sp_defense": 75, "speed": 110},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Cursed Body"],
        "hidden_abilities": []
    },
    {
        "name": "Onix",
        "base_stats": {"hp": 35, "attack": 45, "defense": 160, "sp_attack": 30, "sp_defense": 45, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rock Head", "Sturdy"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Drowzee",
        "base_stats": {"hp": 60, "attack": 48, "defense": 45, "sp_attack": 43, "sp_defense": 90, "speed": 42},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Insomnia", "Forewarn"],
        "hidden_abilities": ["Inner Focus"]
    },
    {
        "name": "Hypno",
        "base_stats": {"hp": 85, "attack": 73, "defense": 70, "sp_attack": 73, "sp_defense": 115, "speed": 67},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Insomnia", "Forewarn"],
        "hidden_abilities": ["Inner Focus"]
    },
    {
        "name": "Krabby",
        "base_stats": {"hp": 30, "attack": 105, "defense": 90, "sp_attack": 25, "sp_defense": 25, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hyper Cutter", "Shell Armor"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Kingler",
        "base_stats": {"hp": 55, "attack": 130, "defense": 115, "sp_attack": 50, "sp_defense": 50, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hyper Cutter", "Shell Armor"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Voltorb",
        "base_stats": {"hp": 40, "attack": 30, "defense": 50, "sp_attack": 55, "sp_defense": 55, "speed": 100},
        "gender_ratio": None,
        "abilities": ["Soundproof", "Static"],
        "hidden_abilities": ["Aftermath"]
    },
    {
        "name": "Electrode",
        "base_stats": {"hp": 60, "attack": 50, "defense": 70, "sp_attack": 80, "sp_defense": 80, "speed": 150},
        "gender_ratio": None,
        "abilities": ["Soundproof", "Static"],
        "hidden_abilities": ["Aftermath"]
    },
    {
        "name": "Exeggcute",
        "base_stats": {"hp": 60, "attack": 40, "defense": 80, "sp_attack": 60, "sp_defense": 45, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll"],
        "hidden_abilities": ["Harvest"]
    },
    {
        "name": "Exeggutor",
        "base_stats": {"hp": 95, "attack": 95, "defense": 85, "sp_attack": 125, "sp_defense": 75, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll"],
        "hidden_abilities": ["Harvest"]
    },
    {
        "name": "Cubone",
        "base_stats": {"hp": 50, "attack": 50, "defense": 95, "sp_attack": 40, "sp_defense": 50, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rock Head", "Lightning Rod"],
        "hidden_abilities": ["Battle Armor"]
    },
    {
        "name": "Marowak",
        "base_stats": {"hp": 60, "attack": 80, "defense": 110, "sp_attack": 50, "sp_defense": 80, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rock Head", "Lightning Rod"],
        "hidden_abilities": ["Battle Armor"]
    },
    {
        "name": "Hitmonlee",
        "base_stats": {"hp": 50, "attack": 120, "defense": 53, "sp_attack": 35, "sp_defense": 110, "speed": 87},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Limber", "Reckless"],
        "hidden_abilities": ["Unburden"]
    },
    {
        "name": "Hitmonchan",
        "base_stats": {"hp": 50, "attack": 105, "defense": 79, "sp_attack": 35, "sp_defense": 110, "speed": 76},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Keen Eye", "Iron Fist"],
        "hidden_abilities": ["Inner Focus"]
    },
    {
        "name": "Lickitung",
        "base_stats": {"hp": 90, "attack": 55, "defense": 75, "sp_attack": 60, "sp_defense": 75, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Own Tempo", "Oblivious"],
        "hidden_abilities": ["Cloud Nine"]
    },
    {
        "name": "Koffing",
        "base_stats": {"hp": 40, "attack": 65, "defense": 95, "sp_attack": 60, "sp_defense": 45, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Weezing",
        "base_stats": {"hp": 65, "attack": 90, "defense": 120, "sp_attack": 85, "sp_defense": 70, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Rhyhorn",
        "base_stats": {"hp": 80, "attack": 85, "defense": 95, "sp_attack": 30, "sp_defense": 30, "speed": 25},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Lightning Rod", "Rock Head"],
        "hidden_abilities": ["Reckless"]
    },
    {
        "name": "Rhydon",
        "base_stats": {"hp": 105, "attack": 130, "defense": 120, "sp_attack": 45, "sp_defense": 45, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Lightning Rod", "Rock Head"],
        "hidden_abilities": ["Reckless"]
    },
    {
        "name": "Chansey",
        "base_stats": {"hp": 250, "attack": 5, "defense": 5, "sp_attack": 35, "sp_defense": 105, "speed": 50},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Natural Cure", "Serene Grace"],
        "hidden_abilities": ["Healer"]
    },
    {
        "name": "Tangela",
        "base_stats": {"hp": 65, "attack": 55, "defense": 115, "sp_attack": 100, "sp_defense": 40, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Leaf Guard"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Kangaskhan",
        "base_stats": {"hp": 105, "attack": 95, "defense": 80, "sp_attack": 40, "sp_defense": 80, "speed": 90},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Early Bird", "Scrappy"],
        "hidden_abilities": ["Inner Focus"]
    },
    {
        "name": "Horsea",
        "base_stats": {"hp": 30, "attack": 40, "defense": 70, "sp_attack": 70, "sp_defense": 25, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Sniper"],
        "hidden_abilities": ["Damp"]
    },
    {
        "name": "Seadra",
        "base_stats": {"hp": 55, "attack": 65, "defense": 95, "sp_attack": 95, "sp_defense": 45, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Poison Point", "Sniper"],
        "hidden_abilities": ["Damp"]
    },
    {
        "name": "Goldeen",
        "base_stats": {"hp": 45, "attack": 67, "defense": 60, "sp_attack": 35, "sp_defense": 50, "speed": 63},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Water Veil"],
        "hidden_abilities": ["Lightning Rod"]
    },
    {
        "name": "Seaking",
        "base_stats": {"hp": 80, "attack": 92, "defense": 65, "sp_attack": 65, "sp_defense": 80, "speed": 68},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Water Veil"],
        "hidden_abilities": ["Lightning Rod"]
    },
    {
        "name": "Staryu",
        "base_stats": {"hp": 30, "attack": 45, "defense": 55, "sp_attack": 70, "sp_defense": 55, "speed": 85},
        "gender_ratio": None,
        "abilities": ["Illuminate", "Natural Cure"],
        "hidden_abilities": ["Analytic"]
    },
    {
        "name": "Starmie",
        "base_stats": {"hp": 60, "attack": 75, "defense": 85, "sp_attack": 100, "sp_defense": 85, "speed": 115},
        "gender_ratio": None,
        "abilities": ["Illuminate", "Natural Cure"],
        "hidden_abilities": ["Analytic"]
    },
    {
        "name": "Mr. Mime",
        "base_stats": {"hp": 40, "attack": 45, "defense": 65, "sp_attack": 100, "sp_defense": 120, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Soundproof", "Filter"],
        "hidden_abilities": ["Technician"]
    },
    {
        "name": "Scyther",
        "base_stats": {"hp": 70, "attack": 110, "defense": 80, "sp_attack": 55, "sp_defense": 80, "speed": 105},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm", "Technician"],
        "hidden_abilities": ["Steadfast"]
    },
    {
        "name": "Jynx",
        "base_stats": {"hp": 65, "attack": 50, "defense": 35, "sp_attack": 115, "sp_defense": 95, "speed": 95},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Oblivious", "Forewarn"],
        "hidden_abilities": ["Dry Skin"]
    },
    {
        "name": "Electabuzz",
        "base_stats": {"hp": 65, "attack": 83, "defense": 57, "sp_attack": 95, "sp_defense": 85, "speed": 105},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Static"],
        "hidden_abilities": ["Vital Spirit"]
    },
    {
        "name": "Magmar",
        "base_stats": {"hp": 65, "attack": 95, "defense": 57, "sp_attack": 100, "sp_defense": 85, "speed": 93},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Flame Body"],
        "hidden_abilities": ["Vital Spirit"]
    },
    {
        "name": "Pinsir",
        "base_stats": {"hp": 65, "attack": 125, "defense": 100, "sp_attack": 55, "sp_defense": 70, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hyper Cutter", "Mold Breaker"],
        "hidden_abilities": ["Moxie"]
    },
    {
        "name": "Tauros",
        "base_stats": {"hp": 75, "attack": 100, "defense": 95, "sp_attack": 40, "sp_defense": 70, "speed": 110},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Intimidate", "Anger Point"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Magikarp",
        "base_stats": {"hp": 20, "attack": 10, "defense": 55, "sp_attack": 15, "sp_defense": 20, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim"],
        "hidden_abilities": ["Rattled"]
    },
    {
        "name": "Gyarados",
        "base_stats": {"hp": 95, "attack": 125, "defense": 79, "sp_attack": 60, "sp_defense": 100, "speed": 81},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate"],
        "hidden_abilities": ["Moxie"]
    },
    {
        "name": "Lapras",
        "base_stats": {"hp": 130, "attack": 85, "defense": 80, "sp_attack": 85, "sp_defense": 95, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Absorb", "Shell Armor"],
        "hidden_abilities": ["Hydration"]
    },
    {
        "name": "Ditto",
        "base_stats": {"hp": 48, "attack": 48, "defense": 48, "sp_attack": 48, "sp_defense": 48, "speed": 48},
        "gender_ratio": None,
        "abilities": ["Limber"],
        "hidden_abilities": ["Imposter"]
    },
    {
        "name": "Eevee",
        "base_stats": {"hp": 55, "attack": 55, "defense": 50, "sp_attack": 45, "sp_defense": 65, "speed": 55},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Run Away", "Adaptability"],
        "hidden_abilities": ["Anticipation"]
    },
    {
        "name": "Vaporeon",
        "base_stats": {"hp": 130, "attack": 65, "defense": 60, "sp_attack": 110, "sp_defense": 95, "speed": 65},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Water Absorb"],
        "hidden_abilities": ["Hydration"]
    },
    {
        "name": "Jolteon",
        "base_stats": {"hp": 65, "attack": 65, "defense": 60, "sp_attack": 110, "sp_defense": 95, "speed": 130},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Volt Absorb"],
        "hidden_abilities": ["Quick Feet"]
    },
    {
        "name": "Flareon",
        "base_stats": {"hp": 65, "attack": 130, "defense": 60, "sp_attack": 95, "sp_defense": 110, "speed": 65},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Flash Fire"],
        "hidden_abilities": ["Guts"]
    },
    {
        "name": "Porygon",
        "base_stats": {"hp": 65, "attack": 60, "defense": 70, "sp_attack": 85, "sp_defense": 75, "speed": 40},
        "gender_ratio": None,
        "abilities": ["Trace", "Download"],
        "hidden_abilities": ["Analytic"]
    },
    {
        "name": "Omanyte",
        "base_stats": {"hp": 35, "attack": 40, "defense": 100, "sp_attack": 90, "sp_defense": 55, "speed": 35},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Swift Swim", "Shell Armor"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Omastar",
        "base_stats": {"hp": 70, "attack": 60, "defense": 125, "sp_attack": 115, "sp_defense": 70, "speed": 55},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Swift Swim", "Shell Armor"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Kabuto",
        "base_stats": {"hp": 30, "attack": 80, "defense": 90, "sp_attack": 55, "sp_defense": 45, "speed": 55},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Swift Swim", "Battle Armor"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Kabutops",
        "base_stats": {"hp": 60, "attack": 115, "defense": 105, "sp_attack": 65, "sp_defense": 70, "speed": 80},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Swift Swim", "Battle Armor"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Aerodactyl",
        "base_stats": {"hp": 80, "attack": 105, "defense": 65, "sp_attack": 60, "sp_defense": 75, "speed": 130},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Rock Head", "Pressure"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Snorlax",
        "base_stats": {"hp": 160, "attack": 110, "defense": 65, "sp_attack": 65, "sp_defense": 110, "speed": 30},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Immunity", "Thick Fat"],
        "hidden_abilities": ["Gluttony"]
    },
    {
        "name": "Articuno",
        "base_stats": {"hp": 90, "attack": 85, "defense": 100, "sp_attack": 95, "sp_defense": 125, "speed": 85},
        "gender_ratio": None,
        "abilities": ["Pressure"],
        "hidden_abilities": ["Snow Cloak"]
    },
    {
        "name": "Zapdos",
        "base_stats": {"hp": 90, "attack": 90, "defense": 85, "sp_attack": 125, "sp_defense": 90, "speed": 100},
        "gender_ratio": None,
        "abilities": ["Pressure"],
        "hidden_abilities": ["Static"]
    },
    {
        "name": "Moltres",
        "base_stats": {"hp": 90, "attack": 100, "defense": 90, "sp_attack": 125, "sp_defense": 85, "speed": 90},
        "gender_ratio": None,
        "abilities": ["Pressure"],
        "hidden_abilities": ["Flame Body"]
    },
    {
        "name": "Dratini",
        "base_stats": {"hp": 41, "attack": 64, "defense": 45, "sp_attack": 50, "sp_defense": 50, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shed Skin"],
        "hidden_abilities": ["Marvel Scale"]
    },
    {
        "name": "Dragonair",
        "base_stats": {"hp": 61, "attack": 84, "defense": 65, "sp_attack": 70, "sp_defense": 70, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shed Skin"],
        "hidden_abilities": ["Marvel Scale"]
    },
    {
        "name": "Dragonite",
        "base_stats": {"hp": 91, "attack": 134, "defense": 95, "sp_attack": 100, "sp_defense": 100, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Inner Focus"],
        "hidden_abilities": ["Multiscale"]
    },
    {
        "name": "Mewtwo",
        "base_stats": {"hp": 106, "attack": 110, "defense": 90, "sp_attack": 154, "sp_defense": 90, "speed": 130},
        "gender_ratio": None,
        "abilities": ["Pressure"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Mew",
        "base_stats": {"hp": 100, "attack": 100, "defense": 100, "sp_attack": 100, "sp_defense": 100, "speed": 100},
        "gender_ratio": None,
        "abilities": ["Synchronize"],
        "hidden_abilities": []
    }
]
POKEMON_GEN2 = [
    {
        "name": "Chikorita",
        "base_stats": {"hp": 45, "attack": 49, "defense": 65, "sp_attack": 49, "sp_defense": 65, "speed": 45},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Leaf Guard"]
    },
    {
        "name": "Bayleef",
        "base_stats": {"hp": 60, "attack": 62, "defense": 80, "sp_attack": 63, "sp_defense": 80, "speed": 60},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Leaf Guard"]
    },
    {
        "name": "Meganium",
        "base_stats": {"hp": 80, "attack": 82, "defense": 100, "sp_attack": 83, "sp_defense": 100, "speed": 80},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Leaf Guard"]
    },
    {
        "name": "Cyndaquil",
        "base_stats": {"hp": 39, "attack": 52, "defense": 43, "sp_attack": 60, "sp_defense": 50, "speed": 65},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Flash Fire"]
    },
    {
        "name": "Quilava",
        "base_stats": {"hp": 58, "attack": 64, "defense": 58, "sp_attack": 80, "sp_defense": 65, "speed": 80},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Flash Fire"]
    },
    {
        "name": "Typhlosion",
        "base_stats": {"hp": 78, "attack": 84, "defense": 78, "sp_attack": 109, "sp_defense": 85, "speed": 100},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Flash Fire"]
    },
    {
        "name": "Totodile",
        "base_stats": {"hp": 50, "attack": 65, "defense": 64, "sp_attack": 44, "sp_defense": 48, "speed": 43},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Croconaw",
        "base_stats": {"hp": 65, "attack": 80, "defense": 80, "sp_attack": 59, "sp_defense": 63, "speed": 58},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Feraligatr",
        "base_stats": {"hp": 85, "attack": 105, "defense": 100, "sp_attack": 79, "sp_defense": 83, "speed": 78},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Sentret",
        "base_stats": {"hp": 35, "attack": 46, "defense": 34, "sp_attack": 35, "sp_defense": 45, "speed": 20},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Keen Eye"],
        "hidden_abilities": ["Frisk"]
    },
    {
        "name": "Furret",
        "base_stats": {"hp": 85, "attack": 76, "defense": 64, "sp_attack": 45, "sp_defense": 55, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Keen Eye"],
        "hidden_abilities": ["Frisk"]
    },
    {
        "name": "Hoothoot",
        "base_stats": {"hp": 60, "attack": 30, "defense": 30, "sp_attack": 36, "sp_defense": 56, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Insomnia", "Keen Eye"],
        "hidden_abilities": ["Tinted Lens"]
    },
    {
        "name": "Noctowl",
        "base_stats": {"hp": 100, "attack": 50, "defense": 50, "sp_attack": 86, "sp_defense": 96, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Insomnia", "Keen Eye"],
        "hidden_abilities": ["Tinted Lens"]
    },
    {
        "name": "Ledyba",
        "base_stats": {"hp": 40, "attack": 20, "defense": 30, "sp_attack": 40, "sp_defense": 80, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm", "Early Bird"],
        "hidden_abilities": ["Rattled"]
    },
    {
        "name": "Ledian",
        "base_stats": {"hp": 55, "attack": 35, "defense": 50, "sp_attack": 55, "sp_defense": 110, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm", "Early Bird"],
        "hidden_abilities": ["Iron Fist"]
    },
    {
        "name": "Spinarak",
        "base_stats": {"hp": 40, "attack": 60, "defense": 40, "sp_attack": 40, "sp_defense": 40, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm", "Insomnia"],
        "hidden_abilities": ["Sniper"]
    },
    {
        "name": "Ariados",
        "base_stats": {"hp": 70, "attack": 90, "defense": 70, "sp_attack": 60, "sp_defense": 70, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm", "Insomnia"],
        "hidden_abilities": ["Sniper"]
    },
    {
        "name": "Crobat",
        "base_stats": {"hp": 85, "attack": 90, "defense": 80, "sp_attack": 70, "sp_defense": 80, "speed": 130},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Inner Focus"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Chinchou",
        "base_stats": {"hp": 75, "attack": 38, "defense": 38, "sp_attack": 56, "sp_defense": 56, "speed": 67},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Volt Absorb", "Illuminate"],
        "hidden_abilities": ["Water Absorb"]
    },
    {
        "name": "Lanturn",
        "base_stats": {"hp": 125, "attack": 58, "defense": 58, "sp_attack": 76, "sp_defense": 76, "speed": 67},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Volt Absorb", "Illuminate"],
        "hidden_abilities": ["Water Absorb"]
    },
    {
        "name": "Pichu",
        "base_stats": {"hp": 20, "attack": 40, "defense": 15, "sp_attack": 35, "sp_defense": 35, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Static"],
        "hidden_abilities": ["Lightning Rod"]
    },
    {
        "name": "Cleffa",
        "base_stats": {"hp": 50, "attack": 25, "defense": 28, "sp_attack": 45, "sp_defense": 55, "speed": 15},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Cute Charm", "Magic Guard"],
        "hidden_abilities": ["Friend Guard"]
    },
    {
        "name": "Igglybuff",
        "base_stats": {"hp": 90, "attack": 30, "defense": 15, "sp_attack": 40, "sp_defense": 20, "speed": 15},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Cute Charm", "Competitive"],
        "hidden_abilities": ["Friend Guard"]
    },
    {
        "name": "Togepi",
        "base_stats": {"hp": 35, "attack": 20, "defense": 65, "sp_attack": 40, "sp_defense": 65, "speed": 20},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Hustle", "Serene Grace"],
        "hidden_abilities": ["Super Luck"]
    },
    {
        "name": "Togetic",
        "base_stats": {"hp": 55, "attack": 40, "defense": 85, "sp_attack": 80, "sp_defense": 105, "speed": 40},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Hustle", "Serene Grace"],
        "hidden_abilities": ["Super Luck"]
    },
    {
        "name": "Natu",
        "base_stats": {"hp": 40, "attack": 50, "defense": 45, "sp_attack": 70, "sp_defense": 45, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Synchronize", "Early Bird"],
        "hidden_abilities": ["Magic Bounce"]
    },
    {
        "name": "Xatu",
        "base_stats": {"hp": 65, "attack": 75, "defense": 70, "sp_attack": 95, "sp_defense": 70, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Synchronize", "Early Bird"],
        "hidden_abilities": ["Magic Bounce"]
    },
    {
        "name": "Mareep",
        "base_stats": {"hp": 55, "attack": 40, "defense": 40, "sp_attack": 65, "sp_defense": 45, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Static"],
        "hidden_abilities": ["Plus"]
    },
    {
        "name": "Flaaffy",
        "base_stats": {"hp": 70, "attack": 55, "defense": 55, "sp_attack": 80, "sp_defense": 60, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Static"],
        "hidden_abilities": ["Plus"]
    },
    {
        "name": "Ampharos",
        "base_stats": {"hp": 90, "attack": 75, "defense": 85, "sp_attack": 115, "sp_defense": 90, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Static"],
        "hidden_abilities": ["Plus"]
    },
    {
        "name": "Bellossom",
        "base_stats": {"hp": 75, "attack": 80, "defense": 95, "sp_attack": 90, "sp_defense": 100, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll"],
        "hidden_abilities": ["Healer"]
    },
    {
        "name": "Marill",
        "base_stats": {"hp": 70, "attack": 20, "defense": 50, "sp_attack": 20, "sp_defense": 50, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Thick Fat", "Huge Power"],
        "hidden_abilities": ["Sap Sipper"]
    },
    {
        "name": "Azumarill",
        "base_stats": {"hp": 100, "attack": 50, "defense": 80, "sp_attack": 60, "sp_defense": 80, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Thick Fat", "Huge Power"],
        "hidden_abilities": ["Sap Sipper"]
    },
    {
        "name": "Sudowoodo",
        "base_stats": {"hp": 70, "attack": 100, "defense": 115, "sp_attack": 30, "sp_defense": 65, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy", "Rock Head"],
        "hidden_abilities": ["Rattled"]
    },
    {
        "name": "Politoed",
        "base_stats": {"hp": 90, "attack": 75, "defense": 75, "sp_attack": 90, "sp_defense": 100, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Absorb", "Damp"],
        "hidden_abilities": ["Drizzle"]
    },
    {
        "name": "Hoppip",
        "base_stats": {"hp": 35, "attack": 35, "defense": 40, "sp_attack": 35, "sp_defense": 55, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Leaf Guard"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Skiploom",
        "base_stats": {"hp": 55, "attack": 45, "defense": 50, "sp_attack": 45, "sp_defense": 65, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Leaf Guard"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Jumpluff",
        "base_stats": {"hp": 75, "attack": 55, "defense": 70, "sp_attack": 55, "sp_defense": 95, "speed": 110},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Leaf Guard"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Aipom",
        "base_stats": {"hp": 55, "attack": 70, "defense": 55, "sp_attack": 40, "sp_defense": 55, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Pickup"],
        "hidden_abilities": ["Skill Link"]
    },
    {
        "name": "Sunkern",
        "base_stats": {"hp": 30, "attack": 30, "defense": 30, "sp_attack": 30, "sp_defense": 30, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Solar Power"],
        "hidden_abilities": ["Early Bird"]
    },
    {
        "name": "Sunflora",
        "base_stats": {"hp": 75, "attack": 75, "defense": 55, "sp_attack": 105, "sp_defense": 85, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Solar Power"],
        "hidden_abilities": ["Early Bird"]
    },
    {
        "name": "Yanma",
        "base_stats": {"hp": 65, "attack": 65, "defense": 45, "sp_attack": 75, "sp_defense": 45, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Speed Boost", "Compound Eyes"],
        "hidden_abilities": ["Frisk"]
    },
    {
        "name": "Wooper",
        "base_stats": {"hp": 55, "attack": 45, "defense": 45, "sp_attack": 25, "sp_defense": 25, "speed": 15},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Damp", "Water Absorb"],
        "hidden_abilities": ["Unaware"]
    },
    {
        "name": "Quagsire",
        "base_stats": {"hp": 95, "attack": 85, "defense": 85, "sp_attack": 65, "sp_defense": 65, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Damp", "Water Absorb"],
        "hidden_abilities": ["Unaware"]
    },
    {
        "name": "Espeon",
        "base_stats": {"hp": 65, "attack": 65, "defense": 60, "sp_attack": 130, "sp_defense": 95, "speed": 110},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Synchronize"],
        "hidden_abilities": ["Magic Bounce"]
    },
    {
        "name": "Umbreon",
        "base_stats": {"hp": 95, "attack": 65, "defense": 110, "sp_attack": 60, "sp_defense": 130, "speed": 65},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Synchronize"],
        "hidden_abilities": ["Inner Focus"]
    },
    {
        "name": "Murkrow",
        "base_stats": {"hp": 60, "attack": 85, "defense": 42, "sp_attack": 85, "sp_defense": 42, "speed": 91},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Insomnia", "Super Luck"],
        "hidden_abilities": ["Prankster"]
    },
    {
        "name": "Slowking",
        "base_stats": {"hp": 95, "attack": 75, "defense": 80, "sp_attack": 100, "sp_defense": 110, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Oblivious", "Own Tempo"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Misdreavus",
        "base_stats": {"hp": 60, "attack": 60, "defense": 60, "sp_attack": 85, "sp_defense": 85, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Unown",
        "base_stats": {"hp": 48, "attack": 72, "defense": 48, "sp_attack": 72, "sp_defense": 48, "speed": 48},
        "gender_ratio": None,
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Wobbuffet",
        "base_stats": {"hp": 190, "attack": 33, "defense": 58, "sp_attack": 33, "sp_defense": 58, "speed": 33},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shadow Tag"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Girafarig",
        "base_stats": {"hp": 70, "attack": 80, "defense": 65, "sp_attack": 90, "sp_defense": 65, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Inner Focus", "Early Bird"],
        "hidden_abilities": ["Sap Sipper"]
    },
    {
        "name": "Pineco",
        "base_stats": {"hp": 50, "attack": 65, "defense": 90, "sp_attack": 35, "sp_defense": 35, "speed": 15},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Forretress",
        "base_stats": {"hp": 75, "attack": 90, "defense": 140, "sp_attack": 60, "sp_defense": 60, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Dunsparce",
        "base_stats": {"hp": 100, "attack": 70, "defense": 70, "sp_attack": 65, "sp_defense": 65, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Serene Grace", "Run Away"],
        "hidden_abilities": ["Rattled"]
    },
    {
        "name": "Gligar",
        "base_stats": {"hp": 65, "attack": 75, "defense": 105, "sp_attack": 35, "sp_defense": 65, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hyper Cutter", "Sand Veil"],
        "hidden_abilities": ["Immunity"]
    },
    {
        "name": "Steelix",
        "base_stats": {"hp": 75, "attack": 85, "defense": 200, "sp_attack": 55, "sp_defense": 65, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rock Head", "Sturdy"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Snubbull",
        "base_stats": {"hp": 60, "attack": 80, "defense": 50, "sp_attack": 40, "sp_defense": 40, "speed": 30},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Intimidate", "Run Away"],
        "hidden_abilities": ["Rattled"]
    },
    {
        "name": "Granbull",
        "base_stats": {"hp": 90, "attack": 120, "defense": 75, "sp_attack": 60, "sp_defense": 60, "speed": 45},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Intimidate", "Quick Feet"],
        "hidden_abilities": ["Rattled"]
    },
    {
        "name": "Qwilfish",
        "base_stats": {"hp": 65, "attack": 95, "defense": 85, "sp_attack": 55, "sp_defense": 55, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Poison Point", "Swift Swim"],
        "hidden_abilities": ["Intimidate"]
    },
    {
        "name": "Scizor",
        "base_stats": {"hp": 70, "attack": 130, "defense": 100, "sp_attack": 55, "sp_defense": 80, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm", "Technician"],
        "hidden_abilities": ["Light Metal"]
    },
    {
        "name": "Shuckle",
        "base_stats": {"hp": 20, "attack": 10, "defense": 230, "sp_attack": 10, "sp_defense": 230, "speed": 5},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy", "Gluttony"],
        "hidden_abilities": ["Contrary"]
    },
    {
        "name": "Heracross",
        "base_stats": {"hp": 80, "attack": 125, "defense": 75, "sp_attack": 40, "sp_defense": 95, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm", "Guts"],
        "hidden_abilities": ["Moxie"]
    },
    {
        "name": "Sneasel",
        "base_stats": {"hp": 55, "attack": 95, "defense": 55, "sp_attack": 35, "sp_defense": 75, "speed": 115},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Inner Focus", "Keen Eye"],
        "hidden_abilities": ["Pickpocket"]
    },
    {
        "name": "Teddiursa",
        "base_stats": {"hp": 60, "attack": 80, "defense": 50, "sp_attack": 50, "sp_defense": 50, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pickup", "Quick Feet"],
        "hidden_abilities": ["Honey Gather"]
    },
    {
        "name": "Ursaring",
        "base_stats": {"hp": 90, "attack": 130, "defense": 75, "sp_attack": 75, "sp_defense": 75, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Guts", "Quick Feet"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Slugma",
        "base_stats": {"hp": 40, "attack": 40, "defense": 40, "sp_attack": 70, "sp_defense": 40, "speed": 20},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Magma Armor", "Flame Body"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Magcargo",
        "base_stats": {"hp": 50, "attack": 50, "defense": 120, "sp_attack": 80, "sp_defense": 80, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Magma Armor", "Flame Body"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Swinub",
        "base_stats": {"hp": 50, "attack": 50, "defense": 40, "sp_attack": 30, "sp_defense": 30, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Oblivious", "Snow Cloak"],
        "hidden_abilities": ["Thick Fat"]
    },
    {
        "name": "Piloswine",
        "base_stats": {"hp": 100, "attack": 100, "defense": 80, "sp_attack": 60, "sp_defense": 60, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Oblivious", "Snow Cloak"],
        "hidden_abilities": ["Thick Fat"]
    },
    {
        "name": "Corsola",
        "base_stats": {"hp": 65, "attack": 55, "defense": 95, "sp_attack": 65, "sp_defense": 95, "speed": 35},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Hustle", "Natural Cure"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Remoraid",
        "base_stats": {"hp": 35, "attack": 65, "defense": 35, "sp_attack": 65, "sp_defense": 35, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hustle", "Sniper"],
        "hidden_abilities": ["Moody"]
    },
    {
        "name": "Octillery",
        "base_stats": {"hp": 75, "attack": 105, "defense": 75, "sp_attack": 105, "sp_defense": 75, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Suction Cups", "Sniper"],
        "hidden_abilities": ["Moody"]
    },
    {
        "name": "Delibird",
        "base_stats": {"hp": 45, "attack": 55, "defense": 45, "sp_attack": 65, "sp_defense": 45, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Vital Spirit", "Hustle"],
        "hidden_abilities": ["Insomnia"]
    },
    {
        "name": "Mantine",
        "base_stats": {"hp": 85, "attack": 40, "defense": 70, "sp_attack": 80, "sp_defense": 140, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Water Absorb"],
        "hidden_abilities": ["Water Veil"]
    },
    {
        "name": "Skarmory",
        "base_stats": {"hp": 65, "attack": 80, "defense": 140, "sp_attack": 40, "sp_defense": 70, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Sturdy"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Houndour",
        "base_stats": {"hp": 45, "attack": 60, "defense": 30, "sp_attack": 80, "sp_defense": 50, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Early Bird", "Flash Fire"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Houndoom",
        "base_stats": {"hp": 75, "attack": 90, "defense": 50, "sp_attack": 110, "sp_defense": 80, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Early Bird", "Flash Fire"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Kingdra",
        "base_stats": {"hp": 75, "attack": 95, "defense": 95, "sp_attack": 95, "sp_defense": 95, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Sniper"],
        "hidden_abilities": ["Damp"]
    },
    {
        "name": "Phanpy",
        "base_stats": {"hp": 90, "attack": 60, "defense": 60, "sp_attack": 40, "sp_defense": 40, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pickup"],
        "hidden_abilities": ["Sand Veil"]
    },
    {
        "name": "Donphan",
        "base_stats": {"hp": 90, "attack": 120, "defense": 120, "sp_attack": 60, "sp_defense": 60, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy"],
        "hidden_abilities": ["Sand Veil"]
    },
    {
        "name": "Porygon2",
        "base_stats": {"hp": 85, "attack": 80, "defense": 90, "sp_attack": 105, "sp_defense": 95, "speed": 60},
        "gender_ratio": None,
        "abilities": ["Trace", "Download"],
        "hidden_abilities": ["Analytic"]
    },
    {
        "name": "Stantler",
        "base_stats": {"hp": 73, "attack": 95, "defense": 62, "sp_attack": 85, "sp_defense": 65, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate", "Frisk"],
        "hidden_abilities": ["Sap Sipper"]
    },
    {
        "name": "Smeargle",
        "base_stats": {"hp": 55, "attack": 20, "defense": 35, "sp_attack": 20, "sp_defense": 45, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Own Tempo", "Technician"],
        "hidden_abilities": ["Moody"]
    },
    {
        "name": "Tyrogue",
        "base_stats": {"hp": 35, "attack": 35, "defense": 35, "sp_attack": 35, "sp_defense": 35, "speed": 35},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Guts", "Steadfast"],
        "hidden_abilities": ["Vital Spirit"]
    },
    {
        "name": "Hitmontop",
        "base_stats": {"hp": 50, "attack": 95, "defense": 95, "sp_attack": 35, "sp_defense": 110, "speed": 70},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Intimidate", "Technician"],
        "hidden_abilities": ["Steadfast"]
    },
    {
        "name": "Smoochum",
        "base_stats": {"hp": 45, "attack": 30, "defense": 15, "sp_attack": 85, "sp_defense": 65, "speed": 65},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Oblivious", "Forewarn"],
        "hidden_abilities": ["Hydration"]
    },
    {
        "name": "Elekid",
        "base_stats": {"hp": 45, "attack": 63, "defense": 37, "sp_attack": 65, "sp_defense": 55, "speed": 95},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Static"],
        "hidden_abilities": ["Vital Spirit"]
    },
    {
        "name": "Magby",
        "base_stats": {"hp": 45, "attack": 75, "defense": 37, "sp_attack": 70, "sp_defense": 55, "speed": 83},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Flame Body"],
        "hidden_abilities": ["Vital Spirit"]
    },
    {
        "name": "Miltank",
        "base_stats": {"hp": 95, "attack": 80, "defense": 105, "sp_attack": 40, "sp_defense": 70, "speed": 100},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Thick Fat", "Scrappy"],
        "hidden_abilities": ["Sap Sipper"]
    },
    {
        "name": "Blissey",
        "base_stats": {"hp": 255, "attack": 10, "defense": 10, "sp_attack": 75, "sp_defense": 135, "speed": 55},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Natural Cure", "Serene Grace"],
        "hidden_abilities": ["Healer"]
    },
    {
        "name": "Raikou",
        "base_stats": {"hp": 90, "attack": 85, "defense": 75, "sp_attack": 115, "sp_defense": 100, "speed": 115},
        "gender_ratio": None,
        "abilities": ["Pressure"],
        "hidden_abilities": ["Inner Focus"]
    },
    {
        "name": "Entei",
        "base_stats": {"hp": 115, "attack": 115, "defense": 85, "sp_attack": 90, "sp_defense": 75, "speed": 100},
        "gender_ratio": None,
        "abilities": ["Pressure"],
        "hidden_abilities": ["Inner Focus"]
    },
    {
        "name": "Suicune",
        "base_stats": {"hp": 100, "attack": 75, "defense": 115, "sp_attack": 90, "sp_defense": 115, "speed": 85},
        "gender_ratio": None,
        "abilities": ["Pressure"],
        "hidden_abilities": ["Inner Focus"]
    },
    {
        "name": "Larvitar",
        "base_stats": {"hp": 50, "attack": 64, "defense": 50, "sp_attack": 45, "sp_defense": 50, "speed": 41},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Guts"],
        "hidden_abilities": ["Sand Veil"]
    },
    {
        "name": "Pupitar",
        "base_stats": {"hp": 70, "attack": 84, "defense": 70, "sp_attack": 65, "sp_defense": 70, "speed": 51},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shed Skin"],
        "hidden_abilities": []
    },
    {
        "name": "Tyranitar",
        "base_stats": {"hp": 100, "attack": 134, "defense": 110, "sp_attack": 95, "sp_defense": 100, "speed": 61},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Stream"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Lugia",
        "base_stats": {"hp": 106, "attack": 90, "defense": 130, "sp_attack": 90, "sp_defense": 154, "speed": 110},
        "gender_ratio": None,
        "abilities": ["Pressure"],
        "hidden_abilities": ["Multiscale"]
    },
    {
        "name": "Ho-oh",
        "base_stats": {"hp": 106, "attack": 130, "defense": 90, "sp_attack": 110, "sp_defense": 154, "speed": 90},
        "gender_ratio": None,
        "abilities": ["Pressure"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Celebi",
        "base_stats": {"hp": 100, "attack": 100, "defense": 100, "sp_attack": 100, "sp_defense": 100, "speed": 100},
        "gender_ratio": None,
        "abilities": ["Natural Cure"],
        "hidden_abilities": []
    }
]
POKEMON_GEN3 = [
    {
        "name": "Treecko",
        "base_stats": {"hp": 40, "attack": 45, "defense": 35, "sp_attack": 65, "sp_defense": 55, "speed": 70},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Unburden"]
    },
    {
        "name": "Grovyle",
        "base_stats": {"hp": 50, "attack": 65, "defense": 45, "sp_attack": 85, "sp_defense": 65, "speed": 95},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Unburden"]
    },
    {
        "name": "Sceptile",
        "base_stats": {"hp": 70, "attack": 85, "defense": 65, "sp_attack": 105, "sp_defense": 85, "speed": 120},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Unburden"]
    },
    {
        "name": "Torchic",
        "base_stats": {"hp": 45, "attack": 60, "defense": 40, "sp_attack": 70, "sp_defense": 50, "speed": 45},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Speed Boost"]
    },
    {
        "name": "Combusken",
        "base_stats": {"hp": 60, "attack": 85, "defense": 60, "sp_attack": 85, "sp_defense": 60, "speed": 55},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Speed Boost"]
    },
    {
        "name": "Blaziken",
        "base_stats": {"hp": 80, "attack": 120, "defense": 70, "sp_attack": 110, "sp_defense": 70, "speed": 80},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Speed Boost"]
    },
    {
        "name": "Mudkip",
        "base_stats": {"hp": 50, "attack": 70, "defense": 50, "sp_attack": 50, "sp_defense": 50, "speed": 40},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Damp"]
    },
    {
        "name": "Marshtomp",
        "base_stats": {"hp": 70, "attack": 85, "defense": 70, "sp_attack": 60, "sp_defense": 70, "speed": 50},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Damp"]
    },
    {
        "name": "Swampert",
        "base_stats": {"hp": 100, "attack": 110, "defense": 90, "sp_attack": 85, "sp_defense": 90, "speed": 60},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Damp"]
    },
    {
        "name": "Poochyena",
        "base_stats": {"hp": 35, "attack": 55, "defense": 35, "sp_attack": 30, "sp_defense": 30, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Quick Feet"],
        "hidden_abilities": ["Rattled"]
    },
    {
        "name": "Mightyena",
        "base_stats": {"hp": 70, "attack": 90, "defense": 70, "sp_attack": 60, "sp_defense": 60, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate", "Quick Feet"],
        "hidden_abilities": ["Moxie"]
    },
    {
        "name": "Zigzagoon",
        "base_stats": {"hp": 38, "attack": 30, "defense": 41, "sp_attack": 30, "sp_defense": 41, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pickup", "Gluttony"],
        "hidden_abilities": ["Quick Feet"]
    },
    {
        "name": "Linoone",
        "base_stats": {"hp": 78, "attack": 70, "defense": 61, "sp_attack": 50, "sp_defense": 61, "speed": 100},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pickup", "Gluttony"],
        "hidden_abilities": ["Quick Feet"]
    },
    {
        "name": "Wurmple",
        "base_stats": {"hp": 45, "attack": 45, "defense": 35, "sp_attack": 20, "sp_defense": 30, "speed": 20},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shield Dust"],
        "hidden_abilities": ["Run Away"]
    },
    {
        "name": "Silcoon",
        "base_stats": {"hp": 50, "attack": 35, "defense": 55, "sp_attack": 25, "sp_defense": 25, "speed": 15},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shed Skin"],
        "hidden_abilities": []
    },
    {
        "name": "Beautifly",
        "base_stats": {"hp": 60, "attack": 70, "defense": 50, "sp_attack": 100, "sp_defense": 50, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm"],
        "hidden_abilities": ["Rivalry"]
    },
    {
        "name": "Cascoon",
        "base_stats": {"hp": 50, "attack": 35, "defense": 55, "sp_attack": 25, "sp_defense": 25, "speed": 15},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shed Skin"],
        "hidden_abilities": []
    },
    {
        "name": "Dustox",
        "base_stats": {"hp": 60, "attack": 50, "defense": 70, "sp_attack": 50, "sp_defense": 90, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shield Dust"],
        "hidden_abilities": ["Compound Eyes"]
    },
    {
        "name": "Lotad",
        "base_stats": {"hp": 40, "attack": 30, "defense": 30, "sp_attack": 40, "sp_defense": 50, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Rain Dish"],
        "hidden_abilities": ["Own Tempo"]
    },
    {
        "name": "Lombre",
        "base_stats": {"hp": 60, "attack": 50, "defense": 50, "sp_attack": 60, "sp_defense": 70, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Rain Dish"],
        "hidden_abilities": ["Own Tempo"]
    },
    {
        "name": "Ludicolo",
        "base_stats": {"hp": 80, "attack": 70, "defense": 70, "sp_attack": 90, "sp_defense": 100, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Rain Dish"],
        "hidden_abilities": ["Own Tempo"]
    },
    {
        "name": "Seedot",
        "base_stats": {"hp": 40, "attack": 40, "defense": 50, "sp_attack": 30, "sp_defense": 30, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Early Bird"],
        "hidden_abilities": ["Pickpocket"]
    },
    {
        "name": "Nuzleaf",
        "base_stats": {"hp": 70, "attack": 70, "defense": 40, "sp_attack": 60, "sp_defense": 40, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Early Bird"],
        "hidden_abilities": ["Pickpocket"]
    },
    {
        "name": "Shiftry",
        "base_stats": {"hp": 90, "attack": 100, "defense": 60, "sp_attack": 90, "sp_defense": 60, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Early Bird"],
        "hidden_abilities": ["Pickpocket"]
    },
    {
        "name": "Taillow",
        "base_stats": {"hp": 40, "attack": 55, "defense": 30, "sp_attack": 30, "sp_defense": 30, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Guts"],
        "hidden_abilities": ["Scrappy"]
    },
    {
        "name": "Swellow",
        "base_stats": {"hp": 60, "attack": 85, "defense": 60, "sp_attack": 50, "sp_defense": 50, "speed": 125},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Guts"],
        "hidden_abilities": ["Scrappy"]
    },
    {
        "name": "Wingull",
        "base_stats": {"hp": 40, "attack": 30, "defense": 30, "sp_attack": 55, "sp_defense": 30, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Hydration"],
        "hidden_abilities": ["Rain Dish"]
    },
    {
        "name": "Pelipper",
        "base_stats": {"hp": 60, "attack": 50, "defense": 100, "sp_attack": 95, "sp_defense": 70, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Drizzle"],
        "hidden_abilities": ["Rain Dish"]
    },
    {
        "name": "Ralts",
        "base_stats": {"hp": 28, "attack": 25, "defense": 25, "sp_attack": 45, "sp_defense": 35, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Synchronize", "Trace"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Kirlia",
        "base_stats": {"hp": 38, "attack": 35, "defense": 35, "sp_attack": 65, "sp_defense": 55, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Synchronize", "Trace"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Gardevoir",
        "base_stats": {"hp": 68, "attack": 65, "defense": 65, "sp_attack": 125, "sp_defense": 115, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Synchronize", "Trace"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Surskit",
        "base_stats": {"hp": 40, "attack": 30, "defense": 32, "sp_attack": 50, "sp_defense": 52, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim"],
        "hidden_abilities": ["Rain Dish"]
    },
    {
        "name": "Masquerain",
        "base_stats": {"hp": 70, "attack": 60, "defense": 62, "sp_attack": 100, "sp_defense": 82, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Shroomish",
        "base_stats": {"hp": 60, "attack": 40, "defense": 60, "sp_attack": 40, "sp_defense": 60, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Effect Spore", "Poison Heal"],
        "hidden_abilities": ["Quick Feet"]
    },
    {
        "name": "Breloom",
        "base_stats": {"hp": 60, "attack": 130, "defense": 80, "sp_attack": 60, "sp_defense": 60, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Effect Spore", "Poison Heal"],
        "hidden_abilities": ["Technician"]
    },
    {
        "name": "Slakoth",
        "base_stats": {"hp": 60, "attack": 60, "defense": 60, "sp_attack": 35, "sp_defense": 35, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Truant"],
        "hidden_abilities": []
    },
    {
        "name": "Vigoroth",
        "base_stats": {"hp": 80, "attack": 80, "defense": 80, "sp_attack": 55, "sp_defense": 55, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Vital Spirit"],
        "hidden_abilities": []
    },
    {
        "name": "Slaking",
        "base_stats": {"hp": 150, "attack": 160, "defense": 100, "sp_attack": 95, "sp_defense": 65, "speed": 100},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Truant"],
        "hidden_abilities": []
    },
    {
        "name": "Nincada",
        "base_stats": {"hp": 31, "attack": 45, "defense": 90, "sp_attack": 30, "sp_defense": 30, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Compound Eyes"],
        "hidden_abilities": ["Run Away"]
    },
    {
        "name": "Ninjask",
        "base_stats": {"hp": 61, "attack": 90, "defense": 45, "sp_attack": 50, "sp_defense": 50, "speed": 160},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Speed Boost"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Shedinja",
        "base_stats": {"hp": 1, "attack": 90, "defense": 45, "sp_attack": 30, "sp_defense": 30, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Wonder Guard"],
        "hidden_abilities": []
    },
    {
        "name": "Whismur",
        "base_stats": {"hp": 64, "attack": 51, "defense": 23, "sp_attack": 51, "sp_defense": 23, "speed": 28},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Soundproof"],
        "hidden_abilities": ["Rattled"]
    },
    {
        "name": "Loudred",
        "base_stats": {"hp": 84, "attack": 71, "defense": 43, "sp_attack": 71, "sp_defense": 43, "speed": 48},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Soundproof"],
        "hidden_abilities": ["Scrappy"]
    },
    {
        "name": "Exploud",
        "base_stats": {"hp": 104, "attack": 91, "defense": 63, "sp_attack": 91, "sp_defense": 73, "speed": 68},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Soundproof"],
        "hidden_abilities": ["Scrappy"]
    },
    {
        "name": "Makuhita",
        "base_stats": {"hp": 72, "attack": 60, "defense": 30, "sp_attack": 20, "sp_defense": 30, "speed": 25},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Thick Fat", "Guts"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Hariyama",
        "base_stats": {"hp": 144, "attack": 120, "defense": 60, "sp_attack": 40, "sp_defense": 60, "speed": 50},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Thick Fat", "Guts"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Azurill",
        "base_stats": {"hp": 50, "attack": 20, "defense": 40, "sp_attack": 20, "sp_defense": 40, "speed": 20},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Thick Fat", "Huge Power"],
        "hidden_abilities": ["Sap Sipper"]
    },
    {
        "name": "Nosepass",
        "base_stats": {"hp": 30, "attack": 45, "defense": 135, "sp_attack": 45, "sp_defense": 90, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy", "Magnet Pull"],
        "hidden_abilities": ["Sand Force"]
    },
    {
        "name": "Skitty",
        "base_stats": {"hp": 50, "attack": 45, "defense": 45, "sp_attack": 35, "sp_defense": 35, "speed": 50},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Cute Charm", "Normalize"],
        "hidden_abilities": ["Wonder Skin"]
    },
    {
        "name": "Delcatty",
        "base_stats": {"hp": 70, "attack": 65, "defense": 65, "sp_attack": 55, "sp_defense": 55, "speed": 90},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Cute Charm", "Normalize"],
        "hidden_abilities": ["Wonder Skin"]
    },
    {
        "name": "Sableye",
        "base_stats": {"hp": 50, "attack": 75, "defense": 75, "sp_attack": 65, "sp_defense": 65, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Stall"],
        "hidden_abilities": ["Prankster"]
    },
    {
        "name": "Mawile",
        "base_stats": {"hp": 50, "attack": 85, "defense": 85, "sp_attack": 55, "sp_defense": 55, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hyper Cutter", "Intimidate"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Aron",
        "base_stats": {"hp": 50, "attack": 70, "defense": 100, "sp_attack": 40, "sp_defense": 40, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy", "Rock Head"],
        "hidden_abilities": ["Heavy Metal"]
    },
    {
        "name": "Lairon",
        "base_stats": {"hp": 60, "attack": 90, "defense": 140, "sp_attack": 50, "sp_defense": 50, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy", "Rock Head"],
        "hidden_abilities": ["Heavy Metal"]
    },
    {
        "name": "Aggron",
        "base_stats": {"hp": 70, "attack": 110, "defense": 180, "sp_attack": 60, "sp_defense": 60, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy", "Rock Head"],
        "hidden_abilities": ["Heavy Metal"]
    },
    {
        "name": "Meditite",
        "base_stats": {"hp": 30, "attack": 40, "defense": 55, "sp_attack": 40, "sp_defense": 55, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pure Power"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Medicham",
        "base_stats": {"hp": 60, "attack": 60, "defense": 75, "sp_attack": 60, "sp_defense": 75, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pure Power"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Electrike",
        "base_stats": {"hp": 40, "attack": 45, "defense": 40, "sp_attack": 65, "sp_defense": 40, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Static", "Lightning Rod"],
        "hidden_abilities": ["Minus"]
    },
    {
        "name": "Manectric",
        "base_stats": {"hp": 70, "attack": 75, "defense": 60, "sp_attack": 105, "sp_defense": 60, "speed": 105},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Static", "Lightning Rod"],
        "hidden_abilities": ["Minus"]
    },
    {
        "name": "Plusle",
        "base_stats": {"hp": 60, "attack": 50, "defense": 40, "sp_attack": 85, "sp_defense": 75, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Plus"],
        "hidden_abilities": ["Lightning Rod"]
    },
    {
        "name": "Minun",
        "base_stats": {"hp": 60, "attack": 40, "defense": 50, "sp_attack": 75, "sp_defense": 85, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Minus"],
        "hidden_abilities": ["Volt Absorb"]
    },
    {
        "name": "Volbeat",
        "base_stats": {"hp": 65, "attack": 73, "defense": 55, "sp_attack": 47, "sp_defense": 75, "speed": 85},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Illuminate", "Swarm"],
        "hidden_abilities": ["Prankster"]
    },
    {
        "name": "Illumise",
        "base_stats": {"hp": 65, "attack": 47, "defense": 55, "sp_attack": 73, "sp_defense": 75, "speed": 85},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Oblivious", "Tinted Lens"],
        "hidden_abilities": ["Prankster"]
    },
    {
        "name": "Roselia",
        "base_stats": {"hp": 50, "attack": 60, "defense": 45, "sp_attack": 100, "sp_defense": 80, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Natural Cure", "Poison Point"],
        "hidden_abilities": ["Leaf Guard"]
    },
    {
        "name": "Gulpin",
        "base_stats": {"hp": 70, "attack": 43, "defense": 53, "sp_attack": 43, "sp_defense": 53, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Liquid Ooze", "Sticky Hold"],
        "hidden_abilities": ["Gluttony"]
    },
    {
        "name": "Swalot",
        "base_stats": {"hp": 100, "attack": 73, "defense": 83, "sp_attack": 73, "sp_defense": 83, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Liquid Ooze", "Sticky Hold"],
        "hidden_abilities": ["Gluttony"]
    },
    {
        "name": "Carvanha",
        "base_stats": {"hp": 45, "attack": 90, "defense": 20, "sp_attack": 65, "sp_defense": 20, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rough Skin"],
        "hidden_abilities": ["Speed Boost"]
    },
    {
        "name": "Sharpedo",
        "base_stats": {"hp": 70, "attack": 120, "defense": 40, "sp_attack": 95, "sp_defense": 40, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rough Skin"],
        "hidden_abilities": ["Speed Boost"]
    },
    {
        "name": "Wailmer",
        "base_stats": {"hp": 130, "attack": 70, "defense": 35, "sp_attack": 70, "sp_defense": 35, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Veil", "Oblivious"],
        "hidden_abilities": ["Pressure"]
    },
    {
        "name": "Wailord",
        "base_stats": {"hp": 170, "attack": 90, "defense": 45, "sp_attack": 90, "sp_defense": 45, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Veil", "Oblivious"],
        "hidden_abilities": ["Pressure"]
    },
    {
        "name": "Numel",
        "base_stats": {"hp": 60, "attack": 60, "defense": 40, "sp_attack": 65, "sp_defense": 45, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Oblivious", "Simple"],
        "hidden_abilities": ["Own Tempo"]
    },
    {
        "name": "Camerupt",
        "base_stats": {"hp": 70, "attack": 100, "defense": 70, "sp_attack": 105, "sp_defense": 75, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Magma Armor", "Solid Rock"],
        "hidden_abilities": ["Anger Point"]
    },
    {
        "name": "Torkoal",
        "base_stats": {"hp": 70, "attack": 85, "defense": 140, "sp_attack": 85, "sp_defense": 70, "speed": 20},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["White Smoke", "Drought"],
        "hidden_abilities": ["Shell Armor"]
    },
    {
        "name": "Spoink",
        "base_stats": {"hp": 60, "attack": 25, "defense": 35, "sp_attack": 70, "sp_defense": 80, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Thick Fat", "Own Tempo"],
        "hidden_abilities": ["Gluttony"]
    },
    {
        "name": "Grumpig",
        "base_stats": {"hp": 80, "attack": 45, "defense": 65, "sp_attack": 90, "sp_defense": 110, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Thick Fat", "Own Tempo"],
        "hidden_abilities": ["Gluttony"]
    },
    {
        "name": "Spinda",
        "base_stats": {"hp": 60, "attack": 60, "defense": 60, "sp_attack": 60, "sp_defense": 60, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Own Tempo", "Tangled Feet"],
        "hidden_abilities": ["Contrary"]
    },
    {
        "name": "Trapinch",
        "base_stats": {"hp": 45, "attack": 100, "defense": 45, "sp_attack": 45, "sp_defense": 45, "speed": 10},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hyper Cutter", "Arena Trap"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Vibrava",
        "base_stats": {"hp": 50, "attack": 70, "defense": 50, "sp_attack": 50, "sp_defense": 50, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Flygon",
        "base_stats": {"hp": 80, "attack": 100, "defense": 80, "sp_attack": 80, "sp_defense": 80, "speed": 100},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Cacnea",
        "base_stats": {"hp": 50, "attack": 85, "defense": 40, "sp_attack": 85, "sp_defense": 40, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Veil"],
        "hidden_abilities": ["Water Absorb"]
    },
    {
        "name": "Cacturne",
        "base_stats": {"hp": 70, "attack": 115, "defense": 60, "sp_attack": 115, "sp_defense": 60, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Veil"],
        "hidden_abilities": ["Water Absorb"]
    },
    {
        "name": "Swablu",
        "base_stats": {"hp": 45, "attack": 40, "defense": 60, "sp_attack": 40, "sp_defense": 75, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Natural Cure"],
        "hidden_abilities": ["Cloud Nine"]
    },
    {
        "name": "Altaria",
        "base_stats": {"hp": 75, "attack": 70, "defense": 90, "sp_attack": 70, "sp_defense": 105, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Natural Cure"],
        "hidden_abilities": ["Cloud Nine"]
    },
    {
        "name": "Zangoose",
        "base_stats": {"hp": 73, "attack": 115, "defense": 60, "sp_attack": 60, "sp_defense": 60, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Immunity"],
        "hidden_abilities": ["Toxic Boost"]
    },
    {
        "name": "Seviper",
        "base_stats": {"hp": 73, "attack": 100, "defense": 60, "sp_attack": 100, "sp_defense": 60, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shed Skin"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Lunatone",
        "base_stats": {"hp": 90, "attack": 55, "defense": 65, "sp_attack": 95, "sp_defense": 85, "speed": 70},
        "gender_ratio": None,
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Solrock",
        "base_stats": {"hp": 90, "attack": 95, "defense": 85, "sp_attack": 55, "sp_defense": 65, "speed": 70},
        "gender_ratio": None,
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Barboach",
        "base_stats": {"hp": 50, "attack": 48, "defense": 43, "sp_attack": 46, "sp_defense": 41, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Oblivious", "Anticipation"],
        "hidden_abilities": ["Hydration"]
    },
    {
        "name": "Whiscash",
        "base_stats": {"hp": 110, "attack": 78, "defense": 73, "sp_attack": 76, "sp_defense": 71, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Oblivious", "Anticipation"],
        "hidden_abilities": ["Hydration"]
    },
    {
        "name": "Corphish",
        "base_stats": {"hp": 43, "attack": 80, "defense": 65, "sp_attack": 50, "sp_defense": 35, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hyper Cutter", "Shell Armor"],
        "hidden_abilities": ["Adaptability"]
    },
    {
        "name": "Crawdaunt",
        "base_stats": {"hp": 63, "attack": 120, "defense": 85, "sp_attack": 90, "sp_defense": 55, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hyper Cutter", "Shell Armor"],
        "hidden_abilities": ["Adaptability"]
    },
    {
        "name": "Baltoy",
        "base_stats": {"hp": 40, "attack": 40, "defense": 55, "sp_attack": 40, "sp_defense": 70, "speed": 55},
        "gender_ratio": None,
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Claydol",
        "base_stats": {"hp": 60, "attack": 70, "defense": 105, "sp_attack": 70, "sp_defense": 120, "speed": 75},
        "gender_ratio": None,
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Lileep",
        "base_stats": {"hp": 66, "attack": 41, "defense": 77, "sp_attack": 61, "sp_defense": 87, "speed": 23},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Suction Cups"],
        "hidden_abilities": ["Storm Drain"]
    },
    {
        "name": "Cradily",
        "base_stats": {"hp": 86, "attack": 81, "defense": 97, "sp_attack": 81, "sp_defense": 107, "speed": 43},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Suction Cups"],
        "hidden_abilities": ["Storm Drain"]
    },
    {
        "name": "Anorith",
        "base_stats": {"hp": 45, "attack": 95, "defense": 50, "sp_attack": 40, "sp_defense": 50, "speed": 75},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Battle Armor"],
        "hidden_abilities": ["Swift Swim"]
    },
    {
        "name": "Armaldo",
        "base_stats": {"hp": 75, "attack": 125, "defense": 100, "sp_attack": 70, "sp_defense": 80, "speed": 45},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Battle Armor"],
        "hidden_abilities": ["Swift Swim"]
    },
    {
        "name": "Feebas",
        "base_stats": {"hp": 20, "attack": 15, "defense": 20, "sp_attack": 10, "sp_defense": 55, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Oblivious"],
        "hidden_abilities": ["Adaptability"]
    },
    {
        "name": "Milotic",
        "base_stats": {"hp": 95, "attack": 60, "defense": 79, "sp_attack": 100, "sp_defense": 125, "speed": 81},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Marvel Scale", "Competitive"],
        "hidden_abilities": ["Cute Charm"]
    },
    {
        "name": "Castform",
        "base_stats": {"hp": 70, "attack": 70, "defense": 70, "sp_attack": 70, "sp_defense": 70, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Forecast"],
        "hidden_abilities": []
    },
    {
        "name": "Kecleon",
        "base_stats": {"hp": 60, "attack": 90, "defense": 70, "sp_attack": 60, "sp_defense": 120, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Color Change"],
        "hidden_abilities": ["Protean"]
    },
    {
        "name": "Shuppet",
        "base_stats": {"hp": 44, "attack": 75, "defense": 35, "sp_attack": 63, "sp_defense": 33, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Insomnia", "Frisk"],
        "hidden_abilities": ["Cursed Body"]
    },
    {
        "name": "Banette",
        "base_stats": {"hp": 64, "attack": 115, "defense": 65, "sp_attack": 83, "sp_defense": 63, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Insomnia", "Frisk"],
        "hidden_abilities": ["Cursed Body"]
    },
    {
        "name": "Duskull",
        "base_stats": {"hp": 20, "attack": 40, "defense": 90, "sp_attack": 30, "sp_defense": 90, "speed": 25},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": ["Frisk"]
    },
    {
        "name": "Dusclops",
        "base_stats": {"hp": 40, "attack": 70, "defense": 130, "sp_attack": 60, "sp_defense": 130, "speed": 25},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pressure"],
        "hidden_abilities": ["Frisk"]
    },
    {
        "name": "Tropius",
        "base_stats": {"hp": 99, "attack": 68, "defense": 83, "sp_attack": 72, "sp_defense": 87, "speed": 51},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Solar Power"],
        "hidden_abilities": ["Harvest"]
    },
    {
        "name": "Chimecho",
        "base_stats": {"hp": 65, "attack": 50, "defense": 70, "sp_attack": 95, "sp_defense": 80, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Absol",
        "base_stats": {"hp": 65, "attack": 130, "defense": 60, "sp_attack": 75, "sp_defense": 60, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pressure", "Super Luck"],
        "hidden_abilities": ["Justified"]
    },
    {
        "name": "Wynaut",
        "base_stats": {"hp": 95, "attack": 23, "defense": 48, "sp_attack": 23, "sp_defense": 48, "speed": 23},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shadow Tag"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Snorunt",
        "base_stats": {"hp": 50, "attack": 50, "defense": 50, "sp_attack": 50, "sp_defense": 50, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Inner Focus", "Ice Body"],
        "hidden_abilities": ["Moody"]
    },
    {
        "name": "Glalie",
        "base_stats": {"hp": 80, "attack": 80, "defense": 80, "sp_attack": 80, "sp_defense": 80, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Inner Focus", "Ice Body"],
        "hidden_abilities": ["Moody"]
    },
    {
        "name": "Spheal",
        "base_stats": {"hp": 70, "attack": 40, "defense": 50, "sp_attack": 55, "sp_defense": 50, "speed": 25},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Thick Fat", "Ice Body"],
        "hidden_abilities": ["Oblivious"]
    },
    {
        "name": "Sealeo",
        "base_stats": {"hp": 90, "attack": 60, "defense": 70, "sp_attack": 75, "sp_defense": 70, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Thick Fat", "Ice Body"],
        "hidden_abilities": ["Oblivious"]
    },
    {
        "name": "Walrein",
        "base_stats": {"hp": 110, "attack": 80, "defense": 90, "sp_attack": 95, "sp_defense": 90, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Thick Fat", "Ice Body"],
        "hidden_abilities": ["Oblivious"]
    },
    {
        "name": "Clamperl",
        "base_stats": {"hp": 35, "attack": 64, "defense": 85, "sp_attack": 74, "sp_defense": 55, "speed": 32},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shell Armor"],
        "hidden_abilities": ["Rattled"]
    },
    {
        "name": "Huntail",
        "base_stats": {"hp": 55, "attack": 104, "defense": 105, "sp_attack": 94, "sp_defense": 75, "speed": 52},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim"],
        "hidden_abilities": ["Water Veil"]
    },
    {
        "name": "Gorebyss",
        "base_stats": {"hp": 55, "attack": 84, "defense": 105, "sp_attack": 114, "sp_defense": 75, "speed": 52},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim"],
        "hidden_abilities": ["Hydration"]
    },
    {
        "name": "Relicanth",
        "base_stats": {"hp": 100, "attack": 90, "defense": 130, "sp_attack": 45, "sp_defense": 65, "speed": 55},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Swift Swim", "Rock Head"],
        "hidden_abilities": ["Sturdy"]
    },
    {
        "name": "Luvdisc",
        "base_stats": {"hp": 43, "attack": 30, "defense": 55, "sp_attack": 40, "sp_defense": 65, "speed": 97},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Swift Swim"],
        "hidden_abilities": ["Hydration"]
    },
    {
        "name": "Bagon",
        "base_stats": {"hp": 45, "attack": 75, "defense": 60, "sp_attack": 40, "sp_defense": 30, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rock Head"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Shelgon",
        "base_stats": {"hp": 65, "attack": 95, "defense": 100, "sp_attack": 60, "sp_defense": 50, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rock Head"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Salamence",
        "base_stats": {"hp": 95, "attack": 135, "defense": 80, "sp_attack": 110, "sp_defense": 80, "speed": 100},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate"],
        "hidden_abilities": ["Moxie"]
    },
    {
        "name": "Beldum",
        "base_stats": {"hp": 40, "attack": 55, "defense": 80, "sp_attack": 35, "sp_defense": 60, "speed": 30},
        "gender_ratio": None,
        "abilities": ["Clear Body"],
        "hidden_abilities": ["Light Metal"]
    },
    {
        "name": "Metang",
        "base_stats": {"hp": 60, "attack": 75, "defense": 100, "sp_attack": 55, "sp_defense": 80, "speed": 50},
        "gender_ratio": None,
        "abilities": ["Clear Body"],
        "hidden_abilities": ["Light Metal"]
    },
    {
        "name": "Metagross",
        "base_stats": {"hp": 80, "attack": 135, "defense": 130, "sp_attack": 95, "sp_defense": 90, "speed": 70},
        "gender_ratio": None,
        "abilities": ["Clear Body"],
        "hidden_abilities": ["Light Metal"]
    },
    {
        "name": "Regirock",
        "base_stats": {"hp": 80, "attack": 100, "defense": 200, "sp_attack": 50, "sp_defense": 100, "speed": 50},
        "gender_ratio": None,
        "abilities": ["Clear Body"],
        "hidden_abilities": ["Sturdy"]
    },
    {
        "name": "Regice",
        "base_stats": {"hp": 80, "attack": 50, "defense": 100, "sp_attack": 100, "sp_defense": 200, "speed": 50},
        "gender_ratio": None,
        "abilities": ["Clear Body"],
        "hidden_abilities": ["Ice Body"]
    },
    {
        "name": "Registeel",
        "base_stats": {"hp": 80, "attack": 75, "defense": 150, "sp_attack": 75, "sp_defense": 150, "speed": 50},
        "gender_ratio": None,
        "abilities": ["Clear Body"],
        "hidden_abilities": ["Light Metal"]
    },
    {
        "name": "Latias",
        "base_stats": {"hp": 80, "attack": 80, "defense": 90, "sp_attack": 110, "sp_defense": 130, "speed": 110},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Latios",
        "base_stats": {"hp": 80, "attack": 90, "defense": 80, "sp_attack": 130, "sp_defense": 110, "speed": 110},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Kyogre",
        "base_stats": {"hp": 100, "attack": 100, "defense": 90, "sp_attack": 150, "sp_defense": 140, "speed": 90},
        "gender_ratio": None,
        "abilities": ["Drizzle"],
        "hidden_abilities": []
    },
    {
        "name": "Groudon",
        "base_stats": {"hp": 100, "attack": 150, "defense": 140, "sp_attack": 100, "sp_defense": 90, "speed": 90},
        "gender_ratio": None,
        "abilities": ["Drought"],
        "hidden_abilities": []
    },
    {
        "name": "Rayquaza",
        "base_stats": {"hp": 105, "attack": 150, "defense": 90, "sp_attack": 150, "sp_defense": 90, "speed": 95},
        "gender_ratio": None,
        "abilities": ["Air Lock"],
        "hidden_abilities": []
    },
    {
        "name": "Jirachi",
        "base_stats": {"hp": 100, "attack": 100, "defense": 100, "sp_attack": 100, "sp_defense": 100, "speed": 100},
        "gender_ratio": None,
        "abilities": ["Serene Grace"],
        "hidden_abilities": []
    },
    {
        "name": "Deoxys",
        "base_stats": {"hp": 50, "attack": 150, "defense": 50, "sp_attack": 150, "sp_defense": 50, "speed": 150},
        "gender_ratio": None,
        "abilities": ["Pressure"],
        "hidden_abilities": []
    }
]
POKEMON_GEN4 = [
    {
        "name": "Turtwig",
        "base_stats": {"hp": 55, "attack": 68, "defense": 64, "sp_attack": 45, "sp_defense": 55, "speed": 31},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Shell Armor"]
    },
    {
        "name": "Grotle",
        "base_stats": {"hp": 75, "attack": 89, "defense": 85, "sp_attack": 55, "sp_defense": 65, "speed": 36},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Shell Armor"]
    },
    {
        "name": "Torterra",
        "base_stats": {"hp": 95, "attack": 109, "defense": 105, "sp_attack": 75, "sp_defense": 85, "speed": 56},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Shell Armor"]
    },
    {
        "name": "Chimchar",
        "base_stats": {"hp": 44, "attack": 58, "defense": 44, "sp_attack": 58, "sp_defense": 44, "speed": 61},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Iron Fist"]
    },
    {
        "name": "Monferno",
        "base_stats": {"hp": 64, "attack": 78, "defense": 52, "sp_attack": 78, "sp_defense": 52, "speed": 81},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Iron Fist"]
    },
    {
        "name": "Infernape",
        "base_stats": {"hp": 76, "attack": 104, "defense": 71, "sp_attack": 104, "sp_defense": 71, "speed": 108},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Iron Fist"]
    },
    {
        "name": "Piplup",
        "base_stats": {"hp": 53, "attack": 51, "defense": 53, "sp_attack": 61, "sp_defense": 56, "speed": 40},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Defiant"]
    },
    {
        "name": "Prinplup",
        "base_stats": {"hp": 64, "attack": 66, "defense": 68, "sp_attack": 81, "sp_defense": 76, "speed": 50},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Defiant"]
    },
    {
        "name": "Empoleon",
        "base_stats": {"hp": 84, "attack": 86, "defense": 88, "sp_attack": 111, "sp_defense": 101, "speed": 60},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Defiant"]
    },
    {
        "name": "Starly",
        "base_stats": {"hp": 40, "attack": 55, "defense": 30, "sp_attack": 30, "sp_defense": 30, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye"],
        "hidden_abilities": ["Reckless"]
    },
    {
        "name": "Staravia",
        "base_stats": {"hp": 55, "attack": 75, "defense": 50, "sp_attack": 40, "sp_defense": 40, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate"],
        "hidden_abilities": ["Reckless"]
    },
    {
        "name": "Staraptor",
        "base_stats": {"hp": 85, "attack": 120, "defense": 70, "sp_attack": 50, "sp_defense": 60, "speed": 100},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate"],
        "hidden_abilities": ["Reckless"]
    },
    {
        "name": "Bidoof",
        "base_stats": {"hp": 59, "attack": 45, "defense": 40, "sp_attack": 35, "sp_defense": 40, "speed": 31},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Simple", "Unaware"],
        "hidden_abilities": ["Moody"]
    },
    {
        "name": "Bibarel",
        "base_stats": {"hp": 79, "attack": 85, "defense": 60, "sp_attack": 55, "sp_defense": 60, "speed": 71},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Simple", "Unaware"],
        "hidden_abilities": ["Moody"]
    },
    {
        "name": "Kricketot",
        "base_stats": {"hp": 37, "attack": 25, "defense": 41, "sp_attack": 25, "sp_defense": 41, "speed": 25},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shed Skin"],
        "hidden_abilities": []
    },
    {
        "name": "Kricketune",
        "base_stats": {"hp": 77, "attack": 85, "defense": 51, "sp_attack": 55, "sp_defense": 51, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm"],
        "hidden_abilities": ["Technician"]
    },
    {
        "name": "Shinx",
        "base_stats": {"hp": 45, "attack": 65, "defense": 34, "sp_attack": 40, "sp_defense": 34, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rivalry", "Intimidate"],
        "hidden_abilities": ["Guts"]
    },
    {
        "name": "Luxio",
        "base_stats": {"hp": 60, "attack": 85, "defense": 49, "sp_attack": 60, "sp_defense": 49, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rivalry", "Intimidate"],
        "hidden_abilities": ["Guts"]
    },
    {
        "name": "Luxray",
        "base_stats": {"hp": 80, "attack": 120, "defense": 79, "sp_attack": 95, "sp_defense": 79, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rivalry", "Intimidate"],
        "hidden_abilities": ["Guts"]
    },
    {
        "name": "Budew",
        "base_stats": {"hp": 40, "attack": 30, "defense": 35, "sp_attack": 50, "sp_defense": 70, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Natural Cure", "Poison Point"],
        "hidden_abilities": ["Leaf Guard"]
    },
    {
        "name": "Roserade",
        "base_stats": {"hp": 60, "attack": 70, "defense": 65, "sp_attack": 125, "sp_defense": 105, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Natural Cure", "Poison Point"],
        "hidden_abilities": ["Technician"]
    },
    {
        "name": "Cranidos",
        "base_stats": {"hp": 67, "attack": 125, "defense": 40, "sp_attack": 30, "sp_defense": 30, "speed": 58},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Mold Breaker"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Rampardos",
        "base_stats": {"hp": 97, "attack": 165, "defense": 60, "sp_attack": 65, "sp_defense": 50, "speed": 58},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Mold Breaker"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Shieldon",
        "base_stats": {"hp": 30, "attack": 42, "defense": 118, "sp_attack": 42, "sp_defense": 88, "speed": 30},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Sturdy"],
        "hidden_abilities": ["Soundproof"]
    },
    {
        "name": "Bastiodon",
        "base_stats": {"hp": 60, "attack": 52, "defense": 168, "sp_attack": 47, "sp_defense": 138, "speed": 30},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Sturdy"],
        "hidden_abilities": ["Soundproof"]
    },
    {
        "name": "Burmy",
        "base_stats": {"hp": 40, "attack": 29, "defense": 45, "sp_attack": 29, "sp_defense": 45, "speed": 36},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shed Skin"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Wormadam",
        "base_stats": {"hp": 60, "attack": 59, "defense": 85, "sp_attack": 79, "sp_defense": 105, "speed": 36},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Anticipation"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Mothim",
        "base_stats": {"hp": 70, "attack": 94, "defense": 50, "sp_attack": 94, "sp_defense": 50, "speed": 66},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Swarm"],
        "hidden_abilities": ["Tinted Lens"]
    },
    {
        "name": "Combee",
        "base_stats": {"hp": 30, "attack": 30, "defense": 42, "sp_attack": 30, "sp_defense": 42, "speed": 70},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Honey Gather"],
        "hidden_abilities": ["Hustle"]
    },
    {
        "name": "Vespiquen",
        "base_stats": {"hp": 70, "attack": 80, "defense": 102, "sp_attack": 80, "sp_defense": 102, "speed": 40},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Pressure"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Pachirisu",
        "base_stats": {"hp": 60, "attack": 45, "defense": 70, "sp_attack": 45, "sp_defense": 90, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Pickup"],
        "hidden_abilities": ["Volt Absorb"]
    },
    {
        "name": "Buizel",
        "base_stats": {"hp": 55, "attack": 65, "defense": 35, "sp_attack": 60, "sp_defense": 30, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim"],
        "hidden_abilities": ["Water Veil"]
    },
    {
        "name": "Floatzel",
        "base_stats": {"hp": 85, "attack": 105, "defense": 55, "sp_attack": 85, "sp_defense": 50, "speed": 115},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim"],
        "hidden_abilities": ["Water Veil"]
    },
    {
        "name": "Cherubi",
        "base_stats": {"hp": 45, "attack": 35, "defense": 45, "sp_attack": 62, "sp_defense": 53, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll"],
        "hidden_abilities": []
    },
    {
        "name": "Cherrim",
        "base_stats": {"hp": 70, "attack": 60, "defense": 70, "sp_attack": 87, "sp_defense": 78, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Flower Gift"],
        "hidden_abilities": []
    },
    {
        "name": "Shellos",
        "base_stats": {"hp": 76, "attack": 48, "defense": 48, "sp_attack": 57, "sp_defense": 62, "speed": 34},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sticky Hold", "Storm Drain"],
        "hidden_abilities": ["Sand Force"]
    },
    {
        "name": "Gastrodon",
        "base_stats": {"hp": 111, "attack": 83, "defense": 68, "sp_attack": 92, "sp_defense": 82, "speed": 39},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sticky Hold", "Storm Drain"],
        "hidden_abilities": ["Sand Force"]
    },
    {
        "name": "Ambipom",
        "base_stats": {"hp": 75, "attack": 100, "defense": 66, "sp_attack": 60, "sp_defense": 66, "speed": 115},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Technician", "Pickup"],
        "hidden_abilities": ["Skill Link"]
    },
    {
        "name": "Drifloon",
        "base_stats": {"hp": 90, "attack": 50, "defense": 34, "sp_attack": 60, "sp_defense": 44, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Aftermath", "Unburden"],
        "hidden_abilities": ["Flare Boost"]
    },
    {
        "name": "Drifblim",
        "base_stats": {"hp": 150, "attack": 80, "defense": 44, "sp_attack": 90, "sp_defense": 54, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Aftermath", "Unburden"],
        "hidden_abilities": ["Flare Boost"]
    },
    {
        "name": "Buneary",
        "base_stats": {"hp": 55, "attack": 66, "defense": 44, "sp_attack": 44, "sp_defense": 56, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Klutz"],
        "hidden_abilities": ["Limber"]
    },
    {
        "name": "Lopunny",
        "base_stats": {"hp": 65, "attack": 76, "defense": 84, "sp_attack": 54, "sp_defense": 96, "speed": 105},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Cute Charm", "Klutz"],
        "hidden_abilities": ["Limber"]
    },
    {
        "name": "Mismagius",
        "base_stats": {"hp": 60, "attack": 60, "defense": 60, "sp_attack": 105, "sp_defense": 105, "speed": 105},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Honchkrow",
        "base_stats": {"hp": 100, "attack": 125, "defense": 52, "sp_attack": 105, "sp_defense": 52, "speed": 71},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Insomnia", "Super Luck"],
        "hidden_abilities": ["Moxie"]
    },
    {
        "name": "Glameow",
        "base_stats": {"hp": 49, "attack": 55, "defense": 42, "sp_attack": 42, "sp_defense": 37, "speed": 85},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Limber", "Own Tempo"],
        "hidden_abilities": ["Keen Eye"]
    },
    {
        "name": "Purugly",
        "base_stats": {"hp": 71, "attack": 82, "defense": 64, "sp_attack": 64, "sp_defense": 59, "speed": 112},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Thick Fat", "Own Tempo"],
        "hidden_abilities": ["Defiant"]
    },
    {
        "name": "Stunky",
        "base_stats": {"hp": 63, "attack": 63, "defense": 47, "sp_attack": 41, "sp_defense": 41, "speed": 74},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Stench", "Aftermath"],
        "hidden_abilities": ["Keen Eye"]
    },
    {
        "name": "Skuntank",
        "base_stats": {"hp": 103, "attack": 93, "defense": 67, "sp_attack": 71, "sp_defense": 61, "speed": 84},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Stench", "Aftermath"],
        "hidden_abilities": ["Keen Eye"]
    },
    {
        "name": "Bronzor",
        "base_stats": {"hp": 57, "attack": 24, "defense": 86, "sp_attack": 24, "sp_defense": 86, "speed": 23},
        "gender_ratio": None,
        "abilities": ["Levitate", "Heatproof"],
        "hidden_abilities": ["Heavy Metal"]
    },
    {
        "name": "Bronzong",
        "base_stats": {"hp": 67, "attack": 89, "defense": 116, "sp_attack": 79, "sp_defense": 116, "speed": 33},
        "gender_ratio": None,
        "abilities": ["Levitate", "Heatproof"],
        "hidden_abilities": ["Heavy Metal"]
    },
    {
        "name": "Bonsly",
        "base_stats": {"hp": 50, "attack": 80, "defense": 95, "sp_attack": 10, "sp_defense": 45, "speed": 10},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy", "Rock Head"],
        "hidden_abilities": ["Rattled"]
    },
    {
        "name": "Mime Jr.",
        "base_stats": {"hp": 20, "attack": 25, "defense": 45, "sp_attack": 70, "sp_defense": 90, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Soundproof", "Filter"],
        "hidden_abilities": ["Technician"]
    },
    {
        "name": "Happiny",
        "base_stats": {"hp": 100, "attack": 5, "defense": 5, "sp_attack": 15, "sp_defense": 65, "speed": 30},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Natural Cure", "Serene Grace"],
        "hidden_abilities": ["Friend Guard"]
    },
    {
        "name": "Chatot",
        "base_stats": {"hp": 76, "attack": 65, "defense": 45, "sp_attack": 92, "sp_defense": 42, "speed": 91},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Tangled Feet"],
        "hidden_abilities": ["Big Pecks"]
    },
    {
        "name": "Spiritomb",
        "base_stats": {"hp": 50, "attack": 92, "defense": 108, "sp_attack": 92, "sp_defense": 108, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pressure"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Gible",
        "base_stats": {"hp": 58, "attack": 70, "defense": 45, "sp_attack": 40, "sp_defense": 45, "speed": 42},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Veil"],
        "hidden_abilities": ["Rough Skin"]
    },
    {
        "name": "Gabite",
        "base_stats": {"hp": 68, "attack": 90, "defense": 65, "sp_attack": 50, "sp_defense": 55, "speed": 82},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Veil"],
        "hidden_abilities": ["Rough Skin"]
    },
    {
        "name": "Garchomp",
        "base_stats": {"hp": 108, "attack": 130, "defense": 95, "sp_attack": 80, "sp_defense": 85, "speed": 102},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Veil"],
        "hidden_abilities": ["Rough Skin"]
    },
    {
        "name": "Munchlax",
        "base_stats": {"hp": 135, "attack": 85, "defense": 40, "sp_attack": 40, "sp_defense": 85, "speed": 5},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Pickup", "Thick Fat"],
        "hidden_abilities": ["Gluttony"]
    },
    {
        "name": "Riolu",
        "base_stats": {"hp": 40, "attack": 70, "defense": 40, "sp_attack": 35, "sp_defense": 40, "speed": 60},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Steadfast", "Inner Focus"],
        "hidden_abilities": ["Prankster"]
    },
    {
        "name": "Lucario",
        "base_stats": {"hp": 70, "attack": 110, "defense": 70, "sp_attack": 115, "sp_defense": 70, "speed": 90},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Steadfast", "Inner Focus"],
        "hidden_abilities": ["Justified"]
    },
    {
        "name": "Hippopotas",
        "base_stats": {"hp": 68, "attack": 72, "defense": 78, "sp_attack": 38, "sp_defense": 42, "speed": 32},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Stream"],
        "hidden_abilities": ["Sand Force"]
    },
    {
        "name": "Hippowdon",
        "base_stats": {"hp": 108, "attack": 112, "defense": 118, "sp_attack": 68, "sp_defense": 72, "speed": 47},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Stream"],
        "hidden_abilities": ["Sand Force"]
    },
    {
        "name": "Skorupi",
        "base_stats": {"hp": 40, "attack": 50, "defense": 90, "sp_attack": 30, "sp_defense": 55, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Battle Armor", "Sniper"],
        "hidden_abilities": ["Keen Eye"]
    },
    {
        "name": "Drapion",
        "base_stats": {"hp": 70, "attack": 90, "defense": 110, "sp_attack": 60, "sp_defense": 75, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Battle Armor", "Sniper"],
        "hidden_abilities": ["Keen Eye"]
    },
    {
        "name": "Croagunk",
        "base_stats": {"hp": 48, "attack": 61, "defense": 40, "sp_attack": 61, "sp_defense": 40, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Anticipation", "Dry Skin"],
        "hidden_abilities": ["Poison Touch"]
    },
    {
        "name": "Toxicroak",
        "base_stats": {"hp": 83, "attack": 106, "defense": 65, "sp_attack": 86, "sp_defense": 65, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Anticipation", "Dry Skin"],
        "hidden_abilities": ["Poison Touch"]
    },
    {
        "name": "Carnivine",
        "base_stats": {"hp": 74, "attack": 100, "defense": 72, "sp_attack": 90, "sp_defense": 72, "speed": 46},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Finneon",
        "base_stats": {"hp": 49, "attack": 49, "defense": 56, "sp_attack": 49, "sp_defense": 61, "speed": 66},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Storm Drain"],
        "hidden_abilities": ["Water Veil"]
    },
    {
        "name": "Lumineon",
        "base_stats": {"hp": 69, "attack": 69, "defense": 76, "sp_attack": 69, "sp_defense": 86, "speed": 91},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Storm Drain"],
        "hidden_abilities": ["Water Veil"]
    },
    {
        "name": "Mantyke",
        "base_stats": {"hp": 45, "attack": 20, "defense": 50, "sp_attack": 60, "sp_defense": 120, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Water Absorb"],
        "hidden_abilities": ["Water Veil"]
    },
    {
        "name": "Snover",
        "base_stats": {"hp": 60, "attack": 62, "defense": 50, "sp_attack": 62, "sp_defense": 60, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Snow Warning"],
        "hidden_abilities": ["Soundproof"]
    },
    {
        "name": "Abomasnow",
        "base_stats": {"hp": 90, "attack": 92, "defense": 75, "sp_attack": 92, "sp_defense": 85, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Snow Warning"],
        "hidden_abilities": ["Soundproof"]
    },
    {
        "name": "Weavile",
        "base_stats": {"hp": 70, "attack": 120, "defense": 65, "sp_attack": 45, "sp_defense": 85, "speed": 125},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pressure"],
        "hidden_abilities": ["Pickpocket"]
    },
    {
        "name": "Magnezone",
        "base_stats": {"hp": 70, "attack": 70, "defense": 115, "sp_attack": 130, "sp_defense": 90, "speed": 60},
        "gender_ratio": None,
        "abilities": ["Magnet Pull", "Sturdy"],
        "hidden_abilities": ["Analytic"]
    },
    {
        "name": "Lickilicky",
        "base_stats": {"hp": 110, "attack": 85, "defense": 95, "sp_attack": 80, "sp_defense": 95, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Own Tempo", "Oblivious"],
        "hidden_abilities": ["Cloud Nine"]
    },
    {
        "name": "Rhyperior",
        "base_stats": {"hp": 115, "attack": 140, "defense": 130, "sp_attack": 55, "sp_defense": 55, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Lightning Rod", "Solid Rock"],
        "hidden_abilities": ["Reckless"]
    },
    {
        "name": "Tangrowth",
        "base_stats": {"hp": 100, "attack": 100, "defense": 125, "sp_attack": 110, "sp_defense": 50, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Leaf Guard"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Electivire",
        "base_stats": {"hp": 75, "attack": 123, "defense": 67, "sp_attack": 95, "sp_defense": 85, "speed": 95},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Motor Drive"],
        "hidden_abilities": ["Vital Spirit"]
    },
    {
        "name": "Magmortar",
        "base_stats": {"hp": 75, "attack": 95, "defense": 67, "sp_attack": 125, "sp_defense": 95, "speed": 83},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Flame Body"],
        "hidden_abilities": ["Vital Spirit"]
    },
    {
        "name": "Togekiss",
        "base_stats": {"hp": 85, "attack": 50, "defense": 95, "sp_attack": 120, "sp_defense": 115, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hustle", "Serene Grace"],
        "hidden_abilities": ["Super Luck"]
    },
    {
        "name": "Yanmega",
        "base_stats": {"hp": 86, "attack": 76, "defense": 86, "sp_attack": 116, "sp_defense": 56, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Speed Boost", "Tinted Lens"],
        "hidden_abilities": ["Frisk"]
    },
    {
        "name": "Leafeon",
        "base_stats": {"hp": 65, "attack": 110, "defense": 130, "sp_attack": 60, "sp_defense": 65, "speed": 95},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Leaf Guard"],
        "hidden_abilities": ["Chlorophyll"]
    },
    {
        "name": "Glaceon",
        "base_stats": {"hp": 65, "attack": 60, "defense": 110, "sp_attack": 130, "sp_defense": 95, "speed": 65},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Snow Cloak"],
        "hidden_abilities": ["Ice Body"]
    },
    {
        "name": "Gliscor",
        "base_stats": {"hp": 75, "attack": 95, "defense": 125, "sp_attack": 45, "sp_defense": 75, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hyper Cutter", "Sand Veil"],
        "hidden_abilities": ["Poison Heal"]
    },
    {
        "name": "Mamoswine",
        "base_stats": {"hp": 110, "attack": 130, "defense": 80, "sp_attack": 70, "sp_defense": 60, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Oblivious", "Snow Cloak"],
        "hidden_abilities": ["Thick Fat"]
    },
    {
        "name": "Porygon-Z",
        "base_stats": {"hp": 85, "attack": 80, "defense": 70, "sp_attack": 135, "sp_defense": 75, "speed": 90},
        "gender_ratio": None,
        "abilities": ["Adaptability", "Download"],
        "hidden_abilities": ["Analytic"]
    },
    {
        "name": "Gallade",
        "base_stats": {"hp": 68, "attack": 125, "defense": 65, "sp_attack": 65, "sp_defense": 115, "speed": 80},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Steadfast"],
        "hidden_abilities": ["Justified"]
    },
    {
        "name": "Probopass",
        "base_stats": {"hp": 60, "attack": 55, "defense": 145, "sp_attack": 75, "sp_defense": 150, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy", "Magnet Pull"],
        "hidden_abilities": ["Sand Force"]
    },
    {
        "name": "Dusknoir",
        "base_stats": {"hp": 45, "attack": 100, "defense": 135, "sp_attack": 65, "sp_defense": 135, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pressure"],
        "hidden_abilities": ["Frisk"]
    },
    {
        "name": "Froslass",
        "base_stats": {"hp": 70, "attack": 80, "defense": 70, "sp_attack": 80, "sp_defense": 70, "speed": 110},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Snow Cloak"],
        "hidden_abilities": ["Cursed Body"]
    },
    {
        "name": "Rotom",
        "base_stats": {"hp": 50, "attack": 50, "defense": 77, "sp_attack": 95, "sp_defense": 77, "speed": 91},
        "gender_ratio": None,
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Uxie",
        "base_stats": {"hp": 75, "attack": 75, "defense": 130, "sp_attack": 75, "sp_defense": 130, "speed": 95},
        "gender_ratio": None,
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Mesprit",
        "base_stats": {"hp": 80, "attack": 105, "defense": 105, "sp_attack": 105, "sp_defense": 105, "speed": 80},
        "gender_ratio": None,
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Azelf",
        "base_stats": {"hp": 75, "attack": 125, "defense": 70, "sp_attack": 125, "sp_defense": 70, "speed": 115},
        "gender_ratio": None,
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Dialga",
        "base_stats": {"hp": 100, "attack": 120, "defense": 120, "sp_attack": 150, "sp_defense": 100, "speed": 90},
        "gender_ratio": None,
        "abilities": ["Pressure"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Palkia",
        "base_stats": {"hp": 90, "attack": 120, "defense": 100, "sp_attack": 150, "sp_defense": 120, "speed": 100},
        "gender_ratio": None,
        "abilities": ["Pressure"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Heatran",
        "base_stats": {"hp": 91, "attack": 90, "defense": 106, "sp_attack": 130, "sp_defense": 106, "speed": 77},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Flash Fire"],
        "hidden_abilities": ["Flame Body"]
    },
    {
        "name": "Regigigas",
        "base_stats": {"hp": 110, "attack": 160, "defense": 110, "sp_attack": 80, "sp_defense": 110, "speed": 100},
        "gender_ratio": None,
        "abilities": ["Slow Start"],
        "hidden_abilities": []
    },
    {
        "name": "Giratina",
        "base_stats": {"hp": 150, "attack": 100, "defense": 120, "sp_attack": 100, "sp_defense": 120, "speed": 90},
        "gender_ratio": None,
        "abilities": ["Pressure"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Cresselia",
        "base_stats": {"hp": 120, "attack": 70, "defense": 120, "sp_attack": 75, "sp_defense": 130, "speed": 85},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Phione",
        "base_stats": {"hp": 80, "attack": 80, "defense": 80, "sp_attack": 80, "sp_defense": 80, "speed": 80},
        "gender_ratio": None,
        "abilities": ["Hydration"],
        "hidden_abilities": []
    },
    {
        "name": "Manaphy",
        "base_stats": {"hp": 100, "attack": 100, "defense": 100, "sp_attack": 100, "sp_defense": 100, "speed": 100},
        "gender_ratio": None,
        "abilities": ["Hydration"],
        "hidden_abilities": []
    },
    {
        "name": "Darkrai",
        "base_stats": {"hp": 70, "attack": 90, "defense": 90, "sp_attack": 135, "sp_defense": 90, "speed": 125},
        "gender_ratio": None,
        "abilities": ["Bad Dreams"],
        "hidden_abilities": []
    },
    {
        "name": "Shaymin",
        "base_stats": {"hp": 100, "attack": 100, "defense": 100, "sp_attack": 100, "sp_defense": 100, "speed": 100},
        "gender_ratio": None,
        "abilities": ["Natural Cure"],
        "hidden_abilities": []
    },
    {
        "name": "Arceus",
        "base_stats": {"hp": 120, "attack": 120, "defense": 120, "sp_attack": 120, "sp_defense": 120, "speed": 120},
        "gender_ratio": None,
        "abilities": ["Multitype"],
        "hidden_abilities": []
    }
]
POKEMON_GEN5 = [
    {
        "name": "Snivy",
        "base_stats": {"hp": 45, "attack": 45, "defense": 55, "sp_attack": 45, "sp_defense": 55, "speed": 63},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Contrary"]
    },
    {
        "name": "Servine",
        "base_stats": {"hp": 60, "attack": 60, "defense": 75, "sp_attack": 60, "sp_defense": 75, "speed": 83},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Contrary"]
    },
    {
        "name": "Serperior",
        "base_stats": {"hp": 75, "attack": 75, "defense": 95, "sp_attack": 75, "sp_defense": 95, "speed": 113},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Contrary"]
    },
    {
        "name": "Tepig",
        "base_stats": {"hp": 65, "attack": 63, "defense": 45, "sp_attack": 45, "sp_defense": 45, "speed": 45},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Thick Fat"]
    },
    {
        "name": "Pignite",
        "base_stats": {"hp": 90, "attack": 93, "defense": 55, "sp_attack": 70, "sp_defense": 55, "speed": 55},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Thick Fat"]
    },
    {
        "name": "Emboar",
        "base_stats": {"hp": 110, "attack": 123, "defense": 65, "sp_attack": 100, "sp_defense": 65, "speed": 65},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Reckless"]
    },
    {
        "name": "Oshawott",
        "base_stats": {"hp": 55, "attack": 55, "defense": 45, "sp_attack": 63, "sp_defense": 45, "speed": 45},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Shell Armor"]
    },
    {
        "name": "Dewott",
        "base_stats": {"hp": 75, "attack": 75, "defense": 60, "sp_attack": 83, "sp_defense": 60, "speed": 60},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Shell Armor"]
    },
    {
        "name": "Samurott",
        "base_stats": {"hp": 95, "attack": 100, "defense": 85, "sp_attack": 108, "sp_defense": 70, "speed": 70},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Shell Armor"]
    },
    {
        "name": "Patrat",
        "base_stats": {"hp": 45, "attack": 55, "defense": 39, "sp_attack": 35, "sp_defense": 39, "speed": 42},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Keen Eye"],
        "hidden_abilities": ["Analytic"]
    },
    {
        "name": "Watchog",
        "base_stats": {"hp": 60, "attack": 85, "defense": 69, "sp_attack": 60, "sp_defense": 69, "speed": 77},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Illuminate", "Keen Eye"],
        "hidden_abilities": ["Analytic"]
    },
    {
        "name": "Lillipup",
        "base_stats": {"hp": 45, "attack": 60, "defense": 45, "sp_attack": 25, "sp_defense": 45, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Vital Spirit", "Pickup"],
        "hidden_abilities": ["Run Away"]
    },
    {
        "name": "Herdier",
        "base_stats": {"hp": 65, "attack": 80, "defense": 65, "sp_attack": 35, "sp_defense": 65, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate", "Sand Rush"],
        "hidden_abilities": ["Scrappy"]
    },
    {
        "name": "Stoutland",
        "base_stats": {"hp": 85, "attack": 110, "defense": 90, "sp_attack": 45, "sp_defense": 90, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate", "Sand Rush"],
        "hidden_abilities": ["Scrappy"]
    },
    {
        "name": "Purrloin",
        "base_stats": {"hp": 41, "attack": 50, "defense": 37, "sp_attack": 50, "sp_defense": 37, "speed": 66},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Limber", "Unburden"],
        "hidden_abilities": ["Prankster"]
    },
    {
        "name": "Liepard",
        "base_stats": {"hp": 64, "attack": 88, "defense": 50, "sp_attack": 88, "sp_defense": 50, "speed": 106},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Limber", "Unburden"],
        "hidden_abilities": ["Prankster"]
    },
    {
        "name": "Pansage",
        "base_stats": {"hp": 50, "attack": 53, "defense": 48, "sp_attack": 53, "sp_defense": 48, "speed": 64},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Gluttony"],
        "hidden_abilities": ["Overgrow"]
    },
    {
        "name": "Simisage",
        "base_stats": {"hp": 75, "attack": 98, "defense": 63, "sp_attack": 98, "sp_defense": 63, "speed": 101},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Gluttony"],
        "hidden_abilities": ["Overgrow"]
    },
    {
        "name": "Pansear",
        "base_stats": {"hp": 50, "attack": 53, "defense": 48, "sp_attack": 53, "sp_defense": 48, "speed": 64},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Gluttony"],
        "hidden_abilities": ["Blaze"]
    },
    {
        "name": "Simisear",
        "base_stats": {"hp": 75, "attack": 98, "defense": 63, "sp_attack": 98, "sp_defense": 63, "speed": 101},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Gluttony"],
        "hidden_abilities": ["Blaze"]
    },
    {
        "name": "Panpour",
        "base_stats": {"hp": 50, "attack": 53, "defense": 48, "sp_attack": 53, "sp_defense": 48, "speed": 64},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Gluttony"],
        "hidden_abilities": ["Torrent"]
    },
    {
        "name": "Simipour",
        "base_stats": {"hp": 75, "attack": 98, "defense": 63, "sp_attack": 98, "sp_defense": 63, "speed": 101},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Gluttony"],
        "hidden_abilities": ["Torrent"]
    },
    {
        "name": "Munna",
        "base_stats": {"hp": 76, "attack": 25, "defense": 45, "sp_attack": 67, "sp_defense": 55, "speed": 24},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Forewarn", "Synchronize"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Musharna",
        "base_stats": {"hp": 116, "attack": 55, "defense": 85, "sp_attack": 107, "sp_defense": 95, "speed": 29},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Forewarn", "Synchronize"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Pidove",
        "base_stats": {"hp": 50, "attack": 55, "defense": 50, "sp_attack": 36, "sp_defense": 30, "speed": 43},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Big Pecks", "Super Luck"],
        "hidden_abilities": ["Rivalry"]
    },
    {
        "name": "Tranquill",
        "base_stats": {"hp": 62, "attack": 77, "defense": 62, "sp_attack": 50, "sp_defense": 42, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Big Pecks", "Super Luck"],
        "hidden_abilities": ["Rivalry"]
    },
    {
        "name": "Unfezant",
        "base_stats": {"hp": 80, "attack": 115, "defense": 80, "sp_attack": 65, "sp_defense": 55, "speed": 93},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Big Pecks", "Super Luck"],
        "hidden_abilities": ["Rivalry"]
    },
    {
        "name": "Blitzle",
        "base_stats": {"hp": 45, "attack": 60, "defense": 32, "sp_attack": 50, "sp_defense": 32, "speed": 76},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Lightning Rod", "Motor Drive"],
        "hidden_abilities": ["Sap Sipper"]
    },
    {
        "name": "Zebstrika",
        "base_stats": {"hp": 75, "attack": 100, "defense": 63, "sp_attack": 80, "sp_defense": 63, "speed": 116},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Lightning Rod", "Motor Drive"],
        "hidden_abilities": ["Sap Sipper"]
    },
    {
        "name": "Roggenrola",
        "base_stats": {"hp": 55, "attack": 75, "defense": 85, "sp_attack": 25, "sp_defense": 25, "speed": 15},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy", "Weak Armor"],
        "hidden_abilities": ["Sand Force"]
    },
    {
        "name": "Boldore",
        "base_stats": {"hp": 70, "attack": 105, "defense": 105, "sp_attack": 50, "sp_defense": 40, "speed": 20},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy", "Weak Armor"],
        "hidden_abilities": ["Sand Force"]
    },
    {
        "name": "Gigalith",
        "base_stats": {"hp": 85, "attack": 135, "defense": 130, "sp_attack": 60, "sp_defense": 80, "speed": 25},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy", "Sand Stream"],
        "hidden_abilities": ["Sand Force"]
    },
    {
        "name": "Woobat",
        "base_stats": {"hp": 65, "attack": 45, "defense": 43, "sp_attack": 55, "sp_defense": 43, "speed": 72},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Unaware", "Klutz"],
        "hidden_abilities": ["Simple"]
    },
    {
        "name": "Swoobat",
        "base_stats": {"hp": 67, "attack": 57, "defense": 55, "sp_attack": 77, "sp_defense": 55, "speed": 114},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Unaware", "Klutz"],
        "hidden_abilities": ["Simple"]
    },
    {
        "name": "Drilbur",
        "base_stats": {"hp": 60, "attack": 85, "defense": 40, "sp_attack": 30, "sp_defense": 45, "speed": 68},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Rush", "Sand Force"],
        "hidden_abilities": ["Mold Breaker"]
    },
    {
        "name": "Excadrill",
        "base_stats": {"hp": 110, "attack": 135, "defense": 60, "sp_attack": 50, "sp_defense": 65, "speed": 88},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Rush", "Sand Force"],
        "hidden_abilities": ["Mold Breaker"]
    },
    {
        "name": "Audino",
        "base_stats": {"hp": 103, "attack": 60, "defense": 86, "sp_attack": 60, "sp_defense": 86, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Healer", "Regenerator"],
        "hidden_abilities": ["Klutz"]
    },
    {
        "name": "Timburr",
        "base_stats": {"hp": 75, "attack": 80, "defense": 55, "sp_attack": 25, "sp_defense": 35, "speed": 35},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Guts", "Sheer Force"],
        "hidden_abilities": ["Iron Fist"]
    },
    {
        "name": "Gurdurr",
        "base_stats": {"hp": 85, "attack": 105, "defense": 85, "sp_attack": 40, "sp_defense": 50, "speed": 40},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Guts", "Sheer Force"],
        "hidden_abilities": ["Iron Fist"]
    },
    {
        "name": "Conkeldurr",
        "base_stats": {"hp": 105, "attack": 140, "defense": 95, "sp_attack": 55, "sp_defense": 65, "speed": 45},
        "gender_ratio": {"male": 75, "female": 25},
        "abilities": ["Guts", "Sheer Force"],
        "hidden_abilities": ["Iron Fist"]
    },
    {
        "name": "Tympole",
        "base_stats": {"hp": 50, "attack": 50, "defense": 40, "sp_attack": 50, "sp_defense": 40, "speed": 64},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Hydration"],
        "hidden_abilities": ["Water Absorb"]
    },
    {
        "name": "Palpitoad",
        "base_stats": {"hp": 75, "attack": 65, "defense": 55, "sp_attack": 65, "sp_defense": 55, "speed": 69},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Hydration"],
        "hidden_abilities": ["Water Absorb"]
    },
    {
        "name": "Seismitoad",
        "base_stats": {"hp": 105, "attack": 95, "defense": 75, "sp_attack": 85, "sp_defense": 75, "speed": 74},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Poison Touch"],
        "hidden_abilities": ["Water Absorb"]
    },
    {
        "name": "Throh",
        "base_stats": {"hp": 120, "attack": 100, "defense": 85, "sp_attack": 30, "sp_defense": 85, "speed": 45},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Guts", "Inner Focus"],
        "hidden_abilities": ["Mold Breaker"]
    },
    {
        "name": "Sawk",
        "base_stats": {"hp": 75, "attack": 125, "defense": 75, "sp_attack": 30, "sp_defense": 75, "speed": 85},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Sturdy", "Inner Focus"],
        "hidden_abilities": ["Mold Breaker"]
    },
    {
        "name": "Sewaddle",
        "base_stats": {"hp": 45, "attack": 53, "defense": 70, "sp_attack": 40, "sp_defense": 60, "speed": 42},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm", "Chlorophyll"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Swadloon",
        "base_stats": {"hp": 55, "attack": 63, "defense": 90, "sp_attack": 50, "sp_defense": 80, "speed": 42},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Leaf Guard", "Chlorophyll"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Leavanny",
        "base_stats": {"hp": 75, "attack": 103, "defense": 80, "sp_attack": 70, "sp_defense": 80, "speed": 92},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm", "Chlorophyll"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Venipede",
        "base_stats": {"hp": 30, "attack": 45, "defense": 59, "sp_attack": 30, "sp_defense": 39, "speed": 57},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Poison Point", "Swarm"],
        "hidden_abilities": ["Speed Boost"]
    },
    {
        "name": "Whirlipede",
        "base_stats": {"hp": 40, "attack": 55, "defense": 99, "sp_attack": 40, "sp_defense": 79, "speed": 47},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Poison Point", "Swarm"],
        "hidden_abilities": ["Speed Boost"]
    },
    {
        "name": "Scolipede",
        "base_stats": {"hp": 60, "attack": 100, "defense": 89, "sp_attack": 55, "sp_defense": 69, "speed": 112},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Poison Point", "Swarm"],
        "hidden_abilities": ["Speed Boost"]
    },
    {
        "name": "Cottonee",
        "base_stats": {"hp": 40, "attack": 27, "defense": 60, "sp_attack": 37, "sp_defense": 50, "speed": 66},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Prankster", "Infiltrator"],
        "hidden_abilities": ["Chlorophyll"]
    },
    {
        "name": "Whimsicott",
        "base_stats": {"hp": 60, "attack": 67, "defense": 85, "sp_attack": 77, "sp_defense": 75, "speed": 116},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Prankster", "Infiltrator"],
        "hidden_abilities": ["Chlorophyll"]
    },
    {
        "name": "Petilil",
        "base_stats": {"hp": 45, "attack": 35, "defense": 50, "sp_attack": 70, "sp_defense": 50, "speed": 30},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Chlorophyll", "Own Tempo"],
        "hidden_abilities": ["Leaf Guard"]
    },
    {
        "name": "Lilligant",
        "base_stats": {"hp": 70, "attack": 60, "defense": 75, "sp_attack": 110, "sp_defense": 75, "speed": 90},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Chlorophyll", "Own Tempo"],
        "hidden_abilities": ["Leaf Guard"]
    },
    {
        "name": "Basculin",
        "base_stats": {"hp": 70, "attack": 92, "defense": 65, "sp_attack": 80, "sp_defense": 55, "speed": 98},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Reckless", "Adaptability"],
        "hidden_abilities": ["Mold Breaker"]
    },
    {
        "name": "Sandile",
        "base_stats": {"hp": 50, "attack": 72, "defense": 35, "sp_attack": 35, "sp_defense": 35, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate", "Moxie"],
        "hidden_abilities": ["Anger Point"]
    },
    {
        "name": "Krokorok",
        "base_stats": {"hp": 60, "attack": 82, "defense": 45, "sp_attack": 45, "sp_defense": 45, "speed": 74},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate", "Moxie"],
        "hidden_abilities": ["Anger Point"]
    },
    {
        "name": "Krookodile",
        "base_stats": {"hp": 95, "attack": 117, "defense": 80, "sp_attack": 65, "sp_defense": 70, "speed": 92},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate", "Moxie"],
        "hidden_abilities": ["Anger Point"]
    },
    {
        "name": "Darumaka",
        "base_stats": {"hp": 70, "attack": 90, "defense": 45, "sp_attack": 15, "sp_defense": 45, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hustle"],
        "hidden_abilities": ["Inner Focus"]
    },
    {
        "name": "Darmanitan",
        "base_stats": {"hp": 105, "attack": 140, "defense": 55, "sp_attack": 30, "sp_defense": 55, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sheer Force"],
        "hidden_abilities": ["Zen Mode"]
    },
    {
        "name": "Maractus",
        "base_stats": {"hp": 75, "attack": 86, "defense": 67, "sp_attack": 106, "sp_defense": 67, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Absorb", "Chlorophyll"],
        "hidden_abilities": ["Storm Drain"]
    },
    {
        "name": "Dwebble",
        "base_stats": {"hp": 50, "attack": 65, "defense": 85, "sp_attack": 35, "sp_defense": 35, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy", "Shell Armor"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Crustle",
        "base_stats": {"hp": 70, "attack": 105, "defense": 125, "sp_attack": 65, "sp_defense": 75, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sturdy", "Shell Armor"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Scraggy",
        "base_stats": {"hp": 50, "attack": 75, "defense": 70, "sp_attack": 35, "sp_defense": 70, "speed": 48},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shed Skin", "Moxie"],
        "hidden_abilities": ["Intimidate"]
    },
    {
        "name": "Scrafty",
        "base_stats": {"hp": 65, "attack": 90, "defense": 115, "sp_attack": 45, "sp_defense": 115, "speed": 58},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shed Skin", "Moxie"],
        "hidden_abilities": ["Intimidate"]
    },
    {
        "name": "Sigilyph",
        "base_stats": {"hp": 72, "attack": 58, "defense": 80, "sp_attack": 103, "sp_defense": 80, "speed": 97},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Wonder Skin", "Magic Guard"],
        "hidden_abilities": ["Tinted Lens"]
    },
    {
        "name": "Yamask",
        "base_stats": {"hp": 38, "attack": 30, "defense": 85, "sp_attack": 55, "sp_defense": 65, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Mummy"],
        "hidden_abilities": []
    },
    {
        "name": "Cofagrigus",
        "base_stats": {"hp": 58, "attack": 50, "defense": 145, "sp_attack": 95, "sp_defense": 105, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Mummy"],
        "hidden_abilities": []
    },
    {
        "name": "Tirtouga",
        "base_stats": {"hp": 54, "attack": 78, "defense": 103, "sp_attack": 53, "sp_defense": 45, "speed": 22},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Solid Rock", "Sturdy"],
        "hidden_abilities": ["Swift Swim"]
    },
    {
        "name": "Carracosta",
        "base_stats": {"hp": 74, "attack": 108, "defense": 133, "sp_attack": 83, "sp_defense": 65, "speed": 32},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Solid Rock", "Sturdy"],
        "hidden_abilities": ["Swift Swim"]
    },
    {
        "name": "Archen",
        "base_stats": {"hp": 55, "attack": 112, "defense": 45, "sp_attack": 74, "sp_defense": 45, "speed": 70},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Defeatist"],
        "hidden_abilities": []
    },
    {
        "name": "Archeops",
        "base_stats": {"hp": 75, "attack": 140, "defense": 65, "sp_attack": 112, "sp_defense": 65, "speed": 110},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Defeatist"],
        "hidden_abilities": []
    },
    {
        "name": "Trubbish",
        "base_stats": {"hp": 50, "attack": 50, "defense": 62, "sp_attack": 40, "sp_defense": 62, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Stench", "Sticky Hold"],
        "hidden_abilities": ["Aftermath"]
    },
    {
        "name": "Garbodor",
        "base_stats": {"hp": 80, "attack": 95, "defense": 82, "sp_attack": 60, "sp_defense": 82, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Stench", "Weak Armor"],
        "hidden_abilities": ["Aftermath"]
    },
    {
        "name": "Zorua",
        "base_stats": {"hp": 40, "attack": 65, "defense": 40, "sp_attack": 80, "sp_defense": 40, "speed": 65},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Illusion"],
        "hidden_abilities": []
    },
    {
        "name": "Zoroark",
        "base_stats": {"hp": 60, "attack": 105, "defense": 60, "sp_attack": 120, "sp_defense": 60, "speed": 105},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Illusion"],
        "hidden_abilities": []
    },
    {
        "name": "Minccino",
        "base_stats": {"hp": 55, "attack": 50, "defense": 40, "sp_attack": 40, "sp_defense": 40, "speed": 75},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Cute Charm", "Technician"],
        "hidden_abilities": ["Skill Link"]
    },
    {
        "name": "Cinccino",
        "base_stats": {"hp": 75, "attack": 95, "defense": 60, "sp_attack": 65, "sp_defense": 60, "speed": 115},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Cute Charm", "Technician"],
        "hidden_abilities": ["Skill Link"]
    },
    {
        "name": "Gothita",
        "base_stats": {"hp": 45, "attack": 30, "defense": 50, "sp_attack": 55, "sp_defense": 65, "speed": 45},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Frisk", "Competitive"],
        "hidden_abilities": ["Shadow Tag"]
    },
    {
        "name": "Gothorita",
        "base_stats": {"hp": 60, "attack": 45, "defense": 70, "sp_attack": 75, "sp_defense": 85, "speed": 55},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Frisk", "Competitive"],
        "hidden_abilities": ["Shadow Tag"]
    },
    {
        "name": "Gothitelle",
        "base_stats": {"hp": 70, "attack": 55, "defense": 95, "sp_attack": 95, "sp_defense": 110, "speed": 65},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Frisk", "Competitive"],
        "hidden_abilities": ["Shadow Tag"]
    },
    {
        "name": "Solosis",
        "base_stats": {"hp": 45, "attack": 30, "defense": 40, "sp_attack": 105, "sp_defense": 50, "speed": 20},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Overcoat", "Magic Guard"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Duosion",
        "base_stats": {"hp": 65, "attack": 40, "defense": 50, "sp_attack": 125, "sp_defense": 60, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Overcoat", "Magic Guard"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Reuniclus",
        "base_stats": {"hp": 110, "attack": 65, "defense": 75, "sp_attack": 125, "sp_defense": 85, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Overcoat", "Magic Guard"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Ducklett",
        "base_stats": {"hp": 62, "attack": 44, "defense": 50, "sp_attack": 44, "sp_defense": 50, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Big Pecks"],
        "hidden_abilities": ["Hydration"]
    },
    {
        "name": "Swanna",
        "base_stats": {"hp": 75, "attack": 87, "defense": 63, "sp_attack": 87, "sp_defense": 63, "speed": 98},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Big Pecks"],
        "hidden_abilities": ["Hydration"]
    },
    {
        "name": "Vanillite",
        "base_stats": {"hp": 36, "attack": 50, "defense": 50, "sp_attack": 65, "sp_defense": 60, "speed": 44},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Ice Body", "Snow Cloak"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Vanillish",
        "base_stats": {"hp": 51, "attack": 65, "defense": 65, "sp_attack": 80, "sp_defense": 75, "speed": 59},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Ice Body", "Snow Cloak"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Vanilluxe",
        "base_stats": {"hp": 71, "attack": 95, "defense": 85, "sp_attack": 110, "sp_defense": 95, "speed": 79},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Ice Body", "Snow Warning"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Deerling",
        "base_stats": {"hp": 60, "attack": 60, "defense": 50, "sp_attack": 40, "sp_defense": 50, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Sap Sipper"],
        "hidden_abilities": ["Serene Grace"]
    },
    {
        "name": "Sawsbuck",
        "base_stats": {"hp": 80, "attack": 100, "defense": 70, "sp_attack": 60, "sp_defense": 70, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Sap Sipper"],
        "hidden_abilities": ["Serene Grace"]
    },
    {
        "name": "Emolga",
        "base_stats": {"hp": 55, "attack": 75, "defense": 60, "sp_attack": 75, "sp_defense": 60, "speed": 103},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Static"],
        "hidden_abilities": ["Motor Drive"]
    },
    {
        "name": "Karrablast",
        "base_stats": {"hp": 50, "attack": 75, "defense": 45, "sp_attack": 40, "sp_defense": 45, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm", "Shed Skin"],
        "hidden_abilities": ["No Guard"]
    },
    {
        "name": "Escavalier",
        "base_stats": {"hp": 70, "attack": 135, "defense": 105, "sp_attack": 60, "sp_defense": 105, "speed": 20},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm", "Shell Armor"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Foongus",
        "base_stats": {"hp": 69, "attack": 55, "defense": 45, "sp_attack": 55, "sp_defense": 55, "speed": 15},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Effect Spore"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Amoonguss",
        "base_stats": {"hp": 114, "attack": 85, "defense": 70, "sp_attack": 85, "sp_defense": 80, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Effect Spore"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Frillish",
        "base_stats": {"hp": 55, "attack": 40, "defense": 50, "sp_attack": 65, "sp_defense": 85, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Absorb", "Cursed Body"],
        "hidden_abilities": ["Damp"]
    },
    {
        "name": "Jellicent",
        "base_stats": {"hp": 100, "attack": 60, "defense": 70, "sp_attack": 85, "sp_defense": 105, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Absorb", "Cursed Body"],
        "hidden_abilities": ["Damp"]
    },
    {
        "name": "Alomomola",
        "base_stats": {"hp": 165, "attack": 75, "defense": 80, "sp_attack": 40, "sp_defense": 45, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Healer", "Hydration"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Joltik",
        "base_stats": {"hp": 50, "attack": 47, "defense": 50, "sp_attack": 57, "sp_defense": 50, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Compound Eyes", "Unnerve"],
        "hidden_abilities": ["Swarm"]
    },
    {
        "name": "Galvantula",
        "base_stats": {"hp": 70, "attack": 77, "defense": 60, "sp_attack": 97, "sp_defense": 60, "speed": 108},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Compound Eyes", "Unnerve"],
        "hidden_abilities": ["Swarm"]
    },
    {
        "name": "Ferroseed",
        "base_stats": {"hp": 44, "attack": 50, "defense": 91, "sp_attack": 24, "sp_defense": 86, "speed": 10},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Iron Barbs"],
        "hidden_abilities": []
    },
    {
        "name": "Ferrothorn",
        "base_stats": {"hp": 74, "attack": 94, "defense": 131, "sp_attack": 54, "sp_defense": 116, "speed": 20},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Iron Barbs"],
        "hidden_abilities": []
    },
    {
        "name": "Klink",
        "base_stats": {"hp": 40, "attack": 55, "defense": 70, "sp_attack": 45, "sp_defense": 60, "speed": 30},
        "gender_ratio": None,
        "abilities": ["Plus", "Minus"],
        "hidden_abilities": ["Clear Body"]
    },
    {
        "name": "Klang",
        "base_stats": {"hp": 60, "attack": 80, "defense": 95, "sp_attack": 70, "sp_defense": 85, "speed": 50},
        "gender_ratio": None,
        "abilities": ["Plus", "Minus"],
        "hidden_abilities": ["Clear Body"]
    },
    {
        "name": "Klinklang",
        "base_stats": {"hp": 60, "attack": 100, "defense": 115, "sp_attack": 70, "sp_defense": 85, "speed": 90},
        "gender_ratio": None,
        "abilities": ["Plus", "Minus"],
        "hidden_abilities": ["Clear Body"]
    },
    {
        "name": "Tynamo",
        "base_stats": {"hp": 35, "attack": 55, "defense": 40, "sp_attack": 45, "sp_defense": 40, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Eelektrik",
        "base_stats": {"hp": 65, "attack": 85, "defense": 70, "sp_attack": 75, "sp_defense": 70, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Eelektross",
        "base_stats": {"hp": 85, "attack": 115, "defense": 80, "sp_attack": 105, "sp_defense": 80, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Elgyem",
        "base_stats": {"hp": 55, "attack": 55, "defense": 55, "sp_attack": 85, "sp_defense": 55, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Telepathy", "Synchronize"],
        "hidden_abilities": ["Analytic"]
    },
    {
        "name": "Beheeyem",
        "base_stats": {"hp": 75, "attack": 75, "defense": 75, "sp_attack": 125, "sp_defense": 95, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Telepathy", "Synchronize"],
        "hidden_abilities": ["Analytic"]
    },
    {
        "name": "Litwick",
        "base_stats": {"hp": 50, "attack": 30, "defense": 55, "sp_attack": 65, "sp_defense": 55, "speed": 20},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Flash Fire", "Flame Body"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Lampent",
        "base_stats": {"hp": 60, "attack": 40, "defense": 60, "sp_attack": 95, "sp_defense": 60, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Flash Fire", "Flame Body"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Chandelure",
        "base_stats": {"hp": 60, "attack": 55, "defense": 90, "sp_attack": 145, "sp_defense": 90, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Flash Fire", "Flame Body"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Axew",
        "base_stats": {"hp": 46, "attack": 87, "defense": 60, "sp_attack": 30, "sp_defense": 40, "speed": 57},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rivalry", "Mold Breaker"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Fraxure",
        "base_stats": {"hp": 66, "attack": 117, "defense": 70, "sp_attack": 40, "sp_defense": 50, "speed": 67},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rivalry", "Mold Breaker"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Haxorus",
        "base_stats": {"hp": 76, "attack": 147, "defense": 90, "sp_attack": 60, "sp_defense": 70, "speed": 97},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rivalry", "Mold Breaker"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Cubchoo",
        "base_stats": {"hp": 55, "attack": 70, "defense": 40, "sp_attack": 60, "sp_defense": 40, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Snow Cloak"],
        "hidden_abilities": ["Rattled"]
    },
    {
        "name": "Beartic",
        "base_stats": {"hp": 95, "attack": 130, "defense": 80, "sp_attack": 70, "sp_defense": 80, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Snow Cloak"],
        "hidden_abilities": ["Swift Swim"]
    },
    {
        "name": "Cryogonal",
        "base_stats": {"hp": 80, "attack": 50, "defense": 50, "sp_attack": 95, "sp_defense": 135, "speed": 105},
        "gender_ratio": None,
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Shelmet",
        "base_stats": {"hp": 50, "attack": 40, "defense": 85, "sp_attack": 40, "sp_defense": 65, "speed": 25},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hydration", "Shell Armor"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Accelgor",
        "base_stats": {"hp": 80, "attack": 70, "defense": 40, "sp_attack": 100, "sp_defense": 60, "speed": 145},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hydration", "Sticky Hold"],
        "hidden_abilities": ["Unburden"]
    },
    {
        "name": "Stunfisk",
        "base_stats": {"hp": 109, "attack": 66, "defense": 84, "sp_attack": 81, "sp_defense": 99, "speed": 32},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Static", "Limber"],
        "hidden_abilities": ["Sand Veil"]
    },
    {
        "name": "Mienfoo",
        "base_stats": {"hp": 45, "attack": 85, "defense": 50, "sp_attack": 55, "sp_defense": 50, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Inner Focus", "Regenerator"],
        "hidden_abilities": ["Reckless"]
    },
    {
        "name": "Mienshao",
        "base_stats": {"hp": 65, "attack": 125, "defense": 60, "sp_attack": 95, "sp_defense": 60, "speed": 105},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Inner Focus", "Regenerator"],
        "hidden_abilities": ["Reckless"]
    },
    {
        "name": "Druddigon",
        "base_stats": {"hp": 77, "attack": 120, "defense": 90, "sp_attack": 60, "sp_defense": 90, "speed": 48},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rough Skin", "Sheer Force"],
        "hidden_abilities": ["Mold Breaker"]
    },
    {
        "name": "Golett",
        "base_stats": {"hp": 59, "attack": 74, "defense": 50, "sp_attack": 35, "sp_defense": 50, "speed": 35},
        "gender_ratio": None,
        "abilities": ["Iron Fist", "Klutz"],
        "hidden_abilities": ["No Guard"]
    },
    {
        "name": "Golurk",
        "base_stats": {"hp": 89, "attack": 124, "defense": 80, "sp_attack": 55, "sp_defense": 80, "speed": 55},
        "gender_ratio": None,
        "abilities": ["Iron Fist", "Klutz"],
        "hidden_abilities": ["No Guard"]
    },
    {
        "name": "Pawniard",
        "base_stats": {"hp": 45, "attack": 85, "defense": 70, "sp_attack": 40, "sp_defense": 40, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Defiant", "Inner Focus"],
        "hidden_abilities": ["Pressure"]
    },
    {
        "name": "Bisharp",
        "base_stats": {"hp": 65, "attack": 125, "defense": 100, "sp_attack": 60, "sp_defense": 70, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Defiant", "Inner Focus"],
        "hidden_abilities": ["Pressure"]
    },
    {
        "name": "Bouffalant",
        "base_stats": {"hp": 95, "attack": 110, "defense": 95, "sp_attack": 40, "sp_defense": 95, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Reckless", "Sap Sipper"],
        "hidden_abilities": ["Soundproof"]
    },
    {
        "name": "Rufflet",
        "base_stats": {"hp": 70, "attack": 83, "defense": 50, "sp_attack": 37, "sp_defense": 50, "speed": 60},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Keen Eye", "Sheer Force"],
        "hidden_abilities": ["Hustle"]
    },
    {
        "name": "Braviary",
        "base_stats": {"hp": 100, "attack": 123, "defense": 75, "sp_attack": 57, "sp_defense": 75, "speed": 80},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Keen Eye", "Sheer Force"],
        "hidden_abilities": ["Defiant"]
    },
    {
        "name": "Vullaby",
        "base_stats": {"hp": 70, "attack": 55, "defense": 75, "sp_attack": 45, "sp_defense": 65, "speed": 60},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Big Pecks", "Overcoat"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Mandibuzz",
        "base_stats": {"hp": 110, "attack": 65, "defense": 105, "sp_attack": 55, "sp_defense": 95, "speed": 80},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Big Pecks", "Overcoat"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Heatmor",
        "base_stats": {"hp": 85, "attack": 97, "defense": 66, "sp_attack": 105, "sp_defense": 66, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Gluttony", "Flash Fire"],
        "hidden_abilities": ["White Smoke"]
    },
    {
        "name": "Durant",
        "base_stats": {"hp": 58, "attack": 109, "defense": 112, "sp_attack": 48, "sp_defense": 48, "speed": 109},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm", "Hustle"],
        "hidden_abilities": ["Truant"]
    },
    {
        "name": "Deino",
        "base_stats": {"hp": 52, "attack": 65, "defense": 50, "sp_attack": 45, "sp_defense": 50, "speed": 38},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hustle"],
        "hidden_abilities": []
    },
    {
        "name": "Zweilous",
        "base_stats": {"hp": 72, "attack": 85, "defense": 70, "sp_attack": 65, "sp_defense": 70, "speed": 58},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hustle"],
        "hidden_abilities": []
    },
    {
        "name": "Hydreigon",
        "base_stats": {"hp": 92, "attack": 105, "defense": 90, "sp_attack": 125, "sp_defense": 90, "speed": 98},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Larvesta",
        "base_stats": {"hp": 55, "attack": 85, "defense": 55, "sp_attack": 50, "sp_defense": 55, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Flame Body"],
        "hidden_abilities": ["Swarm"]
    },
    {
        "name": "Volcarona",
        "base_stats": {"hp": 85, "attack": 60, "defense": 65, "sp_attack": 135, "sp_defense": 105, "speed": 100},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Flame Body"],
        "hidden_abilities": ["Swarm"]
    },
    {
        "name": "Cobalion",
        "base_stats": {"hp": 91, "attack": 90, "defense": 129, "sp_attack": 90, "sp_defense": 72, "speed": 108},
        "gender_ratio": None,
        "abilities": ["Justified"],
        "hidden_abilities": []
    },
    {
        "name": "Terrakion",
        "base_stats": {"hp": 91, "attack": 129, "defense": 90, "sp_attack": 72, "sp_defense": 90, "speed": 108},
        "gender_ratio": None,
        "abilities": ["Justified"],
        "hidden_abilities": []
    },
    {
        "name": "Virizion",
        "base_stats": {"hp": 91, "attack": 90, "defense": 72, "sp_attack": 90, "sp_defense": 129, "speed": 108},
        "gender_ratio": None,
        "abilities": ["Justified"],
        "hidden_abilities": []
    },
    {
        "name": "Tornadus",
        "base_stats": {"hp": 79, "attack": 115, "defense": 70, "sp_attack": 125, "sp_defense": 80, "speed": 111},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Prankster"],
        "hidden_abilities": ["Defiant"]
    },
    {
        "name": "Thundurus",
        "base_stats": {"hp": 79, "attack": 115, "defense": 70, "sp_attack": 125, "sp_defense": 80, "speed": 111},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Prankster"],
        "hidden_abilities": ["Defiant"]
    },
    {
        "name": "Reshiram",
        "base_stats": {"hp": 100, "attack": 120, "defense": 100, "sp_attack": 150, "sp_defense": 120, "speed": 90},
        "gender_ratio": None,
        "abilities": ["Turboblaze"],
        "hidden_abilities": []
    },
    {
        "name": "Zekrom",
        "base_stats": {"hp": 100, "attack": 150, "defense": 120, "sp_attack": 120, "sp_defense": 100, "speed": 90},
        "gender_ratio": None,
        "abilities": ["Teravolt"],
        "hidden_abilities": []
    },
    {
        "name": "Landorus",
        "base_stats": {"hp": 89, "attack": 125, "defense": 90, "sp_attack": 115, "sp_defense": 80, "speed": 101},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Sand Force"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Kyurem",
        "base_stats": {"hp": 125, "attack": 130, "defense": 90, "sp_attack": 130, "sp_defense": 90, "speed": 95},
        "gender_ratio": None,
        "abilities": ["Pressure"],
        "hidden_abilities": []
    },
    {
        "name": "Keldeo",
        "base_stats": {"hp": 91, "attack": 72, "defense": 90, "sp_attack": 129, "sp_defense": 90, "speed": 108},
        "gender_ratio": None,
        "abilities": ["Justified"],
        "hidden_abilities": []
    },
    {
        "name": "Meloetta",
        "base_stats": {"hp": 100, "attack": 77, "defense": 77, "sp_attack": 128, "sp_defense": 128, "speed": 90},
        "gender_ratio": None,
        "abilities": ["Serene Grace"],
        "hidden_abilities": []
    },
    {
        "name": "Genesect",
        "base_stats": {"hp": 71, "attack": 120, "defense": 95, "sp_attack": 120, "sp_defense": 95, "speed": 99},
        "gender_ratio": None,
        "abilities": ["Download"],
        "hidden_abilities": []
    }
]
POKEMON_GEN6 = [
    {
        "name": "Chespin",
        "base_stats": {"hp": 56, "attack": 61, "defense": 65, "sp_attack": 48, "sp_defense": 45, "speed": 38},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Bulletproof"]
    },
    {
        "name": "Quilladin",
        "base_stats": {"hp": 61, "attack": 78, "defense": 95, "sp_attack": 56, "sp_defense": 58, "speed": 57},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Bulletproof"]
    },
    {
        "name": "Chesnaught",
        "base_stats": {"hp": 88, "attack": 107, "defense": 122, "sp_attack": 74, "sp_defense": 75, "speed": 64},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Bulletproof"]
    },
    {
        "name": "Fennekin",
        "base_stats": {"hp": 40, "attack": 45, "defense": 40, "sp_attack": 62, "sp_defense": 60, "speed": 60},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Magician"]
    },
    {
        "name": "Braixen",
        "base_stats": {"hp": 59, "attack": 59, "defense": 58, "sp_attack": 90, "sp_defense": 70, "speed": 73},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Magician"]
    },
    {
        "name": "Delphox",
        "base_stats": {"hp": 75, "attack": 69, "defense": 72, "sp_attack": 114, "sp_defense": 100, "speed": 104},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Magician"]
    },
    {
        "name": "Froakie",
        "base_stats": {"hp": 41, "attack": 56, "defense": 40, "sp_attack": 62, "sp_defense": 44, "speed": 71},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Protean"]
    },
    {
        "name": "Frogadier",
        "base_stats": {"hp": 54, "attack": 63, "defense": 52, "sp_attack": 83, "sp_defense": 56, "speed": 97},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Protean"]
    },
    {
        "name": "Greninja",
        "base_stats": {"hp": 72, "attack": 95, "defense": 67, "sp_attack": 103, "sp_defense": 71, "speed": 122},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Protean"]
    },
    {
        "name": "Bunnelby",
        "base_stats": {"hp": 38, "attack": 36, "defense": 38, "sp_attack": 32, "sp_defense": 36, "speed": 57},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pickup", "Cheek Pouch"],
        "hidden_abilities": ["Huge Power"]
    },
    {
        "name": "Diggersby",
        "base_stats": {"hp": 85, "attack": 56, "defense": 77, "sp_attack": 50, "sp_defense": 77, "speed": 78},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pickup", "Cheek Pouch"],
        "hidden_abilities": ["Huge Power"]
    },
    {
        "name": "Fletchling",
        "base_stats": {"hp": 45, "attack": 50, "defense": 43, "sp_attack": 40, "sp_defense": 38, "speed": 62},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Big Pecks"],
        "hidden_abilities": ["Gale Wings"]
    },
    {
        "name": "Fletchinder",
        "base_stats": {"hp": 62, "attack": 73, "defense": 55, "sp_attack": 56, "sp_defense": 52, "speed": 84},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Flame Body"],
        "hidden_abilities": ["Gale Wings"]
    },
    {
        "name": "Talonflame",
        "base_stats": {"hp": 78, "attack": 81, "defense": 71, "sp_attack": 74, "sp_defense": 69, "speed": 126},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Flame Body"],
        "hidden_abilities": ["Gale Wings"]
    },
    {
        "name": "Scatterbug",
        "base_stats": {"hp": 38, "attack": 35, "defense": 40, "sp_attack": 27, "sp_defense": 25, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shield Dust", "Compound Eyes"],
        "hidden_abilities": ["Friend Guard"]
    },
    {
        "name": "Spewpa",
        "base_stats": {"hp": 45, "attack": 22, "defense": 60, "sp_attack": 27, "sp_defense": 30, "speed": 29},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shed Skin"],
        "hidden_abilities": []
    },
    {
        "name": "Vivillon",
        "base_stats": {"hp": 80, "attack": 52, "defense": 50, "sp_attack": 90, "sp_defense": 50, "speed": 89},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shield Dust", "Compound Eyes"],
        "hidden_abilities": ["Friend Guard"]
    },
    {
        "name": "Litleo",
        "base_stats": {"hp": 62, "attack": 50, "defense": 58, "sp_attack": 73, "sp_defense": 54, "speed": 72},
        "gender_ratio": {"male": 12.5, "female": 87.5},
        "abilities": ["Rivalry", "Unnerve"],
        "hidden_abilities": ["Moxie"]
    },
    {
        "name": "Pyroar",
        "base_stats": {"hp": 86, "attack": 68, "defense": 72, "sp_attack": 109, "sp_defense": 66, "speed": 106},
        "gender_ratio": {"male": 12.5, "female": 87.5},
        "abilities": ["Rivalry", "Unnerve"],
        "hidden_abilities": ["Moxie"]
    },
    {
        "name": "Flabébé",
        "base_stats": {"hp": 44, "attack": 38, "defense": 39, "sp_attack": 61, "sp_defense": 79, "speed": 42},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Flower Veil"],
        "hidden_abilities": ["Symbiosis"]
    },
    {
        "name": "Floette",
        "base_stats": {"hp": 54, "attack": 45, "defense": 47, "sp_attack": 75, "sp_defense": 98, "speed": 52},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Flower Veil"],
        "hidden_abilities": ["Symbiosis"]
    },
    {
        "name": "Florges",
        "base_stats": {"hp": 78, "attack": 65, "defense": 68, "sp_attack": 112, "sp_defense": 154, "speed": 75},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Flower Veil"],
        "hidden_abilities": ["Symbiosis"]
    },
    {
        "name": "Skiddo",
        "base_stats": {"hp": 66, "attack": 65, "defense": 48, "sp_attack": 62, "sp_defense": 57, "speed": 52},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sap Sipper"],
        "hidden_abilities": ["Grass Pelt"]
    },
    {
        "name": "Gogoat",
        "base_stats": {"hp": 123, "attack": 100, "defense": 62, "sp_attack": 97, "sp_defense": 81, "speed": 68},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sap Sipper"],
        "hidden_abilities": ["Grass Pelt"]
    },
    {
        "name": "Pancham",
        "base_stats": {"hp": 67, "attack": 82, "defense": 62, "sp_attack": 46, "sp_defense": 48, "speed": 43},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Iron Fist", "Mold Breaker"],
        "hidden_abilities": ["Scrappy"]
    },
    {
        "name": "Pangoro",
        "base_stats": {"hp": 95, "attack": 124, "defense": 78, "sp_attack": 69, "sp_defense": 71, "speed": 58},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Iron Fist", "Mold Breaker"],
        "hidden_abilities": ["Scrappy"]
    },
    {
        "name": "Furfrou",
        "base_stats": {"hp": 75, "attack": 80, "defense": 60, "sp_attack": 65, "sp_defense": 90, "speed": 102},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Fur Coat"],
        "hidden_abilities": []
    },
    {
        "name": "Espurr",
        "base_stats": {"hp": 62, "attack": 48, "defense": 54, "sp_attack": 63, "sp_defense": 60, "speed": 68},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Infiltrator"],
        "hidden_abilities": ["Own Tempo"]
    },
    {
        "name": "Meowstic",
        "base_stats": {"hp": 74, "attack": 48, "defense": 76, "sp_attack": 83, "sp_defense": 81, "speed": 104},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Infiltrator"],
        "hidden_abilities": ["Prankster"]
    },
    {
        "name": "Honedge",
        "base_stats": {"hp": 45, "attack": 80, "defense": 100, "sp_attack": 35, "sp_defense": 37, "speed": 28},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["No Guard"],
        "hidden_abilities": []
    },
    {
        "name": "Doublade",
        "base_stats": {"hp": 59, "attack": 110, "defense": 150, "sp_attack": 45, "sp_defense": 49, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["No Guard"],
        "hidden_abilities": []
    },
    {
        "name": "Aegislash",
        "base_stats": {"hp": 60, "attack": 50, "defense": 140, "sp_attack": 50, "sp_defense": 140, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Stance Change"],
        "hidden_abilities": []
    },
    {
        "name": "Spritzee",
        "base_stats": {"hp": 78, "attack": 52, "defense": 60, "sp_attack": 63, "sp_defense": 65, "speed": 23},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Healer"],
        "hidden_abilities": ["Aroma Veil"]
    },
    {
        "name": "Aromatisse",
        "base_stats": {"hp": 101, "attack": 72, "defense": 72, "sp_attack": 99, "sp_defense": 89, "speed": 29},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Healer"],
        "hidden_abilities": ["Aroma Veil"]
    },
    {
        "name": "Swirlix",
        "base_stats": {"hp": 62, "attack": 48, "defense": 66, "sp_attack": 59, "sp_defense": 57, "speed": 49},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sweet Veil"],
        "hidden_abilities": ["Unburden"]
    },
    {
        "name": "Slurpuff",
        "base_stats": {"hp": 82, "attack": 80, "defense": 86, "sp_attack": 85, "sp_defense": 75, "speed": 72},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sweet Veil"],
        "hidden_abilities": ["Unburden"]
    },
    {
        "name": "Inkay",
        "base_stats": {"hp": 53, "attack": 54, "defense": 53, "sp_attack": 37, "sp_defense": 46, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Contrary", "Suction Cups"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Malamar",
        "base_stats": {"hp": 86, "attack": 92, "defense": 88, "sp_attack": 68, "sp_defense": 75, "speed": 73},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Contrary", "Suction Cups"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Binacle",
        "base_stats": {"hp": 42, "attack": 52, "defense": 67, "sp_attack": 39, "sp_defense": 56, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Tough Claws", "Sniper"],
        "hidden_abilities": ["Pickpocket"]
    },
    {
        "name": "Barbaracle",
        "base_stats": {"hp": 72, "attack": 105, "defense": 115, "sp_attack": 54, "sp_defense": 86, "speed": 68},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Tough Claws", "Sniper"],
        "hidden_abilities": ["Pickpocket"]
    },
    {
        "name": "Skrelp",
        "base_stats": {"hp": 50, "attack": 60, "defense": 60, "sp_attack": 60, "sp_defense": 60, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Poison Point", "Poison Touch"],
        "hidden_abilities": ["Adaptability"]
    },
    {
        "name": "Dragalge",
        "base_stats": {"hp": 65, "attack": 75, "defense": 90, "sp_attack": 97, "sp_defense": 123, "speed": 44},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Poison Point", "Poison Touch"],
        "hidden_abilities": ["Adaptability"]
    },
    {
        "name": "Clauncher",
        "base_stats": {"hp": 50, "attack": 53, "defense": 62, "sp_attack": 58, "sp_defense": 63, "speed": 44},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Mega Launcher"],
        "hidden_abilities": []
    },
    {
        "name": "Clawitzer",
        "base_stats": {"hp": 71, "attack": 73, "defense": 88, "sp_attack": 120, "sp_defense": 89, "speed": 59},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Mega Launcher"],
        "hidden_abilities": []
    },
    {
        "name": "Helioptile",
        "base_stats": {"hp": 44, "attack": 38, "defense": 33, "sp_attack": 61, "sp_defense": 43, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Dry Skin", "Sand Veil"],
        "hidden_abilities": ["Solar Power"]
    },
    {
        "name": "Heliolisk",
        "base_stats": {"hp": 62, "attack": 55, "defense": 52, "sp_attack": 109, "sp_defense": 94, "speed": 109},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Dry Skin", "Sand Veil"],
        "hidden_abilities": ["Solar Power"]
    },
    {
        "name": "Tyrunt",
        "base_stats": {"hp": 58, "attack": 89, "defense": 77, "sp_attack": 45, "sp_defense": 45, "speed": 48},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Strong Jaw"],
        "hidden_abilities": ["Sturdy"]
    },
    {
        "name": "Tyrantrum",
        "base_stats": {"hp": 82, "attack": 121, "defense": 119, "sp_attack": 69, "sp_defense": 59, "speed": 71},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Strong Jaw"],
        "hidden_abilities": ["Rock Head"]
    },
    {
        "name": "Amaura",
        "base_stats": {"hp": 77, "attack": 59, "defense": 50, "sp_attack": 67, "sp_defense": 63, "speed": 46},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Refrigerate"],
        "hidden_abilities": ["Snow Warning"]
    },
    {
        "name": "Aurorus",
        "base_stats": {"hp": 123, "attack": 77, "defense": 72, "sp_attack": 99, "sp_defense": 92, "speed": 58},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Refrigerate"],
        "hidden_abilities": ["Snow Warning"]
    },
    {
        "name": "Sylveon",
        "base_stats": {"hp": 95, "attack": 65, "defense": 65, "sp_attack": 110, "sp_defense": 130, "speed": 60},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Cute Charm"],
        "hidden_abilities": ["Pixilate"]
    },
    {
        "name": "Hawlucha",
        "base_stats": {"hp": 78, "attack": 92, "defense": 75, "sp_attack": 74, "sp_defense": 63, "speed": 118},
        "gender_ratio": {"male": 100, "female": 0},
        "abilities": ["Limber", "Unburden"],
        "hidden_abilities": ["Mold Breaker"]
    },
    {
        "name": "Dedenne",
        "base_stats": {"hp": 67, "attack": 58, "defense": 57, "sp_attack": 81, "sp_defense": 67, "speed": 101},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Cheek Pouch", "Pickup"],
        "hidden_abilities": ["Plus"]
    },
    {
        "name": "Carbink",
        "base_stats": {"hp": 50, "attack": 50, "defense": 150, "sp_attack": 50, "sp_defense": 150, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Clear Body"],
        "hidden_abilities": ["Sturdy"]
    },
    {
        "name": "Goomy",
        "base_stats": {"hp": 45, "attack": 50, "defense": 35, "sp_attack": 55, "sp_defense": 75, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sap Sipper"],
        "hidden_abilities": ["Gooey"]
    },
    {
        "name": "Sliggoo",
        "base_stats": {"hp": 68, "attack": 75, "defense": 53, "sp_attack": 83, "sp_defense": 113, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sap Sipper"],
        "hidden_abilities": ["Gooey"]
    },
    {
        "name": "Goodra",
        "base_stats": {"hp": 90, "attack": 100, "defense": 70, "sp_attack": 110, "sp_defense": 150, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sap Sipper", "Hydration"],
        "hidden_abilities": ["Gooey"]
    },
    {
        "name": "Klefki",
        "base_stats": {"hp": 57, "attack": 80, "defense": 91, "sp_attack": 80, "sp_defense": 87, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Prankster"],
        "hidden_abilities": ["Magician"]
    },
    {
        "name": "Phantump",
        "base_stats": {"hp": 43, "attack": 70, "defense": 48, "sp_attack": 50, "sp_defense": 60, "speed": 38},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Natural Cure", "Frisk"],
        "hidden_abilities": ["Harvest"]
    },
    {
        "name": "Trevenant",
        "base_stats": {"hp": 85, "attack": 110, "defense": 76, "sp_attack": 65, "sp_defense": 82, "speed": 56},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Natural Cure", "Frisk"],
        "hidden_abilities": ["Harvest"]
    },
    {
        "name": "Pumpkaboo",
        "base_stats": {"hp": 49, "attack": 66, "defense": 70, "sp_attack": 44, "sp_defense": 55, "speed": 51},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pickup", "Frisk"],
        "hidden_abilities": ["Insomnia"]
    },
    {
        "name": "Gourgeist",
        "base_stats": {"hp": 65, "attack": 90, "defense": 122, "sp_attack": 58, "sp_defense": 75, "speed": 84},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pickup", "Frisk"],
        "hidden_abilities": ["Insomnia"]
    },
    {
        "name": "Bergmite",
        "base_stats": {"hp": 55, "attack": 69, "defense": 85, "sp_attack": 32, "sp_defense": 35, "speed": 28},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Own Tempo", "Ice Body"],
        "hidden_abilities": ["Sturdy"]
    },
    {
        "name": "Avalugg",
        "base_stats": {"hp": 95, "attack": 117, "defense": 184, "sp_attack": 44, "sp_defense": 46, "speed": 28},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Own Tempo", "Ice Body"],
        "hidden_abilities": ["Sturdy"]
    },
    {
        "name": "Noibat",
        "base_stats": {"hp": 40, "attack": 30, "defense": 35, "sp_attack": 45, "sp_defense": 40, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Frisk", "Infiltrator"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Noivern",
        "base_stats": {"hp": 85, "attack": 70, "defense": 80, "sp_attack": 97, "sp_defense": 80, "speed": 123},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Frisk", "Infiltrator"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Xerneas",
        "base_stats": {"hp": 126, "attack": 131, "defense": 95, "sp_attack": 131, "sp_defense": 98, "speed": 99},
        "gender_ratio": None,
        "abilities": ["Fairy Aura"],
        "hidden_abilities": []
    },
    {
        "name": "Yveltal",
        "base_stats": {"hp": 126, "attack": 131, "defense": 95, "sp_attack": 131, "sp_defense": 98, "speed": 99},
        "gender_ratio": None,
        "abilities": ["Dark Aura"],
        "hidden_abilities": []
    },
    {
        "name": "Zygarde",
        "base_stats": {"hp": 108, "attack": 100, "defense": 121, "sp_attack": 81, "sp_defense": 95, "speed": 95},
        "gender_ratio": None,
        "abilities": ["Aura Break"],
        "hidden_abilities": ["Power Construct"]
    },
    {
        "name": "Diancie",
        "base_stats": {"hp": 50, "attack": 100, "defense": 150, "sp_attack": 100, "sp_defense": 150, "speed": 50},
        "gender_ratio": None,
        "abilities": ["Clear Body"],
        "hidden_abilities": []
    },
    {
        "name": "Hoopa",
        "base_stats": {"hp": 80, "attack": 110, "defense": 60, "sp_attack": 150, "sp_defense": 130, "speed": 70},
        "gender_ratio": None,
        "abilities": ["Magician"],
        "hidden_abilities": []
    },
    {
        "name": "Volcanion",
        "base_stats": {"hp": 80, "attack": 110, "defense": 120, "sp_attack": 130, "sp_defense": 90, "speed": 70},
        "gender_ratio": None,
        "abilities": ["Water Absorb"],
        "hidden_abilities": []
    }
]
POKEMON_GEN7 = [
    {
        "name": "Rowlet",
        "base_stats": {"hp": 68, "attack": 55, "defense": 55, "sp_attack": 50, "sp_defense": 50, "speed": 42},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Long Reach"]
    },
    {
        "name": "Dartrix",
        "base_stats": {"hp": 78, "attack": 75, "defense": 75, "sp_attack": 70, "sp_defense": 70, "speed": 52},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Long Reach"]
    },
    {
        "name": "Decidueye",
        "base_stats": {"hp": 78, "attack": 107, "defense": 75, "sp_attack": 100, "sp_defense": 100, "speed": 70},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Long Reach"]
    },
    {
        "name": "Litten",
        "base_stats": {"hp": 45, "attack": 65, "defense": 40, "sp_attack": 60, "sp_defense": 40, "speed": 70},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Intimidate"]
    },
    {
        "name": "Torracat",
        "base_stats": {"hp": 65, "attack": 85, "defense": 50, "sp_attack": 80, "sp_defense": 50, "speed": 90},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Intimidate"]
    },
    {
        "name": "Incineroar",
        "base_stats": {"hp": 95, "attack": 115, "defense": 90, "sp_attack": 80, "sp_defense": 90, "speed": 60},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Intimidate"]
    },
    {
        "name": "Popplio",
        "base_stats": {"hp": 50, "attack": 54, "defense": 54, "sp_attack": 66, "sp_defense": 56, "speed": 40},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Liquid Voice"]
    },
    {
        "name": "Brionne",
        "base_stats": {"hp": 60, "attack": 69, "defense": 69, "sp_attack": 91, "sp_defense": 81, "speed": 50},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Liquid Voice"]
    },
    {
        "name": "Primarina",
        "base_stats": {"hp": 80, "attack": 74, "defense": 74, "sp_attack": 126, "sp_defense": 116, "speed": 60},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Liquid Voice"]
    },
    {
        "name": "Pikipek",
        "base_stats": {"hp": 35, "attack": 75, "defense": 30, "sp_attack": 30, "sp_defense": 30, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Skill Link"],
        "hidden_abilities": ["Pickup"]
    },
    {
        "name": "Trumbeak",
        "base_stats": {"hp": 55, "attack": 85, "defense": 50, "sp_attack": 40, "sp_defense": 50, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Skill Link"],
        "hidden_abilities": ["Pickup"]
    },
    {
        "name": "Toucannon",
        "base_stats": {"hp": 80, "attack": 120, "defense": 75, "sp_attack": 75, "sp_defense": 75, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Skill Link"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Yungoos",
        "base_stats": {"hp": 48, "attack": 70, "defense": 30, "sp_attack": 30, "sp_defense": 30, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Stakeout", "Strong Jaw"],
        "hidden_abilities": ["Adaptability"]
    },
    {
        "name": "Gumshoos",
        "base_stats": {"hp": 88, "attack": 110, "defense": 60, "sp_attack": 55, "sp_defense": 60, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Stakeout", "Strong Jaw"],
        "hidden_abilities": ["Adaptability"]
    },
    {
        "name": "Grubbin",
        "base_stats": {"hp": 47, "attack": 62, "defense": 45, "sp_attack": 55, "sp_defense": 45, "speed": 46},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm"],
        "hidden_abilities": []
    },
    {
        "name": "Charjabug",
        "base_stats": {"hp": 57, "attack": 82, "defense": 95, "sp_attack": 55, "sp_defense": 75, "speed": 36},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Battery"],
        "hidden_abilities": []
    },
    {
        "name": "Vikavolt",
        "base_stats": {"hp": 77, "attack": 70, "defense": 90, "sp_attack": 145, "sp_defense": 75, "speed": 43},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Levitate"],
        "hidden_abilities": []
    },
    {
        "name": "Crabrawler",
        "base_stats": {"hp": 47, "attack": 82, "defense": 57, "sp_attack": 42, "sp_defense": 47, "speed": 63},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hyper Cutter", "Iron Fist"],
        "hidden_abilities": ["Anger Point"]
    },
    {
        "name": "Crabominable",
        "base_stats": {"hp": 97, "attack": 132, "defense": 77, "sp_attack": 62, "sp_defense": 67, "speed": 43},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Hyper Cutter", "Iron Fist"],
        "hidden_abilities": ["Anger Point"]
    },
    {
        "name": "Oricorio",
        "base_stats": {"hp": 75, "attack": 70, "defense": 70, "sp_attack": 98, "sp_defense": 70, "speed": 93},
        "gender_ratio": {"male": 25, "female": 75},
        "abilities": ["Dancer"],
        "hidden_abilities": []
    },
    {
        "name": "Cutiefly",
        "base_stats": {"hp": 40, "attack": 45, "defense": 40, "sp_attack": 55, "sp_defense": 40, "speed": 84},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Honey Gather", "Shield Dust"],
        "hidden_abilities": ["Sweet Veil"]
    },
    {
        "name": "Ribombee",
        "base_stats": {"hp": 60, "attack": 55, "defense": 60, "sp_attack": 95, "sp_defense": 70, "speed": 124},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Honey Gather", "Shield Dust"],
        "hidden_abilities": ["Sweet Veil"]
    },
    {
        "name": "Rockruff",
        "base_stats": {"hp": 45, "attack": 65, "defense": 40, "sp_attack": 30, "sp_defense": 40, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Vital Spirit"],
        "hidden_abilities": ["Steadfast"]
    },
    {
        "name": "Lycanroc",
        "base_stats": {"hp": 75, "attack": 115, "defense": 65, "sp_attack": 55, "sp_defense": 65, "speed": 112},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Sand Rush"],
        "hidden_abilities": ["Steadfast"]
    },
    {
        "name": "Wishiwashi",
        "base_stats": {"hp": 45, "attack": 20, "defense": 20, "sp_attack": 25, "sp_defense": 25, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Schooling"],
        "hidden_abilities": []
    },
    {
        "name": "Mareanie",
        "base_stats": {"hp": 50, "attack": 53, "defense": 62, "sp_attack": 43, "sp_defense": 52, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Merciless", "Limber"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Toxapex",
        "base_stats": {"hp": 50, "attack": 63, "defense": 152, "sp_attack": 53, "sp_defense": 142, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Merciless", "Limber"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Mudbray",
        "base_stats": {"hp": 70, "attack": 100, "defense": 70, "sp_attack": 45, "sp_defense": 55, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Own Tempo", "Stamina"],
        "hidden_abilities": ["Inner Focus"]
    },
    {
        "name": "Mudsdale",
        "base_stats": {"hp": 100, "attack": 125, "defense": 100, "sp_attack": 55, "sp_defense": 85, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Own Tempo", "Stamina"],
        "hidden_abilities": ["Inner Focus"]
    },
    {
        "name": "Dewpider",
        "base_stats": {"hp": 38, "attack": 40, "defense": 52, "sp_attack": 40, "sp_defense": 72, "speed": 27},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Bubble"],
        "hidden_abilities": ["Water Absorb"]
    },
    {
        "name": "Araquanid",
        "base_stats": {"hp": 68, "attack": 70, "defense": 92, "sp_attack": 50, "sp_defense": 132, "speed": 42},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Bubble"],
        "hidden_abilities": ["Water Absorb"]
    },
    {
        "name": "Fomantis",
        "base_stats": {"hp": 40, "attack": 55, "defense": 35, "sp_attack": 50, "sp_defense": 35, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Leaf Guard"],
        "hidden_abilities": ["Contrary"]
    },
    {
        "name": "Lurantis",
        "base_stats": {"hp": 70, "attack": 105, "defense": 90, "sp_attack": 80, "sp_defense": 90, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Leaf Guard"],
        "hidden_abilities": ["Contrary"]
    },
    {
        "name": "Morelull",
        "base_stats": {"hp": 40, "attack": 35, "defense": 55, "sp_attack": 65, "sp_defense": 75, "speed": 15},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Illuminate", "Effect Spore"],
        "hidden_abilities": ["Rain Dish"]
    },
    {
        "name": "Shiinotic",
        "base_stats": {"hp": 60, "attack": 45, "defense": 80, "sp_attack": 90, "sp_defense": 100, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Illuminate", "Effect Spore"],
        "hidden_abilities": ["Rain Dish"]
    },
    {
        "name": "Salandit",
        "base_stats": {"hp": 48, "attack": 44, "defense": 40, "sp_attack": 71, "sp_defense": 40, "speed": 77},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Corrosion"],
        "hidden_abilities": ["Oblivious"]
    },
    {
        "name": "Salazzle",
        "base_stats": {"hp": 68, "attack": 64, "defense": 60, "sp_attack": 111, "sp_defense": 60, "speed": 117},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Corrosion"],
        "hidden_abilities": ["Oblivious"]
    },
    {
        "name": "Stufful",
        "base_stats": {"hp": 70, "attack": 75, "defense": 50, "sp_attack": 45, "sp_defense": 50, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Fluffy", "Klutz"],
        "hidden_abilities": ["Cute Charm"]
    },
    {
        "name": "Bewear",
        "base_stats": {"hp": 120, "attack": 125, "defense": 80, "sp_attack": 55, "sp_defense": 60, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Fluffy", "Klutz"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Bounsweet",
        "base_stats": {"hp": 42, "attack": 30, "defense": 38, "sp_attack": 30, "sp_defense": 38, "speed": 32},
        "gender_ratio": {"male": 12.5, "female": 87.5},
        "abilities": ["Leaf Guard", "Oblivious"],
        "hidden_abilities": ["Sweet Veil"]
    },
    {
        "name": "Steenee",
        "base_stats": {"hp": 52, "attack": 40, "defense": 48, "sp_attack": 40, "sp_defense": 48, "speed": 62},
        "gender_ratio": {"male": 12.5, "female": 87.5},
        "abilities": ["Leaf Guard", "Oblivious"],
        "hidden_abilities": ["Sweet Veil"]
    },
    {
        "name": "Tsareena",
        "base_stats": {"hp": 72, "attack": 120, "defense": 98, "sp_attack": 50, "sp_defense": 98, "speed": 72},
        "gender_ratio": {"male": 12.5, "female": 87.5},
        "abilities": ["Leaf Guard", "Queenly Majesty"],
        "hidden_abilities": ["Sweet Veil"]
    },
    {
        "name": "Comfey",
        "base_stats": {"hp": 51, "attack": 52, "defense": 90, "sp_attack": 82, "sp_defense": 110, "speed": 100},
        "gender_ratio": {"male": 24.6, "female": 75.4},
        "abilities": ["Flower Veil", "Triage"],
        "hidden_abilities": ["Natural Cure"]
    },
    {
        "name": "Oranguru",
        "base_stats": {"hp": 90, "attack": 60, "defense": 80, "sp_attack": 90, "sp_defense": 110, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Inner Focus", "Telepathy"],
        "hidden_abilities": ["Symbiosis"]
    },
    {
        "name": "Passimian",
        "base_stats": {"hp": 100, "attack": 120, "defense": 90, "sp_attack": 40, "sp_defense": 60, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Receiver"],
        "hidden_abilities": ["Defiant"]
    },
    {
        "name": "Wimpod",
        "base_stats": {"hp": 25, "attack": 35, "defense": 40, "sp_attack": 20, "sp_defense": 30, "speed": 80},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Wimp Out"],
        "hidden_abilities": []
    },
    {
        "name": "Golisopod",
        "base_stats": {"hp": 75, "attack": 125, "defense": 140, "sp_attack": 60, "sp_defense": 90, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Emergency Exit"],
        "hidden_abilities": []
    },
    {
        "name": "Sandygast",
        "base_stats": {"hp": 55, "attack": 55, "defense": 80, "sp_attack": 70, "sp_defense": 45, "speed": 15},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Compaction"],
        "hidden_abilities": ["Sand Veil"]
    },
    {
        "name": "Palossand",
        "base_stats": {"hp": 85, "attack": 75, "defense": 110, "sp_attack": 100, "sp_defense": 75, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Compaction"],
        "hidden_abilities": ["Sand Veil"]
    },
    {
        "name": "Pyukumuku",
        "base_stats": {"hp": 55, "attack": 60, "defense": 130, "sp_attack": 30, "sp_defense": 130, "speed": 5},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Innards Out"],
        "hidden_abilities": ["Unaware"]
    },
    {
        "name": "Type: Null",
        "base_stats": {"hp": 95, "attack": 95, "defense": 95, "sp_attack": 95, "sp_defense": 95, "speed": 59},
        "gender_ratio": None,
        "abilities": ["Battle Armor"],
        "hidden_abilities": []
    },
    {
        "name": "Silvally",
        "base_stats": {"hp": 95, "attack": 95, "defense": 95, "sp_attack": 95, "sp_defense": 95, "speed": 95},
        "gender_ratio": None,
        "abilities": ["RKS System"],
        "hidden_abilities": []
    },
    {
        "name": "Minior",
        "base_stats": {"hp": 60, "attack": 60, "defense": 100, "sp_attack": 60, "sp_defense": 100, "speed": 60},
        "gender_ratio": None,
        "abilities": ["Shields Down"],
        "hidden_abilities": []
    },
    {
        "name": "Komala",
        "base_stats": {"hp": 65, "attack": 115, "defense": 65, "sp_attack": 75, "sp_defense": 95, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Comatose"],
        "hidden_abilities": []
    },
    {
        "name": "Turtonator",
        "base_stats": {"hp": 60, "attack": 78, "defense": 135, "sp_attack": 91, "sp_defense": 85, "speed": 36},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shell Armor"],
        "hidden_abilities": []
    },
    {
        "name": "Togedemaru",
        "base_stats": {"hp": 65, "attack": 98, "defense": 63, "sp_attack": 40, "sp_defense": 73, "speed": 96},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Iron Barbs", "Lightning Rod"],
        "hidden_abilities": ["Sturdy"]
    },
    {
        "name": "Mimikyu",
        "base_stats": {"hp": 55, "attack": 90, "defense": 80, "sp_attack": 50, "sp_defense": 105, "speed": 96},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Disguise"],
        "hidden_abilities": []
    },
    {
        "name": "Bruxish",
        "base_stats": {"hp": 68, "attack": 105, "defense": 70, "sp_attack": 70, "sp_defense": 70, "speed": 92},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Dazzling", "Strong Jaw"],
        "hidden_abilities": ["Wonder Skin"]
    },
    {
        "name": "Drampa",
        "base_stats": {"hp": 78, "attack": 60, "defense": 85, "sp_attack": 135, "sp_defense": 91, "speed": 36},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Berserk", "Sap Sipper"],
        "hidden_abilities": ["Cloud Nine"]
    },
    {
        "name": "Dhelmise",
        "base_stats": {"hp": 70, "attack": 131, "defense": 100, "sp_attack": 86, "sp_defense": 90, "speed": 40},
        "gender_ratio": None,
        "abilities": ["Steelworker"],
        "hidden_abilities": []
    },
    {
        "name": "Jangmo-o",
        "base_stats": {"hp": 45, "attack": 55, "defense": 65, "sp_attack": 45, "sp_defense": 45, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Bulletproof", "Soundproof"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Hakamo-o",
        "base_stats": {"hp": 55, "attack": 75, "defense": 90, "sp_attack": 65, "sp_defense": 70, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Bulletproof", "Soundproof"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Kommo-o",
        "base_stats": {"hp": 75, "attack": 110, "defense": 125, "sp_attack": 100, "sp_defense": 105, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Bulletproof", "Soundproof"],
        "hidden_abilities": ["Overcoat"]
    },
    {
        "name": "Tapu Koko",
        "base_stats": {"hp": 70, "attack": 115, "defense": 85, "sp_attack": 95, "sp_defense": 75, "speed": 130},
        "gender_ratio": None,
        "abilities": ["Electric Surge"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Tapu Lele",
        "base_stats": {"hp": 70, "attack": 85, "defense": 75, "sp_attack": 130, "sp_defense": 115, "speed": 95},
        "gender_ratio": None,
        "abilities": ["Psychic Surge"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Tapu Bulu",
        "base_stats": {"hp": 70, "attack": 130, "defense": 115, "sp_attack": 85, "sp_defense": 95, "speed": 75},
        "gender_ratio": None,
        "abilities": ["Grassy Surge"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Tapu Fini",
        "base_stats": {"hp": 70, "attack": 75, "defense": 115, "sp_attack": 95, "sp_defense": 130, "speed": 85},
        "gender_ratio": None,
        "abilities": ["Misty Surge"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Cosmog",
        "base_stats": {"hp": 43, "attack": 29, "defense": 31, "sp_attack": 29, "sp_defense": 31, "speed": 37},
        "gender_ratio": None,
        "abilities": ["Unaware"],
        "hidden_abilities": []
    },
    {
        "name": "Cosmoem",
        "base_stats": {"hp": 43, "attack": 29, "defense": 131, "sp_attack": 29, "sp_defense": 131, "speed": 37},
        "gender_ratio": None,
        "abilities": ["Sturdy"],
        "hidden_abilities": []
    },
    {
        "name": "Solgaleo",
        "base_stats": {"hp": 137, "attack": 137, "defense": 107, "sp_attack": 113, "sp_defense": 89, "speed": 97},
        "gender_ratio": None,
        "abilities": ["Full Metal Body"],
        "hidden_abilities": []
    },
    {
        "name": "Lunala",
        "base_stats": {"hp": 137, "attack": 113, "defense": 89, "sp_attack": 137, "sp_defense": 107, "speed": 97},
        "gender_ratio": None,
        "abilities": ["Shadow Shield"],
        "hidden_abilities": []
    },
    {
        "name": "Nihilego",
        "base_stats": {"hp": 109, "attack": 53, "defense": 47, "sp_attack": 127, "sp_defense": 131, "speed": 103},
        "gender_ratio": None,
        "abilities": ["Beast Boost"],
        "hidden_abilities": []
    },
    {
        "name": "Buzzwole",
        "base_stats": {"hp": 107, "attack": 139, "defense": 139, "sp_attack": 53, "sp_defense": 53, "speed": 79},
        "gender_ratio": None,
        "abilities": ["Beast Boost"],
        "hidden_abilities": []
    },
    {
        "name": "Pheromosa",
        "base_stats": {"hp": 71, "attack": 137, "defense": 37, "sp_attack": 137, "sp_defense": 37, "speed": 151},
        "gender_ratio": None,
        "abilities": ["Beast Boost"],
        "hidden_abilities": []
    },
    {
        "name": "Xurkitree",
        "base_stats": {"hp": 83, "attack": 89, "defense": 71, "sp_attack": 173, "sp_defense": 71, "speed": 83},
        "gender_ratio": None,
        "abilities": ["Beast Boost"],
        "hidden_abilities": []
    },
    {
        "name": "Celesteela",
        "base_stats": {"hp": 97, "attack": 101, "defense": 103, "sp_attack": 107, "sp_defense": 101, "speed": 61},
        "gender_ratio": None,
        "abilities": ["Beast Boost"],
        "hidden_abilities": []
    },
    {
        "name": "Kartana",
        "base_stats": {"hp": 59, "attack": 181, "defense": 131, "sp_attack": 59, "sp_defense": 31, "speed": 109},
        "gender_ratio": None,
        "abilities": ["Beast Boost"],
        "hidden_abilities": []
    },
    {
        "name": "Guzzlord",
        "base_stats": {"hp": 223, "attack": 101, "defense": 53, "sp_attack": 97, "sp_defense": 53, "speed": 43},
        "gender_ratio": None,
        "abilities": ["Beast Boost"],
        "hidden_abilities": []
    },
    {
        "name": "Necrozma",
        "base_stats": {"hp": 97, "attack": 107, "defense": 101, "sp_attack": 127, "sp_defense": 89, "speed": 79},
        "gender_ratio": None,
        "abilities": ["Prism Armor"],
        "hidden_abilities": []
    },
    {
        "name": "Magearna",
        "base_stats": {"hp": 80, "attack": 95, "defense": 115, "sp_attack": 130, "sp_defense": 115, "speed": 65},
        "gender_ratio": None,
        "abilities": ["Soul-Heart"],
        "hidden_abilities": []
    },
    {
        "name": "Marshadow",
        "base_stats": {"hp": 90, "attack": 125, "defense": 80, "sp_attack": 90, "sp_defense": 90, "speed": 125},
        "gender_ratio": None,
        "abilities": ["Technician"],
        "hidden_abilities": []
    },
    {
        "name": "Poipole",
        "base_stats": {"hp": 67, "attack": 73, "defense": 67, "sp_attack": 73, "sp_defense": 67, "speed": 73},
        "gender_ratio": None,
        "abilities": ["Beast Boost"],
        "hidden_abilities": []
    },
    {
        "name": "Naganadel",
        "base_stats": {"hp": 73, "attack": 73, "defense": 73, "sp_attack": 127, "sp_defense": 73, "speed": 121},
        "gender_ratio": None,
        "abilities": ["Beast Boost"],
        "hidden_abilities": []
    },
    {
        "name": "Stakataka",
        "base_stats": {"hp": 61, "attack": 131, "defense": 211, "sp_attack": 53, "sp_defense": 101, "speed": 13},
        "gender_ratio": None,
        "abilities": ["Beast Boost"],
        "hidden_abilities": []
    },
    {
        "name": "Blacephalon",
        "base_stats": {"hp": 53, "attack": 127, "defense": 53, "sp_attack": 151, "sp_defense": 79, "speed": 107},
        "gender_ratio": None,
        "abilities": ["Beast Boost"],
        "hidden_abilities": []
    },
    {
        "name": "Zeraora",
        "base_stats": {"hp": 88, "attack": 112, "defense": 75, "sp_attack": 102, "sp_defense": 80, "speed": 143},
        "gender_ratio": None,
        "abilities": ["Volt Absorb"],
        "hidden_abilities": []
    },
    {
        "name": "Meltan",
        "base_stats": {"hp": 46, "attack": 65, "defense": 65, "sp_attack": 55, "sp_defense": 35, "speed": 34},
        "gender_ratio": None,
        "abilities": ["Magnet Pull"],
        "hidden_abilities": []
    },
    {
        "name": "Melmetal",
        "base_stats": {"hp": 135, "attack": 143, "defense": 143, "sp_attack": 80, "sp_defense": 65, "speed": 34},
        "gender_ratio": None,
        "abilities": ["Iron Fist"],
        "hidden_abilities": []
    }
]
POKEMON_GEN8 = [
    {
        "name": "Grookey",
        "base_stats": {"hp": 50, "attack": 65, "defense": 50, "sp_attack": 40, "sp_defense": 40, "speed": 65},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Grassy Surge"]
    },
    {
        "name": "Thwackey",
        "base_stats": {"hp": 70, "attack": 85, "defense": 70, "sp_attack": 55, "sp_defense": 60, "speed": 80},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Grassy Surge"]
    },
    {
        "name": "Rillaboom",
        "base_stats": {"hp": 100, "attack": 125, "defense": 90, "sp_attack": 60, "sp_defense": 70, "speed": 85},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Grassy Surge"]
    },
    {
        "name": "Scorbunny",
        "base_stats": {"hp": 50, "attack": 71, "defense": 40, "sp_attack": 40, "sp_defense": 40, "speed": 69},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Libero"]
    },
    {
        "name": "Raboot",
        "base_stats": {"hp": 65, "attack": 86, "defense": 60, "sp_attack": 55, "sp_defense": 60, "speed": 94},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Libero"]
    },
    {
        "name": "Cinderace",
        "base_stats": {"hp": 80, "attack": 116, "defense": 75, "sp_attack": 65, "sp_defense": 75, "speed": 119},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Libero"]
    },
    {
        "name": "Sobble",
        "base_stats": {"hp": 50, "attack": 40, "defense": 40, "sp_attack": 70, "sp_defense": 40, "speed": 70},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Sniper"]
    },
    {
        "name": "Drizzile",
        "base_stats": {"hp": 65, "attack": 60, "defense": 55, "sp_attack": 95, "sp_defense": 55, "speed": 90},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Sniper"]
    },
    {
        "name": "Inteleon",
        "base_stats": {"hp": 70, "attack": 85, "defense": 65, "sp_attack": 125, "sp_defense": 65, "speed": 120},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Sniper"]
    },
    {
        "name": "Skwovet",
        "base_stats": {"hp": 70, "attack": 55, "defense": 55, "sp_attack": 35, "sp_defense": 35, "speed": 25},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Cheek Pouch", "Gluttony"],
        "hidden_abilities": ["Harvest"]
    },
    {
        "name": "Greedent",
        "base_stats": {"hp": 120, "attack": 95, "defense": 95, "sp_attack": 55, "sp_defense": 75, "speed": 20},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Cheek Pouch", "Gluttony"],
        "hidden_abilities": ["Harvest"]
    },
    {
        "name": "Rookidee",
        "base_stats": {"hp": 38, "attack": 47, "defense": 35, "sp_attack": 33, "sp_defense": 35, "speed": 57},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Sheer Force"],
        "hidden_abilities": ["Big Pecks"]
    },
    {
        "name": "Corvisquire",
        "base_stats": {"hp": 68, "attack": 67, "defense": 55, "sp_attack": 43, "sp_defense": 55, "speed": 77},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Keen Eye", "Sheer Force"],
        "hidden_abilities": ["Big Pecks"]
    },
    {
        "name": "Corviknight",
        "base_stats": {"hp": 98, "attack": 87, "defense": 105, "sp_attack": 53, "sp_defense": 85, "speed": 67},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pressure", "Unnerve"],
        "hidden_abilities": ["Mirror Armor"]
    },
    {
        "name": "Blipbug",
        "base_stats": {"hp": 25, "attack": 20, "defense": 20, "sp_attack": 25, "sp_defense": 45, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm"],
        "hidden_abilities": []
    },
    {
        "name": "Dottler",
        "base_stats": {"hp": 50, "attack": 35, "defense": 80, "sp_attack": 50, "sp_defense": 90, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm"],
        "hidden_abilities": []
    },
    {
        "name": "Orbeetle",
        "base_stats": {"hp": 60, "attack": 45, "defense": 110, "sp_attack": 80, "sp_defense": 120, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swarm"],
        "hidden_abilities": []
    },
    {
        "name": "Nickit",
        "base_stats": {"hp": 40, "attack": 28, "defense": 28, "sp_attack": 47, "sp_defense": 52, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Unburden"],
        "hidden_abilities": ["Stakeout"]
    },
    {
        "name": "Thievul",
        "base_stats": {"hp": 70, "attack": 58, "defense": 58, "sp_attack": 87, "sp_defense": 92, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Run Away", "Unburden"],
        "hidden_abilities": ["Stakeout"]
    },
    {
        "name": "Gossifleur",
        "base_stats": {"hp": 40, "attack": 40, "defense": 60, "sp_attack": 40, "sp_defense": 60, "speed": 10},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Cotton Down"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Eldegoss",
        "base_stats": {"hp": 60, "attack": 50, "defense": 90, "sp_attack": 80, "sp_defense": 120, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Cotton Down"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Wooloo",
        "base_stats": {"hp": 42, "attack": 40, "defense": 55, "sp_attack": 40, "sp_defense": 45, "speed": 48},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Fluffy", "Run Away"],
        "hidden_abilities": ["Bulletproof"]
    },
    {
        "name": "Dubwool",
        "base_stats": {"hp": 72, "attack": 80, "defense": 100, "sp_attack": 60, "sp_defense": 90, "speed": 88},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Fluffy", "Steadfast"],
        "hidden_abilities": ["Bulletproof"]
    },
    {
        "name": "Chewtle",
        "base_stats": {"hp": 50, "attack": 64, "defense": 50, "sp_attack": 38, "sp_defense": 38, "speed": 44},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Strong Jaw"],
        "hidden_abilities": []
    },
    {
        "name": "Drednaw",
        "base_stats": {"hp": 90, "attack": 115, "defense": 90, "sp_attack": 48, "sp_defense": 68, "speed": 74},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Strong Jaw"],
        "hidden_abilities": []
    },
    {
        "name": "Yamper",
        "base_stats": {"hp": 59, "attack": 45, "defense": 50, "sp_attack": 40, "sp_defense": 50, "speed": 26},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Ball Fetch", "Pickup"],
        "hidden_abilities": ["Competitive"]
    },
    {
        "name": "Boltund",
        "base_stats": {"hp": 69, "attack": 90, "defense": 60, "sp_attack": 90, "sp_defense": 60, "speed": 121},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Strong Jaw", "Competitive"],
        "hidden_abilities": ["Volt Absorb"]
    },
    {
        "name": "Rolycoly",
        "base_stats": {"hp": 30, "attack": 40, "defense": 50, "sp_attack": 40, "sp_defense": 50, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Steam Engine", "Power Spot"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Carkol",
        "base_stats": {"hp": 80, "attack": 60, "defense": 90, "sp_attack": 60, "sp_defense": 70, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Steam Engine", "Power Spot"],
        "hidden_abilities": ["Flame Body"]
    },
    {
        "name": "Coalossal",
        "base_stats": {"hp": 110, "attack": 80, "defense": 120, "sp_attack": 80, "sp_defense": 90, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Steam Engine", "Power Spot"],
        "hidden_abilities": ["Flame Body"]
    },
    {
        "name": "Applin",
        "base_stats": {"hp": 40, "attack": 40, "defense": 80, "sp_attack": 40, "sp_defense": 40, "speed": 20},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Ripen", "Gluttony"],
        "hidden_abilities": ["Bulletproof"]
    },
    {
        "name": "Flapple",
        "base_stats": {"hp": 70, "attack": 110, "defense": 80, "sp_attack": 95, "sp_defense": 60, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Ripen"],
        "hidden_abilities": ["Hustle"]
    },
    {
        "name": "Appletun",
        "base_stats": {"hp": 110, "attack": 85, "defense": 80, "sp_attack": 100, "sp_defense": 80, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Ripen"],
        "hidden_abilities": ["Thick Fat"]
    },
    {
        "name": "Silicobra",
        "base_stats": {"hp": 52, "attack": 57, "defense": 75, "sp_attack": 35, "sp_defense": 50, "speed": 46},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Spit"],
        "hidden_abilities": ["Shed Skin"]
    },
    {
        "name": "Sandaconda",
        "base_stats": {"hp": 72, "attack": 107, "defense": 125, "sp_attack": 65, "sp_defense": 70, "speed": 71},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Spit"],
        "hidden_abilities": ["Shed Skin"]
    },
    {
        "name": "Cramorant",
        "base_stats": {"hp": 70, "attack": 85, "defense": 55, "sp_attack": 85, "sp_defense": 95, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Gulp Missile"],
        "hidden_abilities": ["Skill Link"]
    },
    {
        "name": "Arrokuda",
        "base_stats": {"hp": 41, "attack": 63, "defense": 40, "sp_attack": 40, "sp_defense": 30, "speed": 66},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Propeller Tail"],
        "hidden_abilities": ["Sharpness"]
    },
    {
        "name": "Barraskewda",
        "base_stats": {"hp": 61, "attack": 123, "defense": 60, "sp_attack": 60, "sp_defense": 50, "speed": 136},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Swift Swim", "Propeller Tail"],
        "hidden_abilities": ["Swift Swim"]
    },
    {
        "name": "Toxel",
        "base_stats": {"hp": 40, "attack": 38, "defense": 35, "sp_attack": 54, "sp_defense": 35, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Rattled", "Static"],
        "hidden_abilities": ["Galvanize"]
    },
    {
        "name": "Toxtricity",
        "base_stats": {"hp": 75, "attack": 98, "defense": 70, "sp_attack": 114, "sp_defense": 70, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Punk Rock", "Plus"],
        "hidden_abilities": ["Technician"]
    },
    {
        "name": "Sizzlipede",
        "base_stats": {"hp": 50, "attack": 65, "defense": 45, "sp_attack": 50, "sp_defense": 50, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Flash Fire", "White Smoke"],
        "hidden_abilities": ["Flame Body"]
    },
    {
        "name": "Centiskorch",
        "base_stats": {"hp": 100, "attack": 115, "defense": 65, "sp_attack": 90, "sp_defense": 90, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Flash Fire", "White Smoke"],
        "hidden_abilities": ["Flame Body"]
    },
    {
        "name": "Clobbopus",
        "base_stats": {"hp": 50, "attack": 68, "defense": 60, "sp_attack": 50, "sp_defense": 50, "speed": 32},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Limber", "Technician"],
        "hidden_abilities": ["Grip Claw"]
    },
    {
        "name": "Grapploct",
        "base_stats": {"hp": 80, "attack": 118, "defense": 90, "sp_attack": 70, "sp_defense": 80, "speed": 42},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Limber", "Technician"],
        "hidden_abilities": ["No Guard"]
    },
    {
        "name": "Sinistea",
        "base_stats": {"hp": 40, "attack": 45, "defense": 45, "sp_attack": 74, "sp_defense": 54, "speed": 50},
        "gender_ratio": None,
        "abilities": ["Weak Armor"],
        "hidden_abilities": ["Cursed Body"]
    },
    {
        "name": "Polteageist",
        "base_stats": {"hp": 60, "attack": 65, "defense": 65, "sp_attack": 134, "sp_defense": 114, "speed": 70},
        "gender_ratio": None,
        "abilities": ["Weak Armor"],
        "hidden_abilities": ["Cursed Body"]
    },
    {
        "name": "Hatenna",
        "base_stats": {"hp": 42, "attack": 30, "defense": 45, "sp_attack": 56, "sp_defense": 53, "speed": 39},
        "gender_ratio": {"male": 0.0, "female": 100.0},
        "abilities": ["Healer", "Anticipation"],
        "hidden_abilities": ["Magic Bounce"]
    },
    {
        "name": "Hattrem",
        "base_stats": {"hp": 57, "attack": 40, "defense": 65, "sp_attack": 86, "sp_defense": 73, "speed": 49},
        "gender_ratio": {"male": 0.0, "female": 100.0},
        "abilities": ["Healer", "Anticipation"],
        "hidden_abilities": ["Magic Bounce"]
    },
    {
        "name": "Hatterene",
        "base_stats": {"hp": 57, "attack": 90, "defense": 95, "sp_attack": 136, "sp_defense": 103, "speed": 29},
        "gender_ratio": {"male": 0.0, "female": 100.0},
        "abilities": ["Healer", "Anticipation"],
        "hidden_abilities": ["Magic Bounce"]
    },
    {
        "name": "Impidimp",
        "base_stats": {"hp": 45, "attack": 45, "defense": 30, "sp_attack": 55, "sp_defense": 40, "speed": 50},
        "gender_ratio": {"male": 100.0, "female": 0.0},
        "abilities": ["Prankster", "Frisk"],
        "hidden_abilities": ["Pickpocket"]
    },
    {
        "name": "Morgrem",
        "base_stats": {"hp": 65, "attack": 60, "defense": 45, "sp_attack": 75, "sp_defense": 55, "speed": 70},
        "gender_ratio": {"male": 100.0, "female": 0.0},
        "abilities": ["Prankster", "Frisk"],
        "hidden_abilities": ["Pickpocket"]
    },
    {
        "name": "Grimmsnarl",
        "base_stats": {"hp": 95, "attack": 120, "defense": 65, "sp_attack": 95, "sp_defense": 75, "speed": 60},
        "gender_ratio": {"male": 100.0, "female": 0.0},
        "abilities": ["Prankster", "Frisk"],
        "hidden_abilities": ["Pickpocket"]
    },
    {
        "name": "Obstagoon",
        "base_stats": {"hp": 93, "attack": 90, "defense": 101, "sp_attack": 60, "sp_defense": 81, "speed": 95},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Reckless", "Guts"],
        "hidden_abilities": ["Defiant"]
    },
    {
        "name": "Perrserker",
        "base_stats": {"hp": 70, "attack": 110, "defense": 100, "sp_attack": 50, "sp_defense": 60, "speed": 50},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Battle Armor", "Tough Claws"],
        "hidden_abilities": ["Steely Spirit"]
    },
    {
        "name": "Cursola",
        "base_stats": {"hp": 60, "attack": 95, "defense": 50, "sp_attack": 145, "sp_defense": 130, "speed": 30},
        "gender_ratio": {"male": 25.0, "female": 75.0},
        "abilities": ["Weak Armor"],
        "hidden_abilities": ["Perish Body"]
    },
    {
        "name": "Sirfetch’d",
        "base_stats": {"hp": 62, "attack": 135, "defense": 95, "sp_attack": 68, "sp_defense": 82, "speed": 65},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Steadfast"],
        "hidden_abilities": ["Scrappy"]
    },
    {
        "name": "Mr. Rime",
        "base_stats": {"hp": 80, "attack": 85, "defense": 75, "sp_attack": 110, "sp_defense": 100, "speed": 70},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Tangled Feet", "Screen Cleaner"],
        "hidden_abilities": ["Ice Body"]
    },
    {
        "name": "Runerigus",
        "base_stats": {"hp": 58, "attack": 95, "defense": 145, "sp_attack": 50, "sp_defense": 105, "speed": 30},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Wandering Spirit"],
        "hidden_abilities": []
    },
    {
        "name": "Milcery",
        "base_stats": {"hp": 45, "attack": 40, "defense": 40, "sp_attack": 50, "sp_defense": 61, "speed": 34},
        "gender_ratio": {"male": 0.0, "female": 100.0},
        "abilities": ["Sweet Veil"],
        "hidden_abilities": ["Aroma Veil"]
    },
    {
        "name": "Alcremie",
        "base_stats": {"hp": 65, "attack": 60, "defense": 75, "sp_attack": 110, "sp_defense": 121, "speed": 64},
        "gender_ratio": {"male": 0.0, "female": 100.0},
        "abilities": ["Sweet Veil"],
        "hidden_abilities": ["Aroma Veil"]
    },
    {
        "name": "Falinks",
        "base_stats": {"hp": 65, "attack": 100, "defense": 100, "sp_attack": 70, "sp_defense": 60, "speed": 75},
        "gender_ratio": {"male": 0.0, "female": 0.0},
        "abilities": ["Battle Armor"],
        "hidden_abilities": ["Defiant"]
    },
    {
        "name": "Pincurchin",
        "base_stats": {"hp": 48, "attack": 101, "defense": 95, "sp_attack": 91, "sp_defense": 85, "speed": 15},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Lightning Rod"],
        "hidden_abilities": ["Electric Surge"]
    },
    {
        "name": "Snom",
        "base_stats": {"hp": 30, "attack": 25, "defense": 35, "sp_attack": 45, "sp_defense": 30, "speed": 20},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Shield Dust"],
        "hidden_abilities": ["Ice Scales"]
    },
    {
        "name": "Frosmoth",
        "base_stats": {"hp": 70, "attack": 65, "defense": 60, "sp_attack": 125, "sp_defense": 90, "speed": 65},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Shield Dust"],
        "hidden_abilities": ["Ice Scales"]
    },
    {
        "name": "Stonjourner",
        "base_stats": {"hp": 100, "attack": 125, "defense": 135, "sp_attack": 20, "sp_defense": 20, "speed": 70},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Power Spot"],
        "hidden_abilities": []
    },
    {
        "name": "Eiscue",
        "base_stats": {"hp": 75, "attack": 80, "defense": 110, "sp_attack": 65, "sp_defense": 90, "speed": 50},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Ice Face"],
        "hidden_abilities": []
    },
    {
        "name": "Indeedee",
        "base_stats": {"hp": 60, "attack": 65, "defense": 55, "sp_attack": 105, "sp_defense": 95, "speed": 95},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Inner Focus", "Synchronize"],
        "hidden_abilities": ["Psychic Surge"]
    },
    {
        "name": "Morpeko",
        "base_stats": {"hp": 58, "attack": 95, "defense": 58, "sp_attack": 70, "sp_defense": 58, "speed": 97},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Hunger Switch"],
        "hidden_abilities": []
    },
    {
        "name": "Cufant",
        "base_stats": {"hp": 72, "attack": 80, "defense": 49, "sp_attack": 40, "sp_defense": 49, "speed": 40},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Sheer Force"],
        "hidden_abilities": ["Heavy Metal"]
    },
    {
        "name": "Copperajah",
        "base_stats": {"hp": 122, "attack": 130, "defense": 69, "sp_attack": 80, "sp_defense": 69, "speed": 30},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Sheer Force"],
        "hidden_abilities": ["Heavy Metal"]
    },
    {
        "name": "Dracozolt",
        "base_stats": {"hp": 90, "attack": 100, "defense": 90, "sp_attack": 80, "sp_defense": 70, "speed": 75},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Volt Absorb", "Hustle"],
        "hidden_abilities": ["Sand Rush"]
    },
    {
        "name": "Arctozolt",
        "base_stats": {"hp": 90, "attack": 100, "defense": 90, "sp_attack": 90, "sp_defense": 80, "speed": 55},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Volt Absorb", "Static"],
        "hidden_abilities": ["Slush Rush"]
    },
    {
        "name": "Dracovish",
        "base_stats": {"hp": 90, "attack": 90, "defense": 100, "sp_attack": 70, "sp_defense": 80, "speed": 75},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Water Absorb", "Strong Jaw"],
        "hidden_abilities": ["Sand Rush"]
    },
    {
        "name": "Arctovish",
        "base_stats": {"hp": 90, "attack": 90, "defense": 100, "sp_attack": 80, "sp_defense": 90, "speed": 55},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Water Absorb", "Ice Body"],
        "hidden_abilities": ["Slush Rush"]
    },
    {
        "name": "Duraludon",
        "base_stats": {"hp": 70, "attack": 95, "defense": 115, "sp_attack": 120, "sp_defense": 50, "speed": 85},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Light Metal", "Heavy Metal"],
        "hidden_abilities": ["Stalwart"]
    },
    {
        "name": "Dreepy",
        "base_stats": {"hp": 28, "attack": 60, "defense": 30, "sp_attack": 40, "sp_defense": 30, "speed": 82},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Clear Body", "Infiltrator"],
        "hidden_abilities": ["Cursed Body"]
    },
    {
        "name": "Drakloak",
        "base_stats": {"hp": 68, "attack": 80, "defense": 50, "sp_attack": 60, "sp_defense": 50, "speed": 102},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Clear Body", "Infiltrator"],
        "hidden_abilities": ["Cursed Body"]
    },
    {
        "name": "Dragapult",
        "base_stats": {"hp": 88, "attack": 120, "defense": 75, "sp_attack": 100, "sp_defense": 75, "speed": 142},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Clear Body", "Infiltrator"],
        "hidden_abilities": ["Cursed Body"]
    },
    {
        "name": "Zacian",
        "base_stats": {"hp": 92, "attack": 130, "defense": 115, "sp_attack": 80, "sp_defense": 115, "speed": 138},
        "gender_ratio": {"male": 0.0, "female": 0.0},
        "abilities": ["Intrepid Sword"],
        "hidden_abilities": []
    },
    {
        "name": "Zamazenta",
        "base_stats": {"hp": 92, "attack": 130, "defense": 115, "sp_attack": 80, "sp_defense": 115, "speed": 138},
        "gender_ratio": {"male": 0.0, "female": 0.0},
        "abilities": ["Dauntless Shield"],
        "hidden_abilities": []
    },
    {
        "name": "Eternatus",
        "base_stats": {"hp": 140, "attack": 85, "defense": 95, "sp_attack": 145, "sp_defense": 95, "speed": 130},
        "gender_ratio": {"male": 0.0, "female": 0.0},
        "abilities": ["Pressure"],
        "hidden_abilities": []
    },
    {
        "name": "Kubfu",
        "base_stats": {"hp": 60, "attack": 90, "defense": 60, "sp_attack": 53, "sp_defense": 50, "speed": 72},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Inner Focus"],
        "hidden_abilities": []
    },
    {
        "name": "Urshifu",
        "base_stats": {"hp": 100, "attack": 130, "defense": 100, "sp_attack": 63, "sp_defense": 60, "speed": 97},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Unseen Fist"],
        "hidden_abilities": []
    },
    {
        "name": "Zarude",
        "base_stats": {"hp": 105, "attack": 120, "defense": 105, "sp_attack": 70, "sp_defense": 95, "speed": 105},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Leaf Guard"],
        "hidden_abilities": []
    },
    {
        "name": "Regieleki",
        "base_stats": {"hp": 80, "attack": 100, "defense": 50, "sp_attack": 100, "sp_defense": 50, "speed": 200},
        "gender_ratio": {"male": 0.0, "female": 0.0},
        "abilities": ["Transistor"],
        "hidden_abilities": []
    },
    {
        "name": "Regidrago",
        "base_stats": {"hp": 200, "attack": 100, "defense": 50, "sp_attack": 100, "sp_defense": 50, "speed": 80},
        "gender_ratio": {"male": 0.0, "female": 0.0},
        "abilities": ["Dragon's Maw"],
        "hidden_abilities": []
    },
    {
        "name": "Glastrier",
        "base_stats": {"hp": 100, "attack": 145, "defense": 130, "sp_attack": 65, "sp_defense": 110, "speed": 30},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Chilling Neigh"],
        "hidden_abilities": []
    },
    {
        "name": "Spectrier",
        "base_stats": {"hp": 100, "attack": 65, "defense": 60, "sp_attack": 145, "sp_defense": 80, "speed": 130},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Grim Neigh"],
        "hidden_abilities": []
    },
    {
        "name": "Calyrex",
        "base_stats": {"hp": 100, "attack": 80, "defense": 80, "sp_attack": 80, "sp_defense": 80, "speed": 80},
        "gender_ratio": {"male": 0.0, "female": 0.0},
        "abilities": ["Unnerve"],
        "hidden_abilities": []
    },
    {
        "name": "Wyrdeer",
        "base_stats": {"hp": 103, "attack": 105, "defense": 72, "sp_attack": 105, "sp_defense": 75, "speed": 65},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Intimidate", "Frisk"],
        "hidden_abilities": ["Sap Sipper"]
    },
    {
        "name": "Kleavor",
        "base_stats": {"hp": 70, "attack": 135, "defense": 95, "sp_attack": 45, "sp_defense": 70, "speed": 85},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Swarm", "Sheer Force"],
        "hidden_abilities": ["Steadfast"]
    },
    {
        "name": "Ursaluna",
        "base_stats": {"hp": 130, "attack": 140, "defense": 105, "sp_attack": 45, "sp_defense": 80, "speed": 50},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Guts", "Bulletproof"],
        "hidden_abilities": ["Unnerve"]
    },
    {
        "name": "Basculegion",
        "base_stats": {"hp": 120, "attack": 112, "defense": 65, "sp_attack": 80, "sp_defense": 75, "speed": 78},
        "gender_ratio": {"male": 100.0, "female": 0.0},
        "abilities": ["Swift Swim", "Adaptability"],
        "hidden_abilities": ["Mold Breaker"]
    },
    {
        "name": "Basculegion (Female)",
        "base_stats": {"hp": 120, "attack": 92, "defense": 65, "sp_attack": 100, "sp_defense": 75, "speed": 78},
        "gender_ratio": {"male": 0.0, "female": 100.0},
        "abilities": ["Swift Swim", "Adaptability"],
        "hidden_abilities": ["Mold Breaker"]
    },
    {
        "name": "Sneasler",
        "base_stats": {"hp": 80, "attack": 130, "defense": 60, "sp_attack": 40, "sp_defense": 80, "speed": 120},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Pressure", "Unburden"],
        "hidden_abilities": ["Poison Touch"]
    },
    {
        "name": "Overqwil",
        "base_stats": {"hp": 85, "attack": 115, "defense": 95, "sp_attack": 65, "sp_defense": 65, "speed": 85},
        "gender_ratio": {"male": 50.0, "female": 50.0},
        "abilities": ["Poison Point", "Swift Swim"],
        "hidden_abilities": ["Intimidate"]
    },
    {
        "name": "Enamorus",
        "base_stats": {"hp": 74, "attack": 115, "defense": 70, "sp_attack": 135, "sp_defense": 80, "speed": 106},
        "gender_ratio": {"male": 0.0, "female": 100.0},
        "abilities": ["Cute Charm"],
        "hidden_abilities": ["Contrary"]
    }
]
POKEMON_GEN9 = [
    {
        "name": "Sprigatito",
        "base_stats": {"hp": 40, "attack": 61, "defense": 54, "sp_attack": 45, "sp_defense": 45, "speed": 65},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Protean"]
    },
    {
        "name": "Floragato",
        "base_stats": {"hp": 61, "attack": 80, "defense": 63, "sp_attack": 60, "sp_defense": 63, "speed": 83},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Protean"]
    },
    {
        "name": "Meowscarada",
        "base_stats": {"hp": 76, "attack": 110, "defense": 70, "sp_attack": 81, "sp_defense": 70, "speed": 123},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Overgrow"],
        "hidden_abilities": ["Protean"]
    },
    {
        "name": "Fuecoco",
        "base_stats": {"hp": 67, "attack": 45, "defense": 59, "sp_attack": 63, "sp_defense": 40, "speed": 36},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Unaware"]
    },
    {
        "name": "Crocalor",
        "base_stats": {"hp": 81, "attack": 55, "defense": 78, "sp_attack": 90, "sp_defense": 58, "speed": 49},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Unaware"]
    },
    {
        "name": "Skeledirge",
        "base_stats": {"hp": 104, "attack": 75, "defense": 100, "sp_attack": 110, "sp_defense": 75, "speed": 66},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Blaze"],
        "hidden_abilities": ["Unaware"]
    },
    {
        "name": "Quaxly",
        "base_stats": {"hp": 55, "attack": 65, "defense": 45, "sp_attack": 50, "sp_defense": 45, "speed": 50},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Moxie"]
    },
    {
        "name": "Quaxwell",
        "base_stats": {"hp": 70, "attack": 85, "defense": 65, "sp_attack": 65, "sp_defense": 60, "speed": 65},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Moxie"]
    },
    {
        "name": "Quaquaval",
        "base_stats": {"hp": 85, "attack": 120, "defense": 80, "sp_attack": 85, "sp_defense": 75, "speed": 85},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Torrent"],
        "hidden_abilities": ["Moxie"]
    },
    {
        "name": "Lechonk",
        "base_stats": {"hp": 54, "attack": 45, "defense": 40, "sp_attack": 35, "sp_defense": 45, "speed": 35},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Gluttony"],
        "hidden_abilities": ["Healer"]
    },
    {
        "name": "Oinkologne",
        "base_stats": {"hp": 110, "attack": 100, "defense": 75, "sp_attack": 59, "sp_defense": 80, "speed": 65},
        "gender_ratio": {"male": 87.5, "female": 12.5},
        "abilities": ["Gluttony"],
        "hidden_abilities": ["Healer"]
    },
    {
        "name": "Tarountula",
        "base_stats": {"hp": 35, "attack": 41, "defense": 45, "sp_attack": 29, "sp_defense": 40, "speed": 20},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate"],
        "hidden_abilities": ["Rattled"]
    },
    {
        "name": "Spidops",
        "base_stats": {"hp": 60, "attack": 79, "defense": 92, "sp_attack": 52, "sp_defense": 86, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate"],
        "hidden_abilities": ["Rattled"]
    },
    {
        "name": "Nymble",
        "base_stats": {"hp": 33, "attack": 46, "defense": 40, "sp_attack": 21, "sp_defense": 25, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pickup"],
        "hidden_abilities": ["Technician"]
    },
    {
        "name": "Lokix",
        "base_stats": {"hp": 71, "attack": 102, "defense": 78, "sp_attack": 52, "sp_defense": 55, "speed": 92},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Steadfast"],
        "hidden_abilities": ["Inner Focus"]
    },
    {
        "name": "Pawmi",
        "base_stats": {"hp": 45, "attack": 50, "defense": 20, "sp_attack": 40, "sp_defense": 25, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Static"],
        "hidden_abilities": ["Motor Drive"]
    },
    {
        "name": "Pawmo",
        "base_stats": {"hp": 60, "attack": 75, "defense": 40, "sp_attack": 50, "sp_defense": 40, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Static"],
        "hidden_abilities": ["Motor Drive"]
    },
    {
        "name": "Pawmot",
        "base_stats": {"hp": 70, "attack": 115, "defense": 70, "sp_attack": 70, "sp_defense": 60, "speed": 105},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Volt Absorb"],
        "hidden_abilities": ["Motor Drive"]
    },
    {
        "name": "Tandemaus",
        "base_stats": {"hp": 50, "attack": 50, "defense": 45, "sp_attack": 40, "sp_defense": 45, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Cheek Pouch"],
        "hidden_abilities": ["Pickup"]
    },
    {
        "name": "Maushold (Family of Four)",
        "base_stats": {"hp": 74, "attack": 75, "defense": 70, "sp_attack": 65, "sp_defense": 75, "speed": 111},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Friend Guard"],
        "hidden_abilities": []
    },
    {
        "name": "Fidough",
        "base_stats": {"hp": 37, "attack": 55, "defense": 70, "sp_attack": 30, "sp_defense": 55, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Own Tempo"],
        "hidden_abilities": ["Klutz"]
    },
    {
        "name": "Dachsbun",
        "base_stats": {"hp": 57, "attack": 80, "defense": 115, "sp_attack": 50, "sp_defense": 80, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Well-Baked Body"],
        "hidden_abilities": ["Own Tempo"]
    },
    {
        "name": "Smoliv",
        "base_stats": {"hp": 41, "attack": 35, "defense": 45, "sp_attack": 58, "sp_defense": 51, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll"],
        "hidden_abilities": ["Gluttony"]
    },
    {
        "name": "Dolliv",
        "base_stats": {"hp": 52, "attack": 53, "defense": 60, "sp_attack": 78, "sp_defense": 78, "speed": 33},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll"],
        "hidden_abilities": ["Gluttony"]
    },
    {
        "name": "Arboliva",
        "base_stats": {"hp": 78, "attack": 69, "defense": 90, "sp_attack": 125, "sp_defense": 109, "speed": 39},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Seed Sower"],
        "hidden_abilities": ["Harvest"]
    },
    {
        "name": "Squawkabilly",
        "base_stats": {"hp": 82, "attack": 96, "defense": 51, "sp_attack": 45, "sp_defense": 51, "speed": 92},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate", "Hustle", "Guts"],
        "hidden_abilities": []
    },
    {
        "name": "Nacli",
        "base_stats": {"hp": 55, "attack": 55, "defense": 75, "sp_attack": 35, "sp_defense": 35, "speed": 25},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Purifying Salt", "Sturdy"],
        "hidden_abilities": ["Clear Body"]
    },
    {
        "name": "Naclstack",
        "base_stats": {"hp": 60, "attack": 60, "defense": 100, "sp_attack": 35, "sp_defense": 65, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Purifying Salt", "Sturdy"],
        "hidden_abilities": ["Clear Body"]
    },
    {
        "name": "Garganacl",
        "base_stats": {"hp": 100, "attack": 100, "defense": 130, "sp_attack": 45, "sp_defense": 90, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Purifying Salt", "Sturdy"],
        "hidden_abilities": ["Clear Body"]
    },
    {
        "name": "Charcadet",
        "base_stats": {"hp": 40, "attack": 50, "defense": 40, "sp_attack": 50, "sp_defense": 40, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Flash Fire"],
        "hidden_abilities": ["Flame Body"]
    },
    {
        "name": "Armarouge",
        "base_stats": {"hp": 85, "attack": 60, "defense": 100, "sp_attack": 125, "sp_defense": 80, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Flash Fire"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Ceruledge",
        "base_stats": {"hp": 75, "attack": 125, "defense": 80, "sp_attack": 60, "sp_defense": 100, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Flash Fire"],
        "hidden_abilities": ["Weak Armor"]
    },
    {
        "name": "Tadbulb",
        "base_stats": {"hp": 61, "attack": 31, "defense": 41, "sp_attack": 59, "sp_defense": 35, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Own Tempo", "Static"],
        "hidden_abilities": ["Damp"]
    },
    {
        "name": "Bellibolt",
        "base_stats": {"hp": 109, "attack": 64, "defense": 91, "sp_attack": 103, "sp_defense": 83, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Electromorphosis", "Static"],
        "hidden_abilities": ["Damp"]
    },
    {
        "name": "Wattrel",
        "base_stats": {"hp": 40, "attack": 40, "defense": 35, "sp_attack": 55, "sp_defense": 40, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Wind Power", "Volt Absorb"],
        "hidden_abilities": ["Competitive"]
    },
    {
        "name": "Kilowattrel",
        "base_stats": {"hp": 70, "attack": 70, "defense": 60, "sp_attack": 105, "sp_defense": 60, "speed": 125},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Wind Power", "Volt Absorb"],
        "hidden_abilities": ["Competitive"]
    },
    {
        "name": "Maschiff",
        "base_stats": {"hp": 60, "attack": 78, "defense": 60, "sp_attack": 40, "sp_defense": 51, "speed": 51},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate", "Run Away"],
        "hidden_abilities": ["Stakeout"]
    },
    {
        "name": "Mabosstiff",
        "base_stats": {"hp": 80, "attack": 120, "defense": 90, "sp_attack": 60, "sp_defense": 70, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Intimidate", "Guard Dog"],
        "hidden_abilities": ["Stakeout"]
    },
    {
        "name": "Shroodle",
        "base_stats": {"hp": 40, "attack": 65, "defense": 35, "sp_attack": 40, "sp_defense": 35, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Unburden", "Pickpocket"],
        "hidden_abilities": ["Prankster"]
    },
    {
        "name": "Grafaiai",
        "base_stats": {"hp": 63, "attack": 95, "defense": 65, "sp_attack": 80, "sp_defense": 72, "speed": 110},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Unburden", "Poison Touch"],
        "hidden_abilities": ["Prankster"]
    },
    {
        "name": "Bramblin",
        "base_stats": {"hp": 40, "attack": 65, "defense": 30, "sp_attack": 45, "sp_defense": 35, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Wind Rider"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Brambleghast",
        "base_stats": {"hp": 55, "attack": 115, "defense": 70, "sp_attack": 80, "sp_defense": 70, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Wind Rider"],
        "hidden_abilities": ["Infiltrator"]
    },
    {
        "name": "Toedscool",
        "base_stats": {"hp": 40, "attack": 40, "defense": 35, "sp_attack": 50, "sp_defense": 100, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Mycelium Might"],
        "hidden_abilities": []
    },
    {
        "name": "Toedscruel",
        "base_stats": {"hp": 80, "attack": 70, "defense": 65, "sp_attack": 80, "sp_defense": 120, "speed": 100},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Mycelium Might"],
        "hidden_abilities": []
    },
    {
        "name": "Klawf",
        "base_stats": {"hp": 70, "attack": 100, "defense": 115, "sp_attack": 35, "sp_defense": 55, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Anger Shell", "Shell Armor"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Capsakid",
        "base_stats": {"hp": 50, "attack": 62, "defense": 40, "sp_attack": 62, "sp_defense": 40, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Insomnia"],
        "hidden_abilities": ["Klutz"]
    },
    {
        "name": "Scovillain",
        "base_stats": {"hp": 65, "attack": 108, "defense": 65, "sp_attack": 108, "sp_defense": 65, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Chlorophyll", "Insomnia"],
        "hidden_abilities": ["Moody"]
    },
    {
        "name": "Rellor",
        "base_stats": {"hp": 41, "attack": 50, "defense": 60, "sp_attack": 31, "sp_defense": 58, "speed": 30},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Compound Eyes"],
        "hidden_abilities": ["Shed Skin"]
    },
    {
        "name": "Rabsca",
        "base_stats": {"hp": 75, "attack": 50, "defense": 85, "sp_attack": 115, "sp_defense": 100, "speed": 45},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Synchronize"],
        "hidden_abilities": ["Telepathy"]
    },
    {
        "name": "Flittle",
        "base_stats": {"hp": 30, "attack": 35, "defense": 30, "sp_attack": 55, "sp_defense": 30, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Anticipation", "Frisk"],
        "hidden_abilities": ["Speed Boost"]
    },
    {
        "name": "Espathra",
        "base_stats": {"hp": 95, "attack": 60, "defense": 60, "sp_attack": 101, "sp_defense": 60, "speed": 105},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Opportunist", "Frisk"],
        "hidden_abilities": ["Speed Boost"]
    },
    {
        "name": "Tinkatink",
        "base_stats": {"hp": 50, "attack": 45, "defense": 45, "sp_attack": 35, "sp_defense": 64, "speed": 58},
        "gender_ratio": {"male": 10, "female": 90},
        "abilities": ["Mold Breaker", "Own Tempo"],
        "hidden_abilities": ["Pickpocket"]
    },
    {
        "name": "Tinkatuff",
        "base_stats": {"hp": 65, "attack": 55, "defense": 55, "sp_attack": 45, "sp_defense": 82, "speed": 78},
        "gender_ratio": {"male": 10, "female": 90},
        "abilities": ["Mold Breaker", "Own Tempo"],
        "hidden_abilities": ["Pickpocket"]
    },
    {
        "name": "Tinkaton",
        "base_stats": {"hp": 85, "attack": 75, "defense": 77, "sp_attack": 70, "sp_defense": 105, "speed": 94},
        "gender_ratio": {"male": 10, "female": 90},
        "abilities": ["Mold Breaker", "Own Tempo"],
        "hidden_abilities": ["Pickpocket"]
    },
    {
        "name": "Wiglett",
        "base_stats": {"hp": 10, "attack": 55, "defense": 25, "sp_attack": 35, "sp_defense": 25, "speed": 95},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Gooey", "Rattled"],
        "hidden_abilities": ["Sand Veil"]
    },
    {
        "name": "Wugtrio",
        "base_stats": {"hp": 35, "attack": 100, "defense": 50, "sp_attack": 50, "sp_defense": 70, "speed": 120},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Gooey", "Rattled"],
        "hidden_abilities": ["Sand Veil"]
    },
    {
        "name": "Bombirdier",
        "base_stats": {"hp": 70, "attack": 103, "defense": 85, "sp_attack": 60, "sp_defense": 85, "speed": 82},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Big Pecks", "Keen Eye"],
        "hidden_abilities": ["Rocky Payload"]
    },
    {
        "name": "Finizen",
        "base_stats": {"hp": 70, "attack": 45, "defense": 40, "sp_attack": 45, "sp_defense": 40, "speed": 75},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Water Veil"],
        "hidden_abilities": []
    },
    {
        "name": "Palafin",
        "base_stats": {"hp": 100, "attack": 70, "defense": 72, "sp_attack": 53, "sp_defense": 62, "speed": 100},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Zero to Hero"],
        "hidden_abilities": []
    },
    {
        "name": "Varoom",
        "base_stats": {"hp": 45, "attack": 70, "defense": 63, "sp_attack": 30, "sp_defense": 45, "speed": 47},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Overcoat"],
        "hidden_abilities": ["Slow Start"]
    },
    {
        "name": "Revavroom",
        "base_stats": {"hp": 80, "attack": 119, "defense": 90, "sp_attack": 54, "sp_defense": 67, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Overcoat"],
        "hidden_abilities": ["Filter"]
    },
    {
        "name": "Cyclizar",
        "base_stats": {"hp": 70, "attack": 95, "defense": 65, "sp_attack": 85, "sp_defense": 65, "speed": 121},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Shed Skin"],
        "hidden_abilities": ["Regenerator"]
    },
    {
        "name": "Orthworm",
        "base_stats": {"hp": 70, "attack": 85, "defense": 145, "sp_attack": 60, "sp_defense": 55, "speed": 65},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Earth Eater"],
        "hidden_abilities": ["Sand Veil"]
    },
    {
        "name": "Glimmet",
        "base_stats": {"hp": 48, "attack": 35, "defense": 42, "sp_attack": 105, "sp_defense": 60, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Toxic Debris"],
        "hidden_abilities": ["Corrosion"]
    },
    {
        "name": "Glimmora",
        "base_stats": {"hp": 83, "attack": 55, "defense": 90, "sp_attack": 130, "sp_defense": 81, "speed": 86},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Toxic Debris"],
        "hidden_abilities": ["Corrosion"]
    },
    {
        "name": "Greavard",
        "base_stats": {"hp": 50, "attack": 61, "defense": 60, "sp_attack": 30, "sp_defense": 55, "speed": 34},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Pickup"],
        "hidden_abilities": ["Fluffy"]
    },
    {
        "name": "Houndstone",
        "base_stats": {"hp": 72, "attack": 101, "defense": 100, "sp_attack": 50, "sp_defense": 97, "speed": 68},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Sand Rush"],
        "hidden_abilities": ["Fluffy"]
    },
    {
        "name": "Flamigo",
        "base_stats": {"hp": 82, "attack": 115, "defense": 74, "sp_attack": 75, "sp_defense": 64, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Scrappy", "Tangled Feet"],
        "hidden_abilities": ["Costar"]
    },
    {
        "name": "Cetoddle",
        "base_stats": {"hp": 108, "attack": 68, "defense": 45, "sp_attack": 30, "sp_defense": 40, "speed": 43},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Thick Fat", "Snow Cloak"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Cetitan",
        "base_stats": {"hp": 170, "attack": 113, "defense": 65, "sp_attack": 45, "sp_defense": 55, "speed": 73},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Thick Fat", "Snow Cloak"],
        "hidden_abilities": ["Sheer Force"]
    },
    {
        "name": "Veluza",
        "base_stats": {"hp": 90, "attack": 102, "defense": 73, "sp_attack": 78, "sp_defense": 65, "speed": 70},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Mold Breaker", "Sharpness"],
        "hidden_abilities": []
    },
    {
        "name": "Dondozo",
        "base_stats": {"hp": 150, "attack": 100, "defense": 115, "sp_attack": 65, "sp_defense": 65, "speed": 35},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Unaware", "Oblivious"],
        "hidden_abilities": ["Water Veil"]
    },
    {
        "name": "Tatsugiri",
        "base_stats": {"hp": 68, "attack": 50, "defense": 60, "sp_attack": 120, "sp_defense": 95, "speed": 82},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Commander", "Storm Drain"],
        "hidden_abilities": ["Water Veil"]
    },
    {
        "name": "Annihilape",
        "base_stats": {"hp": 110, "attack": 115, "defense": 80, "sp_attack": 50, "sp_defense": 90, "speed": 90},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Vital Spirit", "Inner Focus"],
        "hidden_abilities": ["Defiant"]
    },
    {
        "name": "Clodsire",
        "base_stats": {"hp": 130, "attack": 75, "defense": 60, "sp_attack": 45, "sp_defense": 100, "speed": 20},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Poison Point", "Water Absorb"],
        "hidden_abilities": ["Unaware"]
    },
    {
        "name": "Farigiraf",
        "base_stats": {"hp": 120, "attack": 90, "defense": 70, "sp_attack": 110, "sp_defense": 70, "speed": 60},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Cud Chew", "Armor Tail"],
        "hidden_abilities": ["Sap Sipper"]
    },
    {
        "name": "Dudunsparce",
        "base_stats": {"hp": 125, "attack": 100, "defense": 80, "sp_attack": 85, "sp_defense": 75, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Serene Grace", "Run Away"],
        "hidden_abilities": ["Rattled"]
    },
    {
        "name": "Kingambit",
        "base_stats": {"hp": 100, "attack": 135, "defense": 120, "sp_attack": 60, "sp_defense": 85, "speed": 50},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Defiant"],
        "hidden_abilities": ["Pressure"]
    },
    {
        "name": "Great Tusk",
        "base_stats": {"hp": 115, "attack": 131, "defense": 131, "sp_attack": 53, "sp_defense": 53, "speed": 87},
        "gender_ratio": None,
        "abilities": ["Protosynthesis"],
        "hidden_abilities": []
    },
    {
        "name": "Scream Tail",
        "base_stats": {"hp": 115, "attack": 65, "defense": 99, "sp_attack": 65, "sp_defense": 115, "speed": 111},
        "gender_ratio": None,
        "abilities": ["Protosynthesis"],
        "hidden_abilities": []
    },
    {
        "name": "Brute Bonnet",
        "base_stats": {"hp": 111, "attack": 127, "defense": 99, "sp_attack": 79, "sp_defense": 99, "speed": 55},
        "gender_ratio": None,
        "abilities": ["Protosynthesis"],
        "hidden_abilities": []
    },
    {
        "name": "Flutter Mane",
        "base_stats": {"hp": 55, "attack": 55, "defense": 55, "sp_attack": 135, "sp_defense": 135, "speed": 135},
        "gender_ratio": None,
        "abilities": ["Protosynthesis"],
        "hidden_abilities": []
    },
    {
        "name": "Slither Wing",
        "base_stats": {"hp": 85, "attack": 135, "defense": 79, "sp_attack": 85, "sp_defense": 105, "speed": 81},
        "gender_ratio": None,
        "abilities": ["Protosynthesis"],
        "hidden_abilities": []
    },
    {
        "name": "Sandy Shocks",
        "base_stats": {"hp": 85, "attack": 81, "defense": 97, "sp_attack": 121, "sp_defense": 85, "speed": 101},
        "gender_ratio": None,
        "abilities": ["Protosynthesis"],
        "hidden_abilities": []
    },
    {
        "name": "Iron Treads",
        "base_stats": {"hp": 90, "attack": 112, "defense": 120, "sp_attack": 72, "sp_defense": 70, "speed": 106},
        "gender_ratio": None,
        "abilities": ["Quark Drive"],
        "hidden_abilities": []
    },
    {
        "name": "Iron Bundle",
        "base_stats": {"hp": 56, "attack": 80, "defense": 114, "sp_attack": 124, "sp_defense": 60, "speed": 136},
        "gender_ratio": None,
        "abilities": ["Quark Drive"],
        "hidden_abilities": []
    },
    {
        "name": "Iron Hands",
        "base_stats": {"hp": 154, "attack": 140, "defense": 108, "sp_attack": 50, "sp_defense": 68, "speed": 50},
        "gender_ratio": None,
        "abilities": ["Quark Drive"],
        "hidden_abilities": []
    },
    {
        "name": "Iron Jugulis",
        "base_stats": {"hp": 94, "attack": 80, "defense": 86, "sp_attack": 122, "sp_defense": 80, "speed": 108},
        "gender_ratio": None,
        "abilities": ["Quark Drive"],
        "hidden_abilities": []
    },
    {
        "name": "Iron Moth",
        "base_stats": {"hp": 80, "attack": 70, "defense": 60, "sp_attack": 140, "sp_defense": 110, "speed": 110},
        "gender_ratio": None,
        "abilities": ["Quark Drive"],
        "hidden_abilities": []
    },
    {
        "name": "Iron Thorns",
        "base_stats": {"hp": 100, "attack": 134, "defense": 110, "sp_attack": 70, "sp_defense": 84, "speed": 72},
        "gender_ratio": None,
        "abilities": ["Quark Drive"],
        "hidden_abilities": []
    },
    {
        "name": "Frigibax",
        "base_stats": {"hp": 65, "attack": 75, "defense": 45, "sp_attack": 35, "sp_defense": 45, "speed": 55},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Thermal Exchange"],
        "hidden_abilities": ["Ice Body"]
    },
    {
        "name": "Arctibax",
        "base_stats": {"hp": 90, "attack": 95, "defense": 66, "sp_attack": 45, "sp_defense": 65, "speed": 62},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Thermal Exchange"],
        "hidden_abilities": ["Ice Body"]
    },
    {
        "name": "Baxcalibur",
        "base_stats": {"hp": 115, "attack": 145, "defense": 92, "sp_attack": 75, "sp_defense": 86, "speed": 87},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Thermal Exchange"],
        "hidden_abilities": ["Ice Body"]
    },
    {
        "name": "Gimmighoul",
        "base_stats": {"hp": 45, "attack": 30, "defense": 70, "sp_attack": 75, "sp_defense": 70, "speed": 10},
        "gender_ratio": None,
        "abilities": ["Rattled"],
        "hidden_abilities": []
    },
    {
        "name": "Gholdengo",
        "base_stats": {"hp": 87, "attack": 60, "defense": 95, "sp_attack": 133, "sp_defense": 91, "speed": 84},
        "gender_ratio": None,
        "abilities": ["Good as Gold"],
        "hidden_abilities": []
    },
    {
        "name": "Wo-Chien",
        "base_stats": {"hp": 85, "attack": 85, "defense": 100, "sp_attack": 95, "sp_defense": 135, "speed": 70},
        "gender_ratio": None,
        "abilities": ["Tablets of Ruin"],
        "hidden_abilities": []
    },
    {
        "name": "Chien-Pao",
        "base_stats": {"hp": 80, "attack": 120, "defense": 80, "sp_attack": 90, "sp_defense": 65, "speed": 135},
        "gender_ratio": None,
        "abilities": ["Sword of Ruin"],
        "hidden_abilities": []
    },
    {
        "name": "Ting-Lu",
        "base_stats": {"hp": 155, "attack": 110, "defense": 125, "sp_attack": 55, "sp_defense": 80, "speed": 45},
        "gender_ratio": None,
        "abilities": ["Vessel of Ruin"],
        "hidden_abilities": []
    },
    {
        "name": "Chi-Yu",
        "base_stats": {"hp": 55, "attack": 80, "defense": 80, "sp_attack": 135, "sp_defense": 120, "speed": 100},
        "gender_ratio": None,
        "abilities": ["Beads of Ruin"],
        "hidden_abilities": []
    },
    {
        "name": "Roaring Moon",
        "base_stats": {"hp": 105, "attack": 139, "defense": 71, "sp_attack": 55, "sp_defense": 101, "speed": 119},
        "gender_ratio": None,
        "abilities": ["Protosynthesis"],
        "hidden_abilities": []
    },
    {
        "name": "Iron Valiant",
        "base_stats": {"hp": 74, "attack": 130, "defense": 90, "sp_attack": 120, "sp_defense": 60, "speed": 116},
        "gender_ratio": None,
        "abilities": ["Quark Drive"],
        "hidden_abilities": []
    },
    {
        "name": "Koraidon",
        "base_stats": {"hp": 100, "attack": 135, "defense": 115, "sp_attack": 85, "sp_defense": 100, "speed": 135},
        "gender_ratio": None,
        "abilities": ["Orichalcum Pulse"],
        "hidden_abilities": []
    },
    {
        "name": "Miraidon",
        "base_stats": {"hp": 100, "attack": 85, "defense": 100, "sp_attack": 135, "sp_defense": 115, "speed": 135},
        "gender_ratio": None,
        "abilities": ["Hadron Engine"],
        "hidden_abilities": []
    },
    {
        "name": "Walking Wake",
        "base_stats": {"hp": 99, "attack": 83, "defense": 91, "sp_attack": 125, "sp_defense": 83, "speed": 109},
        "gender_ratio": None,
        "abilities": ["Protosynthesis"],
        "hidden_abilities": []
    },
    {
        "name": "Iron Leaves",
        "base_stats": {"hp": 90, "attack": 130, "defense": 88, "sp_attack": 70, "sp_defense": 108, "speed": 104},
        "gender_ratio": None,
        "abilities": ["Quark Drive"],
        "hidden_abilities": []
    },
    {
        "name": "Dipplin",
        "base_stats": {"hp": 80, "attack": 80, "defense": 110, "sp_attack": 95, "sp_defense": 80, "speed": 40},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Supersweet Syrup", "Gluttony"],
        "hidden_abilities": []
    },
    {
        "name": "Poltchageist",
        "base_stats": {"hp": 40, "attack": 45, "defense": 45, "sp_attack": 74, "sp_defense": 54, "speed": 50},
        "gender_ratio": None,
        "abilities": ["Hospitality"],
        "hidden_abilities": ["Heatproof"]
    },
    {
        "name": "Sinistcha",
        "base_stats": {"hp": 71, "attack": 60, "defense": 106, "sp_attack": 121, "sp_defense": 80, "speed": 70},
        "gender_ratio": None,
        "abilities": ["Hospitality"],
        "hidden_abilities": ["Heatproof"]
    },
    {
        "name": "Okidogi",
        "base_stats": {"hp": 88, "attack": 128, "defense": 115, "sp_attack": 58, "sp_defense": 86, "speed": 80},
        "gender_ratio": None,
        "abilities": ["Guard Dog"],
        "hidden_abilities": []
    },
    {
        "name": "Munkidori",
        "base_stats": {"hp": 88, "attack": 75, "defense": 66, "sp_attack": 130, "sp_defense": 90, "speed": 106},
        "gender_ratio": None,
        "abilities": ["Toxic Chain"],
        "hidden_abilities": []
    },
    {
        "name": "Fezandipiti",
        "base_stats": {"hp": 88, "attack": 91, "defense": 82, "sp_attack": 70, "sp_defense": 125, "speed": 99},
        "gender_ratio": None,
        "abilities": ["Toxic Chain"],
        "hidden_abilities": []
    },
    {
        "name": "Ogerpon",
        "base_stats": {"hp": 80, "attack": 120, "defense": 84, "sp_attack": 60, "sp_defense": 96, "speed": 110},
        "gender_ratio": {"male": 0, "female": 100},
        "abilities": ["Defiant"],
        "hidden_abilities": []
    },
    {
        "name": "Archaludon",
        "base_stats": {"hp": 90, "attack": 105, "defense": 130, "sp_attack": 125, "sp_defense": 65, "speed": 85},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Stamina"],
        "hidden_abilities": ["Stalwart"]
    },
    {
        "name": "Hydrapple",
        "base_stats": {"hp": 106, "attack": 80, "defense": 110, "sp_attack": 120, "sp_defense": 80, "speed": 44},
        "gender_ratio": {"male": 50, "female": 50},
        "abilities": ["Supersweet Syrup", "Regenerator"],
        "hidden_abilities": []
    },
    {
        "name": "Gouging Fire",
        "base_stats": {"hp": 105, "attack": 115, "defense": 121, "sp_attack": 65, "sp_defense": 93, "speed": 91},
        "gender_ratio": None,
        "abilities": ["Protosynthesis"],
        "hidden_abilities": []
    },
    {
        "name": "Raging Bolt",
        "base_stats": {"hp": 125, "attack": 73, "defense": 91, "sp_attack": 137, "sp_defense": 89, "speed": 75},
        "gender_ratio": None,
        "abilities": ["Protosynthesis"],
        "hidden_abilities": []
    },
    {
        "name": "Iron Boulder",
        "base_stats": {"hp": 90, "attack": 120, "defense": 80, "sp_attack": 68, "sp_defense": 108, "speed": 124},
        "gender_ratio": None,
        "abilities": ["Quark Drive"],
        "hidden_abilities": []
    },
    {
        "name": "Iron Crown",
        "base_stats": {"hp": 90, "attack": 72, "defense": 100, "sp_attack": 122, "sp_defense": 108, "speed": 98},
        "gender_ratio": None,
        "abilities": ["Quark Drive"],
        "hidden_abilities": []
    },
    {
        "name": "Terapagos",
        "base_stats": {"hp": 160, "attack": 105, "defense": 110, "sp_attack": 130, "sp_defense": 110, "speed": 85},
        "gender_ratio": None,
        "abilities": ["Tera Shell"],
        "hidden_abilities": []
    },
    {
        "name": "Pecharunt",
        "base_stats": {"hp": 88, "attack": 88, "defense": 160, "sp_attack": 88, "sp_defense": 88, "speed": 88},
        "gender_ratio": None,
        "abilities": ["Poison Puppeteer"],
        "hidden_abilities": []
    }
]
def get_nature_multipliers(nature):
    return NATURE_EFFECTS.get(nature.lower(), {})
def get_all_pokemon():
    return (POKEMON_GEN1 + POKEMON_GEN2 + POKEMON_GEN3 + POKEMON_GEN4 +
            POKEMON_GEN5 + POKEMON_GEN6 + POKEMON_GEN7 + POKEMON_GEN8 + POKEMON_GEN9)
def get_pokemon_by_name(name):
    name_lower = name.lower()
    all_pokemon = get_all_pokemon()
    for pokemon in all_pokemon:
        if pokemon["name"].lower() == name_lower:
            return pokemon
    return None
def assign_gender(gender_ratio):
    if gender_ratio is None:
        return None
    if (isinstance(gender_ratio, dict) and
        gender_ratio.get("male", 0) == 0 and
        gender_ratio.get("female", 0) == 0):
        return None
    if isinstance(gender_ratio, dict):
        male_ratio = gender_ratio.get("male", 50)
        female_ratio = gender_ratio.get("female", 50)
        if male_ratio == 0 and female_ratio == 0:
            return None
        rand = random.random() * 100
        if rand < male_ratio:
            return "<:male:1400956267979214971>"
        else:
            return "<:female:1400956073573224520>"
    return None