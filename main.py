import discord
from discord.ext import commands
from pokémon import (
    get_nature_multipliers,
    POKEMON_GEN1,
    POKEMON_GEN2,
    POKEMON_GEN3,
    POKEMON_GEN4,
    POKEMON_GEN5,
    POKEMON_GEN6,
    POKEMON_GEN7,
    POKEMON_GEN8,
    POKEMON_GEN9,
    NATURES,
    NATURE_EFFECTS,
    get_pokemon_by_name,
    get_all_pokemon,
    assign_gender
)
from stats_iv_calculation import (
    calculate_official_stats,
    generate_pokemon_ivs,
    calculate_iv_percentage
)
from moves import POKEMON_MOVES, get_move_by_name
from type_effectiveness import get_type_effectiveness, get_effectiveness_text
from movesets_scraper import get_all_moves_comprehensive
import random
import json
import string
import os
import math
import requests
from bs4 import BeautifulSoup
import asyncio
import time
import re
from datetime import datetime
from discord.ui import View, Button
from PIL import Image, ImageDraw, ImageFont
import io
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    intents=intents
)

# Global state variables (moved from bot attributes)
message_count = 0
current_spawn = None
active_battles = {}
SHOP_ITEMS = {
    "rare candy": {
        "name": "Rare Candy",
        "price": 50,
        "currency": "pokécoins",
        "emoji": "<:rare_candy:1403486543477473521>",
        "description": "A candy that is packed with energy. It raises the level of a Pokémon by one."
    },
    "summoning stone": {
        "name": "Summoning Stone",
        "price": 200,
        "currency": "gems",
        "emoji": "<:Summoning_stone:1405194343056408747>",
        "description": "An ancient stone filled with powerful energy that can summon any pokémon."
    }
}
class PurchaseConfirmationView(View):
    def __init__(self, user_id, item_name, amount, total_cost, currency, is_gems=False):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.item_name = item_name
        self.amount = amount
        self.total_cost = total_cost
        self.currency = currency
        self.is_gems = is_gems
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, emoji='✅')
    async def confirm(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your purchase confirmation.", ephemeral=True)
            return
        trainer_data = get_trainer_data(self.user_id)
        if not trainer_data:
            await interaction.response.send_message("You are not registered as a trainer.", ephemeral=True)
            return
        if self.is_gems:
            current_coins = get_user_pokecoins(trainer_data)
            if current_coins < self.total_cost:
                await interaction.response.edit_message(
                    content=f"Not enough pokécoins! You have {current_coins} pokécoins but need {self.total_cost} pokécoins to buy {self.amount} gems.",
                    view=None
                )
                return
            if deduct_pokecoins(trainer_data, self.total_cost):
                current_gems = trainer_data.get("Shards", 0)
                trainer_data["Shards"] = current_gems + self.amount
                if update_trainer_data(str(self.user_id), trainer_data):
                    await interaction.response.edit_message(
                        content=f"You purchased {self.amount} Gems type @Pokékiro#8400 inventory to see your items.",
                        view=None
                    )
                else:
                    await interaction.response.edit_message(
                        content="Purchase failed. Please try again later.",
                        view=None
                    )
            else:
                await interaction.response.edit_message(
                    content="Purchase failed. Please try again later.",
                    view=None
                )
        else:
            if self.currency == "gems":
                current_balance = trainer_data.get("Shards", 0)
                if current_balance < self.total_cost:
                    await interaction.response.edit_message(
                        content="You not have enough Gems to buy Summoning Stone.",
                        view=None
                    )
                    return
                trainer_data["Shards"] -= self.total_cost
            else:
                if not deduct_pokecoins(trainer_data, self.total_cost):
                    await interaction.response.edit_message(
                        content="You don't have enough pokécoins to complete this purchase.",
                        view=None
                    )
                    return
            add_item_to_inventory(trainer_data, self.item_name, self.amount)
            if update_trainer_data(str(self.user_id), trainer_data):
                await interaction.response.edit_message(
                    content=f"You purchased {self.amount} {self.item_name} type @Pokékiro#8400 inventory to see your items.",
                    view=None
                )
            else:
                await interaction.response.edit_message(
                    content="Purchase failed. Please try again later.",
                    view=None
                )
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, emoji='❌')
    async def cancel(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your purchase confirmation.", ephemeral=True)
            return
        await interaction.response.edit_message(content="Aborted.", view=None)
def load_trainers():
    try:
        if os.path.exists("trainers.json"):
            with open("trainers.json", "r") as f:
                return json.load(f)
        return {}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}
def save_trainers(trainers_data):
    try:
        with open("trainers.json", "w") as f:
            json.dump(trainers_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving trainers data: {e}")
        return False
def load_market():
    try:
        if os.path.exists("market.json"):
            with open("market.json", "r") as f:
                return json.load(f)
        return {"listings": [], "next_id": 1}
    except (json.JSONDecodeError, FileNotFoundError):
        return {"listings": [], "next_id": 1}
def save_market(market_data):
    try:
        with open("market.json", "w") as f:
            json.dump(market_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving market data: {e}")
        return False
def generate_trainer_id():
    length = random.randint(5, 10)
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
def is_trainer_registered(user_id):
    trainers = load_trainers()
    return str(user_id) in trainers
def register_trainer(user_id, gender):
    trainers = load_trainers()
    if str(user_id) in trainers:
        return None, "You are already registered."
    trainer_id = generate_trainer_id()
    registered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trainer_data = {
        "UserID": str(user_id),
        "Gender": gender,
        "TrainerID": trainer_id,
        "RegisteredAt": registered_at,
        "StarterPokemon": None,
        "HasChosenStarter": False,
        "TotalMessages": 0,
        "LastLevelUp": 1,
        "pokécoins": 0,
        "Shards": 0,
        "BattlePasses": 0,
        "inventory": {},
        "SelectedPokemon": None
    }
    trainers[str(user_id)] = trainer_data
    if save_trainers(trainers):
        return trainer_data, None
    else:
        return None, "Failed to save registration. Please try again."
def get_trainer_data(user_id):
    trainers = load_trainers()
    trainer_data = trainers.get(str(user_id))
    if trainer_data:
        if "inventory" not in trainer_data:
            trainer_data["inventory"] = {}
        if "pokécoins" not in trainer_data and "pokecoins" not in trainer_data:
            trainer_data["pokécoins"] = 0
        if "SelectedPokemon" not in trainer_data:
            trainer_data["SelectedPokemon"] = None
        if "Shards" not in trainer_data:
            trainer_data["Shards"] = 0
        if "HasChosenStarter" not in trainer_data:
            trainer_data["HasChosenStarter"] = trainer_data.get("StarterPokemon") is not None
    return trainer_data
def update_trainer_data(user_id, trainer_data):
    trainers = load_trainers()
    trainers[str(user_id)] = trainer_data
    return save_trainers(trainers)
def get_user_pokecoins(trainer_data):
    if "pokécoins" in trainer_data:
        pokecoins = trainer_data["pokécoins"]
        if isinstance(pokecoins, list):
            return sum(pokecoins)
        return pokecoins
    elif "pokecoins" in trainer_data:
        return trainer_data["pokecoins"]
    return 0
def deduct_pokecoins(trainer_data, amount):
    current_coins = get_user_pokecoins(trainer_data)
    if current_coins < amount:
        return False
    new_amount = current_coins - amount
    if "pokécoins" in trainer_data:
        trainer_data["pokécoins"] = new_amount
    else:
        trainer_data["pokécoins"] = new_amount
    return True
def add_item_to_inventory(trainer_data, item_name, amount):
    if "inventory" not in trainer_data:
        trainer_data["inventory"] = {}
    if item_name in trainer_data["inventory"]:
        trainer_data["inventory"][item_name] += amount
    else:
        trainer_data["inventory"][item_name] = amount
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
def migrate_pokemon_stats():
    print("Starting Pokémon stats migration...")
    trainers = load_trainers()
    updated_count = 0
    for user_id, trainer_data in trainers.items():
        if trainer_data.get("StarterPokemon"):
            starter = trainer_data["StarterPokemon"]
            if update_pokemon_data(starter):
                updated_count += 1
                print(f"Updated starter {starter['name']} for user {user_id}")
        if "CaughtPokemons" in trainer_data:
            for i, pokemon in enumerate(trainer_data["CaughtPokemons"]):
                if update_pokemon_data(pokemon):
                    updated_count += 1
                    print(f"Updated caught {pokemon['name']} for user {user_id}")
    if save_trainers(trainers):
        print(f"Migration completed successfully! Updated {updated_count} Pokémon.")
        return True
    else:
        print("Migration failed - could not save updated data.")
        return False
def update_pokemon_data(pokemon):
    try:
        if "ivs" not in pokemon or "base_stats" not in pokemon:
            print(f"Skipping {pokemon.get('name', 'Unknown')} - missing required data")
            return False
        level = pokemon.get("level", 1)
        nature = pokemon.get("nature", "hardy").lower()
        evs = pokemon.get("evs", {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
        new_stats = calculate_official_stats(pokemon["base_stats"], pokemon["ivs"], level, nature, evs)
        new_iv_percentage = calculate_iv_percentage(pokemon["ivs"])
        pokemon["calculated_stats"] = new_stats
        pokemon["iv_percentage"] = new_iv_percentage
        if "evs" not in pokemon:
            pokemon["evs"] = evs
        return True
    except Exception as e:
        print(f"Error updating Pokémon {pokemon.get('name', 'Unknown')}: {e}")
        return False
def convert_text_gender_to_emoji(gender):
    if isinstance(gender, str):
        gender_lower = gender.lower().strip()
        if gender_lower == "male" or gender_lower == "m":
            return "<:male:1400956267979214971>"
        elif gender_lower == "female" or gender_lower == "f":
            return "<:female:1400956073573224520>"
        elif gender_lower == "unknown" or gender_lower == "genderless" or gender_lower == "":
            return "<:unknown:1401145566863560755>"
        elif gender.startswith("<:") and gender.endswith(">"):
            return gender
    return "<:unknown:1401145566863560755>"
def assign_pokemon_gender(pokemon_name):
    pokemon_data = get_pokemon_by_name(pokemon_name)
    if not pokemon_data or "gender_ratio" not in pokemon_data:
        gender_ratio = {"male": 87.5, "female": 12.5}
    else:
        gender_ratio = pokemon_data["gender_ratio"]
    gender_result = assign_gender(gender_ratio)
    if gender_result is None:
        return "<:unknown:1401145566863560755>"
    return gender_result
def create_spawned_pokemon(pokemon_data, level=None):
    if level is None:
        level = random.randint(1, 50)
    ivs = generate_pokemon_ivs()
    nature = random.choice(NATURES).lower()
    evs = {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0}
    base_stats = pokemon_data["base_stats"]
    iv_percentage = calculate_iv_percentage(ivs)
    calculated_stats = calculate_official_stats(base_stats, ivs, level, nature, evs)
    ability = pokemon_data.get("abilities", ["Unknown"])[0] if pokemon_data.get("abilities") else "Unknown"
    gender = assign_pokemon_gender(pokemon_data["name"])
    spawned_pokemon = {
        "dex": pokemon_data.get("dex", 0),
        "name": pokemon_data["name"].lower(),
        "gender": gender,
        "level": level,
        "iv_percentage": iv_percentage,
        "ivs": ivs,
        "nature": nature,
        "ability": ability,
        "base_stats": base_stats.copy(),
        "calculated_stats": calculated_stats,
        "evs": evs.copy()
    }
    return spawned_pokemon
def get_pokemon_sprite_url(pokemon_name, is_back_sprite=False):
    sprite_name = pokemon_name.lower().replace(" ", "").replace("'", "").replace(".", "").replace("-", "")
    special_names = {
        "charizard": "charizard",
        "rowlet": "rowlet",
        "mr.mime": "mrmime",
        "farfetch'd": "farfetchd",
        "ho-oh": "hooh"
    }
    if sprite_name in special_names:
        sprite_name = special_names[sprite_name]
    sprite_urls = []
    if is_back_sprite:
        sprite_urls.append(f"https://play.pokemonshowdown.com/sprites/gen5ani-back/{sprite_name}.gif")
        sprite_urls.append(f"https://play.pokemonshowdown.com/sprites/xyani-back/{sprite_name}.gif")
        sprite_urls.append(f"https://play.pokemonshowdown.com/sprites/gen5-back/{sprite_name}.png")
    else:
        sprite_urls.append(f"https://play.pokemonshowdown.com/sprites/gen5ani/{sprite_name}.gif")
        sprite_urls.append(f"https://play.pokemonshowdown.com/sprites/xyani/{sprite_name}.gif")
        sprite_urls.append(f"https://play.pokemonshowdown.com/sprites/gen5/{sprite_name}.png")
    return sprite_urls
def download_pokemon_sprite(pokemon_name, is_back_sprite=False, preserve_animation=False):
    sprite_urls = get_pokemon_sprite_url(pokemon_name, is_back_sprite)
    for sprite_url in sprite_urls:
        try:
            response = requests.get(sprite_url, timeout=10)
            response.raise_for_status()
            if preserve_animation:
                print(f"Successfully downloaded animated sprite for {pokemon_name} from {sprite_url}")
                return io.BytesIO(response.content)
            sprite_image = Image.open(io.BytesIO(response.content))
            if sprite_image.format == 'GIF':
                sprite_image.seek(0)
                sprite_image = sprite_image.convert("RGBA")
            else:
                if sprite_image.mode != 'RGBA':
                    sprite_image = sprite_image.convert("RGBA")
            print(f"Successfully downloaded sprite for {pokemon_name} from {sprite_url}")
            return sprite_image
        except requests.exceptions.RequestException as e:
            print(f"Failed to download sprite for {pokemon_name} from {sprite_url}: {e}")
            continue
        except Exception as e:
            print(f"Error processing sprite for {pokemon_name} from {sprite_url}: {e}")
            continue
    print(f"Failed to download sprite for {pokemon_name} from all available sources")
    return None
def create_animated_battle_field(user_pokemon_name, opponent_pokemon_name, viewing_user_id, battle_data):
    try:
        print(f"Creating animated battle field with {user_pokemon_name} vs {opponent_pokemon_name}")
        user_sprite_data = download_pokemon_sprite(user_pokemon_name, is_back_sprite=True, preserve_animation=True)
        opponent_sprite_data = download_pokemon_sprite(opponent_pokemon_name, is_back_sprite=False, preserve_animation=True)
        if not user_sprite_data or not opponent_sprite_data:
            print("Failed to download animated sprites, falling back to static image")
            return create_battle_field_image(user_pokemon_name, opponent_pokemon_name, viewing_user_id, battle_data)
        battle_field = Image.open("battle_field.png").convert("RGBA")
        battle_width, battle_height = battle_field.size
        user_sprite_gif = Image.open(io.BytesIO(user_sprite_data))
        opponent_sprite_gif = Image.open(io.BytesIO(opponent_sprite_data))
        challenger_pokemon_pos = (250, 550)
        target_pokemon_pos = (680, 275)
        user_frames = getattr(user_sprite_gif, 'n_frames', 1)
        opponent_frames = getattr(opponent_sprite_gif, 'n_frames', 1)
        max_frames = max(user_frames, opponent_frames)
        final_frames = []
        durations = []
        for frame_idx in range(max_frames):
            frame = battle_field.copy()
            user_sprite_gif.seek(frame_idx % user_frames)
            original_size = user_sprite_gif.size
            scale_factor = 3
            new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
            user_frame = user_sprite_gif.convert("RGBA").resize(new_size, Image.Resampling.LANCZOS)
            opponent_sprite_gif.seek(frame_idx % opponent_frames)
            original_size = opponent_sprite_gif.size
            new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
            opponent_frame = opponent_sprite_gif.convert("RGBA").resize(new_size, Image.Resampling.LANCZOS)
            user_centered_pos = (challenger_pokemon_pos[0] - user_frame.width // 2,
                                challenger_pokemon_pos[1] - user_frame.height // 2)
            opponent_centered_pos = (target_pokemon_pos[0] - opponent_frame.width // 2,
                                   target_pokemon_pos[1] - opponent_frame.height // 2)
            frame.paste(user_frame, user_centered_pos, user_frame)
            frame.paste(opponent_frame, opponent_centered_pos, opponent_frame)
            
            # Add challenger health bar at the specified position for each frame
            try:
                challenger_health_bar = Image.open("challenger_health_bar.png").convert("RGBA")
                challenger_health_bar_pos = (449, 480)
                frame.paste(challenger_health_bar, challenger_health_bar_pos, challenger_health_bar)
            except Exception as e:
                print(f"Failed to add challenger health bar to frame {frame_idx}: {e}")
            
            # Add target health bar for opponent Pokemon
            try:
                target_health_bar = Image.open("target_health_bar.png").convert("RGBA")
                target_health_bar_pos = (0, 120)
                frame.paste(target_health_bar, target_health_bar_pos, target_health_bar)
            except Exception as e:
                print(f"Failed to add target health bar to frame {frame_idx}: {e}")
            
            final_frames.append(frame)
            try:
                duration = user_sprite_gif.info.get('duration', 100)
            except:
                duration = 100
            durations.append(duration)
        image_buffer = io.BytesIO()
        final_frames[0].save(
            image_buffer,
            format='GIF',
            save_all=True,
            append_images=final_frames[1:],
            duration=150,
            loop=0,
            optimize=True
        )
        image_buffer.seek(0)
        print(f"Created animated battle field with {max_frames} frames")
        return image_buffer
    except Exception as e:
        print(f"Error creating animated battle field: {e}")
        return create_battle_field_image(user_pokemon_name, opponent_pokemon_name, viewing_user_id, battle_data)
def create_battle_field_image(user_pokemon_name, opponent_pokemon_name, viewing_user_id, battle_data):
    try:
        print(f"Creating battle field with {user_pokemon_name} vs {opponent_pokemon_name}")
        battle_field = Image.open("battle_field.png").convert("RGBA")
        battle_width, battle_height = battle_field.size
        print(f"Battle field size: {battle_width}x{battle_height}")
        challenger_pokemon_pos = (250, 550)
        target_pokemon_pos = (670, 280)
        print(f"Challenger sprite position: {challenger_pokemon_pos}, Target sprite position: {target_pokemon_pos}")
        challenger_sprite = download_pokemon_sprite(user_pokemon_name, is_back_sprite=True)
        if challenger_sprite:
            print(f"Downloaded challenger sprite for {user_pokemon_name}: {challenger_sprite.size} {challenger_sprite.mode}")
            original_size = challenger_sprite.size
            scale_factor = 2.5
            new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
            challenger_sprite = challenger_sprite.resize(new_size, Image.Resampling.LANCZOS)
            challenger_centered_pos = (challenger_pokemon_pos[0] - challenger_sprite.width // 2,
                                     challenger_pokemon_pos[1] - challenger_sprite.height // 2)
            battle_field.paste(challenger_sprite, challenger_centered_pos, challenger_sprite)
            print(f"Pasted challenger sprite at centered position {challenger_centered_pos}")
        else:
            print(f"Failed to download challenger sprite for {user_pokemon_name}")
        target_sprite = download_pokemon_sprite(opponent_pokemon_name, is_back_sprite=False)
        if target_sprite:
            print(f"Downloaded target sprite for {opponent_pokemon_name}: {target_sprite.size} {target_sprite.mode}")
            original_size = target_sprite.size
            scale_factor = 2.5
            new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
            target_sprite = target_sprite.resize(new_size, Image.Resampling.LANCZOS)
            target_centered_pos = (target_pokemon_pos[0] - target_sprite.width // 2,
                                 target_pokemon_pos[1] - target_sprite.height // 2)
            battle_field.paste(target_sprite, target_centered_pos, target_sprite)
            print(f"Pasted target sprite at centered position {target_centered_pos}")
        else:
            print(f"Failed to download target sprite for {opponent_pokemon_name}")
        
        # Add challenger health bar at the specified position
        try:
            challenger_health_bar = Image.open("challenger_health_bar.png").convert("RGBA")
            challenger_health_bar_pos = (459, 480)
            battle_field.paste(challenger_health_bar, challenger_health_bar_pos, challenger_health_bar)
            print(f"Added challenger health bar at position {challenger_health_bar_pos}")
        except Exception as e:
            print(f"Failed to add challenger health bar: {e}")
        
        # Add target health bar for opponent Pokemon
        try:
            target_health_bar = Image.open("target_health_bar.png").convert("RGBA")
            target_health_bar_pos = (5, 120)
            battle_field.paste(target_health_bar, target_health_bar_pos, target_health_bar)
            print(f"Added target health bar at position {target_health_bar_pos}")
        except Exception as e:
            print(f"Failed to add target health bar: {e}")
        
        image_buffer = io.BytesIO()
        battle_field.save(image_buffer, format='PNG')
        image_buffer.seek(0)
        print("Battle field image created successfully")
        return image_buffer
    except Exception as e:
        print(f"Error creating battle field image: {e}")
        import traceback
        traceback.print_exc()
        return None
def fix_existing_pokemon_genders():
    trainers = load_trainers()
    updated = False
    for user_id, trainer_data in trainers.items():
        if trainer_data.get("StarterPokemon"):
            starter = trainer_data["StarterPokemon"]
            old_gender = starter.get("gender", "")
            pokemon_name = starter["name"]
            new_gender = assign_pokemon_gender(pokemon_name)
            if old_gender != new_gender:
                trainer_data["StarterPokemon"]["gender"] = new_gender
                updated = True
                print(f"Fixed starter {pokemon_name} gender for user {user_id}: {old_gender} -> {new_gender}")
        if "CaughtPokemons" in trainer_data:
            for i, pokemon in enumerate(trainer_data["CaughtPokemons"]):
                old_gender = pokemon.get("gender", "")
                pokemon_name = pokemon["name"]
                new_gender = assign_pokemon_gender(pokemon_name)
                if old_gender != new_gender:
                    trainer_data["CaughtPokemons"][i]["gender"] = new_gender
                    updated = True
                    print(f"Fixed caught {pokemon_name} gender for user {user_id}: {old_gender} -> {new_gender}")
    if updated:
        save_trainers(trainers)
        return True
    return False
def fix_market_listings_genders():
    market_data = load_market()
    updated = False
    for listing in market_data.get("listings", []):
        pokemon = listing.get("pokemon", {})
        old_gender = pokemon.get("gender", "")
        pokemon_name = pokemon.get("name", "")
        if pokemon_name:
            new_gender = assign_pokemon_gender(pokemon_name)
            if old_gender != new_gender:
                listing["pokemon"]["gender"] = new_gender
                updated = True
                print(f"Fixed market listing {listing.get('market_id', 'unknown')} {pokemon_name} gender: {old_gender} -> {new_gender}")
    if updated:
        save_market(market_data)
        return True
    return False
def get_user_pokemon_list(trainer_data):
    pokemon_list = []
    starter = trainer_data.get("StarterPokemon")
    if starter:
        pokemon_list.append({
            "order": 1,
            "name": starter["name"],
            "level": starter.get("level", 1),
            "type": "starter",
            "data": starter
        })
    if "CaughtPokemons" in trainer_data:
        order = 2 if starter else 1
        for caught_pokemon in trainer_data["CaughtPokemons"]:
            pokemon_list.append({
                "order": order,
                "name": caught_pokemon["name"],
                "level": caught_pokemon.get("level", 1),
                "type": "caught",
                "data": caught_pokemon
            })
            order += 1
    return pokemon_list
def get_pokemon_by_order(trainer_data, order_number):
    pokemon_list = get_user_pokemon_list(trainer_data)
    for pokemon in pokemon_list:
        if pokemon["order"] == order_number:
            return pokemon
    return None
def get_starter_pokemon_list():
    return {
        "bulbasaur": {"name": "Bulbasaur", "emoji": "<:bulbasaur:1390604553321189406>", "generation": "I (Kanto)"},
        "charmander": {"name": "Charmander", "emoji": "<:charmander:1390604778584801320>", "generation": "I (Kanto)"},
        "squirtle": {"name": "Squirtle", "emoji": "<:squirtle:1390604851091607564>", "generation": "I (Kanto)"},
        "chikorita": {"name": "Chikorita", "emoji": "<:grass_type:1406552601415122945>", "generation": "II (Johto)"},
        "cyndaquil": {"name": "Cyndaquil", "emoji": "<:fire_type:1406552697653559336>", "generation": "II (Johto)"},
        "totodile": {"name": "Totodile", "emoji": "<:water_type:1406552467319029860>", "generation": "II (Johto)"},
        "treecko": {"name": "Treecko", "emoji": "<:grass_type:1406552601415122945>", "generation": "III (Hoenn)"},
        "torchic": {"name": "Torchic", "emoji": "<:fire_type:1406552697653559336>", "generation": "III (Hoenn)"},
        "mudkip": {"name": "Mudkip", "emoji": "<:water_type:1406552467319029860>", "generation": "III (Hoenn)"},
        "turtwig": {"name": "Turtwig", "emoji": "<:grass_type:1406552601415122945>", "generation": "IV (Sinnoh)"},
        "chimchar": {"name": "Chimchar", "emoji": "<:fire_type:1406552697653559336>", "generation": "IV (Sinnoh)"},
        "piplup": {"name": "Piplup", "emoji": "<:water_type:1406552467319029860>", "generation": "IV (Sinnoh)"},
        "snivy": {"name": "Snivy", "emoji": "<:grass_type:1406552601415122945>", "generation": "V (Unova)"},
        "tepig": {"name": "Tepig", "emoji": "<:fire_type:1406552697653559336>", "generation": "V (Unova)"},
        "oshawott": {"name": "Oshawott", "emoji": "<:water_type:1406552467319029860>", "generation": "V (Unova)"},
        "chespin": {"name": "Chespin", "emoji": "<:grass_type:1406552601415122945>", "generation": "VI (Kalos)"},
        "fennekin": {"name": "Fennekin", "emoji": "<:fire_type:1406552697653559336>", "generation": "VI (Kalos)"},
        "froakie": {"name": "Froakie", "emoji": "<:water_type:1406552467319029860>", "generation": "VI (Kalos)"},
        "rowlet": {"name": "Rowlet", "emoji": "<:grass_type:1406552601415122945>", "generation": "VII (Alola)"},
        "litten": {"name": "Litten", "emoji": "<:fire_type:1406552697653559336>", "generation": "VII (Alola)"},
        "popplio": {"name": "Popplio", "emoji": "<:water_type:1406552467319029860>", "generation": "VII (Alola)"},
        "grookey": {"name": "Grookey", "emoji": "<:grass_type:1406552601415122945>", "generation": "VIII (Galar)"},
        "scorbunny": {"name": "Scorbunny", "emoji": "<:fire_type:1406552697653559336>", "generation": "VIII (Galar)"},
        "sobble": {"name": "Sobble", "emoji": "<:water_type:1406552467319029860>", "generation": "VIII (Galar)"},
        "sprigatito": {"name": "Sprigatito", "emoji": "<:sprigatito:1390607793266102302>", "generation": "IX (Paldea)"},
        "fuecoco": {"name": "Fuecoco", "emoji": "<:fuecoco:1390607859049435221>", "generation": "IX (Paldea)"},
        "quaxly": {"name": "Quaxly", "emoji": "<:quaxly:1390607905115602944>", "generation": "IX (Paldea)"}
    }
def get_pokemon_database():
    return {
        "bulbasaur": {
            "dex": 1, "name": "Bulbasaur", "emoji": "<:bulbasaur:1390604553321189406>",
            "base_stats": {"hp": 45, "attack": 49, "defense": 49, "sp_attack": 65, "sp_defense": 65, "speed": 45},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Grass", "Poison"]
        },
        "charmander": {
            "dex": 4, "name": "Charmander", "emoji": "<:charmander:1390604778584801320>",
            "base_stats": {"hp": 39, "attack": 52, "defense": 43, "sp_attack": 60, "sp_defense": 50, "speed": 65},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Fire"]
        },
        "squirtle": {
            "dex": 7, "name": "Squirtle", "emoji": "<:squirtle:1390604851091607564>",
            "base_stats": {"hp": 44, "attack": 48, "defense": 65, "sp_attack": 50, "sp_defense": 64, "speed": 43},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Water"]
        },
        "chikorita": {
            "dex": 152, "name": "Chikorita", "emoji": "<:grass_type:1406552601415122945>",
            "base_stats": {"hp": 45, "attack": 49, "defense": 65, "sp_attack": 49, "sp_defense": 65, "speed": 45},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Grass"]
        },
        "cyndaquil": {
            "dex": 155, "name": "Cyndaquil", "emoji": "<:fire_type:1406552697653559336>",
            "base_stats": {"hp": 39, "attack": 52, "defense": 43, "sp_attack": 60, "sp_defense": 50, "speed": 65},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Fire"]
        },
        "totodile": {
            "dex": 158, "name": "Totodile", "emoji": "<:water_type:1406552467319029860>",
            "base_stats": {"hp": 50, "attack": 65, "defense": 64, "sp_attack": 44, "sp_defense": 48, "speed": 43},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Water"]
        },
        "treecko": {
            "dex": 252, "name": "Treecko", "emoji": "<:grass_type:1406552601415122945>",
            "base_stats": {"hp": 40, "attack": 45, "defense": 35, "sp_attack": 65, "sp_defense": 55, "speed": 70},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Grass"]
        },
        "torchic": {
            "dex": 255, "name": "Torchic", "emoji": "<:fire_type:1406552697653559336>",
            "base_stats": {"hp": 45, "attack": 60, "defense": 40, "sp_attack": 70, "sp_defense": 50, "speed": 45},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Fire"]
        },
        "mudkip": {
            "dex": 258, "name": "Mudkip", "emoji": "<:water_type:1406552467319029860>",
            "base_stats": {"hp": 50, "attack": 70, "defense": 50, "sp_attack": 50, "sp_defense": 50, "speed": 40},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Water"]
        },
        "turtwig": {
            "dex": 387, "name": "Turtwig", "emoji": "<:grass_type:1406552601415122945>",
            "base_stats": {"hp": 55, "attack": 68, "defense": 64, "sp_attack": 45, "sp_defense": 55, "speed": 31},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Grass"]
        },
        "chimchar": {
            "dex": 390, "name": "Chimchar", "emoji": "<:fire_type:1406552697653559336>",
            "base_stats": {"hp": 44, "attack": 58, "defense": 44, "sp_attack": 58, "sp_defense": 44, "speed": 61},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Fire"]
        },
        "piplup": {
            "dex": 393, "name": "Piplup", "emoji": "<:water_type:1406552467319029860>",
            "base_stats": {"hp": 53, "attack": 51, "defense": 53, "sp_attack": 61, "sp_defense": 56, "speed": 40},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Water"]
        },
        "snivy": {
            "dex": 495, "name": "Snivy", "emoji": "<:grass_type:1406552601415122945>",
            "base_stats": {"hp": 45, "attack": 45, "defense": 55, "sp_attack": 45, "sp_defense": 55, "speed": 63},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Grass"]
        },
        "tepig": {
            "dex": 498, "name": "Tepig", "emoji": "<:fire_type:1406552697653559336>",
            "base_stats": {"hp": 65, "attack": 63, "defense": 45, "sp_attack": 45, "sp_defense": 45, "speed": 45},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Fire"]
        },
        "oshawott": {
            "dex": 501, "name": "Oshawott", "emoji": "<:water_type:1406552467319029860>",
            "base_stats": {"hp": 55, "attack": 55, "defense": 45, "sp_attack": 63, "sp_defense": 45, "speed": 45},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Water"]
        },
        "chespin": {
            "dex": 650, "name": "Chespin", "emoji": "<:grass_type:1406552601415122945>",
            "base_stats": {"hp": 56, "attack": 61, "defense": 65, "sp_attack": 48, "sp_defense": 45, "speed": 38},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Grass"]
        },
        "fennekin": {
            "dex": 653, "name": "Fennekin", "emoji": "<:fire_type:1406552697653559336>",
            "base_stats": {"hp": 40, "attack": 45, "defense": 40, "sp_attack": 62, "sp_defense": 60, "speed": 60},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Fire"]
        },
        "froakie": {
            "dex": 656, "name": "Froakie", "emoji": "<:water_type:1406552467319029860>",
            "base_stats": {"hp": 41, "attack": 56, "defense": 40, "sp_attack": 62, "sp_defense": 44, "speed": 71},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Water"]
        },
        "rowlet": {
            "dex": 722, "name": "Rowlet", "emoji": "<:grass_type:1406552601415122945>",
            "base_stats": {"hp": 68, "attack": 55, "defense": 55, "sp_attack": 50, "sp_defense": 50, "speed": 42},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Grass", "Flying"]
        },
        "litten": {
            "dex": 725, "name": "Litten", "emoji": "<:fire_type:1406552697653559336>",
            "base_stats": {"hp": 45, "attack": 65, "defense": 40, "sp_attack": 60, "sp_defense": 40, "speed": 70},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Fire"]
        },
        "popplio": {
            "dex": 728, "name": "Popplio", "emoji": "<:water_type:1406552467319029860>",
            "base_stats": {"hp": 50, "attack": 54, "defense": 54, "sp_attack": 66, "sp_defense": 56, "speed": 40},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Water"]
        },
        "grookey": {
            "dex": 810, "name": "Grookey", "emoji": "<:grass_type:1406552601415122945>",
            "base_stats": {"hp": 50, "attack": 65, "defense": 50, "sp_attack": 40, "sp_defense": 40, "speed": 65},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Grass"]
        },
        "scorbunny": {
            "dex": 813, "name": "Scorbunny", "emoji": "<:fire_type:1406552697653559336>",
            "base_stats": {"hp": 50, "attack": 71, "defense": 40, "sp_attack": 40, "sp_defense": 40, "speed": 69},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Fire"]
        },
        "sobble": {
            "dex": 816, "name": "Sobble", "emoji": "<:water_type:1406552467319029860>",
            "base_stats": {"hp": 50, "attack": 40, "defense": 40, "sp_attack": 70, "sp_defense": 40, "speed": 70},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Water"]
        },
        "sprigatito": {
            "dex": 906, "name": "Sprigatito", "emoji": "<:sprigatito:1390607793266102302>",
            "base_stats": {"hp": 40, "attack": 61, "defense": 54, "sp_attack": 45, "sp_defense": 45, "speed": 65},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Grass"]
        },
        "fuecoco": {
            "dex": 909, "name": "Fuecoco", "emoji": "<:fuecoco:1390607859049435221>",
            "base_stats": {"hp": 67, "attack": 45, "defense": 59, "sp_attack": 63, "sp_defense": 40, "speed": 36},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Fire"]
        },
        "quaxly": {
            "dex": 912, "name": "Quaxly", "emoji": "<:quaxly:1390607905115602944>",
            "base_stats": {"hp": 55, "attack": 65, "defense": 45, "sp_attack": 50, "sp_defense": 45, "speed": 50},
            "gender_ratio": {"male": 87.5, "female": 12.5}, "type": ["Water"]
        }
    }
def get_nature_database():
    return {
        "adamant": {"name": "Adamant", "increased": "attack", "decreased": "sp_attack"},
        "bashful": {"name": "Bashful", "increased": None, "decreased": None},
        "bold": {"name": "Bold", "increased": "defense", "decreased": "attack"},
        "brave": {"name": "Brave", "increased": "attack", "decreased": "speed"},
        "calm": {"name": "Calm", "increased": "sp_defense", "decreased": "attack"},
        "careful": {"name": "Careful", "increased": "sp_defense", "decreased": "sp_attack"},
        "docile": {"name": "Docile", "increased": None, "decreased": None},
        "gentle": {"name": "Gentle", "increased": "sp_defense", "decreased": "defense"},
        "hardy": {"name": "Hardy", "increased": None, "decreased": None},
        "hasty": {"name": "Hasty", "increased": "speed", "decreased": "defense"},
        "impish": {"name": "Impish", "increased": "defense", "decreased": "sp_attack"},
        "jolly": {"name": "Jolly", "increased": "speed", "decreased": "sp_attack"},
        "lax": {"name": "Lax", "increased": "defense", "decreased": "sp_defense"},
        "lonely": {"name": "Lonely", "increased": "attack", "decreased": "defense"},
        "mild": {"name": "Mild", "increased": "sp_attack", "decreased": "defense"},
        "modest": {"name": "Modest", "increased": "sp_attack", "decreased": "attack"},
        "naive": {"name": "Naive", "increased": "speed", "decreased": "sp_defense"},
        "naughty": {"name": "Naughty", "increased": "attack", "decreased": "sp_defense"},
        "quiet": {"name": "Quiet", "increased": "sp_attack", "decreased": "speed"},
        "quirky": {"name": "Quirky", "increased": None, "decreased": None},
        "rash": {"name": "Rash", "increased": "sp_attack", "decreased": "sp_defense"},
        "relaxed": {"name": "Relaxed", "increased": "defense", "decreased": "speed"},
        "sassy": {"name": "Sassy", "increased": "sp_defense", "decreased": "speed"},
        "serious": {"name": "Serious", "increased": None, "decreased": None},
        "timid": {"name": "Timid", "increased": "speed", "decreased": "attack"}
    }
def get_abilities_database():
    return {
        "bulbasaur": {"normal": "Overgrow", "hidden": "Chlorophyll"},
        "charmander": {"normal": "Blaze", "hidden": "Solar Power"},
        "squirtle": {"normal": "Torrent", "hidden": "Rain Dish"},
        "chikorita": {"normal": "Overgrow", "hidden": "Leaf Guard"},
        "cyndaquil": {"normal": "Blaze", "hidden": "Flash Fire"},
        "totodile": {"normal": "Torrent", "hidden": "Sheer Force"},
        "treecko": {"normal": "Overgrow", "hidden": "Unburden"},
        "torchic": {"normal": "Blaze", "hidden": "Speed Boost"},
        "mudkip": {"normal": "Torrent", "hidden": "Damp"},
        "turtwig": {"normal": "Overgrow", "hidden": "Shell Armor"},
        "chimchar": {"normal": "Blaze", "hidden": "Iron Fist"},
        "piplup": {"normal": "Torrent", "hidden": "Defiant"},
        "snivy": {"normal": "Overgrow", "hidden": "Contrary"},
        "tepig": {"normal": "Blaze", "hidden": "Reckless"},
        "oshawott": {"normal": "Torrent", "hidden": "Shell Armor"},
        "chespin": {"normal": "Overgrow", "hidden": "Bulletproof"},
        "fennekin": {"normal": "Blaze", "hidden": "Magician"},
        "froakie": {"normal": "Torrent", "hidden": "Protean"},
        "rowlet": {"normal": "Overgrow", "hidden": "Long Reach"},
        "litten": {"normal": "Blaze", "hidden": "Intimidate"},
        "popplio": {"normal": "Torrent", "hidden": "Liquid Voice"},
        "grookey": {"normal": "Overgrow", "hidden": "Grassy Surge"},
        "scorbunny": {"normal": "Blaze", "hidden": "Libero"},
        "sobble": {"normal": "Torrent", "hidden": "Sniper"},
        "sprigatito": {"normal": "Overgrow", "hidden": "Protean"},
        "fuecoco": {"normal": "Blaze", "hidden": "Unaware"},
        "quaxly": {"normal": "Torrent", "hidden": "Moxie"}
    }
def calculate_xp_required(level):
    if level >= 100:
        return 0
    return level * 50
def calculate_level_from_messages(total_xp):
    # Level N requires N × 50 XP total
    # Level 1 = 50 XP, Level 2 = 100 XP, Level 3 = 150 XP, etc.
    level = 1
    remaining_xp = total_xp
    
    while level < 100:
        xp_needed_for_next_level = level * 50  # XP needed to reach next level
        if remaining_xp >= xp_needed_for_next_level:
            remaining_xp -= xp_needed_for_next_level
            level += 1
        else:
            break
    
    
    return level, remaining_xp
def update_trainer_xp(user_id):
    trainers = load_trainers()
    if str(user_id) not in trainers:
        return False, None
    trainer = trainers[str(user_id)]
    trainer["TotalMessages"] = trainer.get("TotalMessages", 0) + 1
    level_up_info = None
    selected_pokemon = trainer.get("SelectedPokemon")
    if selected_pokemon is not None:
        pokemon_data = None
        if selected_pokemon["type"] == "starter" and trainer["StarterPokemon"] is not None:
            pokemon_data = trainer["StarterPokemon"]
        elif selected_pokemon["type"] == "caught" and "CaughtPokemons" in trainer:
            caught_index = selected_pokemon["order"] - 2
            if 0 <= caught_index < len(trainer["CaughtPokemons"]):
                pokemon_data = trainer["CaughtPokemons"][caught_index]
        if pokemon_data is not None:
            # Add individual Pokemon XP tracking
            if "xp" not in pokemon_data:
                pokemon_data["xp"] = 0
            
            old_xp = pokemon_data["xp"]
            # Add 1 XP per message
            pokemon_data["xp"] += 1
            total_xp = pokemon_data["xp"]
            
            
            # Calculate what level this Pokemon should be
            target_level, remaining_xp = calculate_level_from_messages(total_xp)
            current_level = pokemon_data.get("level", 1)
            
            # Only level up if target level is higher
            if target_level > current_level:
                # Level up one level at a time for proper move learning
                new_level = current_level + 1
                pokemon_data["level"] = new_level
                trainer["LastLevelUp"] = new_level
                
                moves_to_learn = []
                try:
                    movesets = get_all_moves_comprehensive(pokemon_data["name"])
                    if "level_up" in movesets and movesets["level_up"]:
                        for level in range(current_level + 1, new_level + 1):
                            for move_info in movesets["level_up"]:
                                if move_info.get("level") and move_info["level"].isdigit():
                                    move_level = int(move_info["level"])
                                    if move_level == level:
                                        moves_to_learn.append(move_info["move"])
                except:
                    pass
                if moves_to_learn:
                    if "learned_moves" not in pokemon_data:
                        pokemon_data["learned_moves"] = []
                    for move in moves_to_learn:
                        if move not in pokemon_data["learned_moves"]:
                            pokemon_data["learned_moves"].append(move)
                level_up_info = {
                    "pokemon_name": pokemon_data["name"],
                    "new_level": new_level,
                    "old_level": current_level,
                    "moves_learned": moves_to_learn,
                    "total_xp": total_xp,
                    "xp_for_next_level": (new_level + 1) * 50 - total_xp
                }
    trainers[str(user_id)] = trainer
    save_success = save_trainers(trainers)
    return save_success, level_up_info
def get_gender_emoji(pokemon_name):
    return assign_pokemon_gender(pokemon_name)
def pick_starter_pokemon(user_id, pokemon_name):
    trainers = load_trainers()
    user_id_str = str(user_id)
    if user_id_str not in trainers:
        return None, "You need to register first! Use the register command."
    if trainers[user_id_str].get("HasChosenStarter", False):
        return None, "You already have chosen a starter Pokemon! You cannot choose another one."
    starters = get_starter_pokemon_list()
    pokemon_key = pokemon_name.lower()
    if pokemon_key not in starters:
        return None, f"'{pokemon_name}' is not a valid starter Pokemon!"
    pokemon_data = get_pokemon_database()[pokemon_key]
    abilities_db = get_abilities_database()
    ivs = generate_pokemon_ivs()
    iv_percentage = calculate_iv_percentage(ivs)
    gender = get_gender_emoji(pokemon_key)
    nature_keys = list(get_nature_database().keys())
    random_nature = random.choice(nature_keys)
    ability_roll = random.random()
    if ability_roll <= 0.3:
        chosen_ability = abilities_db[pokemon_key]["hidden"]
    else:
        chosen_ability = abilities_db[pokemon_key]["normal"]
    trainers[user_id_str]["StarterPokemon"] = {
        "name": starters[pokemon_key]["name"],
        "emoji": starters[pokemon_key]["emoji"],
        "pickedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dex": pokemon_data["dex"],
        "level": 1,
        "ivs": ivs,
        "iv_percentage": iv_percentage,
        "gender": gender,
        "base_stats": pokemon_data["base_stats"],
        "nature": random_nature,
        "ability": chosen_ability
    }
    trainers[user_id_str]["HasChosenStarter"] = True
    if save_trainers(trainers):
        return starters[pokemon_key], None
    else:
        return None, "Failed to save your starter Pokemon. Please try again."
class GenderSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Male", style=discord.ButtonStyle.blurple)
    async def male(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_gender_selection(interaction, "Male")
    @discord.ui.button(label="Female", style=discord.ButtonStyle.danger)
    async def female(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_gender_selection(interaction, "Female")
    async def handle_gender_selection(self, interaction: discord.Interaction, gender: str):
        user_id = interaction.user.id
        if is_trainer_registered(user_id):
            await interaction.response.send_message("You are already registered in Pokékiro", ephemeral=True)
            return
        trainer_data, error_message = register_trainer(user_id, gender)
        if error_message:
            await interaction.response.send_message(error_message, ephemeral=True)
        elif trainer_data:
            success_message = (
                f"✅ You selected **{gender}**!\n"
                f"🆔 Trainer ID: {trainer_data['TrainerID']}\n"
                f"📅 Registered at: {trainer_data['RegisteredAt']}"
            )
            await interaction.response.send_message(success_message, ephemeral=True)
        else:
            await interaction.response.send_message("An unexpected error occurred. Please try again.", ephemeral=True)
class PokemonCollectionView(discord.ui.View):
    def __init__(self, user_id, pokemon_list, page=0):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.pokemon_list = pokemon_list
        self.page = page
        self.per_page = 20
        self.total_pages = max(1, (len(pokemon_list) + self.per_page - 1) // self.per_page)
        self.update_buttons()
    def update_buttons(self):
        if len(self.children) >= 2:
            self.children[0].disabled = (self.page <= 0)
            self.children[1].disabled = (self.page >= self.total_pages - 1)
    @discord.ui.button(emoji="◀️", style=discord.ButtonStyle.secondary)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your Pokemon collection!", ephemeral=True)
            return
        if self.page > 0:
            self.page -= 1
            self.update_buttons()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()
    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your Pokemon collection!", ephemeral=True)
            return
        if self.page < self.total_pages - 1:
            self.page += 1
            self.update_buttons()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()
    def create_embed(self):
        embed = discord.Embed(
            title="Your pokémon",
            color=0xFFD700
        )
        start_idx = self.page * self.per_page
        end_idx = min(start_idx + self.per_page, len(self.pokemon_list))
        page_pokemon = self.pokemon_list[start_idx:end_idx]
        pokemon_text = ""
        for i, pokemon in enumerate(page_pokemon):
            collection_number = pokemon['caught_order']
            pokemon_text += f"{collection_number}　**{pokemon['name']}**{pokemon['gender']}　•　Lvl. {pokemon['level']}　•　{pokemon['iv_percentage']}%\n"
        if pokemon_text:
            embed.description = pokemon_text
        else:
            embed.description = "No Pokémon found."
        if self.total_pages > 1:
            start_showing = start_idx + 1
            end_showing = end_idx
            total_pokemon = len(self.pokemon_list)
            current_page = self.page + 1
            embed.set_footer(text=f"Showing entries {start_showing}–{end_showing} out of {total_pokemon}. Page {current_page} of {self.total_pages}.")
        return embed
class MarketConfirmationView(View):
    def __init__(self, user_id, pokemon_data, order_number, amount, timeout=300):
        super().__init__(timeout=timeout)
        self.user_id = user_id
        self.pokemon_data = pokemon_data
        self.order_number = order_number
        self.amount = amount
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.success)
    async def confirm_listing(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your confirmation dialog.", ephemeral=True)
            return
        market_data = load_market()
        market_id = market_data["next_id"]
        listing = {
            "market_id": market_id,
            "user_id": str(self.user_id),
            "order_number": self.order_number,
            "amount": self.amount,
            "pokemon": self.pokemon_data["data"].copy(),
            "listed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        market_data["listings"].append(listing)
        market_data["next_id"] += 1
        if save_market(market_data):
            trainer_data = get_trainer_data(str(self.user_id))
            if trainer_data:
                caught_pokemon = trainer_data.get("CaughtPokemons", [])
                updated_pokemon = []
                for i, pokemon in enumerate(caught_pokemon):
                    if i != (self.order_number - 2):
                        updated_pokemon.append(pokemon)
                trainer_data["CaughtPokemons"] = updated_pokemon
                update_trainer_data(str(self.user_id), trainer_data)
            pokemon = self.pokemon_data["data"]
            gender_emoji = convert_text_gender_to_emoji(pokemon.get('gender', 'Unknown'))
            success_message = (f"Listed your Level {pokemon['level']} {pokemon['name'].title()}{gender_emoji} "
                             f"({pokemon['iv_percentage']}%) No. {self.order_number} on "
                             f"the market for {self.amount} Pokécoins (Listing #{market_id}).")
            await interaction.response.edit_message(view=None)
            await interaction.followup.send(success_message)
        else:
            error_message = "Failed to list Pokemon on the market. Please try again."
            await interaction.response.edit_message(view=None)
            await interaction.followup.send(error_message)
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel_listing(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your confirmation dialog.", ephemeral=True)
            return
        await interaction.response.edit_message(view=None)
        await interaction.followup.send("Listing cancelled.")
class MarketplacePagination(View):
    def __init__(self, listings, page=0, per_page=20, timeout=300):
        super().__init__(timeout=timeout)
        self.listings = listings
        self.page = page
        self.per_page = per_page
        self.max_pages = max(1, math.ceil(len(listings) / per_page))
        self.update_buttons()
    def update_buttons(self):
        if len(self.children) >= 2:
            self.children[0].disabled = (self.page <= 0)
            self.children[1].disabled = (self.page >= self.max_pages - 1)
    def get_current_page_listings(self):
        start_idx = self.page * self.per_page
        end_idx = start_idx + self.per_page
        return self.listings[start_idx:end_idx]
    def create_embed(self):
        embed = discord.Embed(
            title="Pokétwo Marketplace",
            color=0xFFD700
        )
        if not self.listings:
            embed.description = "No Pokémon available in the marketplace."
            return embed
        page_listings = self.get_current_page_listings()
        description_lines = []
        for listing in page_listings:
            pokemon = listing["pokemon"]
            gender_emoji = convert_text_gender_to_emoji(pokemon.get('gender', 'Unknown'))
            line = f"{listing['market_id']}　**{pokemon['name'].title()}**{gender_emoji}　•　Lvl. {pokemon['level']}　•　{pokemon['iv_percentage']}%　•　{listing['amount']} Pokécoins"
            description_lines.append(line)
        embed.description = "\n".join(description_lines)
        if self.max_pages > 1:
            embed.set_footer(text=f"Page {self.page + 1}/{self.max_pages}")
        return embed
    @discord.ui.button(emoji="◀️", style=discord.ButtonStyle.secondary)
    async def back_button(self, interaction: discord.Interaction, button: Button):
        if self.page > 0:
            self.page -= 1
            self.update_buttons()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()
    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: Button):
        if self.page < self.max_pages - 1:
            self.page += 1
            self.update_buttons()
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()
@bot.command()
async def register(ctx):
    embed = discord.Embed(
        title="Welcome to the world of Pokémon!",
        description="Choose your character by clicking on **Male** or **Female**.",
        color=discord.Color.gold()
    )
    embed.set_image(url="https://static.wikia.nocookie.net/ultimate-pokemon-fanon/images/c/c5/Ivy-Rye.jpg/revision/latest?cb=20201212225708")
    await ctx.send(embed=embed, view=GenderSelect())
@bot.command(name="starter")
async def starter_selection(ctx):
    embed = discord.Embed(
        title="Welcome to the world of Pokémon!",
        description="To start, choose one of the starter Pokémon using the\n@Pokékiro#8400 pick <pokemon> command.",
        color=discord.Color.gold()
    )
    embed.add_field(
        name="**Generation I (Kanto)**",
        value="<:bulbasaur:1390604553321189406>  Bulbasaur  ·  <:charmander:1390604778584801320>  Charmander  ·  <:squirtle:1390604851091607564>  Squirtle",
        inline=False
    )
    embed.add_field(
        name="**Generation II (Johto)**",
        value="<:chikorita:1390605119489577053>  Chikorita  ·  <:cyndaquil:1390605148664889344>  Cyndaquil  ·  <:totodile:1390605177123246144>  Totodile",
        inline=False
    )
    embed.add_field(
        name="**Generation III (Hoenn)**",
        value="<:treecko:1390605513892429897>  Treecko  ·  <:torchic:1390605536558452826>  Torchic  ·  <:mudkip:1390605558347989064>  Mudkip",
        inline=False
    )
    embed.add_field(
        name="**Generation IV (Sinnoh)**",
        value="<:grotle:1390605781271052298>  Turtwig  ·  <:chimchar:1390605819296485376>  Chimchar  ·  <:piplup:1390605848023400550>  Piplup",
        inline=False
    )
    embed.add_field(
        name="**Generation V (Unova)**",
        value="<:snivy:1390606080958009384>  Snivy  ·  <:tepig:1390606123068952666>  Tepig  ·  <:oshawott:1390606151527301121>  Oshawott",
        inline=False
    )
    embed.add_field(
        name="**Generation VI (Kalos)**",
        value="<:chespin:1390606464179240961>  Chespin  ·  <:fennekin:1390606541740314675>  Fennekin  ·  <:froakie:1390606610644336800>  Froakie",
        inline=False
    )
    embed.add_field(
        name="**Generation VII (Alola)**",
        value="<:rowlet:1390606834905256047>  Rowlet  ·  <:litten:1390606869290029157>   Litten  ·  <:popplio:1390606900533526591>  Popplio",
        inline=False
    )
    embed.add_field(
        name="**Generation VIII (Galar)**",
        value="<:grookey:1390607074689286315>  Grookey  ·  <:scorbunny:1390607113080016956>  Scorbunny  ·  <:sobble:1390607161671024721>  Sobble",
        inline=False
    )
    embed.add_field(
        name="**Generation IX (Paldea)**",
        value="<:sprigatito:1390607793266102302>  Sprigatito  ·  <:fuecoco:1390607859049435221>  Fuecoco  ·  <:quaxly:1390607905115602944>  Quaxly",
        inline=False
    )
    embed.set_image(url="https://cdn.dribbble.com/userupload/21948821/file/original-8de46059d7383343f9a16199b5d89488.gif")
    await ctx.send(embed=embed)
@bot.command()
async def pick(ctx, *, pokemon_name: str = ""):
    if not pokemon_name:
        await ctx.send("Please specify a Pokemon! Example: `@Pokékiro#8400 pick charmander`")
        return
    pokemon_data, error_message = pick_starter_pokemon(ctx.author.id, pokemon_name)
    if error_message:
        await ctx.send(error_message)
    elif pokemon_data:
        success_message = (
            f"🎉 Congratulations on entering the world of pokémon!\n"
            f"{pokemon_data['emoji']} **{pokemon_data['name']}** is your first pokémon.\n"
            f"Type @Pokékiro#8400 info to view it!"
        )
        await ctx.send(success_message)
    else:
        await ctx.send("An unexpected error occurred. Please try again.")
def generate_missing_pokemon_data(pokemon_data, pokemon_name=None):
    from pokémon import NATURES
    if "ivs" not in pokemon_data or not pokemon_data["ivs"]:
        pokemon_data["ivs"] = generate_pokemon_ivs()
    if "iv_percentage" not in pokemon_data:
        pokemon_data["iv_percentage"] = calculate_iv_percentage(pokemon_data["ivs"])
    if "nature" not in pokemon_data or not pokemon_data["nature"]:
        pokemon_data["nature"] = random.choice(NATURES).lower()
    if "ability" not in pokemon_data or not pokemon_data["ability"]:
        pokemon_name = pokemon_data.get("name", "").lower()
        found_pokemon = get_pokemon_by_name(pokemon_name)
        if found_pokemon:
            correct_abilities = found_pokemon.get("abilities", ["Unknown"])
        else:
            correct_abilities = ["Unknown"]
        pokemon_data["ability"] = random.choice(correct_abilities)
    if "gender" not in pokemon_data or not pokemon_data["gender"]:
        pokemon_data["gender"] = assign_pokemon_gender(pokemon_data["name"])
    if "base_stats" not in pokemon_data or not pokemon_data["base_stats"]:
        pokemon_data["base_stats"] = {
            "hp": 45, "attack": 49, "defense": 49,
            "sp_attack": 65, "sp_defense": 65, "speed": 45
        }
    if "evs" not in pokemon_data:
        pokemon_data["evs"] = {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0}
    level = pokemon_data.get("level", 1)
    nature = pokemon_data.get("nature", "hardy")
    pokemon_data["calculated_stats"] = calculate_official_stats(
        pokemon_data["base_stats"],
        pokemon_data["ivs"],
        level,
        nature,
        pokemon_data["evs"]
    )
    return pokemon_data
def enhance_caught_pokemon_data(caught_pokemon, pokemon_db):
    pokemon_name = caught_pokemon.get("name", "").lower()
    base_data = None
    for pokemon in pokemon_db:
        if pokemon["name"].lower() == pokemon_name:
            base_data = pokemon
            break
    if not base_data:
        starter_db = get_starter_pokemon_list()
        if pokemon_name in starter_db:
            starter_info = starter_db[pokemon_name]
            comp_db = get_pokemon_database()
            if pokemon_name in comp_db:
                base_data = comp_db[pokemon_name]
    enhanced_data = caught_pokemon.copy()
    if "ivs" not in enhanced_data:
        enhanced_data["ivs"] = generate_pokemon_ivs()
    if "iv_percentage" not in enhanced_data:
        enhanced_data["iv_percentage"] = calculate_iv_percentage(enhanced_data["ivs"])
    if "nature" not in enhanced_data:
        from pokémon import NATURES
        enhanced_data["nature"] = random.choice(NATURES).lower()
    if "ability" not in enhanced_data and base_data:
        abilities = base_data.get("abilities", ["Unknown"])
        enhanced_data["ability"] = random.choice(abilities)
    if "base_stats" not in enhanced_data and base_data:
        enhanced_data["base_stats"] = base_data.get("base_stats", {})
    if "dex" not in enhanced_data and base_data:
        enhanced_data["dex"] = base_data.get("dex", 0)
    if "evs" not in enhanced_data:
        enhanced_data["evs"] = {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0}
    if "calculated_stats" not in enhanced_data and "base_stats" in enhanced_data:
        level = enhanced_data.get("level", 1)
        nature = enhanced_data.get("nature", "hardy")
        enhanced_data["calculated_stats"] = calculate_official_stats(
            enhanced_data["base_stats"],
            enhanced_data["ivs"],
            level,
            nature,
            enhanced_data["evs"]
        )
    return enhanced_data
@bot.command()
async def info(ctx, order_number: int = 0):
    if order_number == 0:
        embed = discord.Embed(
            title="Missing Order Number",
            description="Please specify which Pokemon you want to view!\n\nUse: `@Pokékiro info [order_number]`\nExample: `@Pokékiro info 1`",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return
    if not is_trainer_registered(ctx.author.id):
        embed = discord.Embed(
            title="Not Registered",
            description="You need to register first!\n\nUse: `@Pokékiro register [Male/Female]`",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return
    trainer_data = get_trainer_data(ctx.author.id)
    if not trainer_data:
        await ctx.send("Unable to retrieve trainer data.")
        return
    pokemon_info = get_pokemon_by_order(trainer_data, order_number)
    if not pokemon_info:
        embed = discord.Embed(
            title="Pokemon Not Found",
            description=f"You don't have a Pokemon at position #{order_number}.\n\nUse `@Pokékiro pokémons` to see your collection.",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return
    pokemon = pokemon_info["data"]
    pokemon_type = pokemon_info["type"]
    if pokemon_type == "caught":
        pokemon = generate_missing_pokemon_data(pokemon, pokemon.get("name"))
        for i, p in enumerate(trainer_data.get("CaughtPokemons", [])):
            if p["name"] == pokemon["name"] and i == (order_number - 2):
                trainer_data["CaughtPokemons"][i] = pokemon
                update_trainer_data(ctx.author.id, trainer_data)
                break
    current_level = pokemon.get("level", 1)
    if pokemon_type == "starter":
        total_messages = trainer_data.get("TotalMessages", 0)
        calculated_level = max(1, total_messages // 100 + 1)
        if calculated_level > current_level:
            current_level = calculated_level
            pokemon["level"] = current_level
            trainer_data["StarterPokemon"] = pokemon
            update_trainer_data(ctx.author.id, trainer_data)
        # Calculate XP display using TOTAL XP values from user's table
        pokemon_xp = pokemon.get("xp", 0)  # XP within current level
        if current_level >= 100:
            xp_display = "MAX LEVEL"
            xp_to_next = 0
        else:
            # Show XP progress: within-level XP / current level requirement  
            current_level_requirement = current_level * 50         # XP requirement for current level
            # XP to next level = remaining XP to complete current level requirement
            xp_to_next = max(0, current_level_requirement - pokemon_xp)
            
            # Format: within-level XP / current level requirement
            xp_display = f"{pokemon_xp}/{current_level_requirement}"
    else:
        # For caught Pokemon, use TOTAL XP values from user's table
        pokemon_xp = pokemon.get("xp", 0)  # XP within current level
        if current_level >= 100:
            xp_display = "MAX LEVEL"
            xp_to_next = 0
        else:
            # Show XP progress: within-level XP / current level requirement  
            current_level_requirement = current_level * 50         # XP requirement for current level
            # XP to next level = remaining XP to complete current level requirement
            xp_to_next = max(0, current_level_requirement - pokemon_xp)
            
            # Format: within-level XP / current level requirement
            xp_display = f"{pokemon_xp}/{current_level_requirement}"
    base_stats = pokemon.get("base_stats", {})
    ivs = pokemon.get("ivs", {})
    nature = pokemon.get("nature", "hardy")
    evs = pokemon.get("evs", {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
    current_stats = calculate_official_stats(base_stats, ivs, current_level, nature, evs)
    embed = discord.Embed(
        title=f"Level {current_level} {pokemon['name']}",
        color=0xFFD700
    )
    embed.set_image(url=get_pokemon_image_url(pokemon['name']))
    nature_name = pokemon.get("nature", "Hardy").title()
    ability_name = pokemon.get("ability", "Unknown")
    gender_emoji = pokemon.get('gender', '<:unknown:1401145566863560755>')
    if gender_emoji == '<:male:1400956267979214971>':
        gender_display = gender_emoji
    elif gender_emoji == '<:female:1400956073573224520>':
        gender_display = gender_emoji
    elif gender_emoji == '<:unknown:1401145566863560755>':
        gender_display = gender_emoji
    else:
        gender_display = convert_text_gender_to_emoji(str(gender_emoji))
    details_value = f"**XP:** {xp_display}"
    if pokemon_type == "starter" and current_level < 100:
        details_value += f" ({xp_to_next} XP to next level)"
    elif pokemon_type == "caught":
        details_value += f" ({xp_to_next} XP to next level)"
    details_value += f"\n**Nature:** {nature_name}\n**Ability:** {ability_name}\n**Gender:** {gender_display}"
    embed.add_field(
        name="📋 Details",
        value=details_value,
        inline=False
    )
    stats_value = ""
    stat_names = {
        "hp": "HP",
        "attack": "Attack",
        "defense": "Defense",
        "sp_attack": "Sp. Atk",
        "sp_defense": "Sp. Def",
        "speed": "Speed"
    }
    for stat_key, stat_name in stat_names.items():
        stat_value = current_stats.get(stat_key, 50)
        iv_value = pokemon.get("ivs", {}).get(stat_key, 15)
        stats_value += f"**{stat_name}:** {stat_value} – IV: {iv_value}/31\n"
    total_iv = pokemon.get("iv_percentage", 50.0)
    stats_value += f"**Total IV:** {total_iv}%"
    embed.add_field(
        name="📊 Stats",
        value=stats_value,
        inline=False
    )
    embed.set_footer(text="Official Pokémon Artwork")
    await ctx.send(embed=embed)
@bot.command(name="pokémons", aliases=["pokemon", "pokemons"])
async def pokemon_collection(ctx):
    trainers = load_trainers()
    user_id = str(ctx.author.id)
    if user_id not in trainers:
        await ctx.send("You are not registered yet. Use the register command first!")
        return
    trainer = trainers[user_id]
    pokemon_list = []
    starter = trainer.get("StarterPokemon")
    if starter:
        if "dex" not in starter:
            save_trainers(trainers)
        pokemon_list.append({
            "dex": starter.get("dex", 0),
            "name": starter["name"],
            "gender": starter.get("gender", "?"),
            "level": starter.get("level", 1),
            "iv_percentage": starter.get("iv_percentage", 0.0),
            "caught_order": 1
        })
    caught_pokemons = trainer.get("CaughtPokemons", [])
    order = 2 if starter else 1
    for poke in caught_pokemons:
        pokemon_list.append({
            "dex": poke.get("dex", 0),
            "name": poke["name"],
            "gender": poke.get("gender", "?"),
            "level": poke.get("level", 1),
            "iv_percentage": poke.get("iv_percentage", 0.0),
            "caught_order": order
        })
        order += 1
    if not pokemon_list:
        embed = discord.Embed(
            title="Your pokémon",
            description="You don't have any Pokémon yet! Use `@Pokékiro#8400 starter` to choose your first Pokémon.",
            color=0xFFD700
        )
        await ctx.send(embed=embed)
        return
    pokemon_list.sort(key=lambda x: x["caught_order"])
    view = PokemonCollectionView(ctx.author.id, pokemon_list)
    embed = view.create_embed()
    await ctx.send(embed=embed, view=view)
class ShopPageSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Page 1",
                description="XP Boosters & Candies",
                value="1"
            ),
            discord.SelectOption(
                label="Page 2",
                description="Evolution Stones & Fossils",
                value="2"
            ),
            discord.SelectOption(
                label="Page 3",
                description="Form Change Items",
                value="3"
            ),
            discord.SelectOption(
                label="Page 4",
                description="Held Items & Battle Items",
                value="4"
            ),
            discord.SelectOption(
                label="Page 5",
                description="Nature Mints & Healing Items",
                value="5"
            ),
            discord.SelectOption(
                label="Page 6",
                description="Key Items & Valuable Items",
                value="6"
            ),
            discord.SelectOption(
                label="Page 7",
                description="TM/HM & Berries",
                value="7"
            ),
            discord.SelectOption(
                label="Page 8",
                description="Currency Exchange & Currency Buy",
                value="8"
            ),
            discord.SelectOption(
                label="Page 9",
                description="Passes & Chests",
                value="9"
            ),
            discord.SelectOption(
                label="Page 10",
                description="Energy",
                value="10"
            )
        ]
        super().__init__(placeholder="Open a page", options=options)
    async def callback(self, interaction: discord.Interaction):
        page_num = int(self.values[0])
        if page_num == 1:
            embed = discord.Embed(
                title=f"Pokékiro Shop — Page {page_num} (XP Boosters & Candies)",
                description=(
                    "Welcome to the Pokékiro Shop!\n"
                    "Here, you can purchase any item you want. Just type `@Pokékiro#8400 buy <item> <amount>` to purchase it.\n\n"
                ),
                color=0xFFD700
            )
            if "rare candy" in SHOP_ITEMS:
                item = SHOP_ITEMS["rare candy"]
                embed.description += f"**{item['emoji']} {item['name']} - {item['price']} pokécoins each**\n{item['description']}\n\n"
        elif page_num == 4:
            embed = discord.Embed(
                title=f"Pokékiro Shop — Page {page_num} (Held Items & Battle Items)",
                description=(
                    "Welcome to the Pokékiro Shop!\n"
                    "Here, you can purchase any item you want. Just type `@Pokékiro#8400 buy <item> <amount>` to purchase it.\n\n"
                ),
                color=0xFFD700
            )
            for item_key, item in SHOP_ITEMS.items():
                currency = item.get("currency", "pokécoins")
                embed.description += f"**{item['emoji']} {item['name']} - {item['price']} {currency} each**\n{item['description']}\n\n"
        elif page_num == 8:
            embed = discord.Embed(
                title=f"Pokékiro Shop — Page {page_num} (Currency Exchange & Currency Buy)",
                description=(
                    "Welcome to the Pokékiro Shop!\n"
                    "Here, you can purchase any item you want. Just type `@Pokékiro#8400 buy <item> <amount>` to purchase it.\n\n"
                    "**<:gems:1390696438383509555> Gems - 400 pokécoins each**\n"
                    "Gems is currency with which you can buy expensive items\n\n"
                ),
                color=0xFFD700
            )
        elif page_num == 10:
            embed = discord.Embed(
                title=f"Pokékiro Shop — Page {page_num} (Energy)",
                description=(
                    "Welcome to the Pokékiro Shop!\n"
                    "Here, you can purchase any item you want. Just type `@Pokékiro#8400 buy <item> <amount>` to purchase it.\n\n"
                ),
                color=0xFFD700
            )
            if "summoning stone" in SHOP_ITEMS:
                item = SHOP_ITEMS["summoning stone"]
                currency = item.get("currency", "pokécoins")
                embed.description += f"**{item['emoji']} {item['name']} - {item['price']} {currency} each**\n{item['description']}\n\n"
        else:
            embed = discord.Embed(
                title=f"Pokékiro Shop — Page {page_num}",
                description=f"This is page {page_num} content. (Feature coming soon!)",
                color=0xFFD700
            )
        await interaction.response.edit_message(embed=embed, view=None)
class ShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(ShopPageSelect())
def get_trainer_pokécoins(user_id):
    trainers = load_trainers()
    trainer = trainers.get(str(user_id))
    if trainer:
        return get_user_pokecoins(trainer)
    return 0
def get_trainer_gems(user_id):
    trainers = load_trainers()
    trainer = trainers.get(str(user_id))
    if trainer:
        return trainer.get("Shards", 0)
    return 0
@bot.command()
async def shop(ctx, page: int = None):
    if not is_trainer_registered(ctx.author.id):
        embed = discord.Embed(
            title="Not Registered",
            description="You need to register first!\n\nUse: `@Pokékiro register [Male/Female]`",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return
    pokécoins_balance = get_trainer_pokécoins(ctx.author.id)
    gems_balance = get_trainer_gems(ctx.author.id)
    if page == 1:
        embed = discord.Embed(
            title=f"Pokékiro Shop — Page {page} (XP Boosters & Candies)",
            description=(
                "Welcome to the Pokékiro Shop!\n"
                "Here, you can purchase any item you want. Just type `@Pokékiro#8400 buy <item> <amount>` to purchase it.\n\n"
            ),
            color=0xFFD700
        )
        if "rare candy" in SHOP_ITEMS:
            item = SHOP_ITEMS["rare candy"]
            currency = item.get("currency", "pokécoins")
            embed.description += f"**{item['emoji']} {item['name']} - {item['price']} {currency} each**\n{item['description']}\n\n"
        await ctx.send(embed=embed)
        return
    if page == 4:
        embed = discord.Embed(
            title=f"Pokékiro Shop — Page {page} (Held Items & Battle Items)",
            description=(
                "Welcome to the Pokékiro Shop!\n"
                "Here, you can purchase any item you want. Just type `@Pokékiro#8400 buy <item> <amount>` to purchase it.\n\n"
            ),
            color=0xFFD700
        )
        for item_key, item in SHOP_ITEMS.items():
            currency = item.get("currency", "pokécoins")
            embed.description += f"**{item['emoji']} {item['name']} - {item['price']} {currency} each**\n{item['description']}\n\n"
        await ctx.send(embed=embed)
        return
    if page == 8:
        embed = discord.Embed(
            title=f"Pokékiro Shop — Page {page} (Currency Exchange & Currency Buy)",
            description=(
                "Welcome to the Pokékiro Shop!\n"
                "Here, you can purchase any item you want. Just type `@Pokékiro#8400 buy <item> <amount>` to purchase it.\n\n"
                "**<:gems:1390696438383509555> Gems - 400 pokécoins each**\n"
                "Gems is currency with which you can buy expensive items\n\n"
            ),
            color=0xFFD700
        )
        await ctx.send(embed=embed)
        return
    if page == 10:
        embed = discord.Embed(
            title=f"Pokékiro Shop — Page {page} (Energy)",
            description=(
                "Welcome to the Pokékiro Shop!\n"
                "Here, you can purchase any item you want. Just type `@Pokékiro#8400 buy <item> <amount>` to purchase it.\n\n"
            ),
            color=0xFFD700
        )
        if "summoning stone" in SHOP_ITEMS:
            item = SHOP_ITEMS["summoning stone"]
            currency = item.get("currency", "pokécoins")
            embed.description += f"**{item['emoji']} {item['name']} - {item['price']} {currency} each**\n{item['description']}\n\n"
        await ctx.send(embed=embed)
        return
    embed = discord.Embed(
        title=f"Pokékiro Shop — {pokécoins_balance} pokécoins | {gems_balance} gems",
        description=(
            "Welcome to the Pokékiro Shop!\n"
            "Here, you can purchase any item you want. Just type `@Pokékiro#8400 buy <item> <amount>` to purchase it.\n\n"
            "Use `@Pokékiro shop <page>` to view different pages.\n\n"
            "**Page 1** — XP Boosters & Candies\n"
            "**Page 2** — Evolution Stones & Fossils\n"
            "**Page 3** — Form Change Items\n"
            "**Page 4** — Held Items & Battle Items\n"
            "**Page 5** — Nature Mints & Healing Items\n"
            "**Page 6** — Key Items & Valuable Items\n"
            "**Page 7** — TM/HM & Berries\n"
            "**Page 8** — Currency Exchange & Currency Buy\n"
            "**Page 9** — Passes & Chests\n"
            "**Page 10** — Energy"
        ),
        color=0xFFD700
    )
    view = ShopView()
    await ctx.send(embed=embed, view=view)
class InventoryDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Hunting Items",
                description="Total Items = 0",
                value="hunting"
            ),
            discord.SelectOption(
                label="Stones & Fossils",
                description="Total Items = 0",
                value="stones"
            ),
            discord.SelectOption(
                label="Held Items & Battle Items",
                description="Total Items = 0",
                value="held"
            ),
            discord.SelectOption(
                label="Nature Mints & Healing Items",
                description="Total Items = 0",
                value="nature"
            ),
            discord.SelectOption(
                label="Key Items & Valuable Items",
                description="Total Items = 0",
                value="key"
            ),
            discord.SelectOption(
                label="TM/HM & Barriers",
                description="Total Items = 0",
                value="tm"
            ),
            discord.SelectOption(
                label="Wallet & Passes",
                description="Total Items = 0",
                value="wallet"
            ),
            discord.SelectOption(
                label="Energy Capsule & Chest",
                description="Total Items = 0",
                value="energy"
            )
        ]
        super().__init__(placeholder="Open a page", options=options, row=1)
    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        if category == "wallet":
            trainers = load_trainers()
            user_id = str(interaction.user.id)
            if user_id not in trainers:
                await interaction.response.send_message("You need to register first!", ephemeral=True)
                return
            trainer = trainers[user_id]
            user_name = interaction.user.display_name
            user_avatar = interaction.user.display_avatar.url
            pokécoins = trainer.get("pokécoins", 0)
            shards = trainer.get("Shards", 0)
            battle_passes = trainer.get("BattlePasses", 0)
            embed = discord.Embed(
                title=f"{user_name}'s balance",
                color=0xFFD700
            )
            balance_text = (
                f"**<:pokecoins:1403472605620732099> pokécoins**\n{pokécoins}\n\n"
                f"**<:gems:1390696438383509555> Gems**\n{shards}\n\n"
                f"**<:battle_pass:1390698653215363082> Battle Passes**\n{battle_passes}"
            )
            embed.add_field(name="", value=balance_text, inline=False)
            embed.set_thumbnail(url=user_avatar)
            await interaction.response.edit_message(embed=embed, view=None)
        elif category == "hunting":
            trainers = load_trainers()
            user_id = str(interaction.user.id)
            trainer = trainers.get(user_id, {})
            inventory = trainer.get("inventory", {})
            hunting_items = {}
            hunting_item_names = ["Summoning Stone"]
            for item_name, quantity in inventory.items():
                if item_name in hunting_item_names:
                    hunting_items[item_name] = quantity
            total_items = sum(hunting_items.values())
            embed = discord.Embed(
                title="🎯 Hunting Items",
                description=f"Total Items = {total_items}",
                color=0xFFD700
            )
            if hunting_items:
                items_text = ""
                for item_name, quantity in hunting_items.items():
                    item_emoji = "🎯"
                    for shop_item in SHOP_ITEMS.values():
                        if shop_item["name"] == item_name:
                            item_emoji = shop_item["emoji"]
                            break
                    items_text += f"{item_emoji} **{item_name}** x{quantity}\n"
                embed.add_field(
                    name="📋 Items",
                    value=items_text,
                    inline=False
                )
            else:
                embed.add_field(
                    name="📋 Items",
                    value="No hunting items found. Visit the shop to purchase hunting items!",
                    inline=False
                )
            await interaction.response.edit_message(embed=embed)
        elif category == "held":
            trainers = load_trainers()
            user_id = str(interaction.user.id)
            trainer = trainers.get(user_id, {})
            inventory = trainer.get("inventory", {})
            held_items = {}
            shop_item_names = [item["name"] for item in SHOP_ITEMS.values()]
            hunting_item_names = ["Summoning Stone"]
            for item_name, quantity in inventory.items():
                if item_name in shop_item_names and item_name not in hunting_item_names:
                    held_items[item_name] = quantity
            total_items = sum(held_items.values())
            embed = discord.Embed(
                title="📦 Held Items & Battle Items",
                description=f"Total Items = {total_items}",
                color=0xFFD700
            )
            if held_items:
                items_text = ""
                for item_name, quantity in held_items.items():
                    item_emoji = "📦"
                    for shop_item in SHOP_ITEMS.values():
                        if shop_item["name"] == item_name:
                            item_emoji = shop_item["emoji"]
                            break
                    items_text += f"{item_emoji} **{item_name}** x{quantity}\n"
                embed.add_field(
                    name="📋 Items",
                    value=items_text,
                    inline=False
                )
            else:
                embed.add_field(
                    name="📋 Items",
                    value="No items found. Visit the shop to purchase items!",
                    inline=False
                )
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(f"Selected category: {category} (Feature coming soon!)", ephemeral=True)
class InventoryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(InventoryDropdown())


@bot.command()
async def inventory(ctx):
    if not is_trainer_registered(ctx.author.id):
        embed = discord.Embed(
            title="Not Registered",
            description="You need to register first!\n\nUse: `@Pokékiro register`",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return
    trainers = load_trainers()
    user_id = str(ctx.author.id)
    if "pokécoins" not in trainers[user_id]:
        trainers[user_id]["pokécoins"] = 0
        save_trainers(trainers)
    trainer = trainers[user_id]
    trainer_id = trainer.get("TrainerID", "Unknown")
    pokécoins_amount = trainer.get("pokécoins", 0)
    embed = discord.Embed(
        title="📦 Your Inventory",
        description="Select a category from the dropdown below to view your items.",
        color=0xFFD700
    )
    categories_text = (
        "📋 **Categories**\n\n"
        "**Hunting Items**\n"
        "Total Items = 0\n\n"
        "**Stones & Fossils**\n"
        "Total Items = 0\n\n"
        "**Held Items & Battle Items**\n"
        "Total Items = 0\n\n"
        "**Nature Mints & Healing Items**\n"
        "Total Items = 0\n\n"
        "**Key Items & Valuable Items**\n"
        "Total Items = 0\n\n"
        "**TM/HM & Barriers**\n"
        "Total Items = 0\n\n"
        f"**Wallet & Passes**\n"
        f"pokécoins = {pokécoins_amount}\n\n"
        "**Energy Capsule & Chest**\n"
        "Total Items = 0\n\n"
        "📊 **Summary**\n\n"
        "**Total Items Across All Categories: 53**"
    )
    embed.add_field(name="", value=categories_text, inline=False)
    embed.set_footer(text=f"Trainer ID: {trainer_id} • Use the dropdown to explore categories")
    view = InventoryView()
    await ctx.send(embed=embed, view=view)
@bot.command()
async def catch(ctx, *, pokemon_name: str):
    global current_spawn
    if current_spawn is None:
        await ctx.send("❌ No Pokémon has spawned! Wait for one to appear.")
        return
    spawn_data = current_spawn
    if spawn_data["name"].lower() != pokemon_name.lower():
        await ctx.send(f"❌ That's not the right Pokémon! Try guessing again.")
        return
    if spawn_data.get("caught", False):
        await ctx.send("❌ This Pokémon has already been caught!")
        return
    trainers = load_trainers()
    user_id = str(ctx.author.id)
    if user_id not in trainers:
        await ctx.send("❌ You need to register first! Use `@Pokékiro register [Male/Female]` to get started.")
        return
    if "CaughtPokemons" not in trainers[user_id]:
        trainers[user_id]["CaughtPokemons"] = []
    matched = next((p for p in POKEMON_GEN1 if p["name"].lower() == spawn_data["name"].lower()), None)
    dex = matched["dex"] if matched and "dex" in matched else 0
    gender_symbol = {
        "male": "<:male:1400956267979214971>",
        "female": "<:female:1400956073573224520>",
        "genderless": "<:unknown:1401145566863560755>"
    }.get(spawn_data["gender"].lower(), "❔")
    if "full_data" in spawn_data:
        complete_pokemon = spawn_data["full_data"]
        trainers[user_id]["CaughtPokemons"].append(complete_pokemon)
    else:
        trainers[user_id]["CaughtPokemons"].append({
            "dex": dex,
            "name": spawn_data["name"],
            "gender": gender_symbol,
            "level": spawn_data["level"],
            "iv_percentage": spawn_data["total_iv"]
        })
    if "pokécoins" not in trainers[user_id]:
        trainers[user_id]["pokécoins"] = 0
    trainers[user_id]["pokécoins"] += 50
    save_trainers(trainers)
    spawn_data["caught"] = True
    current_spawn = None
    if "full_data" in spawn_data:
        pokemon_data = spawn_data["full_data"]
        success_message = f"Congratulations <@{ctx.author.id}>! You caught a Level {pokemon_data['level']} {pokemon_data['name'].title()}{pokemon_data['gender']} ({pokemon_data['iv_percentage']}%) you received 50 Pokécoins <:pokecoins:1403472605620732099>!"
        await ctx.send(success_message)
    else:
        await ctx.send(
            f"Congratulations <@{ctx.author.id}>! "
            f"You caught a Level {spawn_data['level']} {spawn_data['name']}{gender_symbol} "
            f"({spawn_data['total_iv']}%) you received 50 Pokécoins <:pokecoins:1403472605620732099>!"
        )
@bot.command()
async def release(ctx, order_number: int):
    trainers = load_trainers()
    user_id = str(ctx.author.id)
    if user_id not in trainers:
        await ctx.send("You are not registered yet.")
        return
    pokemon_list = get_user_pokemon_list(trainers[user_id])
    if not pokemon_list:
        await ctx.send("You have no Pokémon to release.")
        return
    selected_pokemon = None
    for pokemon in pokemon_list:
        if pokemon["order"] == order_number:
            selected_pokemon = pokemon
            break
    if not selected_pokemon:
        await ctx.send("Invalid Pokémon order number.")
        return
    trainer_data = trainers[user_id]
    currently_selected = trainer_data.get("SelectedPokemon")
    if currently_selected and currently_selected.get("order") == order_number:
        await ctx.send("You cannot release your selected pokémon!")
        return
    pokemon_data = selected_pokemon["data"]
    gender_emoji = pokemon_data.get("gender", "<:unknown:1401145566863560755>")
    if gender_emoji in ["<:male:1400956267979214971>", "<:female:1400956073573224520>", "<:unknown:1401145566863560755>"]:
        gender_symbol = gender_emoji
    else:
        gender_symbol = convert_text_gender_to_emoji(str(gender_emoji))
    msg_text = (
        f">>> Are you sure you want to **release** your Level {pokemon_data.get('level', 1)} "
        f"{pokemon_data['name']}{gender_symbol} ({pokemon_data.get('iv_percentage', 0)}%) "
        f"No. {order_number} for **1,000,000 pokécoins**?"
    )
    view = View()
    async def confirm_callback(interaction):
        trainers = load_trainers()
        if user_id in trainers:
            success = False
            if selected_pokemon["type"] == "starter":
                if trainers[user_id].get("StarterPokemon"):
                    trainers[user_id]["StarterPokemon"] = None
                    success = True
            elif selected_pokemon["type"] == "caught":
                if "CaughtPokemons" in trainers[user_id]:
                    caught_index = selected_pokemon["order"] - 2
                    if 0 <= caught_index < len(trainers[user_id]["CaughtPokemons"]):
                        trainers[user_id]["CaughtPokemons"].pop(caught_index)
                        success = True
            if success:
                current_coins = get_user_pokecoins(trainers[user_id])
                trainers[user_id]["pokécoins"] = current_coins + 1000000
                currently_selected = trainers[user_id].get("SelectedPokemon")
                if currently_selected and currently_selected.get("order") == selected_pokemon["order"]:
                    trainers[user_id]["SelectedPokemon"] = None
                save_trainers(trainers)
                view.clear_items()
                await interaction.response.edit_message(
                    content="✅ You released 1 Pokémon. You received **1,000,000 pokécoins!**",
                    view=None
                )
            else:
                await interaction.response.edit_message(
                    content="Release failed. Pokémon not found.",
                    view=None
                )
        else:
            await interaction.response.edit_message(
                content="Release failed. Pokémon not found.",
                view=None
            )
    async def cancel_callback(interaction):
        view.clear_items()
        await interaction.response.edit_message(
            content="Aborted.",
            view=None
        )
    confirm_btn = Button(label="Confirm", style=discord.ButtonStyle.green)
    confirm_btn.callback = confirm_callback
    cancel_btn = Button(label="Cancel", style=discord.ButtonStyle.red)
    cancel_btn.callback = cancel_callback
    view.add_item(confirm_btn)
    view.add_item(cancel_btn)
    await ctx.send(content=msg_text, view=view)
@bot.command(name="buy")
async def buy_command(ctx, *, args: str = None):
    user_id = str(ctx.author.id)
    if not is_trainer_registered(user_id):
        await ctx.send("You are not registered as a trainer. Use the register command first.")
        return
    if not args:
        await ctx.send("Please specify an item to buy. Examples:\n`@Pokékiro#8400 buy gems 5`\n`@Pokékiro#8400 buy summoning stone 1`\n`@Pokékiro#8400 buy rare candy 1`")
        return
    parts = args.strip().split()
    if len(parts) == 0:
        await ctx.send("Please specify an item to buy.")
        return
    amount = 1
    if len(parts) > 1 and parts[-1].isdigit():
        amount = int(parts[-1])
        item_name = " ".join(parts[:-1])
        if amount <= 0:
            await ctx.send("Amount must be a positive number.")
            return
    else:
        item_name = " ".join(parts)
    trainer_data = get_trainer_data(user_id)
    if not trainer_data:
        await ctx.send("Unable to retrieve trainer data.")
        return
    item_key = item_name.lower()
    if item_key == "gems" or item_key == "gem":
        gem_price = 400
        total_cost = gem_price * amount
        current_coins = get_user_pokecoins(trainer_data)
        if current_coins < total_cost:
            await ctx.send(f"Not enough pokécoins! You have {current_coins} pokécoins but need {total_cost} pokécoins to buy {amount} gems.")
            return
        confirmation_view = PurchaseConfirmationView(ctx.author.id, "Gems", amount, total_cost, "pokécoins", is_gems=True)
        await ctx.send(f"Are you sure you want to buy {amount} Gems?", view=confirmation_view)
        return
    if item_key not in SHOP_ITEMS:
        matched_item = None
        for shop_key, shop_item in SHOP_ITEMS.items():
            if item_key == shop_key or shop_item["name"].lower() == item_key:
                matched_item = shop_key
                break
            elif "summoning stone" in item_key and shop_key == "summoning stone":
                matched_item = shop_key
                break
        if matched_item:
            item_key = matched_item
        else:
            available_items = ", ".join([item["name"] for item in SHOP_ITEMS.values()])
            await ctx.send(f"Item not found in shop. Available items: {available_items}, gems")
            return
    item = SHOP_ITEMS[item_key]
    total_cost = item["price"] * amount
    currency = item.get("currency", "pokécoins")
    if currency == "gems":
        current_balance = trainer_data.get("Shards", 0)
        if current_balance < total_cost:
            await ctx.send("You not have enough Gems to buy Summoning Stone.")
            return
    else:
        current_coins = get_user_pokecoins(trainer_data)
        if current_coins < total_cost:
            await ctx.send(f"Not enough pokécoins! You have {current_coins} pokécoins but need {total_cost} pokécoins.")
            return
    if item_key == "summoning stone":
        confirmation_view = PurchaseConfirmationView(ctx.author.id, item["name"], amount, total_cost, currency)
        await ctx.send(f"Are you sure you want to buy {item['name']}?", view=confirmation_view)
        return
    if currency == "pokécoins":
        if deduct_pokecoins(trainer_data, total_cost):
            add_item_to_inventory(trainer_data, item["name"], amount)
            if update_trainer_data(user_id, trainer_data):
                await ctx.send(f"✅ You purchased {amount} {item['name']}! Use `@Pokékiro#8400 inventory` to check your item.")
            else:
                await ctx.send("Failed to save purchase. Please try again.")
        else:
            await ctx.send("Purchase failed. Please try again.")
@bot.command(name="select")
async def select_pokemon(ctx, order_number: int):
    user_id = str(ctx.author.id)
    if not is_trainer_registered(user_id):
        await ctx.send("You need to register first! Use `@Pokékiro#8400 register` to get started.")
        return
    trainer_data = get_trainer_data(user_id)
    if not trainer_data:
        await ctx.send("Unable to retrieve trainer data.")
        return
    selected_pokemon = get_pokemon_by_order(trainer_data, order_number)
    if not selected_pokemon:
        await ctx.send(f"No Pokemon found with order number {order_number}. Use `@Pokékiro#8400 pokémons` to see your collection.")
        return
    trainer_data["SelectedPokemon"] = {
        "order": selected_pokemon["order"],
        "name": selected_pokemon["name"],
        "type": selected_pokemon["type"]
    }
    if update_trainer_data(user_id, trainer_data):
        pokemon_data = selected_pokemon["data"]
        pokemon_level = pokemon_data.get("level", 1)
        embed = discord.Embed(
            title="🎯 Pokemon Selected!",
            description=f"You selected **{selected_pokemon['name']}** (Level {pokemon_level}) from your collection.\n\nThis Pokemon will now receive XP when you level up!",
            color=0xFFD700
        )
        if "emoji" in pokemon_data:
            embed.add_field(name="Pokemon", value=f"{pokemon_data['emoji']} {selected_pokemon['name']}", inline=True)
        else:
            embed.add_field(name="Pokemon", value=selected_pokemon['name'], inline=True)
        embed.add_field(name="Order #", value=f"#{order_number}", inline=True)
        embed.add_field(name="Level", value=pokemon_level, inline=True)
        if selected_pokemon["type"] == "starter":
            embed.set_footer(text="💡 This is your starter Pokemon!")
        else:
            embed.set_footer(text="💡 This is from your caught Pokemon collection!")
        await ctx.send(embed=embed)
    else:
        await ctx.send("Failed to select Pokemon. Please try again.")
valid_names = [p["name"].lower() for p in POKEMON_GEN1]
@bot.event
async def on_ready():
    if hasattr(bot, '_ready_called'):
        return
    bot._ready_called = True
    print(f"{bot.user} has connected to Discord!")
    if not os.path.exists("trainers.json"):
        with open("trainers.json", "w") as f:
            json.dump({}, f)
        print("📁 Created trainers.json file")
    print("🎮 Pokemon trainer registration system is ready!")
processed_messages = set()
@bot.event
async def on_message(message):
    global message_count, current_spawn
    if message.author.bot:
        return
    
    # Stronger duplicate detection using just message ID 
    message_id = str(message.id)
    if message_id in processed_messages:
        print(f"DUPLICATE MESSAGE DETECTED: {message_id} - SKIPPING")
        return
    processed_messages.add(message_id)
    
    # Keep only last 1000 processed messages for better duplicate detection
    if len(processed_messages) > 1000:
        old_messages = list(processed_messages)[:100]
        for old_msg in old_messages:
            processed_messages.discard(old_msg)
    
    
    await bot.process_commands(message)
    if is_trainer_registered(message.author.id):
        save_success, level_up_info = update_trainer_xp(message.author.id)
        if level_up_info is not None:
            embed = discord.Embed(
                title="🎉 Level Up!",
                description=f"Congratulations {message.author.display_name}\nYour {level_up_info['pokemon_name']} is now level {level_up_info['new_level']}!",
                color=0xFFD700
            )
            embed.set_thumbnail(url=get_pokemon_image_url(level_up_info['pokemon_name']))
            embed.set_footer(text="Keep chatting to level up more!")
            await message.channel.send(embed=embed)
    message_count += 1
    if message_count >= 10:
        message_count = 0
        spawn_roll = random.random()
        if spawn_roll < 0.90:
            all_pokemon = get_all_pokemon()
            pokemon_choice = random.choice(all_pokemon)
            spawned_pokemon = create_spawned_pokemon(pokemon_choice)
            current_spawn = {
                "name": spawned_pokemon["name"],
                "level": spawned_pokemon["level"],
                "gender": spawned_pokemon["gender"],
                "total_iv": spawned_pokemon["iv_percentage"],
                "caught": False,
                "full_data": spawned_pokemon
            }
            embed = discord.Embed(
                title="A wild pokémon has appeared!",
                description=f"Guess the pokémon and type `@Pokékiro catch <pokémon>` to catch it!",
                color=0xFFD700
            )
            embed.set_image(url=get_pokemon_image_url(spawned_pokemon['name']))
            await message.channel.send(embed=embed)
@bot.command(name='hint')
async def hint_command(ctx):
    global current_spawn
    if current_spawn is None:
        embed = discord.Embed(
            title="No Pokemon Spawned",
            description="There's no Pokemon currently spawned! Wait for one to appear or keep chatting.",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    if current_spawn.get("caught", False):
        embed = discord.Embed(
            title="Pokemon Already Caught",
            description="The spawned Pokemon has already been caught! Wait for a new one to appear.",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    pokemon_name = current_spawn["name"].title()
    embed = discord.Embed(
        title="🔍 Pokemon Hint",
        description=f"The pokémon is ||{pokemon_name}||",
        color=0x3498db
    )
    embed.set_footer(text="Click the spoiler to reveal the answer!")
    await ctx.send(embed=embed)
@bot.group(name='market', invoke_without_command=True)
async def market_command(ctx):
    market_data = load_market()
    listings = market_data.get("listings", [])
    view = MarketplacePagination(listings)
    embed = view.create_embed()
    await ctx.send(embed=embed, view=view)
@market_command.command(name='add')
async def market_add(ctx, order_number: str = None, amount: int = None):
    if order_number is None or amount is None:
        await ctx.send("Please specify both order number and amount. Example: `market add 1 500`")
        return
    trainer_data = get_trainer_data(ctx.author.id)
    if not trainer_data:
        await ctx.send("You need to register first using the `register` command.")
        return
    if amount <= 0:
        await ctx.send("Amount must be a positive number.")
        return
    try:
        order_int = int(order_number)
    except ValueError:
        await ctx.send("Order number must be a valid number.")
        return
    pokemon_data = get_pokemon_by_order(trainer_data, order_int)
    if not pokemon_data:
        await ctx.send("No Pokémon found with that order number. Use `pokémons` to see your collection.")
        return
    pokemon = pokemon_data["data"]
    confirmation_message = f"Are you sure you want to list your **Level {pokemon['level']} {pokemon['name'].title()}{pokemon['gender']} ({pokemon['iv_percentage']}%) No. {order_int}** for **{amount}** Pokécoins?"
    view = MarketConfirmationView(ctx.author.id, pokemon_data, order_int, amount)
    await ctx.reply(confirmation_message, view=view)
@market_command.command(name="remove")
async def market_remove(ctx, listing_id: int = None):
    if listing_id is None:
        await ctx.send("Please specify a listing ID. Example: `market remove 1`")
        return
    user_id = str(ctx.author.id)
    if not is_trainer_registered(user_id):
        await ctx.send("You need to register first! Use `register` to get started.")
        return
    market_data = load_market()
    listings = market_data.get("listings", [])
    listing_to_remove = None
    listing_index = None
    for i, listing in enumerate(listings):
        if listing["market_id"] == listing_id and listing["user_id"] == user_id:
            listing_to_remove = listing
            listing_index = i
            break
    if not listing_to_remove:
        await ctx.send("No listing found with that ID, or it's not your listing.")
        return
    pokemon = listing_to_remove["pokemon"]
    confirmation_message = f"Are you sure you want to remove your **Level {pokemon['level']} {pokemon['name'].title()}{pokemon['gender']} ({pokemon['iv_percentage']}%)** from the market?"
    view = MarketRemovalConfirmationView(ctx.author.id, listing_to_remove, listing_index)
    await ctx.reply(confirmation_message, view=view)
class MarketRemovalConfirmationView(View):
    def __init__(self, user_id: int, listing: dict, listing_index: int):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.listing = listing
        self.listing_index = listing_index
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.success)
    async def confirm_removal(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your confirmation dialog.", ephemeral=True)
            return
        market_data = load_market()
        if self.listing_index < len(market_data["listings"]):
            removed_listing = market_data["listings"].pop(self.listing_index)
            if save_market(market_data):
                trainer_data = get_trainer_data(str(self.user_id))
                if trainer_data:
                    if "CaughtPokemons" not in trainer_data:
                        trainer_data["CaughtPokemons"] = []
                    trainer_data["CaughtPokemons"].append(self.listing["pokemon"])
                    if update_trainer_data(str(self.user_id), trainer_data):
                        pokemon = self.listing["pokemon"]
                        success_message = f"Removed your Level {pokemon['level']} {pokemon['name'].title()}{pokemon['gender']} ({pokemon['iv_percentage']}%) from the market."
                        await interaction.response.edit_message(view=None)
                        await interaction.followup.send(success_message)
                    else:
                        await interaction.response.edit_message(view=None)
                        await interaction.followup.send("Failed to return Pokemon to your collection. Please contact support.")
                else:
                    await interaction.response.edit_message(view=None)
                    await interaction.followup.send("Failed to retrieve your trainer data. Please try again.")
            else:
                await interaction.response.edit_message(view=None)
                await interaction.followup.send("Failed to remove listing from market. Please try again.")
        else:
            await interaction.response.edit_message(view=None)
            await interaction.followup.send("Listing no longer exists.")
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel_removal(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your confirmation dialog.", ephemeral=True)
            return
        await interaction.response.edit_message(view=None)
        await interaction.followup.send("Removal cancelled.")
class MarketBuyConfirmView(View):
    def __init__(self, listing, buyer_id):
        super().__init__(timeout=60.0)
        self.listing = listing
        self.buyer_id = buyer_id
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, emoji='✅')
    async def confirm(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.buyer_id:
            await interaction.response.send_message("You can't interact with someone else's confirmation.", ephemeral=True)
            return
        market_data = load_market()
        listing_found = None
        listing_index = -1
        for i, listing in enumerate(market_data["listings"]):
            if listing["market_id"] == self.listing["market_id"]:
                listing_found = listing
                listing_index = i
                break
        if not listing_found:
            await interaction.response.send_message("This listing is no longer available.", ephemeral=True)
            return
        buyer_data = get_trainer_data(self.buyer_id)
        if not buyer_data:
            await interaction.response.send_message("You need to register first!", ephemeral=True)
            return
        buyer_coins = get_user_pokecoins(buyer_data)
        if buyer_coins < self.listing["amount"]:
            await interaction.response.send_message(f"You don't have enough Pokécoins! You need {self.listing['amount']:,} but only have {buyer_coins:,}.", ephemeral=True)
            return
        if not deduct_pokecoins(buyer_data, self.listing["amount"]):
            await interaction.response.send_message("Failed to deduct Pokécoins. Please try again.", ephemeral=True)
            return
        if "CaughtPokemons" not in buyer_data:
            buyer_data["CaughtPokemons"] = []
        buyer_data["CaughtPokemons"].append(self.listing["pokemon"])
        market_data["listings"].pop(listing_index)
        if update_trainer_data(self.buyer_id, buyer_data) and save_market(market_data):
            pokemon = self.listing["pokemon"]
            success_message = f"You purchased a Level {pokemon['level']} {pokemon['name']}{pokemon['gender']} ({pokemon['iv_percentage']}%) from the market (Listing #{self.listing['market_id']}) for {self.listing['amount']:,} Pokécoins. Do @Pokékiro#8400 info latest to view it!"
            await interaction.response.send_message(success_message)
        else:
            await interaction.response.send_message("Failed to complete the purchase. Please try again.", ephemeral=True)
        for item in self.children:
            item.disabled = True
        await interaction.edit_original_response(view=self)
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.buyer_id:
            await interaction.response.send_message("You can't interact with someone else's confirmation.", ephemeral=True)
            return
        await interaction.response.send_message("Aborted.")
        for item in self.children:
            item.disabled = True
        await interaction.edit_original_response(view=self)
@market_command.command(name='buy')
async def market_buy(ctx, listing_id: int = None):
    if listing_id is None:
        embed = discord.Embed(
            title="Missing Parameters",
            description="Please specify a listing ID. Example: `market buy 1`",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    if not is_trainer_registered(ctx.author.id):
        embed = discord.Embed(
            title="Not Registered",
            description="You need to register first!\n\nUse: `@Pokékiro register [Male/Female]`",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return
    market_data = load_market()
    listings = market_data.get("listings", [])
    listing_found = None
    for listing in listings:
        if listing["market_id"] == listing_id:
            listing_found = listing
            break
    if not listing_found:
        embed = discord.Embed(
            title="Listing Not Found",
            description=f"Listing #{listing_id} not found!",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    if listing_found["user_id"] == str(ctx.author.id):
        await ctx.send("You can't purchase your own listing!")
        return
    buyer_data = get_trainer_data(ctx.author.id)
    if not buyer_data:
        await ctx.send("Trainer data not found!")
        return
    buyer_coins = get_user_pokecoins(buyer_data)
    pokemon = listing_found["pokemon"]
    embed = discord.Embed(
        title="💰 Purchase Confirmation",
        description=f"Are you sure you want to buy this Level {pokemon['level']} {pokemon['name']}{pokemon['gender']} ({pokemon['iv_percentage']}%) (Listing #{listing_id}) for {listing_found['amount']:,} Pokécoins?",
        color=0x3498db
    )
    pokemon_info = f"**Level {pokemon['level']} {pokemon['name']}{pokemon['gender']}**\n"
    pokemon_info += f"IV: {pokemon['iv_percentage']}% | Nature: {pokemon['nature'].title()}\n"
    pokemon_info += f"**Price:** {listing_found['amount']:,} Pokécoins\n"
    pokemon_info += f"**Your Pokécoins:** {buyer_coins:,}"
    if buyer_coins < listing_found['amount']:
        pokemon_info += f"\n**You need {listing_found['amount'] - buyer_coins:,} more Pokécoins!**"
        embed.color = 0xe74c3c
    embed.add_field(name="Purchase Details", value=pokemon_info, inline=False)
    if buyer_coins >= listing_found['amount']:
        view = MarketBuyConfirmView(listing_found, ctx.author.id)
        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send(embed=embed)
@market_command.command(name='info')
async def market_info(ctx, listing_id: int = None):
    if listing_id is None:
        embed = discord.Embed(
            title="Missing Parameters",
            description="Please specify a listing ID. Example: `@Pokékiro#8400 market info 38116209`",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    market_data = load_market()
    listing_found = None
    for listing in market_data["listings"]:
        if listing["market_id"] == listing_id:
            listing_found = listing
            break
    if not listing_found:
        embed = discord.Embed(
            title="❌ Listing Not Found",
            description=f"No Pokemon found with market ID {listing_id}.",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    pokemon = listing_found["pokemon"]
    seller_id = listing_found["user_id"]
    try:
        seller = await bot.fetch_user(int(seller_id))
        seller_name = seller.name
        seller_avatar = seller.avatar.url if seller.avatar else seller.default_avatar.url
    except:
        seller_name = "Unknown User"
        seller_avatar = None
    current_level = pokemon["level"]
    current_xp = pokemon.get("xp", 0)
    xp_required_for_current_level = current_level * 50
    pokemon_moves = ["None"]
    embed = discord.Embed(
        title=f"Level {pokemon['level']} {pokemon['name'].title()}",
        color=0xFFD700
    )
    embed.set_author(name=seller_name, icon_url=seller_avatar)
    xp_to_next_level = xp_required_for_current_level - current_xp
    details_text = f"**XP:** {current_xp}/{xp_required_for_current_level} ({xp_to_next_level} XP to next level)\n"
    details_text += f"**Nature:** {pokemon['nature'].title()}\n"
    details_text += f"**Ability:** {pokemon.get('ability', 'Unknown')}\n"
    gender_emoji = pokemon.get('gender', '<:unknown:1401145566863560755>')
    if gender_emoji == '<:male:1400956267979214971>':
        gender_display = gender_emoji
    elif gender_emoji == '<:female:1400956073573224520>':
        gender_display = gender_emoji
    elif gender_emoji == '<:unknown:1401145566863560755>':
        gender_display = gender_emoji
    else:
        gender_display = convert_text_gender_to_emoji(str(gender_emoji))
    details_text += f"**Gender:** {gender_display}\n"
    embed.add_field(name="Details", value=details_text, inline=False)
    stats_text = ""
    ivs = pokemon.get("ivs", {})
    calculated_stats = pokemon.get("calculated_stats", {})
    stat_names = [
        ("HP", "hp"),
        ("Attack", "attack"),
        ("Defense", "defense"),
        ("Sp. Atk", "sp_attack"),
        ("Sp. Def", "sp_defense"),
        ("Speed", "speed")
    ]
    for display_name, stat_key in stat_names:
        stat_value = calculated_stats.get(stat_key, 0)
        iv_value = ivs.get(stat_key, 0)
        stats_text += f"**{display_name}:** {stat_value} – IV: {iv_value}/31\n"
    total_ivs = sum(ivs.values()) if ivs else 0
    iv_percentage = pokemon.get("iv_percentage", (total_ivs / 186) * 100)
    stats_text += f"**Total IV:** {iv_percentage:.2f}%"
    embed.add_field(name="Stats", value=stats_text, inline=False)
    embed.add_field(name="Current Moves", value="None", inline=False)
    listing_text = f"**ID:** {listing_found['market_id']}\n"
    listing_text += f"**Price:** {listing_found['amount']:,} pc"
    embed.add_field(name="Market Listing", value=listing_text, inline=False)
    embed.set_image(url=get_pokemon_image_url(pokemon["name"]))
    await ctx.send(embed=embed)
active_trades = {}
class TradeRequestView(View):
    def __init__(self, requester_id: int, target_id: int):
        super().__init__(timeout=300)
        self.requester_id = requester_id
        self.target_id = target_id
        self.trade_accepted = False
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept_trade(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.target_id:
            await interaction.response.send_message("This trade request is not for you!", ephemeral=True)
            return
        self.trade_accepted = True
        requester = interaction.guild.get_member(self.requester_id)
        target = interaction.guild.get_member(self.target_id)
        if not requester:
            try:
                requester = await interaction.client.fetch_user(self.requester_id)
            except:
                pass
        if not target:
            try:
                target = await interaction.client.fetch_user(self.target_id)
            except:
                pass
        if hasattr(requester, 'display_name'):
            requester_name = requester.display_name
        elif hasattr(requester, 'name'):
            requester_name = requester.name
        else:
            requester_name = "User"
        if hasattr(target, 'display_name'):
            target_name = target.display_name
        elif hasattr(target, 'name'):
            target_name = target.name
        else:
            target_name = "User"
        embed = discord.Embed(
            title=f"Trade between {requester_name} & {target_name}",
            color=0xFFD700
        )
        trade_key = f"{self.requester_id}_{self.target_id}"
        alt_trade_key = f"{self.target_id}_{self.requester_id}"
        trade_data = active_trades.get(trade_key, active_trades.get(alt_trade_key, {
            "requester_pokécoins": 0,
            "target_pokécoins": 0,
            "requester_pokemon": [],
            "target_pokemon": [],
            "requester_confirmed": False,
            "target_confirmed": False
        }))
        requester_display = "None"
        if trade_data.get("requester_pokécoins", 0) > 0:
            requester_display = f"{trade_data['requester_pokécoins']:,} Pokécoins <:pokecoins:1403472605620732099>"
        target_display = "None"
        if trade_data.get("target_pokécoins", 0) > 0:
            target_display = f"{trade_data['target_pokécoins']:,} Pokécoins <:pokecoins:1403472605620732099>"
        requester_dot = "🟢" if trade_data.get("requester_confirmed", False) else "🔴"
        target_dot = "🟢" if trade_data.get("target_confirmed", False) else "🔴"
        embed.add_field(
            name=f"{requester_dot} " + requester_name,
            value=requester_display,
            inline=False
        )
        embed.add_field(
            name=f"{target_dot} " + target_name,
            value=target_display,
            inline=False
        )
        embed.add_field(
            name="Page Info",
            value="Showing page 1 out of 1.",
            inline=False
        )
        embed.add_field(
            name="⚠️ Important Reminder",
            value="Trading Pokécoins or Pokémon for real-life currencies or items in other bots is prohibited and will result in the suspension of your Pokékiro account!",
            inline=False
        )
        trade_key = f"{self.requester_id}_{self.target_id}"
        alt_trade_key = f"{self.target_id}_{self.requester_id}"
        if trade_key in active_trades:
            active_trades[trade_key]["trade_embed"] = embed
            active_trades[trade_key]["trade_message"] = interaction.message
        elif alt_trade_key in active_trades:
            active_trades[alt_trade_key]["trade_embed"] = embed
            active_trades[alt_trade_key]["trade_message"] = interaction.message
        await interaction.response.edit_message(content="", embed=embed, view=None)
    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger)
    async def reject_trade(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.target_id:
            await interaction.response.send_message("This trade request is not for you!", ephemeral=True)
            return
        await interaction.response.edit_message(content="Trade rejected.", view=None)
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        try:
            await self.message.edit(content="Trade request expired.", view=self)
        except:
            pass
@bot.group(invoke_without_command=True)
async def trade(ctx, *, arg=None):
    if arg is None:
        await ctx.send("Usage: `trade @user`")
        return
    try:
        user = await commands.MemberConverter().convert(ctx, arg.strip())
        if user.id == ctx.author.id:
            await ctx.send("You can't trade with yourself!")
            return
        if user.bot:
            await ctx.send("You can't trade with bots nigga !!! 🤡")
            return
        requester_data = get_trainer_data(ctx.author.id)
        if not requester_data:
            await ctx.send(f"<@{ctx.author.id}> You need to register first! Use `register [Male/Female]` to get started.")
            return
        target_data = get_trainer_data(user.id)
        if not target_data:
            await ctx.send(f"<@{user.id}> needs to register first before they can trade!")
            return
        user_id = ctx.author.id
        for trade_data in active_trades.values():
            if trade_data["requester_id"] == user_id or trade_data["target_id"] == user_id:
                await ctx.send("You are already in trade")
                return
        trade_key = f"{ctx.author.id}_{user.id}"
        active_trades[trade_key] = {
            "requester_pokécoins": 0,
            "target_pokécoins": 0,
            "requester_pokemon": [],
            "target_pokemon": [],
            "requester_id": ctx.author.id,
            "target_id": user.id,
            "trade_message": None,
            "trade_embed": None,
            "requester_confirmed": False,
            "target_confirmed": False
        }
        view = TradeRequestView(ctx.author.id, user.id)
        message = await ctx.send(
            f"Requesting a trade with <@{user.id}>. Click the accept button to accept!",
            view=view
        )
        view.message = message
    except commands.MemberNotFound:
        await ctx.send("User not found! Make sure to mention a valid user.")
    except Exception as e:
        await ctx.send("Invalid command. Use `trade @user`")
@trade.command(name="add")
async def trade_add(ctx, *args):
    if not args:
        await ctx.send("Usage: `trade add pokécoins <amount>` or `trade add <order_number(s)>`\nExamples:\n• `trade add pokécoins 1000`\n• `trade add 1` - Add one Pokemon\n• `trade add 1 2 3` - Add multiple Pokemon")
        return
    item_type = args[0]
    amount = args[1] if len(args) > 1 else None
    if item_type.lower() in ["pokécoins", "pokecoins"]:
        if amount is None:
            await ctx.send("Please specify the amount of pokécoins. Example: `trade add pokécoins 1000`")
            return
        try:
            amount_int = int(amount)
            if amount_int <= 0:
                await ctx.send("Amount must be positive!")
                return
        except ValueError:
            await ctx.send("Please enter a valid number for pokécoins amount.")
            return
        requester_data = get_trainer_data(ctx.author.id)
        if not requester_data:
            await ctx.send(f"<@{ctx.author.id}> You need to register first! Use `register [Male/Female]` to get started.")
            return
        user_coins = get_user_pokecoins(requester_data)
        if user_coins < amount_int:
            await ctx.send(f"You don't have enough pokécoins! You have {user_coins:,}, but need {amount_int:,}.")
            return
        user_id = ctx.author.id
        trade_found = None
        trade_key = None
        for key, trade_data in active_trades.items():
            if trade_data["requester_id"] == user_id or trade_data["target_id"] == user_id:
                trade_found = trade_data
                trade_key = key
                break
        if not trade_found:
            await ctx.send("You don't have an active trade! Start a trade first with `trade @user`")
            return
        if trade_found["requester_id"] == user_id:
            active_trades[trade_key]["requester_pokécoins"] += amount_int
        else:
            active_trades[trade_key]["target_pokécoins"] += amount_int
        trade_message = active_trades[trade_key].get("trade_message")
        if trade_message:
            trade_data = active_trades[trade_key]
            try:
                requester = ctx.guild.get_member(trade_data["requester_id"])
                target = ctx.guild.get_member(trade_data["target_id"])
                if not requester:
                    requester = await ctx.bot.fetch_user(trade_data["requester_id"])
                if not target:
                    target = await ctx.bot.fetch_user(trade_data["target_id"])
                requester_name = getattr(requester, 'display_name', getattr(requester, 'name', 'User'))
                target_name = getattr(target, 'display_name', getattr(target, 'name', 'User'))
                embed = discord.Embed(
                    title=f"Trade between {requester_name} & {target_name}",
                    color=0xFFD700
                )
                requester_display = []
                if trade_data.get("requester_pokécoins", 0) > 0:
                    requester_display.append(f"{trade_data['requester_pokécoins']:,} Pokécoins <:pokecoins:1403472605620732099>")
                requester_pokemon = trade_data.get("requester_pokemon", [])
                for pokemon_data in requester_pokemon:
                    requester_display.append(f"{pokemon_data['order']}    {pokemon_data['name']}    •    Lvl.{pokemon_data['level']}    {pokemon_data['iv_percent']}")
                target_display = []
                if trade_data.get("target_pokécoins", 0) > 0:
                    target_display.append(f"{trade_data['target_pokécoins']:,} Pokécoins <:pokecoins:1403472605620732099>")
                target_pokemon = trade_data.get("target_pokemon", [])
                for pokemon_data in target_pokemon:
                    target_display.append(f"{pokemon_data['order']}    {pokemon_data['name']}    •    Lvl.{pokemon_data['level']}    {pokemon_data['iv_percent']}")
                requester_display_text = "\n".join(requester_display) if requester_display else "None"
                target_display_text = "\n".join(target_display) if target_display else "None"
                requester_dot = "🟢" if trade_data.get("requester_confirmed", False) else "🔴"
                target_dot = "🟢" if trade_data.get("target_confirmed", False) else "🔴"
                embed.add_field(
                    name=f"{requester_dot} " + requester_name,
                    value=requester_display_text,
                    inline=False
                )
                embed.add_field(
                    name=f"{target_dot} " + target_name,
                    value=target_display_text,
                    inline=False
                )
                embed.add_field(
                    name="Page Info",
                    value="Showing page 1 out of 1.",
                    inline=False
                )
                embed.add_field(
                    name="⚠️ Important Reminder",
                    value="Trading Pokécoins or Pokémon for real-life currencies or items in other bots is prohibited and will result in the suspension of your Pokékiro account!",
                    inline=False
                )
                await trade_message.edit(embed=embed)
            except Exception as e:
                print(f"Error updating trade embed: {e}")
                await ctx.send(f"Added {amount_int:,} Pokécoins to your trade!")
        else:
            await ctx.send(f"Added {amount_int:,} Pokécoins to your trade!")
    else:
        try:
            order_numbers = [int(arg) for arg in args]
            for order_number in order_numbers:
                if order_number <= 0:
                    await ctx.send("All order numbers must be positive!")
                    return
        except ValueError:
            await ctx.send("Invalid item type. Use `trade add pokécoins <amount>` or `trade add <order_number(s)>`")
            return
        requester_data = get_trainer_data(ctx.author.id)
        if not requester_data:
            await ctx.send(f"<@{ctx.author.id}> You need to register first! Use `register [Male/Female]` to get started.")
            return
        pokemon_collection = []
        if requester_data.get("StarterPokemon"):
            pokemon_collection.append(requester_data["StarterPokemon"])
        if "CaughtPokemons" in requester_data and requester_data["CaughtPokemons"]:
            pokemon_collection.extend(requester_data["CaughtPokemons"])
        if not pokemon_collection:
            await ctx.send("You don't have any Pokémon to trade!")
            return
        user_id = ctx.author.id
        trade_found = None
        trade_key = None
        for key, trade_data in active_trades.items():
            if trade_data["requester_id"] == user_id or trade_data["target_id"] == user_id:
                trade_found = trade_data
                trade_key = key
                break
        if not trade_found:
            await ctx.send("You don't have an active trade! Start a trade first with `trade @user`")
            return
        added_pokemon = []
        skipped_pokemon = []
        for order_number in order_numbers:
            if order_number > len(pokemon_collection):
                skipped_pokemon.append(f"#{order_number} (invalid number)")
                continue
            pokemon_index = order_number - 1
            pokemon = pokemon_collection[pokemon_index]
            user_pokemon_list = []
            if trade_found["requester_id"] == user_id:
                user_pokemon_list = active_trades[trade_key]["requester_pokemon"]
            else:
                user_pokemon_list = active_trades[trade_key]["target_pokemon"]
            already_added = False
            for trade_pokemon in user_pokemon_list:
                if trade_pokemon.get("order") == order_number:
                    skipped_pokemon.append(f"#{order_number} (already added)")
                    already_added = True
                    break
            if already_added:
                continue
            iv_percent = f"{pokemon.get('iv_percentage', 0)}%"
            pokemon_trade_data = {
                "order": order_number,
                "name": pokemon.get("name", "Unknown"),
                "level": pokemon.get("level", 1),
                "iv_percent": iv_percent,
                "original_index": pokemon_index,
                "pokemon_data": pokemon
            }
            if trade_found["requester_id"] == user_id:
                active_trades[trade_key]["requester_pokemon"].append(pokemon_trade_data)
            else:
                active_trades[trade_key]["target_pokemon"].append(pokemon_trade_data)
            added_pokemon.append(f"#{order_number} {pokemon.get('name', 'Unknown')}")
        trade_message = active_trades[trade_key].get("trade_message")
        if trade_message:
            trade_data = active_trades[trade_key]
            try:
                requester = ctx.guild.get_member(trade_data["requester_id"])
                target = ctx.guild.get_member(trade_data["target_id"])
                if not requester:
                    requester = await ctx.bot.fetch_user(trade_data["requester_id"])
                if not target:
                    target = await ctx.bot.fetch_user(trade_data["target_id"])
                requester_name = getattr(requester, 'display_name', getattr(requester, 'name', 'User'))
                target_name = getattr(target, 'display_name', getattr(target, 'name', 'User'))
                embed = discord.Embed(
                    title=f"Trade between {requester_name} & {target_name}",
                    color=0xFFD700
                )
                requester_display = []
                if trade_data.get("requester_pokécoins", 0) > 0:
                    requester_display.append(f"{trade_data['requester_pokécoins']:,} Pokécoins <:pokecoins:1403472605620732099>")
                requester_pokemon = trade_data.get("requester_pokemon", [])
                for pokemon_data in requester_pokemon:
                    requester_display.append(f"{pokemon_data['order']}    {pokemon_data['name']}    •    Lvl.{pokemon_data['level']}    {pokemon_data['iv_percent']}")
                target_display = []
                if trade_data.get("target_pokécoins", 0) > 0:
                    target_display.append(f"{trade_data['target_pokécoins']:,} Pokécoins <:pokecoins:1403472605620732099>")
                target_pokemon = trade_data.get("target_pokemon", [])
                for pokemon_data in target_pokemon:
                    target_display.append(f"{pokemon_data['order']}    {pokemon_data['name']}    •    Lvl.{pokemon_data['level']}    {pokemon_data['iv_percent']}")
                requester_display_text = "\n".join(requester_display) if requester_display else "None"
                target_display_text = "\n".join(target_display) if target_display else "None"
                requester_dot = "🟢" if trade_data.get("requester_confirmed", False) else "🔴"
                target_dot = "🟢" if trade_data.get("target_confirmed", False) else "🔴"
                embed.add_field(
                    name=f"{requester_dot} " + requester_name,
                    value=requester_display_text,
                    inline=False
                )
                embed.add_field(
                    name=f"{target_dot} " + target_name,
                    value=target_display_text,
                    inline=False
                )
                embed.add_field(
                    name="Page Info",
                    value="Showing page 1 out of 1.",
                    inline=False
                )
                embed.add_field(
                    name="⚠️ Important Reminder",
                    value="Trading Pokécoins or Pokémon for real-life currencies or items in other bots is prohibited and will result in the suspension of your Pokékiro account!",
                    inline=False
                )
                await trade_message.edit(embed=embed)
            except Exception as e:
                print(f"Error updating trade embed: {e}")
                feedback_parts = []
                if added_pokemon:
                    feedback_parts.append(f"Added: {', '.join(added_pokemon)}")
                if skipped_pokemon:
                    feedback_parts.append(f"Skipped: {', '.join(skipped_pokemon)}")
                await ctx.send("\n".join(feedback_parts) if feedback_parts else "No Pokemon were added.")
        else:
            feedback_parts = []
            if added_pokemon:
                feedback_parts.append(f"Added: {', '.join(added_pokemon)}")
            if skipped_pokemon:
                feedback_parts.append(f"Skipped: {', '.join(skipped_pokemon)}")
            await ctx.send("\n".join(feedback_parts) if feedback_parts else "No Pokemon were added.")
@trade.command(name="cancel")
async def trade_cancel(ctx):
    user_id = ctx.author.id
    trade_found = None
    trade_key = None
    for key, trade_data in active_trades.items():
        if trade_data["requester_id"] == user_id or trade_data["target_id"] == user_id:
            trade_found = trade_data
            trade_key = key
            break
    if not trade_found:
        await ctx.send("You don't have an active trade to cancel!")
        return
    del active_trades[trade_key]
    await ctx.send("The trade has been cancelled")
@trade.command(name="confirm")
async def trade_confirm(ctx):
    user_id = ctx.author.id
    trade_found = None
    trade_key = None
    for key, trade_data in active_trades.items():
        if trade_data["requester_id"] == user_id or trade_data["target_id"] == user_id:
            trade_found = trade_data
            trade_key = key
            break
    if not trade_found:
        await ctx.send("You don't have an active trade to confirm!")
        return
    if trade_found["requester_id"] == user_id:
        active_trades[trade_key]["requester_confirmed"] = True
        confirmation_status = "You have confirmed the trade!"
    else:
        active_trades[trade_key]["target_confirmed"] = True
        confirmation_status = "You have confirmed the trade!"
    both_confirmed = (active_trades[trade_key]["requester_confirmed"] and
                     active_trades[trade_key]["target_confirmed"])
    await update_trade_embed(ctx, trade_key)
    if both_confirmed:
        await execute_pokécoin_trade(ctx, trade_key)
    else:
        await ctx.send(confirmation_status)
async def update_trade_embed(ctx, trade_key):
    trade_data = active_trades[trade_key]
    trade_message = trade_data.get("trade_message")
    if not trade_message:
        return
    try:
        requester = ctx.guild.get_member(trade_data["requester_id"])
        target = ctx.guild.get_member(trade_data["target_id"])
        if not requester:
            requester = await ctx.bot.fetch_user(trade_data["requester_id"])
        if not target:
            target = await ctx.bot.fetch_user(trade_data["target_id"])
        requester_name = getattr(requester, 'display_name', getattr(requester, 'name', 'User'))
        target_name = getattr(target, 'display_name', getattr(target, 'name', 'User'))
        embed = discord.Embed(
            title=f"Trade between {requester_name} & {target_name}",
            color=0xFFD700
        )
        requester_display = []
        if trade_data.get("requester_pokécoins", 0) > 0:
            requester_display.append(f"{trade_data['requester_pokécoins']:,} Pokécoins <:pokecoins:1403472605620732099>")
        requester_pokemon = trade_data.get("requester_pokemon", [])
        for pokemon_data in requester_pokemon:
            requester_display.append(f"{pokemon_data['order']}    {pokemon_data['name']}    •    Lvl.{pokemon_data['level']}    {pokemon_data['iv_percent']}")
        target_display = []
        if trade_data.get("target_pokécoins", 0) > 0:
            target_display.append(f"{trade_data['target_pokécoins']:,} Pokécoins <:pokecoins:1403472605620732099>")
        target_pokemon = trade_data.get("target_pokemon", [])
        for pokemon_data in target_pokemon:
            target_display.append(f"{pokemon_data['order']}    {pokemon_data['name']}    •    Lvl.{pokemon_data['level']}    {pokemon_data['iv_percent']}")
        requester_display_text = "\n".join(requester_display) if requester_display else "None"
        target_display_text = "\n".join(target_display) if target_display else "None"
        requester_dot = "🟢" if trade_data.get("requester_confirmed", False) else "🔴"
        target_dot = "🟢" if trade_data.get("target_confirmed", False) else "🔴"
        embed.add_field(
            name=f"{requester_dot} " + requester_name,
            value=requester_display_text,
            inline=False
        )
        embed.add_field(
            name=f"{target_dot} " + target_name,
            value=target_display_text,
            inline=False
        )
        embed.add_field(
            name="Page Info",
            value="Showing page 1 out of 1.",
            inline=False
        )
        embed.add_field(
            name="⚠️ Important Reminder",
            value="Trading Pokécoins or Pokémon for real-life currencies or items in other bots is prohibited and will result in the suspension of your Pokékiro account!",
            inline=False
        )
        await trade_message.edit(embed=embed)
    except Exception as e:
        print(f"Error updating trade embed: {e}")
async def execute_pokécoin_trade(ctx, trade_key):
    trade_data = active_trades[trade_key]
    try:
        requester_data = get_trainer_data(trade_data["requester_id"])
        target_data = get_trainer_data(trade_data["target_id"])
        if not requester_data or not target_data:
            await ctx.send("Error: Could not retrieve trainer data!")
            return
        requester_coins = get_user_pokecoins(requester_data)
        target_coins = get_user_pokecoins(target_data)
        if requester_coins < trade_data["requester_pokécoins"]:
            await ctx.send(f"Trade failed: Requester doesn't have enough pokécoins!")
            return
        if target_coins < trade_data["target_pokécoins"]:
            await ctx.send(f"Trade failed: Target user doesn't have enough pokécoins!")
            return
        new_requester_coins = requester_coins - trade_data["requester_pokécoins"] + trade_data["target_pokécoins"]
        new_target_coins = target_coins - trade_data["target_pokécoins"] + trade_data["requester_pokécoins"]
        requester_data["pokécoins"] = new_requester_coins
        target_data["pokécoins"] = new_target_coins
        requester_pokemon_collection = []
        if requester_data.get("StarterPokemon"):
            requester_pokemon_collection.append(requester_data["StarterPokemon"])
        if "CaughtPokemons" in requester_data and requester_data["CaughtPokemons"]:
            requester_pokemon_collection.extend(requester_data["CaughtPokemons"])
        target_pokemon_collection = []
        if target_data.get("StarterPokemon"):
            target_pokemon_collection.append(target_data["StarterPokemon"])
        if "CaughtPokemons" in target_data and target_data["CaughtPokemons"]:
            target_pokemon_collection.extend(target_data["CaughtPokemons"])
        requester_remove_indices = []
        target_remove_indices = []
        requester_traded_pokemon = []
        for pokemon_trade in trade_data.get("requester_pokemon", []):
            original_index = pokemon_trade["original_index"]
            requester_remove_indices.append(original_index)
            requester_traded_pokemon.append(pokemon_trade["pokemon_data"])
        target_traded_pokemon = []
        for pokemon_trade in trade_data.get("target_pokemon", []):
            original_index = pokemon_trade["original_index"]
            target_remove_indices.append(original_index)
            target_traded_pokemon.append(pokemon_trade["pokemon_data"])
        requester_traded_pokemon = []
        for pokemon_trade in trade_data.get("requester_pokemon", []):
            requester_traded_pokemon.append(pokemon_trade["pokemon_data"])
        target_traded_pokemon = []
        for pokemon_trade in trade_data.get("target_pokemon", []):
            target_traded_pokemon.append(pokemon_trade["pokemon_data"])
        if "CaughtPokemons" not in requester_data:
            requester_data["CaughtPokemons"] = []
        if "CaughtPokemons" not in target_data:
            target_data["CaughtPokemons"] = []
        requester_data["CaughtPokemons"].extend(target_traded_pokemon)
        target_data["CaughtPokemons"].extend(requester_traded_pokemon)
        if update_trainer_data(str(trade_data["requester_id"]), requester_data) and update_trainer_data(str(trade_data["target_id"]), target_data):
            del active_trades[trade_key]
            await ctx.send(f"Trade between <@{trade_data['requester_id']}> & <@{trade_data['target_id']}> completed successfully! ✅")
        else:
            await ctx.send("❌ Trade failed: Could not update trainer data!")
    except Exception as e:
        print(f"Error executing trade: {e}")
        await ctx.send("❌ Trade failed due to an error!")
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        command_content = ctx.message.content.lower()
        if any(word in command_content for word in ["summoning", "stone", "gems", "gem", "buy"]):
            await ctx.send(
                "It looks like you're trying to buy something! Use these commands:\n"
                "`@Pokékiro#8400 buy gems <amount>` - Buy gems with pokécoins\n"
                "`@Pokékiro#8400 buy summoning stone <amount>` - Buy summoning stones with gems\n"
                "`@Pokékiro#8400 shop 8` - View gems purchase page\n"
                "`@Pokékiro#8400 shop 10` - View summoning stone page"
            )
    elif isinstance(error, discord.ext.commands.CommandInvokeError):
        print(f"Command error: {error}")
def remove_item_from_inventory(trainer_data, item_name, amount=1):
    if "inventory" not in trainer_data:
        return False
    if item_name not in trainer_data["inventory"]:
        return False
    if trainer_data["inventory"][item_name] < amount:
        return False
    trainer_data["inventory"][item_name] -= amount
    if trainer_data["inventory"][item_name] <= 0:
        del trainer_data["inventory"][item_name]
    return True
def get_pokemon_image_url(pokemon_name):
    from pokémon_dex_entry import get_pokemon_artwork_url
    return get_pokemon_artwork_url(pokemon_name)
def find_pokemon_by_name(pokemon_name):
    pokemon_name_lower = pokemon_name.lower().strip()
    all_generations = [POKEMON_GEN1, POKEMON_GEN2, POKEMON_GEN3, POKEMON_GEN4, POKEMON_GEN5, POKEMON_GEN6, POKEMON_GEN7, POKEMON_GEN8, POKEMON_GEN9]
    for generation in all_generations:
        for i, pokemon in enumerate(generation):
            if pokemon["name"].lower() == pokemon_name_lower:
                return pokemon, i
    return None, None
@bot.command(name='summon')
async def summon_command(ctx, *, pokemon_name=None):
    global current_spawn
    if not pokemon_name:
        embed = discord.Embed(
            title="Missing Pokemon Name",
            description="Please specify which Pokemon to summon!\nExample: `@Pokékiro summon Pikachu`",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    trainer_data = get_trainer_data(ctx.author.id)
    if not trainer_data:
        embed = discord.Embed(
            title="Not Registered",
            description="You need to register first!\nUse: `@Pokékiro register [Male/Female]`",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return
    if "inventory" not in trainer_data or "Summoning Stone" not in trainer_data["inventory"] or trainer_data["inventory"]["Summoning Stone"] < 1:
        embed = discord.Embed(
            title="No Summoning Stone",
            description="You need a Summoning Stone to summon Pokemon!\nBuy one from the shop: `@Pokékiro buy summoning stone`",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    if current_spawn is not None:
        embed = discord.Embed(
            title="Pokemon Already Spawned",
            description="There's already a Pokemon spawned! Catch it first before summoning another.",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    pokemon_data, pokemon_index = find_pokemon_by_name(pokemon_name)
    if not pokemon_data:
        embed = discord.Embed(
            title="Pokemon Not Found",
            description=f"Pokemon '{pokemon_name}' not found in the database!\nMake sure you spelled it correctly.",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    if not remove_item_from_inventory(trainer_data, "Summoning Stone", 1):
        embed = discord.Embed(
            title="Error",
            description="Failed to use Summoning Stone. Please try again.",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    if not update_trainer_data(ctx.author.id, trainer_data):
        embed = discord.Embed(
            title="Error",
            description="Failed to update your inventory. Please try again.",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    spawned_pokemon = create_spawned_pokemon(pokemon_data)
    current_spawn = {
        "name": spawned_pokemon["name"],
        "level": spawned_pokemon["level"],
        "gender": spawned_pokemon["gender"],
        "total_iv": spawned_pokemon["iv_percentage"],
        "caught": False,
        "full_data": spawned_pokemon
    }
    embed = discord.Embed(
        title="A wild pokémon has been summoned!",
        description=f"{ctx.author.mention} used a Summoning Stone <:Summoning_stone:1405194343056408747> guess the pokémon and type `Pokékiro#8400 catch <pokémon>` to catch it!",
        color=0x9932CC
    )
    embed.set_image(url=get_pokemon_image_url(spawned_pokemon['name']))
    remaining_stones = trainer_data["inventory"].get("Summoning Stone", 0)
    embed.set_footer(text=f"Summoning Stones remaining: {remaining_stones}")
    await ctx.send(embed=embed)
BASE_URL = "https://pokemondb.net/pokedex/"
def analyze_special_case(pokemon_name):
    lower_name = pokemon_name.lower().strip()
    special_case_info = {
        "is_special_case": False,
        "category": None,
        "explanation": None,
        "alternative_name": None,
        "note": None
    }
    if any(keyword in lower_name for keyword in ["mega ", "gigantamax ", "primal "]):
        special_case_info.update({
            "is_special_case": True,
            "category": "Transformation",
            "explanation": "This Pokemon uses a temporary transformation. Movesets are usually the same as the base form.",
            "alternative_name": lower_name.replace("mega ", "").replace("gigantamax ", "").replace("primal ", "").strip(),
            "note": "Try searching for the base Pokemon name instead."
        })
    elif "eternamax" in lower_name:
        special_case_info.update({
            "is_special_case": True,
            "category": "Unique Form",
            "explanation": "Eternamax Eternatus is a special raid-only form with the same movesets as regular Eternatus.",
            "alternative_name": "eternatus",
            "note": "This form cannot be used in normal battles."
        })
    elif any(region in lower_name for region in ["alolan ", "galarian ", "hisuian ", "paldean "]):
        special_case_info.update({
            "is_special_case": True,
            "category": "Regional Form",
            "explanation": "This is a regional variant with different movesets from the original form.",
            "note": "Regional forms have unique movesets - this should work with the enhanced scraper."
        })
    elif "urshifu" in lower_name and ("single strike" in lower_name or "rapid strike" in lower_name):
        special_case_info.update({
            "is_special_case": True,
            "category": "Combat Style",
            "explanation": "Urshifu has two different combat styles with different signature moves.",
            "note": "Each style learns different moves at certain levels."
        })
    return special_case_info
def get_level_up_moves(pokemon_name):
    url_name = pokemon_name.lower().strip()
    url_replacements = {
        "mr. mime": "mr-mime",
        "mime jr.": "mime-jr",
        "mr. rime": "mr-rime",
        "farfetch'd": "farfetchd",
        "sirfetch'd": "sirfetchd",
        "nidoran♀": "nidoran-f",
        "nidoran♂": "nidoran-m",
        "ho-oh": "ho-oh",
        "porygon-z": "porygon-z",
        "jangmo-o": "jangmo-o",
        "hakamo-o": "hakamo-o",
        "kommo-o": "kommo-o",
        "tapu koko": "tapu-koko",
        "tapu lele": "tapu-lele",
        "tapu bulu": "tapu-bulu",
        "tapu fini": "tapu-fini",
        "type: null": "type-null",
        "flabébé": "flabebe",
        "mega venusaur": "venusaur",
        "mega charizard x": "charizard",
        "mega charizard y": "charizard",
        "mega blastoise": "blastoise",
        "mega alakazam": "alakazam",
        "mega gengar": "gengar",
        "mega kangaskhan": "kangaskhan",
        "mega pinsir": "pinsir",
        "mega gyarados": "gyarados",
        "mega aerodactyl": "aerodactyl",
        "mega mewtwo x": "mewtwo",
        "mega mewtwo y": "mewtwo",
        "mega ampharos": "ampharos",
        "mega scizor": "scizor",
        "mega heracross": "heracross",
        "mega houndoom": "houndoom",
        "mega tyranitar": "tyranitar",
        "mega blaziken": "blaziken",
        "mega gardevoir": "gardevoir",
        "mega mawile": "mawile",
        "mega aggron": "aggron",
        "mega medicham": "medicham",
        "mega manectric": "manectric",
        "mega banette": "banette",
        "mega absol": "absol",
        "mega garchomp": "garchomp",
        "mega lucario": "lucario",
        "mega abomasnow": "abomasnow",
        "mega rayquaza": "rayquaza",
        "primal groudon": "groudon",
        "primal kyogre": "kyogre",
        "gigantamax charizard": "charizard",
        "gigantamax butterfree": "butterfree",
        "gigantamax pikachu": "pikachu",
        "gigantamax meowth": "meowth",
        "gigantamax machamp": "machamp",
        "gigantamax gengar": "gengar",
        "gigantamax kingler": "kingler",
        "gigantamax lapras": "lapras",
        "gigantamax eevee": "eevee",
        "gigantamax snorlax": "snorlax",
        "gigantamax garbodor": "garbodor",
        "gigantamax corviknight": "corviknight",
        "gigantamax orbeetle": "orbeetle",
        "gigantamax drednaw": "drednaw",
        "gigantamax coalossal": "coalossal",
        "gigantamax flapple": "flapple",
        "gigantamax appletun": "appletun",
        "gigantamax sandaconda": "sandaconda",
        "gigantamax toxapex": "toxapex",
        "gigantamax centiskorch": "centiskorch",
        "gigantamax hatterene": "hatterene",
        "gigantamax grimmsnarl": "grimmsnarl",
        "gigantamax alcremie": "alcremie",
        "gigantamax copperajah": "copperajah",
        "gigantamax duraludon": "duraludon",
        "urshifu single strike style": "urshifu-single-strike",
        "urshifu rapid strike style": "urshifu-rapid-strike",
        "urshifu single strike": "urshifu-single-strike",
        "urshifu rapid strike": "urshifu-rapid-strike",
        "eternamax eternatus": "eternatus",
        "rotom heat": "rotom-heat",
        "rotom wash": "rotom-wash",
        "rotom frost": "rotom-frost",
        "rotom fan": "rotom-fan",
        "rotom mow": "rotom-mow",
        "deoxys attack forme": "deoxys-attack",
        "deoxys defense forme": "deoxys-defense",
        "deoxys speed forme": "deoxys-speed",
        "deoxys attack": "deoxys-attack",
        "deoxys defense": "deoxys-defense",
        "deoxys speed": "deoxys-speed",
        "wormadam plant cloak": "wormadam-plant",
        "wormadam sandy cloak": "wormadam-sandy",
        "wormadam trash cloak": "wormadam-trash",
        "wormadam plant": "wormadam-plant",
        "wormadam sandy": "wormadam-sandy",
        "wormadam trash": "wormadam-trash",
        "shaymin land forme": "shaymin",
        "shaymin sky forme": "shaymin-sky",
        "shaymin land": "shaymin",
        "shaymin sky": "shaymin-sky",
        "alolan rattata": "alolan-rattata",
        "alolan raticate": "alolan-raticate",
        "alolan raichu": "alolan-raichu",
        "alolan sandshrew": "alolan-sandshrew",
        "alolan sandslash": "alolan-sandslash",
        "alolan vulpix": "alolan-vulpix",
        "alolan ninetales": "alolan-ninetales",
        "alolan diglett": "alolan-diglett",
        "alolan dugtrio": "alolan-dugtrio",
        "alolan meowth": "alolan-meowth",
        "alolan persian": "alolan-persian",
        "alolan geodude": "alolan-geodude",
        "alolan graveler": "alolan-graveler",
        "alolan golem": "alolan-golem",
        "alolan grimer": "alolan-grimer",
        "alolan muk": "alolan-muk",
        "alolan exeggutor": "alolan-exeggutor",
        "alolan marowak": "alolan-marowak",
        "galarian meowth": "galarian-meowth",
        "galarian ponyta": "galarian-ponyta",
        "galarian rapidash": "galarian-rapidash",
        "galarian slowpoke": "galarian-slowpoke",
        "galarian slowbro": "galarian-slowbro",
        "galarian farfetch'd": "galarian-farfetchd",
        "galarian weezing": "galarian-weezing",
        "galarian mr. mime": "galarian-mr-mime",
        "galarian articuno": "galarian-articuno",
        "galarian zapdos": "galarian-zapdos",
        "galarian moltres": "galarian-moltres",
        "galarian slowking": "galarian-slowking",
        "galarian corsola": "galarian-corsola",
        "galarian zigzagoon": "galarian-zigzagoon",
        "galarian linoone": "galarian-linoone",
        "galarian darumaka": "galarian-darumaka",
        "galarian darmanitan": "galarian-darmanitan",
        "galarian yamask": "galarian-yamask",
        "galarian stunfisk": "galarian-stunfisk",
        "hisuian growlithe": "hisuian-growlithe",
        "hisuian arcanine": "hisuian-arcanine",
        "hisuian voltorb": "hisuian-voltorb",
        "hisuian electrode": "hisuian-electrode",
        "hisuian typhlosion": "hisuian-typhlosion",
        "hisuian qwilfish": "hisuian-qwilfish",
        "hisuian sneasel": "hisuian-sneasel",
        "hisuian samurott": "hisuian-samurott",
        "hisuian lilligant": "hisuian-lilligant",
        "hisuian zorua": "hisuian-zorua",
        "hisuian zoroark": "hisuian-zoroark",
        "hisuian braviary": "hisuian-braviary",
        "hisuian sliggoo": "hisuian-sliggoo",
        "hisuian goodra": "hisuian-goodra",
        "hisuian avalugg": "hisuian-avalugg",
        "hisuian decidueye": "hisuian-decidueye",
        "paldean tauros (combat breed)": "tauros-paldea-combat",
        "paldean tauros (blaze breed)": "tauros-paldea-blaze",
        "paldean tauros (aqua breed)": "tauros-paldea-aqua",
        "paldean tauros combat": "tauros-paldea-combat",
        "paldean tauros blaze": "tauros-paldea-blaze",
        "paldean tauros aqua": "tauros-paldea-aqua",
        "paldean wooper": "paldean-wooper",
        "arceus bug": "arceus",
        "arceus dark": "arceus",
        "arceus dragon": "arceus",
        "arceus electric": "arceus",
        "arceus fairy": "arceus",
        "arceus fighting": "arceus",
        "arceus fire": "arceus",
        "arceus flying": "arceus",
        "arceus ghost": "arceus",
        "arceus grass": "arceus",
        "arceus ground": "arceus",
        "arceus ice": "arceus",
        "arceus poison": "arceus",
        "arceus psychic": "arceus",
        "arceus rock": "arceus",
        "arceus steel": "arceus",
        "arceus water": "arceus"
    }
    if url_name in url_replacements:
        url_name = url_replacements[url_name]
    else:
        url_name = url_name.replace(" ", "-")
    url = BASE_URL + url_name
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            special_info = analyze_special_case(pokemon_name)
            if special_info["is_special_case"]:
                error_msg = f"❌ **{special_info['category']} Detected:** {pokemon_name.title()}\n\n"
                error_msg += f"ℹ️ **{special_info['explanation']}**\n"
                if special_info['alternative_name']:
                    error_msg += f"💡 **Suggestion:** Try searching for `{special_info['alternative_name'].title()}`\n"
                if special_info['note']:
                    error_msg += f"📝 **Note:** {special_info['note']}"
                return error_msg
            else:
                return f"❌ **Pokemon not found:** Could not fetch data for **{pokemon_name.title()}**. Please check the spelling and try again."
        soup = BeautifulSoup(resp.text, "html.parser")
        moves_section = soup.find("h3", string="Moves learnt by level up")
        if not moves_section:
            moves_section = soup.find("h3", string=lambda text: text and "level up" in text.lower() if text else False)
        if not moves_section:
            moves_section = soup.find("h2", string="Moves learnt by level up")
        if not moves_section:
            moves_section = soup.find("h2", string=lambda text: text and "level up" in text.lower() if text else False)
        if not moves_section:
            return f"❌ **No level-up moves found** for **{pokemon_name.title()}**. This Pokemon may not learn moves by leveling up."
        table = moves_section.find_next("table")
        if not table:
            return f"❌ **No movesets table found** for **{pokemon_name.title()}**."
        rows = table.find_all("tr")
        if len(rows) <= 1:
            return f"❌ **No moves data found** for **{pokemon_name.title()}**."
        formatted_moves = []
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue
            level = cols[0].get_text(strip=True)
            move = cols[1].get_text(strip=True)
            move_type = cols[2].get_text(strip=True)
            category = cols[3].get_text(strip=True)
            formatted_moves.append(f"**Level {level}** - {move} `[{move_type}/{category}]`")
        if not formatted_moves:
            return f"❌ **No valid moves found** for **{pokemon_name.title()}**."
        output = f"📋 **{pokemon_name.title()} — Level-up Movesets**\n\n"
        output += "\n".join(formatted_moves)
        output += f"\n\n*Data fetched from pokemondb.net*"
        return output
    except requests.RequestException as e:
        return f"❌ **Network error:** Could not fetch data from pokemondb.net. Please try again later."
    except Exception as e:
        return f"❌ **Error processing data** for **{pokemon_name.title()}**: {str(e)}"
async def get_level_up_moves_async(pokemon_name):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, get_level_up_moves, pokemon_name)
def split_long_message(text, max_length=2000):
    if len(text) <= max_length:
        return [text]
    parts = []
    lines = text.split('\n')
    current_part = ""
    for line in lines:
        if len(current_part) + len(line) + 1 > max_length:
            if current_part:
                parts.append(current_part)
                current_part = line
            else:
                while len(line) > max_length:
                    parts.append(line[:max_length])
                    line = line[max_length:]
                current_part = line
        else:
            if current_part:
                current_part += "\n" + line
            else:
                current_part = line
    if current_part:
        parts.append(current_part)
    return parts
def get_move_by_name(move_name):
    move_key = move_name.lower().strip().replace(" ", "-")
    if move_key in POKEMON_MOVES:
        return POKEMON_MOVES[move_key]
    for key, move_data in POKEMON_MOVES.items():
        if move_data["name"].lower() == move_name.lower().strip():
            return move_data
        if key.replace("-", " ").lower() == move_name.lower().strip():
            return move_data
    return None
def get_all_moves():
    return POKEMON_MOVES
def search_moves_by_type(move_type):
    matching_moves = []
    for move_key, move_data in POKEMON_MOVES.items():
        if move_data["type"].lower() == move_type.lower():
            matching_moves.append(move_data)
    return matching_moves
def search_moves_by_class(move_class):
    matching_moves = []
    for move_key, move_data in POKEMON_MOVES.items():
        if move_data["class"].lower() == move_class.lower():
            matching_moves.append(move_data)
    return matching_moves
def format_move_info(move_data):
    if not move_data:
        return "Move not found."
    output = f"**{move_data['name']}**\n"
    output += f"**Type:** {move_data['type']}\n"
    output += f"**Class:** {move_data['class']}\n"
    output += f"**Power:** {move_data.get('power', 'N/A')}\n"
    output += f"**Accuracy:** {move_data.get('accuracy', 'N/A')}%\n"
    output += f"**PP:** {move_data.get('pp', 'N/A')}\n"
    output += f"**Priority:** {move_data.get('priority', 0)}\n"
    output += f"**Target:** {move_data.get('target', 'N/A')}\n"
    output += f"**Generation:** {move_data.get('generation', 'Unknown')}\n"
    if move_data.get('description'):
        output += f"**Description:** {move_data['description']}\n"
    return output
@bot.command()
async def movesets(ctx, *, pokemon_name=None):
    if not pokemon_name:
        embed = discord.Embed(
            title="Missing Pokemon Name",
            description="Please specify a Pokemon name!\nExample: `@Pokékiro movesets Charizard`",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    async with ctx.typing():
        try:
            from movesets_scraper import get_all_moves_comprehensive_async, MovePaginationView
            move_data = await get_all_moves_comprehensive_async(pokemon_name)
            if "error" in move_data:
                embed = discord.Embed(
                    title="Error",
                    description=move_data["error"],
                    color=0xff0000
                )
                await ctx.send(embed=embed)
                return
            if not any([move_data["level_up"], move_data["evolution"], move_data["egg"], move_data["tm"]]):
                embed = discord.Embed(
                    title="No Moves Found",
                    description=f"No movesets were found for **{pokemon_name.title()}**. Please check the spelling and try again.",
                    color=0xff0000
                )
                await ctx.send(embed=embed)
                return
            view = MovePaginationView(move_data, ctx.author.id)
            await ctx.send(embed=view.get_current_embed(), view=view)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred while fetching movesets: {str(e)}",
                color=0xff0000
            )
            await ctx.send(embed=embed)
@bot.command(name="use")
async def use_command(ctx, *, args: str):
    trainer_data = get_trainer_data(ctx.author.id)
    if not trainer_data:
        await ctx.send("❌ You are not registered as a trainer. Use `@Pokékiro register` first.")
        return
    
    parts = args.split()
    if len(parts) == 0:
        await ctx.send("❌ Usage: @Pokékiro use rare candy <amount> or @Pokékiro use move <move-name>")
        return
    
    # Check if user is in a battle and wants to use a move
    battle_id = None
    for bid, battle_data in active_battles.items():
        if ctx.author.id in [battle_data.get("challenger_id"), battle_data.get("target_id")] and battle_data.get("battle_started"):
            battle_id = bid
            break
    
    # If first argument is "move" and user is in battle, handle move usage
    if parts[0].lower() == "move" and battle_id:
        if len(parts) < 2:
            await ctx.send("Usage: `@Pokékiro use move <move-name>`")
            return
        move_name = " ".join(parts[1:]).lower().replace(" ", "-")
        
        await ctx.send(f"✅ You used {move_name.replace('-', ' ').title()}!")
        return
    
    # Handle item usage (existing functionality)
    try:
        amount = int(parts[-1])
        item = " ".join(parts[:-1]).lower()
    except ValueError:
        amount = 1
        item = " ".join(parts).lower()
    if item not in ["rare candy", "rare_candy", "rare-candy", "rare"]:
        await ctx.send("❌ Currently, only Rare Candy usage is supported.")
        return
    inventory = trainer_data.get("inventory", {})
    inventory_normalized = {k.lower(): v for k, v in inventory.items()}
    rare_candies = inventory_normalized.get("rare candy", 0)
    if rare_candies < amount:
        await ctx.send(f"❌ You don’t have enough Rare Candies! (You have {rare_candies})")
        return
    inventory_key = next((k for k in inventory if k.lower() == "rare candy"), "Rare Candy")
    trainer_data["inventory"][inventory_key] = rare_candies - amount
    selected = trainer_data.get("SelectedPokemon")
    if not selected:
        await ctx.send("❌ You must select a Pokémon first using `@Pokékiro select <order_number>`.")
        return
    pokemon_entry = None
    if selected["type"] == "starter":
        pokemon_entry = trainer_data.get("StarterPokemon")
    elif selected["type"] == "caught":
        starter = trainer_data.get("StarterPokemon")
        if starter:
            idx = selected["order"] - 2
        else:
            idx = selected["order"] - 1
        if "CaughtPokemons" in trainer_data and 0 <= idx < len(trainer_data["CaughtPokemons"]):
            pokemon_entry = trainer_data["CaughtPokemons"][idx]
    if not pokemon_entry:
        await ctx.send("❌ Selected Pokémon not found.")
        return
    original_name = pokemon_entry.get("name", "Unknown").title()
    old_level = pokemon_entry.get("level", 1)
    old_stats = pokemon_entry.get("calculated_stats", {}).copy()
    pokemon_entry["level"] = min(100, old_level + amount)
    new_level = pokemon_entry["level"]
    base_stats = pokemon_entry.get("base_stats", {})
    ivs = pokemon_entry.get("ivs", {})
    nature = pokemon_entry.get("nature", "hardy")
    evs = pokemon_entry.get("evs", {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
    new_stats = calculate_official_stats(base_stats, ivs, new_level, nature, evs)
    pokemon_entry["calculated_stats"] = new_stats
    try:
        from evolutions import LEVEL_ONLY_EVOLUTIONS as EVOLUTIONS
    except Exception:
        EVOLUTIONS = {}
    evolutions_done = []
    while True:
        current_name_lower = pokemon_entry.get("name", "").lower()
        evo_info = EVOLUTIONS.get(current_name_lower)
        if not evo_info:
            break
        required_level = evo_info.get("level", 9999)
        if new_level >= required_level:
            old_species = pokemon_entry.get("name", "").title()
            new_species = evo_info.get("evolves_to", "").lower()
            try:
                species_data = get_pokemon_by_name(new_species)
            except Exception:
                species_data = None
            pokemon_entry["name"] = new_species
            if species_data:
                new_base = species_data.get("base_stats") or species_data.get("stats") or {}
                if new_base:
                    pokemon_entry["base_stats"] = new_base
                sprite_candidate = species_data.get("sprite") if species_data else None
                if sprite_candidate:
                    pokemon_entry["sprite"] = sprite_candidate
            try:
                img_url = get_pokemon_image_url(pokemon_entry["name"])
                if img_url:
                    pokemon_entry["sprite"] = img_url
            except Exception:
                pass
            base_stats = pokemon_entry.get("base_stats", base_stats)
            new_stats = calculate_official_stats(base_stats, ivs, new_level, nature, evs)
            pokemon_entry["calculated_stats"] = new_stats
            evolutions_done.append((old_species, pokemon_entry["name"].title()))
            continue
        else:
            break
    moves_learned = []
    try:
        current_name = pokemon_entry.get("name", original_name)
        movesets = get_all_moves_comprehensive(current_name)
        if "level_up" in movesets and movesets["level_up"]:
            for level in range(old_level + 1, new_level + 1):
                for move_info in movesets["level_up"]:
                    if move_info.get("level") and move_info["level"].isdigit():
                        move_level = int(move_info["level"])
                        if move_level == level:
                            moves_learned.append(move_info["move"])
    except:
        pass
    if moves_learned:
        if "learned_moves" not in pokemon_entry:
            pokemon_entry["learned_moves"] = []
        for move in moves_learned:
            if move not in pokemon_entry["learned_moves"]:
                pokemon_entry["learned_moves"].append(move)
    update_trainer_data(str(ctx.author.id), trainer_data)
    description = (
        f"You used {amount} Rare Candy <:rare_candy:1403486543477473521>!\n\n"
        f"Your {original_name} grew from level {old_level} → {new_level}!"
    )
    if moves_learned:
        moves_text = ", ".join([move.replace("-", " ").title() for move in moves_learned])
        description += f"\n\n✨ **New moves learned:** {moves_text}"
    embed = discord.Embed(
        title="🎉 Level Up!",
        description=description,
        color=discord.Color.gold()
    )
    if evolutions_done:
        first_old = evolutions_done[0][0]
        last_new = evolutions_done[-1][1]
        embed.description += f"\n\n🎉 Congratulations {ctx.author.display_name}!\nYour {first_old} evolved into **{last_new}**!"
    stats_text = ""
    for stat in ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]:
        before = old_stats.get(stat, 0)
        after = new_stats.get(stat, 0)
        diff = after - before
        stats_text += f"**{stat.upper()}**: {before} → {after} (+{diff})\n"
    embed.add_field(name="📊 Stats Update", value=stats_text, inline=False)
    try:
        embed.set_image(url=get_pokemon_image_url(pokemon_entry["name"]))
    except Exception:
        if pokemon_entry.get("sprite"):
            embed.set_thumbnail(url=pokemon_entry["sprite"])
    embed.set_footer(text=f"Remaining Rare Candies: {trainer_data['inventory'][inventory_key]}")
    await ctx.send(embed=embed)
@bot.command(name="moves")
async def show_pokemon_moves(ctx):
    trainer_data = get_trainer_data(ctx.author.id)
    if not trainer_data:
        await ctx.send("❌ You are not registered as a trainer.")
        return
    selected_pokemon = trainer_data.get("SelectedPokemon")
    if not selected_pokemon:
        await ctx.send("❌ You need to select a Pokemon first using `@Pokékiro select <order>`")
        return
    pokemon_data = None
    if selected_pokemon["type"] == "starter" and trainer_data["StarterPokemon"] is not None:
        pokemon_data = trainer_data["StarterPokemon"]
    elif selected_pokemon["type"] == "caught" and "CaughtPokemons" in trainer_data:
        starter = trainer_data.get("StarterPokemon")
        if starter:
            caught_index = selected_pokemon["order"] - 2
        else:
            caught_index = selected_pokemon["order"] - 1
        if 0 <= caught_index < len(trainer_data["CaughtPokemons"]):
            pokemon_data = trainer_data["CaughtPokemons"][caught_index]
    if not pokemon_data:
        await ctx.send("❌ Selected Pokemon not found.")
        return
    pokemon_name = pokemon_data.get("name", "Unknown")
    pokemon_level = pokemon_data.get("level", 1)
    learned_moves = pokemon_data.get("learned_moves", [])
    available_moves = []
    try:
        from movesets_scraper import get_all_moves_comprehensive
        moveset_data = get_all_moves_comprehensive(pokemon_name.lower())
        if moveset_data and 'level_up' in moveset_data:
            for move_info in moveset_data['level_up']:
                level = move_info['level']
                if level.isdigit() and int(level) <= pokemon_level:
                    move_name = move_info['move'].replace('-', ' ').title()
                    available_moves.append(f"{level}. {move_name}")
        available_moves.sort(key=lambda x: int(x.split('.')[0]))
    except Exception as e:
        available_moves = ["Unable to fetch moves data"]
    embed = discord.Embed(
        title=f"Level {pokemon_level} {pokemon_name.title()} — Moves",
        description=f"Here are the moves your pokémon can learn right now. View all moves and how to get them using `@PᴏᴋéKɪʀᴏ movesets {pokemon_name.lower()}`!",
        color=discord.Color.gold()
    )
    if available_moves and available_moves[0] != "Unable to fetch moves data":
        clean_moves = []
        for move in available_moves:
            move_name = move.split('. ', 1)[1] if '. ' in move else move
            clean_moves.append(f"{len(clean_moves)+1}. {move_name}")
        available_text = "\n".join(clean_moves)
    else:
        available_text = "No moves available"
    embed.add_field(name="**Available Moves**", value=available_text, inline=False)
    current_moves = pokemon_data.get("current_moves", [])
    current_moves_text = ""
    for i in range(1, 5):
        if i-1 < len(current_moves):
            current_moves_text += f"{i}. {current_moves[i-1].replace('-', ' ').title()}\n"
        else:
            current_moves_text += f"{i}. None\n"
    embed.add_field(name="**Current Moves**", value=current_moves_text, inline=False)
    await ctx.send(embed=embed)

class MoveReplaceView(View):
    def __init__(self, user_id, pokemon_data, pokemon_type, new_move, trainer_data):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.pokemon_data = pokemon_data
        self.pokemon_type = pokemon_type
        self.new_move = new_move
        self.trainer_data = trainer_data
        
        # Add dropdown for move selection
        current_moves = pokemon_data.get("current_moves", [])
        options = []
        for i, move in enumerate(current_moves):
            if move:
                options.append(discord.SelectOption(
                    label=move.replace('-', ' ').title(),
                    value=str(i),
                    description=f"Slot {i+1}"
                ))
        
        if options:
            self.select_move.options = options
        else:
            self.select_move.disabled = True

    @discord.ui.select(placeholder="Replace a move", min_values=1, max_values=1)
    async def select_move(self, interaction: discord.Interaction, select):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Only the Pokemon owner can replace moves!", ephemeral=True)
            return
            
        slot_index = int(select.values[0])
        old_move = self.pokemon_data["current_moves"][slot_index]
        
        # Replace the move
        self.pokemon_data["current_moves"][slot_index] = self.new_move
        
        # Update trainer data
        if self.pokemon_type == "starter":
            self.trainer_data["StarterPokemon"] = self.pokemon_data
        elif self.pokemon_type == "caught":
            starter = self.trainer_data.get("StarterPokemon")
            if starter:
                caught_index = self.pokemon_data.get("order", 1) - 2
            else:
                caught_index = self.pokemon_data.get("order", 1) - 1
            if 0 <= caught_index < len(self.trainer_data["CaughtPokemons"]):
                self.trainer_data["CaughtPokemons"][caught_index] = self.pokemon_data
        
        update_trainer_data(self.user_id, self.trainer_data)
        
        embed = discord.Embed(
            title="✅ Move Learned!",
            description=f"Your Pokémon has learned **{self.new_move.replace('-', ' ').title()}** and forgotten **{old_move.replace('-', ' ').title()}**!",
            color=0x00ff00
        )
        
        await interaction.response.edit_message(embed=embed, view=None)


async def send_battle_interface_to_players(battle_id, challenger_id, target_id, challenger_party, target_party, challenger_name, target_name, channel):
    """Send battle interface embed to both players"""
    pass



@bot.command(name="learn")
async def learn_move(ctx, *, move_name: str = None):
    if not move_name:
        embed = discord.Embed(
            title="Missing Move Name",
            description="Please specify which move you want to learn!\n\nUse: `@Pokékiro learn <move_name>`\nExample: `@Pokékiro learn thunderbolt`",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return
        
    if not is_trainer_registered(ctx.author.id):
        embed = discord.Embed(
            title="Not Registered",
            description="You need to register first!\n\nUse: `@Pokékiro register [Male/Female]`",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return
        
    trainer_data = get_trainer_data(ctx.author.id)
    if not trainer_data:
        await ctx.send("❌ Unable to retrieve trainer data.")
        return
        
    selected_pokemon = trainer_data.get("SelectedPokemon")
    if not selected_pokemon:
        await ctx.send("❌ You need to select a Pokemon first using `@Pokékiro select <order>`")
        return
        
    # Get the selected Pokemon data
    pokemon_data = None
    pokemon_type = selected_pokemon["type"]
    
    if pokemon_type == "starter" and trainer_data["StarterPokemon"] is not None:
        pokemon_data = trainer_data["StarterPokemon"]
    elif pokemon_type == "caught" and "CaughtPokemons" in trainer_data:
        starter = trainer_data.get("StarterPokemon")
        if starter:
            caught_index = selected_pokemon["order"] - 2
        else:
            caught_index = selected_pokemon["order"] - 1
        if 0 <= caught_index < len(trainer_data["CaughtPokemons"]):
            pokemon_data = trainer_data["CaughtPokemons"][caught_index]
            
    if not pokemon_data:
        await ctx.send("❌ Selected Pokemon not found.")
        return
        
    pokemon_name = pokemon_data.get("name", "Unknown")
    pokemon_level = pokemon_data.get("level", 1)
    
    # Normalize move name for comparison
    move_name_normalized = move_name.lower().replace(" ", "-")
    
    # Check if Pokemon can learn this move
    try:
        from movesets_scraper import get_all_moves_comprehensive
        moveset_data = get_all_moves_comprehensive(pokemon_name.lower())
        
        can_learn = False
        required_level = 999
        
        if moveset_data and 'level_up' in moveset_data:
            for move_info in moveset_data['level_up']:
                move_db_name = move_info['move'].lower().replace(" ", "-")
                if move_db_name == move_name_normalized:
                    move_level = move_info['level']
                    if move_level.isdigit():
                        required_level = int(move_level)
                        if pokemon_level >= required_level:
                            can_learn = True
                        break
                        
    except Exception:
        embed = discord.Embed(
            title="❌ Error",
            description="Unable to fetch move data. Please try again later.",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return
        
    if not can_learn:
        if required_level == 999:
            embed = discord.Embed(
                title="❌ Cannot Learn Move",
                description=f"Your {pokemon_name.title()} cannot learn **{move_name.title()}**.",
                color=0xe74c3c
            )
        else:
            embed = discord.Embed(
                title="❌ Level Too Low",
                description=f"Your Pokemon level is too low to learn this move. Required level: {required_level}",
                color=0xe74c3c
            )
        await ctx.send(embed=embed)
        return
        
    # Initialize current_moves if it doesn't exist
    if "current_moves" not in pokemon_data:
        pokemon_data["current_moves"] = []
        
    current_moves = pokemon_data["current_moves"]
    
    # Check if Pokemon already knows this move
    if move_name_normalized in [move.lower().replace(" ", "-") for move in current_moves]:
        embed = discord.Embed(
            title="❌ Already Known",
            description=f"Your {pokemon_name.title()} already knows **{move_name.title()}**!",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return
        
    # If Pokemon has less than 4 moves, add it directly
    if len(current_moves) < 4:
        current_moves.append(move_name_normalized)
        
        # Update trainer data
        if pokemon_type == "starter":
            trainer_data["StarterPokemon"] = pokemon_data
        elif pokemon_type == "caught":
            starter = trainer_data.get("StarterPokemon")
            if starter:
                caught_index = selected_pokemon["order"] - 2
            else:
                caught_index = selected_pokemon["order"] - 1
            if 0 <= caught_index < len(trainer_data["CaughtPokemons"]):
                trainer_data["CaughtPokemons"][caught_index] = pokemon_data
                
        update_trainer_data(ctx.author.id, trainer_data)
        
        embed = discord.Embed(
            title="✅ Move Learned!",
            description=f"Your Pokémon has learned **{move_name.title()}**!",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
        
    else:
        # Pokemon already knows 4 moves, need to replace one
        embed = discord.Embed(
            title="<:status:1407693796787097672> Replace Move",
            description="Your pokémon already knows the max number of moves! Please select a move to replace.",
            color=0xffa500
        )
        
        view = MoveReplaceView(ctx.author.id, pokemon_data, pokemon_type, move_name_normalized, trainer_data)
        await ctx.send(embed=embed, view=view)

def calculate_damage(attacker, defender, move_data, type_effectiveness_multiplier):
    """Calculate damage using official Pokemon formula"""
    # Get move data
    move_power = move_data.get('power', 0)
    if move_power == '—' or move_power == 0:
        return 0
    
    move_class = move_data.get('class', 'Physical')
    attacker_level = attacker.get('level', 1)
    
    # Get attacker's attack stat
    if move_class == 'Physical':
        attack_stat = attacker.get('calculated_stats', {}).get('attack', 50)
    else:  # Special
        attack_stat = attacker.get('calculated_stats', {}).get('sp_attack', 50)
    
    # Get defender's defense stat
    if move_class == 'Physical':
        defense_stat = defender.get('calculated_stats', {}).get('defense', 50)
    else:  # Special
        defense_stat = defender.get('calculated_stats', {}).get('sp_defense', 50)
    
    # Official Pokemon damage formula
    level_factor = (2 * attacker_level + 10) / 250
    damage_base = (attack_stat / defense_stat) * move_power * level_factor + 2
    
    # Apply type effectiveness
    damage = damage_base * type_effectiveness_multiplier
    
    # Add random factor (85-100%)
    random_factor = random.uniform(0.85, 1.0)
    final_damage = int(damage * random_factor)
    
    return max(1, final_damage)  # Minimum 1 damage

def is_all_pokemon_fainted(party):
    """Check if all Pokemon in a party are fainted (HP <= 0)"""
    if not party:
        return True
    
    for pokemon in party:
        current_hp = pokemon.get('current_hp', 0)
        # If any Pokemon has HP > 0, the party is not fully fainted
        if current_hp > 0:
            return False
    
    # All Pokemon have HP <= 0
    return True

async def end_battle_with_winner(battle_id, winner_id, winner_name, channel):
    """End battle and send winner message"""
    if battle_id in active_battles:
        del active_battles[battle_id]
    
    # Send winner message (await to ensure proper ordering)
    await channel.send(f"<@{winner_id}> has won")

def check_battle_end_conditions(battle_id, attacker_party, defender_party, attacker_id, defender_id, attacker_name, defender_name, channel):
    """Check if battle should end due to all Pokemon being fainted"""
    messages = []
    
    attacker_fainted = is_all_pokemon_fainted(attacker_party)
    defender_fainted = is_all_pokemon_fainted(defender_party)
    
    # Handle simultaneous double faint - declare attacker as winner (consistent rule)
    if attacker_fainted and defender_fainted:
        messages.append(f"Both trainers' Pokémon have fainted!")
        messages.append(f"In a double knockout, {attacker_name} wins by priority!")
        asyncio.create_task(end_battle_with_winner(battle_id, attacker_id, attacker_name, channel))
        return messages, True
    
    # Check if defender's party is fully fainted
    if defender_fainted:
        messages.append(f"All of {defender_name}'s Pokémon have fainted!")
        asyncio.create_task(end_battle_with_winner(battle_id, attacker_id, attacker_name, channel))
        return messages, True
    
    # Check if attacker's party is fully fainted
    if attacker_fainted:
        messages.append(f"All of {attacker_name}'s Pokémon have fainted!")
        asyncio.create_task(end_battle_with_winner(battle_id, defender_id, defender_name, channel))
        return messages, True
    
    # Battle continues
    return messages, False

def get_move_status_effect(move_name, move_data):
    """Check if move has status effects and determine chance"""
    description = move_data.get('description', '').lower()
    
    # Parse common status effects from descriptions
    if 'paralyze' in description:
        # Extract percentage (e.g., "30% chance to paralyze")
        import re
        match = re.search(r'(\d+)%.*chance.*paralyze', description)
        chance = int(match.group(1)) if match else 30
        return {'type': 'paralysis', 'chance': chance}
    
    elif 'poison' in description:
        match = re.search(r'(\d+)%.*chance.*poison', description)
        chance = int(match.group(1)) if match else 30
        return {'type': 'poison', 'chance': chance}
    
    elif 'burn' in description:
        match = re.search(r'(\d+)%.*chance.*burn', description)
        chance = int(match.group(1)) if match else 10
        return {'type': 'burn', 'chance': chance}
    
    elif 'freeze' in description:
        match = re.search(r'(\d+)%.*chance.*freeze', description)
        chance = int(match.group(1)) if match else 10
        return {'type': 'freeze', 'chance': chance}
    
    return None

def get_move_stat_changes(move_name, move_data):
    """Check if move changes stats"""
    description = move_data.get('description', '').lower()
    
    # Handle specific moves
    if move_name.lower() == 'close-combat':
        return {
            'target': 'user',
            'stats': {'defense': -1, 'sp_defense': -1},
            'message': "Close Combat lowered {pokemon}'s Defense and Special Defense!"
        }
    
    # Parse other stat changes from descriptions
    stat_changes = {}
    
    if 'lowers the user\'s defense' in description and 'special defense' in description:
        return {
            'target': 'user',
            'stats': {'defense': -1, 'sp_defense': -1},
            'message': f"{move_data.get('name', move_name)} lowered {{pokemon}}'s Defense and Special Defense!"
        }
    
    return None

async def execute_battle_move(attacker, defender, move_name, channel, attacker_name, defender_name):
    """Execute a battle move and return battle messages"""
    move_data = get_move_by_name(move_name)
    if not move_data:
        return [f"Move '{move_name}' not found!"]
    
    messages = []
    
    # Move usage message
    move_display_name = move_data.get('name', move_name.replace('-', ' ').title())
    messages.append(f"**{attacker['name'].title()} used {move_display_name}!**")
    
    # Calculate type effectiveness
    attacker_pokemon_data = get_pokemon_by_name(attacker['name'])
    defender_pokemon_data = get_pokemon_by_name(defender['name'])
    
    move_type = move_data.get('type', 'Normal').lower()
    defender_types = defender_pokemon_data.get('types', ['Normal']) if defender_pokemon_data else ['Normal']
    
    type_effectiveness = 1.0
    for def_type in defender_types:
        effectiveness = get_type_effectiveness(move_type, def_type.lower())
        type_effectiveness *= effectiveness
    
    # Calculate damage
    damage = calculate_damage(attacker, defender, move_data, type_effectiveness)
    
    if damage > 0:
        messages.append(f"{move_display_name} dealt {damage} damage!")
        
        # Type effectiveness message
        if type_effectiveness > 1.0:
            messages.append("**It's super effective!**")
        elif type_effectiveness < 1.0 and type_effectiveness > 0:
            messages.append("**It's not very effective!**")
        elif type_effectiveness == 0:
            messages.append("**It had no effect!**")
    
    # Check for status effects
    status_effect = get_move_status_effect(move_name, move_data)
    if status_effect:
        chance_roll = random.randint(1, 100)
        if chance_roll <= status_effect['chance']:
            status_name = status_effect['type'].title()
            messages.append(f"**It inflicted {status_name}!**")
    
    # Check for stat changes
    stat_changes = get_move_stat_changes(move_name, move_data)
    if stat_changes:
        target_pokemon = attacker if stat_changes['target'] == 'user' else defender
        stat_message = stat_changes['message'].format(pokemon=target_pokemon['name'].title())
        messages.append(f"**{stat_message}**")
    
    # Apply HP damage system
    if damage > 0:
        # Calculate max HP if not already available
        max_hp = defender.get('calculated_stats', {}).get('hp', 0)
        if max_hp == 0 and 'base_stats' in defender and 'ivs' in defender:
            calculated_stats = calculate_official_stats(
                defender['base_stats'],
                defender['ivs'],
                defender.get('level', 1),
                defender.get('nature', 'hardy'),
                defender.get('evs', {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
            )
            max_hp = calculated_stats['hp']
            defender['calculated_stats'] = calculated_stats
        
        # Get current HP (if not set, initialize to max HP)
        current_hp = defender.get('current_hp', max_hp)
        
        # Apply damage to current HP
        new_hp = max(0, current_hp - damage)
        defender['current_hp'] = new_hp
        
        # Show HP status after damage (normal text - no bold)
        messages.append(f"{defender['name'].title()} has {new_hp}/{max_hp} HP remaining.")
        
        # Check if defender faints
        if new_hp <= 0:
            messages.append(f"**{defender['name'].title()} has fainted!**")
            # Note: Battle end is now handled by the calling function that checks all Pokemon
    
    # If defender didn't faint, continue battle
    messages.append("")  # Add blank line
    messages.append("The next round will begin in 5 seconds.")
    
    return messages

def create_battle_interface_embed(current_pokemon, party_pokemon, opponent_name=None):
    """Create the battle interface embed"""
    pokemon_name = current_pokemon.get("name", "Unknown").title()
    
    # Create title with waiting status if opponent name is provided
    if opponent_name:
        title = f"Waiting for {opponent_name}... What should {pokemon_name} do?"
    else:
        title = f"**What should {pokemon_name} do?**"
    
    embed = discord.Embed(
        title=title,
        color=0xFFD700
    )
    
    # Available Moves section
    current_moves = current_pokemon.get("current_moves", [])
    moves_text = ""
    type_emojis = {
        'normal': '<:normal_type:1406551478184706068>', 'fire': '<:fire_type:1406552697653559336>', 
        'water': '<:water_type:1406552467319029860>', 'electric': '<:electric_type:1406551930406436935>', 
        'grass': '<:grass_type:1406552601415122945>', 'ice': '<:ice_type:1406553274584399934>', 
        'fighting': '<:fighting_type:1406551764483702906>', 'poison': '<:poison_type:1406555023382413343>', 
        'ground': '<:ground_type:1406552961253117993>', 'flying': '<:flying_type:1406553554897862779>',
        'psychic': '<:psychic_type:1406552310808576122>', 'bug': '<:bug_type:1406555435980427358>', 
        'rock': '<:rock_type:1406552394950512711>', 'ghost': '<:ghost_type:1406553684887998484>', 
        'dragon': '<:dragon_type:1406552069669916742>', 'dark': '<:dark_type:1406553165624774666>', 
        'steel': '<:steel_type:1406552865291501629>', 'fairy': '<:fairy_type:1406552167283691691>'
    }
    
    for move in current_moves:
        if move:
            move_data = get_move_by_name(move)
            move_name = move.replace('-', ' ').title()
            emoji = "<:normal_type:1406551478184706068>"  # Default emoji for moves
            if move_data:
                move_type = move_data.get('type', 'Normal').lower()
                emoji = type_emojis.get(move_type, "<:normal_type:1406551478184706068>")
            moves_text += f"{emoji} {move_name}\n"
    
    if not moves_text:
        moves_text = "No moves learned"
    
    embed.add_field(name="**Available Moves**", value=moves_text, inline=False)
    
    # Available Pokemon section
    pokemon_text = ""
    for pokemon in party_pokemon:
        max_hp = pokemon.get('calculated_stats', {}).get('hp', 0)
        if max_hp == 0 and 'base_stats' in pokemon and 'ivs' in pokemon:
            from stats_iv_calculation import calculate_official_stats
            calculated_stats = calculate_official_stats(
                pokemon['base_stats'],
                pokemon['ivs'],
                pokemon.get('level', 1),
                pokemon.get('nature', 'hardy'),
                pokemon.get('evs', {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
            )
            max_hp = calculated_stats['hp']
        current_hp = pokemon.get('current_hp', max_hp)
        pokemon_text += f"L{pokemon['level']} {pokemon['iv_percentage']}% {pokemon['name'].title()}{pokemon['gender']} (#{pokemon.get('order', 'N/A')})\n"
    
    embed.add_field(name="**Available Pokémons**", value=pokemon_text, inline=False)
    
    # Commands help
    embed.add_field(
        name="",
        value="You can also use `@Pokékiro use move <move-name> | switch <order_number> | flee | pass`",
        inline=False
    )
    
    return embed

class BattleInterfaceView(View):
    def __init__(self, user_id: int, battle_id: str, user_pokemon: dict, user_party: list, channel=None):
        super().__init__(timeout=1800)
        self.user_id = user_id
        self.battle_id = battle_id
        self.user_pokemon = user_pokemon
        self.user_party = user_party
        self.channel = channel
        
        # Add move selection dropdown
        move_options = []
        current_moves = user_pokemon.get("current_moves", [])
        
        # Get move emojis for types
        type_emojis = {
            'normal': '<:normal_type:1406551478184706068>', 'fire': '<:fire_type:1406552697653559336>', 
            'water': '<:water_type:1406552467319029860>', 'electric': '<:electric_type:1406551930406436935>', 
            'grass': '<:grass_type:1406552601415122945>', 'ice': '<:ice_type:1406553274584399934>', 
            'fighting': '<:fighting_type:1406551764483702906>', 'poison': '<:poison_type:1406555023382413343>', 
            'ground': '<:ground_type:1406552961253117993>', 'flying': '<:flying_type:1406553554897862779>',
            'psychic': '<:psychic_type:1406552310808576122>', 'bug': '<:bug_type:1406555435980427358>', 
            'rock': '<:rock_type:1406552394950512711>', 'ghost': '<:ghost_type:1406553684887998484>', 
            'dragon': '<:dragon_type:1406552069669916742>', 'dark': '<:dark_type:1406553165624774666>', 
            'steel': '<:steel_type:1406552865291501629>', 'fairy': '<:fairy_type:1406552167283691691>'
        }
        
        for i, move in enumerate(current_moves):
            if move:
                move_data = get_move_by_name(move)
                move_name = move.replace('-', ' ').title()
                emoji = '⚔️'
                if move_data:
                    move_type = move_data.get('type', 'Normal').lower()
                    emoji = type_emojis.get(move_type, '⚔️')
                
                move_options.append(discord.SelectOption(
                    label=move_name,
                    value=move,
                    emoji=emoji,
                    description=f"Slot {i+1}"
                ))
        
        if not move_options:
            move_options.append(discord.SelectOption(
                label="No moves learned",
                value="none",
                description="This Pokemon hasn't learned any moves yet"
            ))
        
        self.move_select.options = move_options
        
        # Add Pokemon switch dropdown
        switch_options = []
        for pokemon in user_party:
            if pokemon.get("current_hp", 0) > 0:  # Only show Pokemon that can battle
                switch_options.append(discord.SelectOption(
                    label=f"Lvl.{pokemon['level']} {pokemon['iv_percentage']}% {pokemon['name'].title()}",
                    value=str(pokemon.get('order', 0)),
                    description=f"#{pokemon.get('order', 'N/A')}"
                ))
        
        if switch_options:
            self.pokemon_switch.options = switch_options
        else:
            self.pokemon_switch.disabled = True

    async def send_immediate_switch_activity(self, battle_data, challenger_name, target_name):
        """Send immediate activity for Pokemon switches"""
        activities = battle_data.get('battle_activities', [])
        
        # Get only unnotified switch activities from this round
        switch_activities = [activity for activity in activities if activity.get('type') == 'switch' and not activity.get('notified', False)]
        
        if not switch_activities:
            return
        
        # Send immediate notification for each switch that hasn't been notified
        for switch_activity in switch_activities:
            # Create the embed for immediate switch notification (no "next round" message)
            embed = discord.Embed(
                title=f"Battle between {challenger_name} and {target_name}",
                description=switch_activity['message'],
                color=0xFFD700  # Gold color
            )
            
            # Send to channel
            await self.channel.send(embed=embed)
            
            # Mark this switch as notified to prevent duplicate messages
            switch_activity['notified'] = True
        
        # Don't clear activities - keep them for combining with subsequent actions

    async def send_battle_activity_embed(self, battle_data, challenger_name, target_name, clear_activities=True):
        """Send an embed showing all recent battle activities"""
        activities = battle_data.get('battle_activities', [])
        
        if not activities:
            return
        
        # Get the latest activity messages
        activity_messages = []
        for activity in activities[-5:]:  # Show last 5 activities
            activity_messages.append(activity['message'])
        
        # Create the embed
        embed = discord.Embed(
            title=f"Battle between {challenger_name} and {target_name}",
            description="\n\n".join(activity_messages) + "\n\nNext round will begin in 5 seconds.",
            color=0xFFD700  # Gold color
        )
        
        # Send to channel
        await self.channel.send(embed=embed)
        
        # Clear activities after sending (unless specified not to)
        if clear_activities:
            battle_data['battle_activities'] = []

    async def edit_battle_interfaces_after_switch(self, battle_data, challenger_id, target_id, challenger_name, target_name):
        """Edit existing battle interface messages after a Pokemon switch"""
        try:
            print(f"[DEBUG] Editing battle interfaces after switch")
            
            # Get the current active Pokemon for each player from battle_data
            challenger_pokemon = battle_data.get('challenger_pokemon')
            target_pokemon = battle_data.get('target_pokemon')
            
            if not challenger_pokemon or not target_pokemon:
                print(f"[DEBUG] Missing active Pokemon data: challenger={bool(challenger_pokemon)}, target={bool(target_pokemon)}")
                return
            
            print(f"[DEBUG] Active Pokemon: challenger={challenger_pokemon.get('name')}, target={target_pokemon.get('name')}")
            
            # Get stored message IDs (handle both int and string keys)
            dm_messages = battle_data.get('dm_messages', {})
            if not dm_messages:
                print(f"[DEBUG] No stored DM message IDs found, cannot edit interfaces")
                return
                
            # Get the full party data
            challenger_party = battle_data.get('challenger_party', [])
            target_party = battle_data.get('target_party', [])
            
            # Regenerate battlefield images with the switched Pokemon
            print(f"[DEBUG] Regenerating battlefield images for switch")
            challenger_image_buffer = create_animated_battle_field(
                challenger_pokemon.get('name', 'Unknown'), 
                target_pokemon.get('name', 'Unknown'), 
                challenger_id, 
                battle_data
            )
            target_image_buffer = create_animated_battle_field(
                target_pokemon.get('name', 'Unknown'),
                challenger_pokemon.get('name', 'Unknown'),
                target_id,
                battle_data
            )
            
            # Create updated interfaces for both players with current active Pokemon
            challenger_embed = create_battle_interface_embed(challenger_pokemon, challenger_party, target_name)
            target_embed = create_battle_interface_embed(target_pokemon, target_party, challenger_name)
            
            # Create new views with updated Pokemon data
            challenger_view = BattleInterfaceView(challenger_id, self.battle_id, challenger_pokemon, challenger_party, self.channel)
            target_view = BattleInterfaceView(target_id, self.battle_id, target_pokemon, target_party, self.channel)
            
            # Send updated battle overview to channel
            try:
                # Create battle overview embed showing both players' teams
                overview_embed = discord.Embed(
                    title=f"Battle between {challenger_name} and {target_name}",
                    description="Choose your moves using the interface below. After both players have chosen, the move will be executed.",
                    color=0xFFD700
                )
                
                # Add challenger's team
                challenger_team_text = ""
                for i, pokemon in enumerate(challenger_party, 1):
                    # Use correct HP calculation from original code
                    max_hp = pokemon.get('calculated_stats', {}).get('hp', 0)
                    if max_hp == 0 and 'base_stats' in pokemon and 'ivs' in pokemon:
                        from stats_iv_calculation import calculate_official_stats
                        calculated_stats = calculate_official_stats(
                            pokemon['base_stats'],
                            pokemon['ivs'],
                            pokemon.get('level', 1),
                            pokemon.get('nature', 'hardy'),
                            pokemon.get('evs', {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
                        )
                        max_hp = calculated_stats['hp']
                    current_hp = pokemon.get('current_hp', max_hp)
                    
                    iv_total = sum([pokemon.get('ivs', {}).get(stat, 0) for stat in ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']])
                    iv_percentage = round((iv_total / 186) * 100, 2)
                    gender_symbol = convert_text_gender_to_emoji(pokemon.get('gender', 'unknown'))
                    challenger_team_text += f"L{pokemon.get('level', 1)} {iv_percentage}% {pokemon.get('name', 'Unknown').title()}{gender_symbol} (#{i}) • {current_hp}/{max_hp} HP\n"
                
                overview_embed.add_field(
                    name=challenger_name, 
                    value=challenger_team_text.strip() or "No Pokemon", 
                    inline=False
                )
                
                # Add target's team
                target_team_text = ""
                for i, pokemon in enumerate(target_party, 1):
                    # Use correct HP calculation from original code
                    max_hp = pokemon.get('calculated_stats', {}).get('hp', 0)
                    if max_hp == 0 and 'base_stats' in pokemon and 'ivs' in pokemon:
                        from stats_iv_calculation import calculate_official_stats
                        calculated_stats = calculate_official_stats(
                            pokemon['base_stats'],
                            pokemon['ivs'],
                            pokemon.get('level', 1),
                            pokemon.get('nature', 'hardy'),
                            pokemon.get('evs', {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
                        )
                        max_hp = calculated_stats['hp']
                    current_hp = pokemon.get('current_hp', max_hp)
                    
                    iv_total = sum([pokemon.get('ivs', {}).get(stat, 0) for stat in ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']])
                    iv_percentage = round((iv_total / 186) * 100, 2)
                    gender_symbol = convert_text_gender_to_emoji(pokemon.get('gender', 'unknown'))
                    target_team_text += f"L{pokemon.get('level', 1)} {iv_percentage}% {pokemon.get('name', 'Unknown').title()}{gender_symbol} (#{i}) • {current_hp}/{max_hp} HP\n"
                
                overview_embed.add_field(
                    name=target_name, 
                    value=target_team_text.strip() or "No Pokemon", 
                    inline=False
                )
                
                # Create battlefield image for the overview using challenger's perspective
                if challenger_image_buffer:
                    import time
                    timestamp = int(time.time())
                    
                    challenger_image_buffer.seek(0)
                    header = challenger_image_buffer.read(4)
                    challenger_image_buffer.seek(0)
                    
                    if header.startswith(b'GIF8'):
                        extension = "gif"
                    else:
                        extension = "png"
                    
                    filename = f"battle_overview_{timestamp}.{extension}"
                    file = discord.File(challenger_image_buffer, filename=filename)
                    overview_embed.set_image(url=f"attachment://{filename}")
                    
                    # Send the overview to channel
                    await self.channel.send(embed=overview_embed, file=file)
                    print(f'[DEBUG] Sent battle overview to channel after Pokemon switch')
                
            except Exception as e:
                print(f'[DEBUG] Error sending battle overview to channel: {e}')
                
        except Exception as e:
            print(f"[DEBUG] Error editing battle interfaces: {e}")

    async def send_switch_waiting_embed(self, battle_data, switching_player, opponent_name, pokemon_name):
        """Send gold embed notification about switch waiting to both players"""
        try:
            # Create gold embed for switch notification
            embed = discord.Embed(
                title="🔄 Pokémon Switch Initiated!",
                description=f"**{switching_player}** is switching to **{pokemon_name}**!\n\n**{opponent_name}** has 20 seconds to respond:",
                color=0xFFD700  # Gold color
            )
            embed.add_field(
                name="Response Options",
                value="• Switch your Pokémon\n• Use a move\n• Pass your turn",
                inline=False
            )
            embed.add_field(
                name="⏰ Timer",
                value="20 seconds remaining",
                inline=False
            )
            
            # Send to channel for visibility
            await self.channel.send(embed=embed)
            
        except Exception as e:
            print(f"Error sending switch waiting embed: {e}")

    async def handle_switch_timer(self, battle_data, switching_player, opponent_name, opponent_id):
        """Handle the 20-second timer for opponent response to switch"""
        try:
            start_time = battle_data.get('switch_timer_start', time.time())
            timeout_duration = 20  # 20 seconds
            
            # Wait for the timeout duration or until opponent responds
            while True:
                elapsed = time.time() - start_time
                remaining = timeout_duration - elapsed
                
                # Check if opponent has responded
                if battle_data.get('opponent_response') is not None:
                    await self.resolve_switch_response(battle_data, switching_player, opponent_name)
                    return
                
                # Check if time is up
                if remaining <= 0:
                    await self.handle_switch_timeout(battle_data, switching_player, opponent_name)
                    return
                
                # Wait a bit before checking again
                await asyncio.sleep(1)
                
        except Exception as e:
            print(f"Error in switch timer: {e}")

    async def handle_switch_timeout(self, battle_data, switching_player, opponent_name):
        """Handle when opponent doesn't respond within 20 seconds"""
        try:
            # Get Pokemon name from battle data
            switching_pokemon_name = battle_data.get('switch_pokemon_name', 'Unknown')
            
            # Create the battle description for timeout scenario (only first player switched)
            battle_title = f"Battle between {switching_player} and {opponent_name}"
            description = f"{battle_title}\n\n"
            description += f"**{switching_player} switched pokémon!**\n"
            description += f"{switching_pokemon_name} is now on the field!\n\n"
            description += "Next round will begin in 5 seconds."
            
            embed = discord.Embed(
                description=description,
                color=0xFFD700
            )
            
            # Complete the switch
            await self.complete_switch(battle_data, switching_player, "timeout")
            
            # Send timeout message
            await self.channel.send(embed=embed)
            
            # Wait 5 seconds before continuing
            await asyncio.sleep(5)
            
        except Exception as e:
            print(f"Error handling switch timeout: {e}")

    async def resolve_switch_response(self, battle_data, switching_player, opponent_name):
        """Resolve the opponent's response to the switch"""
        try:
            response = battle_data.get('opponent_response')
            
            # Get Pokemon names from battle data
            switching_pokemon_name = battle_data.get('switch_pokemon_name', 'Unknown')
            opponent_pokemon_name = battle_data.get('opponent_switch_pokemon_name', 'Unknown')
            
            # Create the battle description
            battle_title = f"Battle between {switching_player} and {opponent_name}"
            
            if response == 'switch':
                # Both players switched - create formatted message
                description = f"{battle_title}\n\n"
                description += f"**{switching_player} switched pokémon!**\n"
                description += f"{switching_pokemon_name} is now on the field!\n"
                description += f"**{opponent_name} switched pokémon!**\n"
                description += f"{opponent_pokemon_name} is now on the field!\n\n"
                description += "Next round will begin in 5 seconds."
                
                embed = discord.Embed(
                    description=description,
                    color=0xFFD700
                )
            elif response == 'move':
                # Opponent used a move - create formatted message
                move_name = battle_data.get('opponent_move', 'a move')
                
                # Get opponent's active Pokemon name
                challenger_id = battle_data.get('challenger_id')
                target_id = battle_data.get('target_id')
                
                # Determine which player used the move and get their Pokemon
                if battle_data.get('switch_initiator') == challenger_id:
                    # Challenger switched, target used move
                    opponent_pokemon = battle_data.get('target_pokemon', {})
                else:
                    # Target switched, challenger used move
                    opponent_pokemon = battle_data.get('challenger_pokemon', {})
                
                opponent_pokemon_name = opponent_pokemon.get('name', 'Unknown').title()
                
                # Calculate basic damage (placeholder for now)
                damage = 10.0  # Basic damage for demonstration
                
                description = f"{battle_title}\n\n"
                description += f"**{switching_player} switched pokémon!**\n"
                description += f"{switching_pokemon_name} is now on the field!\n"
                description += f"**{opponent_pokemon_name} used {move_name}!**\n"
                description += f"{move_name} dealt {damage} damage!\n\n"
                description += "Next round will begin in 5 seconds."
                
                embed = discord.Embed(
                    description=description,
                    color=0xFFD700
                )
            else:  # pass response (not timeout)
                # Get the opponent name for the pass message
                challenger_id = battle_data.get('challenger_id')
                target_id = battle_data.get('target_id')
                challenger_name = battle_data.get('challenger_name', 'Player 1')
                target_name = battle_data.get('target_name', 'Player 2')
                
                # Determine who passed
                switch_initiator = battle_data.get('switch_initiator')
                passing_player = target_name if switch_initiator == challenger_id else challenger_name
                
                # Create formatted message with both switch and pass
                description = f"**Battle between {switching_player} and {passing_player}**\n\n"
                description += f"**{switching_player} switched pokémon!**\n"
                description += f"{switching_pokemon_name} is now on the field!\n"
                description += f"**{passing_player} passed their turn!**\n\n"
                description += "Next round will begin in 5 seconds."
                
                embed = discord.Embed(
                    description=description,
                    color=0xFFD700
                )
            
            # Complete the switch with response
            await self.complete_switch(battle_data, switching_player, response)
            
            # Send resolution message
            await self.channel.send(embed=embed)
            
            # Wait 5 seconds before continuing for all switch scenarios
            if response in ['switch', 'pass', 'move']:
                await asyncio.sleep(5)
            
        except Exception as e:
            print(f"Error resolving switch response: {e}")

    async def complete_switch(self, battle_data, switching_player, opponent_response):
        """Complete the switch process and update battle state"""
        try:
            # Get player info
            challenger_id = battle_data.get('challenger_id')
            target_id = battle_data.get('target_id')
            challenger_name = battle_data.get('challenger_name', 'Player 1')
            target_name = battle_data.get('target_name', 'Player 2')
            
            # Record the switch activity
            pokemon_name = battle_data.get('switch_pokemon_name', 'Unknown')
            
            if 'battle_activities' not in battle_data:
                battle_data['battle_activities'] = []
            
            battle_data['battle_activities'].append({
                'type': 'switch',
                'player_name': switching_player,
                'pokemon_name': pokemon_name,
                'message': f"**{switching_player} switched to {pokemon_name}!**"
            })
            
            # Reset battle phase
            battle_data['battle_phase'] = 'normal'
            battle_data.pop('switch_initiator', None)
            battle_data.pop('switch_pokemon_name', None)
            battle_data.pop('switch_timer_start', None)
            battle_data.pop('opponent_response', None)
            battle_data.pop('opponent_move', None)
            
            # Update battle interfaces for both players
            await self.edit_battle_interfaces_after_switch(battle_data, challenger_id, target_id, challenger_name, target_name)
            
        except Exception as e:
            print(f"Error completing switch: {e}")

    @discord.ui.select(placeholder="Use a Move", min_values=1, max_values=1, row=0)
    async def move_select(self, interaction: discord.Interaction, select):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your battle!", ephemeral=True)
            return
        
        if select.values[0] == "none":
            await interaction.response.send_message("❌ This Pokemon hasn't learned any moves yet!", ephemeral=True)
            return
            
        move_name = select.values[0]
        
        # Get battle data
        battle_data = active_battles.get(self.battle_id, {})
        if not battle_data:
            await interaction.response.send_message("❌ Battle data not found!", ephemeral=True)
            return
        
        # Check if we're in switch waiting phase
        if battle_data.get('battle_phase') == 'switch_waiting':
            # Check if this user is the opponent who should respond
            switch_initiator = battle_data.get('switch_initiator')
            if self.user_id != switch_initiator:
                # This is the opponent responding with a move
                battle_data['opponent_response'] = 'move'
                battle_data['opponent_move'] = move_name.replace('-', ' ').title()
                await interaction.response.send_message(f"✅ You used {move_name.replace('-', ' ').title()} in response to opponent's switch!", ephemeral=True)
                return
            else:
                await interaction.response.send_message("❌ You are currently switching! Wait for opponent response.", ephemeral=True)
                return
        
        # Normal move selection logic
        # Initialize pending moves if not exists
        if 'pending_moves' not in battle_data:
            battle_data['pending_moves'] = {}
        
        # Store the selected move for this user
        battle_data['pending_moves'][self.user_id] = move_name
        
        challenger_id = battle_data.get('challenger_id')
        target_id = battle_data.get('target_id')
        challenger_name = battle_data.get('challenger_name', 'Player 1')
        target_name = battle_data.get('target_name', 'Player 2')
        
        # Check if both players have selected moves
        if challenger_id in battle_data['pending_moves'] and target_id in battle_data['pending_moves']:
            # Both players have selected moves - execute simultaneously
            await self.execute_simultaneous_moves(battle_data, challenger_name, target_name)
            await interaction.response.send_message(f"✅ You used {move_name.replace('-', ' ').title()}! Both moves executed!", ephemeral=True)
        else:
            # Only one player has selected - set up timer for other player
            await interaction.response.send_message(f"✅ You selected {move_name.replace('-', ' ').title()}! Waiting for opponent...", ephemeral=True)
            
            # Disable UI for the player who just selected
            self.disable_all_components()
            
            # Set up timer task for timeout
            battle_data['timer_start'] = time.time()
            
            # Start background timer task if not already running
            if 'timer_task' not in battle_data or battle_data['timer_task'].done():
                battle_data['timer_task'] = asyncio.create_task(
                    self.handle_move_timeout(battle_data, challenger_name, target_name, challenger_id, target_id)
                )

    def disable_all_components(self):
        """Disable all UI components but keep them visible"""
        self.move_select.disabled = True
        self.pokemon_switch.disabled = True
        for child in self.children:
            if hasattr(child, 'disabled'):
                child.disabled = True

    def enable_all_components(self):
        """Re-enable all UI components"""
        self.move_select.disabled = False
        self.pokemon_switch.disabled = False
        for child in self.children:
            if hasattr(child, 'disabled'):
                child.disabled = False

    async def handle_move_timeout(self, battle_data, challenger_name, target_name, challenger_id, target_id):
        """Handle the 20-second timeout for move selection"""
        start_time = battle_data.get('timer_start', time.time())
        
        # Wait for 20 seconds or until both players have selected
        while True:
            await asyncio.sleep(1)  # Check every second
            
            # Check if both players have selected moves
            if challenger_id in battle_data['pending_moves'] and target_id in battle_data['pending_moves']:
                # Both players selected - execute moves
                await self.execute_simultaneous_moves(battle_data, challenger_name, target_name)
                self.enable_all_components()
                return
            
            # Check if 20 seconds have passed
            if time.time() - start_time >= 20:
                # Timeout reached - determine who didn't select and execute moves
                if challenger_id not in battle_data['pending_moves']:
                    # Challenger didn't select - set to pass
                    battle_data['pending_moves'][challenger_id] = "pass"
                elif target_id not in battle_data['pending_moves']:
                    # Target didn't select - set to pass
                    battle_data['pending_moves'][target_id] = "pass"
                
                # Now execute both moves (one real, one pass) using the unified system
                await self.execute_simultaneous_moves(battle_data, challenger_name, target_name)
                self.enable_all_components()
                return

    async def execute_simultaneous_moves(self, battle_data, challenger_name, target_name):
        """Execute both players' moves simultaneously and combine with any existing activities"""
        challenger_id = battle_data.get('challenger_id')
        target_id = battle_data.get('target_id')
        challenger_move = battle_data['pending_moves'][challenger_id]
        target_move = battle_data['pending_moves'][target_id]
        
        challenger_party = battle_data.get('challenger_party', [])
        target_party = battle_data.get('target_party', [])
        
        challenger_pokemon = challenger_party[0] if challenger_party else None
        target_pokemon = target_party[0] if target_party else None
        
        if challenger_pokemon and target_pokemon:
            # Initialize battle activities if not exists
            if 'battle_activities' not in battle_data:
                battle_data['battle_activities'] = []
            
            # Record move/pass activities
            if challenger_move == "pass":
                battle_data['battle_activities'].append({
                    'type': 'pass',
                    'player_name': challenger_name,
                    'message': f"**{challenger_name} did nothing.**"
                })
            else:
                # Execute challenger's move and record activity
                challenger_messages = await execute_battle_move(
                    challenger_pokemon, target_pokemon, challenger_move, self.channel,
                    challenger_pokemon.get('name', 'Unknown'), target_pokemon.get('name', 'Unknown')
                )
                # Convert move messages to battle activity format
                move_display_name = challenger_move.replace('-', ' ').title()
                battle_data['battle_activities'].append({
                    'type': 'move',
                    'player_name': challenger_name,
                    'pokemon_name': challenger_pokemon.get('name', 'Unknown'),
                    'move_name': move_display_name,
                    'message': "\n".join(challenger_messages[:-2])  # Remove blank line and "next round"
                })
            
            if target_move == "pass":
                battle_data['battle_activities'].append({
                    'type': 'pass',
                    'player_name': target_name,
                    'message': f"**{target_name} did nothing.**"
                })
            else:
                # Execute target's move and record activity
                target_messages = await execute_battle_move(
                    target_pokemon, challenger_pokemon, target_move, self.channel,
                    target_pokemon.get('name', 'Unknown'), challenger_pokemon.get('name', 'Unknown')
                )
                # Convert move messages to battle activity format
                move_display_name = target_move.replace('-', ' ').title()
                battle_data['battle_activities'].append({
                    'type': 'move',
                    'player_name': target_name,
                    'pokemon_name': target_pokemon.get('name', 'Unknown'),
                    'move_name': move_display_name,
                    'message': "\n".join(target_messages[:-2])  # Remove blank line and "next round"
                })
            
            # Check if battle should end due to all Pokemon being fainted
            challenger_party = battle_data.get('challenger_party', [])
            target_party = battle_data.get('target_party', [])
            challenger_id = battle_data.get('challenger_id')
            target_id = battle_data.get('target_id')
            
            end_messages, battle_ended = check_battle_end_conditions(
                self.battle_id, challenger_party, target_party, 
                challenger_id, target_id, challenger_name, target_name, self.channel
            )
            
            if battle_ended:
                # Add end messages to battle activities
                for msg in end_messages:
                    battle_data['battle_activities'].append({
                        'type': 'battle_end',
                        'message': msg
                    })
            
            # Send combined battle activity embed (includes switches + moves/passes)
            await self.send_battle_activity_embed(battle_data, challenger_name, target_name, clear_activities=True)
            
            if not battle_ended:
                # Clear pending moves for next round only if battle continues
                battle_data['pending_moves'] = {}
            else:
                # Battle ended - disable UI components
                self.disable_all_components()

    @discord.ui.select(placeholder="Switch Pokémon", min_values=1, max_values=1, row=1)
    async def pokemon_switch(self, interaction: discord.Interaction, select):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your battle!", ephemeral=True)
            return
        
        # Immediately defer the interaction to prevent timeout
        await interaction.response.defer(ephemeral=True)
        
        try:
            order_number = int(select.values[0])
            
            # Get battle data
            battle_data = active_battles.get(self.battle_id, {})
            if not battle_data:
                await interaction.followup.send("❌ Battle data not found!", ephemeral=True)
                return
            
            # Find the Pokemon to switch to by order number first
            new_pokemon_wrapper = None
            print(f"[DEBUG] User {self.user_id} switching to order {order_number}")
            print(f"[DEBUG] Available party: {[{'order': p.get('order'), 'name': p.get('name')} for p in self.user_party]}")
            
            for pokemon in self.user_party:
                if pokemon.get('order') == order_number:
                    new_pokemon_wrapper = pokemon
                    break
            
            if not new_pokemon_wrapper:
                print(f"[DEBUG] Pokemon with order {order_number} not found in party")
                await interaction.followup.send("❌ Pokemon not found!", ephemeral=True)
                return
            
            print(f"[DEBUG] Selected Pokemon: {new_pokemon_wrapper.get('name')} (order {new_pokemon_wrapper.get('order')})")
            
            # Get the actual Pokemon data from the wrapper
            new_pokemon_data = new_pokemon_wrapper.get('data', new_pokemon_wrapper)
            
            # Check if Pokemon is fainted (HP should be in the data field)
            current_hp = new_pokemon_data.get('current_hp', new_pokemon_data.get('calculated_stats', {}).get('hp', 100))
            if current_hp <= 0:
                await interaction.followup.send("❌ Cannot switch to a fainted Pokemon!", ephemeral=True)
                return
            
            # Check if we're already in a switch waiting phase
            if battle_data.get('battle_phase') == 'switch_waiting':
                # Check if this user is the opponent who should respond to the switch
                switch_initiator = battle_data.get('switch_initiator')
                if self.user_id != switch_initiator:
                    # This is the opponent responding with a switch
                    battle_data['opponent_response'] = 'switch'
                    battle_data['opponent_switch_pokemon_name'] = new_pokemon_wrapper['name'].title()
                    
                    # Update the active Pokemon for the opponent
                    challenger_id = battle_data.get('challenger_id')
                    target_id = battle_data.get('target_id')
                    
                    if self.user_id == challenger_id:
                        battle_data['challenger_pokemon'] = new_pokemon_wrapper
                    else:
                        battle_data['target_pokemon'] = new_pokemon_wrapper
                    
                    # Update the user_pokemon for this interface
                    self.user_pokemon = new_pokemon_wrapper
                    
                    await interaction.followup.send(f"✅ You switched to {new_pokemon_wrapper['name'].title()} in response to opponent's switch!", ephemeral=True)
                    return
                else:
                    await interaction.followup.send("❌ You are currently switching! Wait for opponent response.", ephemeral=True)
                    return
            
            # Update the battle data with the new active Pokemon
            challenger_id = battle_data.get('challenger_id')
            target_id = battle_data.get('target_id')
            challenger_name = battle_data.get('challenger_name', 'Player 1')
            target_name = battle_data.get('target_name', 'Player 2')
            
            # Determine which player is switching and the opponent
            if self.user_id == challenger_id:
                battle_data['challenger_pokemon'] = new_pokemon_wrapper
                switching_player = challenger_name
                opponent_id = target_id
                opponent_name = target_name
            else:
                battle_data['target_pokemon'] = new_pokemon_wrapper
                switching_player = target_name
                opponent_id = challenger_id
                opponent_name = challenger_name
            
            # Update the user_pokemon for this interface
            self.user_pokemon = new_pokemon_wrapper
            
            # Initialize battle activities if not exists
            if 'battle_activities' not in battle_data:
                battle_data['battle_activities'] = []
            
            # Check if opponent already has a pending move - if so, execute together
            if 'pending_moves' in battle_data and opponent_id in battle_data['pending_moves']:
                # Opponent already selected a move - execute both actions together
                opponent_move = battle_data['pending_moves'][opponent_id]
                
                # Record switch activity
                battle_data['battle_activities'].append({
                    'type': 'switch',
                    'player_name': switching_player,
                    'pokemon_name': new_pokemon_wrapper['name'].title(),
                    'message': f"**{switching_player}** switched to {new_pokemon_wrapper['name'].title()}!"
                })
                
                # Execute opponent's move if it's not "pass"
                if opponent_move != "pass":
                    # Get opponent's Pokemon
                    opponent_pokemon = battle_data.get('challenger_pokemon') if opponent_id == challenger_id else battle_data.get('target_pokemon')
                    if opponent_pokemon:
                        opponent_messages = await execute_battle_move(
                            opponent_pokemon, new_pokemon_wrapper, opponent_move, self.channel,
                            opponent_pokemon.get('name', 'Unknown'), new_pokemon_wrapper.get('name', 'Unknown')
                        )
                        move_display_name = opponent_move.replace('-', ' ').title()
                        battle_data['battle_activities'].append({
                            'type': 'move',
                            'player_name': opponent_name,
                            'pokemon_name': opponent_pokemon.get('name', 'Unknown'),
                            'move_name': move_display_name,
                            'message': "\n".join(opponent_messages[:-2])  # Remove blank line and "next round"
                        })
                else:
                    # Opponent passed
                    battle_data['battle_activities'].append({
                        'type': 'pass',
                        'player_name': opponent_name,
                        'message': f"**{opponent_name}** did nothing!"
                    })
                
                # Check if battle should end due to all Pokemon being fainted
                challenger_party = battle_data.get('challenger_party', [])
                target_party = battle_data.get('target_party', [])
                challenger_id = battle_data.get('challenger_id')
                target_id = battle_data.get('target_id')
                
                end_messages, battle_ended = check_battle_end_conditions(
                    self.battle_id, challenger_party, target_party, 
                    challenger_id, target_id, challenger_name, target_name, self.channel
                )
                
                if battle_ended:
                    # Add end messages to battle activities
                    for msg in end_messages:
                        battle_data['battle_activities'].append({
                            'type': 'battle_end',
                            'message': msg
                        })
                
                # Send combined battle activity embed
                await self.send_battle_activity_embed(battle_data, challenger_name, target_name, clear_activities=True)
                
                if battle_ended:
                    # Battle ended - disable UI components and return early
                    self.disable_all_components()
                    await interaction.followup.send(f"✅ Battle ended!", ephemeral=True)
                    return
                
                # Clear pending moves for next round only if battle continues
                battle_data['pending_moves'] = {}
                
                # Reset battle phase
                battle_data['battle_phase'] = 'normal'
                
                await interaction.followup.send(f"✅ Switched to {new_pokemon_wrapper['name'].title()}! Both actions executed!", ephemeral=True)
                
            else:
                # No pending moves - enter switch waiting phase
                battle_data['battle_phase'] = 'switch_waiting'
                battle_data['switch_initiator'] = self.user_id
                battle_data['switch_pokemon_name'] = new_pokemon_wrapper['name'].title()
                battle_data['switch_timer_start'] = time.time()
                battle_data['opponent_response'] = None
                
                # Start the 20-second timer
                asyncio.create_task(self.handle_switch_timer(battle_data, switching_player, opponent_name, opponent_id))
                
                # Send confirmation to user
                await interaction.followup.send(f"✅ Switching to {new_pokemon_wrapper['name'].title()}! Waiting for opponent response...", ephemeral=True)
            
        except Exception as e:
            print(f"Error in pokemon_switch: {e}")
            try:
                await interaction.followup.send("❌ An error occurred while switching Pokemon.", ephemeral=True)
            except:
                pass

    @discord.ui.button(label="Flee", style=discord.ButtonStyle.danger, row=2)
    async def flee_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your battle!", ephemeral=True)
            return
        
        # Get battle data to find the opponent
        battle_data = active_battles.get(self.battle_id, {})
        challenger_id = battle_data.get('challenger_id')
        target_id = battle_data.get('target_id')
        challenger_name = battle_data.get('challenger_name', 'Player 1')
        target_name = battle_data.get('target_name', 'Player 2')
        
        # Determine who fled and who won
        if self.user_id == challenger_id:
            fled_user = challenger_name
            winner_id = target_id
            winner_name = target_name
        else:
            fled_user = target_name
            winner_id = challenger_id
            winner_name = challenger_name
        
        # Send flee message to channel as normal message
        flee_message = f"<@{self.user_id}> has fled the battle! <@{winner_id}> has won."
        await self.channel.send(flee_message)
        
        # Properly end the battle using the battle end system
        asyncio.create_task(end_battle_with_winner(self.battle_id, winner_id, winner_name, self.channel))
        
        # Disable all components to stop the battle UI
        self.disable_all_components()
        
        await interaction.response.send_message("✅ You fled from the battle!", ephemeral=True)

    @discord.ui.button(label="Pass", style=discord.ButtonStyle.secondary, row=2)
    async def pass_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your battle!", ephemeral=True)
            return
        
        # Get battle data
        battle_data = active_battles.get(self.battle_id, {})
        if not battle_data:
            await interaction.response.send_message("❌ Battle data not found!", ephemeral=True)
            return
        
        # Check if we're in a switch waiting phase
        if battle_data.get('battle_phase') == 'switch_waiting':
            # Check if this user is the opponent who should respond to the switch
            switch_initiator = battle_data.get('switch_initiator')
            if self.user_id != switch_initiator:
                # This is the opponent responding with a pass
                battle_data['opponent_response'] = 'pass'
                
                challenger_id = battle_data.get('challenger_id')
                target_id = battle_data.get('target_id')
                challenger_name = battle_data.get('challenger_name', 'Player 1')
                target_name = battle_data.get('target_name', 'Player 2')
                
                # Get the names for the battle message
                switching_player = challenger_name if switch_initiator == challenger_id else target_name
                passing_player = target_name if switch_initiator == challenger_id else challenger_name
                
                await interaction.response.send_message(f"✅ You passed your turn! {switching_player} switched and you passed.", ephemeral=True)
                return
            else:
                await interaction.response.send_message("❌ You are currently switching! Wait for opponent response.", ephemeral=True)
                return
        
        # Normal pass flow when not in switch waiting phase
        # Initialize pending moves if not exists
        if 'pending_moves' not in battle_data:
            battle_data['pending_moves'] = {}
        
        # Store the pass action for this user
        battle_data['pending_moves'][self.user_id] = "pass"
        
        challenger_id = battle_data.get('challenger_id')
        target_id = battle_data.get('target_id')
        challenger_name = battle_data.get('challenger_name', 'Player 1')
        target_name = battle_data.get('target_name', 'Player 2')
        
        # Initialize battle activities if not exists
        if 'battle_activities' not in battle_data:
            battle_data['battle_activities'] = []
        
        # Record the pass activity
        player_name = challenger_name if self.user_id == challenger_id else target_name
        battle_data['battle_activities'].append({
            'type': 'pass',
            'player_name': player_name,
            'message': f"**{player_name}** did nothing!"
        })
        
        # Check if both players have made their choices
        if challenger_id in battle_data['pending_moves'] and target_id in battle_data['pending_moves']:
            # Both players have made choices - send activity embed
            await self.send_battle_activity_embed(battle_data, challenger_name, target_name)
            
            # Clear pending moves for next round
            battle_data['pending_moves'] = {}
            
            await interaction.response.send_message("✅ You passed your turn! Battle result executed!", ephemeral=True)
        else:
            # Only one player has made a choice - wait for the other
            await interaction.response.send_message("✅ You passed your turn! Waiting for opponent...", ephemeral=True)

async def send_battle_interface_to_players(battle_id, challenger_id, target_id, challenger_party, target_party, challenger_name, target_name, channel):
    """Send battle interface to both players via DM and store message IDs for editing"""
    try:
        # Get battle data to store message IDs
        battle_data = active_battles.get(battle_id, {})
        
        # Get current Pokemon for each player
        challenger_current = challenger_party[0] if challenger_party else None
        target_current = target_party[0] if target_party else None
        
        if not challenger_current or not target_current:
            return
        
        # Store active Pokemon in battle data for consistent tracking
        battle_data['challenger_pokemon'] = challenger_current
        battle_data['target_pokemon'] = target_current
        
        # Initialize dm_messages storage
        if 'dm_messages' not in battle_data:
            battle_data['dm_messages'] = {}
        
        # Create interface for challenger
        challenger_embed = create_battle_interface_embed(challenger_current, challenger_party, target_name)
        challenger_view = BattleInterfaceView(challenger_id, battle_id, challenger_current, challenger_party, channel)
        
        # Create interface for target  
        target_embed = create_battle_interface_embed(target_current, target_party, challenger_name)
        target_view = BattleInterfaceView(target_id, battle_id, target_current, target_party, channel)
        
        # Send DM to challenger and store message ID
        try:
            challenger_user = bot.get_user(challenger_id)
            if not challenger_user:
                challenger_user = await bot.fetch_user(challenger_id)
            if challenger_user:
                msg = await challenger_user.send(embed=challenger_embed, view=challenger_view)
                battle_data['dm_messages'][str(challenger_id)] = msg.id
                print(f'Sent battle interface DM to {challenger_user.name}, stored message ID {msg.id}')
        except discord.Forbidden:
            print(f'DM failed for challenger - user has DMs disabled')
        except Exception as e:
            print(f'Error sending DM to challenger: {e}')
        
        # Send DM to target and store message ID
        try:
            target_user = bot.get_user(target_id)
            if not target_user:
                target_user = await bot.fetch_user(target_id)
            if target_user:
                msg = await target_user.send(embed=target_embed, view=target_view)
                battle_data['dm_messages'][str(target_id)] = msg.id
                print(f'Sent battle interface DM to {target_user.name}, stored message ID {msg.id}')
        except discord.Forbidden:
            print(f'DM failed for target - user has DMs disabled')
        except Exception as e:
            print(f'Error sending DM to target: {e}')
            
    except Exception as e:
        print(f"Error sending battle interfaces: {e}")

class BattlePartyView(View):
    def __init__(self, challenger_id: int, target_id: int, challenger_name: str, target_name: str):
        super().__init__(timeout=1800)
        self.challenger_id = challenger_id
        self.target_id = target_id
        self.challenger_name = challenger_name
        self.target_name = target_name
        battle_id = f"{challenger_id}_{target_id}"
        active_battles[battle_id] = {
            "challenger_id": challenger_id,
            "target_id": target_id,
            "challenger_name": challenger_name,
            "target_name": target_name,
            "challenger_party": [],
            "target_party": [],
            "status": "setup",
            "view_message": None
        }
    def get_battle_embed(self):
        battle_id = f"{self.challenger_id}_{self.target_id}"
        battle_data = active_battles.get(battle_id, {})
        embed = discord.Embed(
            title="Choose your party",
            description="Choose **6** pokémon to fight in the battle. The battle will begin once both trainers have chosen their party.",
            color=0xFFD700
        )
        challenger_party = battle_data.get("challenger_party", [])
        challenger_text_lines = []
        for p in challenger_party:
            max_hp = p.get('calculated_stats', {}).get('hp', 0)
            if max_hp == 0 and 'base_stats' in p and 'ivs' in p:
                from stats_iv_calculation import calculate_official_stats
                calculated_stats = calculate_official_stats(
                    p['base_stats'],
                    p['ivs'],
                    p.get('level', 1),
                    p.get('nature', 'hardy'),
                    p.get('evs', {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
                )
                max_hp = calculated_stats['hp']
            current_hp = p.get('current_hp', max_hp)
            challenger_text_lines.append(f"L{p['level']} {p['iv_percentage']}% {p['name'].title()}{p['gender']} (#{p.get('order', 'N/A')})  •  {current_hp}/{max_hp} HP")
        challenger_text = "\n".join(challenger_text_lines) if challenger_text_lines else "None"
        embed.add_field(name=f"{self.challenger_name}'s Party", value=challenger_text, inline=False)
        target_party = battle_data.get("target_party", [])
        target_text_lines = []
        for p in target_party:
            max_hp = p.get('calculated_stats', {}).get('hp', 0)
            if max_hp == 0 and 'base_stats' in p and 'ivs' in p:
                from stats_iv_calculation import calculate_official_stats
                calculated_stats = calculate_official_stats(
                    p['base_stats'],
                    p['ivs'],
                    p.get('level', 1),
                    p.get('nature', 'hardy'),
                    p.get('evs', {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
                )
                max_hp = calculated_stats['hp']
            current_hp = p.get('current_hp', max_hp)
            target_text_lines.append(f"L{p['level']} {p['iv_percentage']}% {p['name'].title()}{p['gender']} (#{p.get('order', 'N/A')})  •  {current_hp}/{max_hp} HP")
        target_text = "\n".join(target_text_lines) if target_text_lines else "None"
        embed.add_field(name=f"{self.target_name}'s Party", value=target_text, inline=False)
        embed.add_field(
            name="How to add pokémon:",
            value="Use `@PᴏᴋéKɪʀᴏ battle add <pokemon>` to add a pokémon to the party!",
            inline=False
        )
        return embed
    async def on_timeout(self):
        battle_id = f"{self.challenger_id}_{self.target_id}"
        if battle_id in active_battles:
            del active_battles[battle_id]
        try:
            embed = discord.Embed(
                title="Battle Setup Expired",
                description="The battle setup has timed out. Please start a new challenge.",
                color=0xe74c3c
            )
            await self.message.edit(embed=embed, view=None)
        except:
            pass
class ChallengeRequestView(View):
    def __init__(self, challenger_id: int, target_id: int):
        super().__init__(timeout=300)
        self.challenger_id = challenger_id
        self.target_id = target_id
        self.challenge_accepted = False
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept_challenge(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.target_id:
            await interaction.response.send_message("This challenge request is not for you!", ephemeral=True)
            return
        self.challenge_accepted = True
        challenger = interaction.guild.get_member(self.challenger_id)
        target = interaction.guild.get_member(self.target_id)
        if not challenger:
            try:
                challenger_user = await interaction.client.fetch_user(self.challenger_id)
                challenger_name = challenger_user.display_name
            except:
                challenger_name = "Unknown"
        else:
            challenger_name = challenger.display_name
        if not target:
            try:
                target_user = await interaction.client.fetch_user(self.target_id)
                target_name = target_user.display_name
            except:
                target_name = "Unknown"
        else:
            target_name = target.display_name
        battle_view = BattlePartyView(self.challenger_id, self.target_id, challenger_name, target_name)
        embed = battle_view.get_battle_embed()
        await interaction.response.edit_message(embed=embed, view=battle_view, content=None)
        battle_view.message = await interaction.original_response()
        battle_id = f"{self.challenger_id}_{self.target_id}"
        if battle_id in active_battles:
            active_battles[battle_id]["view_message"] = battle_view.message
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel_challenge(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.target_id:
            await interaction.response.send_message("This challenge request is not for you!", ephemeral=True)
            return
        await interaction.response.edit_message(content="Challenge request canceled.", view=None)
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        try:
            await self.message.edit(content="Challenge request expired.", view=self)
        except:
            pass
@bot.group(name="battle", invoke_without_command=True)
async def battle_group(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(
            title="Battle Commands",
            description="Available battle commands:\n`@PokéKiro battle add <pokemon_order(s)>` - Add pokémon to your battle party\n`@PokéKiro challenge @user` - Challenge another trainer to battle\n\nExamples:\n• `@PokéKiro battle add 1` - Add one Pokemon\n• `@PokéKiro battle add 1 2 3 4 5 6` - Add multiple Pokemon",
            color=0x3498db
        )
        await ctx.send(embed=embed)
@battle_group.command(name="add")
async def battle_add_command(ctx, *pokemon_orders):
    if not pokemon_orders:
        await ctx.send("Usage: `@PokéKiro battle add <pokemon_order(s)>`\nExample: `@PokéKiro battle add 1` or `@PokéKiro battle add 1 2 3 4 5 6`")
        return
    try:
        pokemon_order_list = [int(order) for order in pokemon_orders]
    except ValueError:
        await ctx.send("Please provide valid Pokemon order numbers (integers only).")
        return
    trainer_data = get_trainer_data(ctx.author.id)
    if not trainer_data:
        await ctx.send("You need to register first! Use `@PokéKiro register [Male/Female]` to get started.")
        return
    user_battle = None
    battle_id = None
    user_party_key = None
    for bid, battle_data in active_battles.items():
        if battle_data["challenger_id"] == ctx.author.id:
            user_battle = battle_data
            battle_id = bid
            user_party_key = "challenger_party"
            break
        elif battle_data["target_id"] == ctx.author.id:
            user_battle = battle_data
            battle_id = bid
            user_party_key = "target_party"
            break
    if not user_battle:
        await ctx.send("You are not in an active battle! Use `@PokéKiro challenge @user` to start a battle.")
        return
    current_party = user_battle[user_party_key]
    if len(current_party) >= 6:
        await ctx.send("Your battle party is already full! (Maximum 6 pokémon)")
        return
    added_pokemon = []
    skipped_pokemon = []
    for pokemon_order in pokemon_order_list:
        if len(current_party) >= 6:
            skipped_pokemon.append(f"#{pokemon_order} (party full)")
            continue
        pokemon_info = get_pokemon_by_order(trainer_data, pokemon_order)
        if not pokemon_info:
            skipped_pokemon.append(f"#{pokemon_order} (not found)")
            continue
        already_added = False
        for party_pokemon in current_party:
            if party_pokemon.get("order") == pokemon_order:
                skipped_pokemon.append(f"#{pokemon_order} (already added)")
                already_added = True
                break
        if already_added:
            continue
        pokemon_data = pokemon_info["data"].copy()
        pokemon_data["order"] = pokemon_order
        if "current_hp" not in pokemon_data:
            max_hp = pokemon_data.get('calculated_stats', {}).get('hp', 0)
            if max_hp == 0 and 'base_stats' in pokemon_data and 'ivs' in pokemon_data:
                from stats_iv_calculation import calculate_official_stats
                calculated_stats = calculate_official_stats(
                    pokemon_data['base_stats'],
                    pokemon_data['ivs'],
                    pokemon_data.get('level', 1),
                    pokemon_data.get('nature', 'hardy'),
                    pokemon_data.get('evs', {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
                )
                max_hp = calculated_stats['hp']
            pokemon_data["current_hp"] = max_hp
        current_party.append(pokemon_data)
        added_pokemon.append(f"#{pokemon_order} {pokemon_data['name'].title()}")
    battle_view_message = user_battle.get("view_message")
    if battle_view_message:
        try:
            challenger_name = user_battle.get("challenger_name", "Unknown")
            target_name = user_battle.get("target_name", "Unknown")
            embed = discord.Embed(
                title="Choose your party",
                description="Choose **6** pokémon to fight in the battle. The battle will begin once both trainers have chosen their party.",
                color=0xFFD700
            )
            challenger_party = user_battle.get("challenger_party", [])
            challenger_text_lines = []
            for p in challenger_party:
                max_hp = p.get('calculated_stats', {}).get('hp', 0)
                if max_hp == 0 and 'base_stats' in p and 'ivs' in p:
                    from stats_iv_calculation import calculate_official_stats
                    calculated_stats = calculate_official_stats(
                        p['base_stats'],
                        p['ivs'],
                        p.get('level', 1),
                        p.get('nature', 'hardy'),
                        p.get('evs', {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
                    )
                    max_hp = calculated_stats['hp']
                current_hp = p.get('current_hp', max_hp)
                challenger_text_lines.append(f"L{p['level']} {p['iv_percentage']}% {p['name'].title()}{p['gender']} (#{p.get('order', 'N/A')})  •  {current_hp}/{max_hp} HP")
            challenger_text = "\n".join(challenger_text_lines) if challenger_text_lines else "None"
            embed.add_field(name=f"{challenger_name}'s Party", value=challenger_text, inline=False)
            target_party = user_battle.get("target_party", [])
            target_text_lines = []
            for p in target_party:
                max_hp = p.get('calculated_stats', {}).get('hp', 0)
                if max_hp == 0 and 'base_stats' in p and 'ivs' in p:
                    from stats_iv_calculation import calculate_official_stats
                    calculated_stats = calculate_official_stats(
                        p['base_stats'],
                        p['ivs'],
                        p.get('level', 1),
                        p.get('nature', 'hardy'),
                        p.get('evs', {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
                    )
                    max_hp = calculated_stats['hp']
                current_hp = p.get('current_hp', max_hp)
                target_text_lines.append(f"L{p['level']} {p['iv_percentage']}% {p['name'].title()}{p['gender']} (#{p.get('order', 'N/A')})  •  {current_hp}/{max_hp} HP")
            target_text = "\n".join(target_text_lines) if target_text_lines else "None"
            embed.add_field(name=f"{target_name}'s Party", value=target_text, inline=False)
            challenger_party = user_battle.get("challenger_party", [])
            target_party = user_battle.get("target_party", [])
            if len(challenger_party) == 6 and len(target_party) == 6:
                ready_embed = discord.Embed(
                    title="💥 Ready to battle!",
                    description="The battle will begin in 5 seconds.",
                    color=0xFF6B6B
                )
                challenger_text_lines = []
                for p in challenger_party:
                    max_hp = p.get('calculated_stats', {}).get('hp', 0)
                    if max_hp == 0 and 'base_stats' in p and 'ivs' in p:
                        from stats_iv_calculation import calculate_official_stats
                        calculated_stats = calculate_official_stats(
                            p['base_stats'],
                            p['ivs'],
                            p.get('level', 1),
                            p.get('nature', 'hardy'),
                            p.get('evs', {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
                        )
                        max_hp = calculated_stats['hp']
                    current_hp = p.get('current_hp', max_hp)
                    challenger_text_lines.append(f"L{p['level']} {p['iv_percentage']}% {p['name'].title()}{p['gender']} (#{p.get('order', 'N/A')})  •  {current_hp}/{max_hp} HP")
                challenger_text = "\n".join(challenger_text_lines)
                ready_embed.add_field(name=f"{challenger_name}'s Party", value=challenger_text, inline=False)
                target_text_lines = []
                for p in target_party:
                    max_hp = p.get('calculated_stats', {}).get('hp', 0)
                    if max_hp == 0 and 'base_stats' in p and 'ivs' in p:
                        from stats_iv_calculation import calculate_official_stats
                        calculated_stats = calculate_official_stats(
                            p['base_stats'],
                            p['ivs'],
                            p.get('level', 1),
                            p.get('nature', 'hardy'),
                            p.get('evs', {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
                        )
                        max_hp = calculated_stats['hp']
                    current_hp = p.get('current_hp', max_hp)
                    target_text_lines.append(f"L{p['level']} {p['iv_percentage']}% {p['name'].title()}{p['gender']} (#{p.get('order', 'N/A')})  •  {current_hp}/{max_hp} HP")
                target_text = "\n".join(target_text_lines)
                ready_embed.add_field(name=f"{target_name}'s Party", value=target_text, inline=False)
                await battle_view_message.edit(embed=ready_embed)
                await asyncio.sleep(5)
                battle_embed = discord.Embed(
                    title=f"Battle between {challenger_name} and {target_name}",
                    description="Choose your moves using the interface below. After both players have chosen, the move will be executed.",
                    color=0x28A745
                )
                challenger_pokemon_lines = []
                for p in challenger_party:
                    max_hp = p.get('calculated_stats', {}).get('hp', 0)
                    if max_hp == 0 and 'base_stats' in p and 'ivs' in p:
                        from stats_iv_calculation import calculate_official_stats
                        calculated_stats = calculate_official_stats(
                            p['base_stats'],
                            p['ivs'],
                            p.get('level', 1),
                            p.get('nature', 'hardy'),
                            p.get('evs', {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
                        )
                        max_hp = calculated_stats['hp']
                    current_hp = p.get('current_hp', max_hp)
                    challenger_pokemon_lines.append(f"L{p['level']} {p['iv_percentage']}% {p['name'].title()}{p['gender']} (#{p.get('order', 'N/A')})  •  {current_hp}/{max_hp} HP")
                challenger_pokemon_list = "\n".join(challenger_pokemon_lines)
                battle_embed.add_field(name=challenger_name, value=challenger_pokemon_list, inline=False)
                target_pokemon_lines = []
                for p in target_party:
                    max_hp = p.get('calculated_stats', {}).get('hp', 0)
                    if max_hp == 0 and 'base_stats' in p and 'ivs' in p:
                        from stats_iv_calculation import calculate_official_stats
                        calculated_stats = calculate_official_stats(
                            p['base_stats'],
                            p['ivs'],
                            p.get('level', 1),
                            p.get('nature', 'hardy'),
                            p.get('evs', {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
                        )
                        max_hp = calculated_stats['hp']
                    current_hp = p.get('current_hp', max_hp)
                    target_pokemon_lines.append(f"L{p['level']} {p['iv_percentage']}% {p['name'].title()}{p['gender']} (#{p.get('order', 'N/A')})  •  {current_hp}/{max_hp} HP")
                target_pokemon_list = "\n".join(target_pokemon_lines)
                battle_embed.add_field(name=target_name, value=target_pokemon_list, inline=False)
                challenger_first_pokemon = challenger_party[0]["name"] if challenger_party else "pikachu"
                target_first_pokemon = target_party[0]["name"] if target_party else "pikachu"
                challenger_id = user_battle.get("challenger_id")
                target_id = user_battle.get("target_id")
                challenger_battle_image = create_animated_battle_field(
                    challenger_first_pokemon, target_first_pokemon,
                    challenger_id, battle_data
                )
                target_battle_image = challenger_battle_image
                battle_embed.set_image(url="attachment://battle_field_with_sprites.gif")
                if challenger_battle_image:
                    file = discord.File(challenger_battle_image, filename="battle_field_with_sprites.gif")
                    await battle_view_message.edit(embed=battle_embed, attachments=[file])
                else:
                    with open("battle_field.png", "rb") as f:
                        file = discord.File(f, filename="battle_field_with_sprites.gif")
                        await battle_view_message.edit(embed=battle_embed, attachments=[file])
                if battle_id in active_battles:
                    active_battles[battle_id]["battle_started"] = True
                    active_battles[battle_id]["turn"] = 1
                    active_battles[battle_id]["turn_actions"] = {}
                    active_battles[battle_id]["challenger_current_pokemon"] = challenger_party[0]
                    active_battles[battle_id]["target_current_pokemon"] = target_party[0]
                await battle_view_message.edit(embed=battle_embed)
                
                # Send battle interface to both players
                await send_battle_interface_to_players(battle_id, challenger_id, target_id, challenger_party, target_party, challenger_name, target_name, battle_view_message.channel)
            else:
                embed.add_field(
                    name="How to add pokémon:",
                    value="Use `@PᴏᴋéKɪʀᴏ battle add <pokemon>` to add a pokémon to the party!",
                    inline=False
                )
                await battle_view_message.edit(embed=embed)
        except Exception as e:
            print(f"Error updating battle embed: {e}")
            feedback_parts = []
            if added_pokemon:
                feedback_parts.append(f"Added: {', '.join(added_pokemon)}")
            if skipped_pokemon:
                feedback_parts.append(f"Skipped: {', '.join(skipped_pokemon)}")
            if feedback_parts:
                await ctx.send("\n".join(feedback_parts))
@bot.command(name="challenge")
async def challenge_command(ctx, *, arg=None):
    if arg is None:
        await ctx.send("Usage: `@Pokékiro challenge @user`")
        return
    try:
        user = await commands.MemberConverter().convert(ctx, arg.strip())
        if user.id == ctx.author.id:
            await ctx.send("You can't challenge yourself!")
            return
        if user.bot:
            await ctx.send("You can't challenge bots!")
            return
        challenger_data = get_trainer_data(ctx.author.id)
        if not challenger_data:
            await ctx.send(f"<@{ctx.author.id}> You need to register first! Use `register [Male/Female]` to get started.")
            return
        target_data = get_trainer_data(user.id)
        if not target_data:
            await ctx.send(f"<@{user.id}> needs to register first! Tell them to use `register [Male/Female]` to get started.")
            return
        challenger_name = ctx.author.display_name
        target_name = user.display_name
        view = ChallengeRequestView(ctx.author.id, user.id)
        message = await ctx.send(
            content=f"Challenging <@{user.id}> to a battle. Click the accept button to accept!",
            view=view
        )
        view.message = message
    except commands.BadArgument:
        await ctx.send("Please mention a valid user! Example: `@Pokékiro challenge @username`")
        return
@bot.command(name="evolve")
async def evolve_command(ctx):
    trainer_data = get_trainer_data(ctx.author.id)
    if not trainer_data:
        await ctx.send("❌ You are not registered as a trainer. Use `@Pokékiro register` first.")
        return
    selected = trainer_data.get("SelectedPokemon")
    if not selected:
        await ctx.send("❌ You must select a Pokémon first using `@Pokékiro select <order_number>`.")
        return
    pokemon_entry = None
    if selected["type"] == "starter":
        pokemon_entry = trainer_data.get("StarterPokemon")
    elif selected["type"] == "caught":
        idx = selected["order"] - 2
        if "CaughtPokemons" in trainer_data and 0 <= idx < len(trainer_data["CaughtPokemons"]):
            pokemon_entry = trainer_data["CaughtPokemons"][idx]
    if not pokemon_entry:
        await ctx.send("❌ Selected Pokémon not found.")
        return
    try:
        from evolutions import LEVEL_ONLY_EVOLUTIONS as EVOLUTIONS
    except Exception:
        EVOLUTIONS = {}
    current_name = pokemon_entry.get("name", "").lower()
    evo_info = EVOLUTIONS.get(current_name)
    if not evo_info:
        await ctx.send(f"❌ {pokemon_entry['name'].title()} cannot evolve further.")
        return
    required_level = evo_info.get("level", 9999)
    current_level = pokemon_entry.get("level", 1)
    if current_level < required_level:
        await ctx.send(f"❌ {pokemon_entry['name'].title()} needs to be at least level {required_level} to evolve.")
        return
    old_stats = pokemon_entry.get("calculated_stats", {}).copy()
    old_species = pokemon_entry["name"].title()
    new_species = evo_info.get("evolves_to", "").lower()
    try:
        species_data = get_pokemon_by_name(new_species)
    except Exception:
        species_data = None
    pokemon_entry["name"] = new_species
    if species_data:
        pokemon_entry["base_stats"] = species_data.get("base_stats") or species_data.get("stats") or {}
        if "sprite" in species_data:
            pokemon_entry["sprite"] = species_data["sprite"]
    base_stats = pokemon_entry.get("base_stats", {})
    ivs = pokemon_entry.get("ivs", {})
    nature = pokemon_entry.get("nature", "hardy")
    evs = pokemon_entry.get("evs", {"hp": 0, "attack": 0, "defense": 0, "sp_attack": 0, "sp_defense": 0, "speed": 0})
    new_stats = calculate_official_stats(base_stats, ivs, current_level, nature, evs)
    pokemon_entry["calculated_stats"] = new_stats
    update_trainer_data(str(ctx.author.id), trainer_data)
    embed = discord.Embed(
        description=(
            f"🎉 Congratulations {ctx.author.display_name}!\n"
            f"Your {old_species} evolved into **{pokemon_entry['name'].title()}**!"
        ),
        color=discord.Color.gold()
    )
    stats_text = ""
    for stat in ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]:
        before = old_stats.get(stat, 0)
        after = new_stats.get(stat, 0)
        diff = after - before
        stats_text += f"**{stat.upper()}**: {before} → {after} (+{diff})\n"
    embed.add_field(name="📊 Stats Update", value=stats_text, inline=False)
    try:
        embed.set_image(url=get_pokemon_image_url(pokemon_entry["name"]))
    except Exception:
        if "sprite" in pokemon_entry:
            embed.set_thumbnail(url=pokemon_entry["sprite"])
    await ctx.send(embed=embed)
@bot.group(name="move")
async def move_group(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(
            title="Move Commands",
            description="Available move commands:\n`@Pokékiro move info <move_name>` - Get information about a move",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
@move_group.command(name="info")
async def move_info(ctx, *, move_name=None):
    if not move_name:
        embed = discord.Embed(
            title="Missing Move Name",
            description="Please specify a move name!\nExample: `@Pokékiro move info Thunderbolt`",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    move_data = get_move_by_name(move_name)
    if move_data:
        description_text = move_data.get('description', 'No description available.')
        embed = discord.Embed(
            title=move_data['name'],
            description=description_text,
            color=0xFFD700
        )
        power_value = move_data.get('power', 'N/A')
        embed.add_field(name="Power", value=str(power_value), inline=False)
        accuracy_value = move_data.get('accuracy', 'N/A')
        embed.add_field(name="Accuracy", value=str(accuracy_value), inline=False)
        pp_value = move_data.get('pp', 'N/A')
        embed.add_field(name="PP", value=str(pp_value), inline=False)
        priority_value = move_data.get('priority', 0)
        embed.add_field(name="Priority", value=str(priority_value), inline=False)
        type_value = move_data['type']
        type_emojis = {
            'Normal': '<:normal_type:1406551478184706068>', 'Fire': '<:fire_type:1406552697653559336>', 'Water': '<:water_type:1406552467319029860>', 'Electric': '<:electric_type:1406551930406436935>', 'Grass': '<:grass_type:1406552601415122945>',
            'Ice': '<:ice_type:1406553274584399934>', 'Fighting': '<:fighting_type:1406551764483702906>', 'Poison': '<:poison_type:1406555023382413343>', 'Ground': '<:ground_type:1406552961253117993>', 'Flying': '<:flying_type:1406553554897862779>',
            'Psychic': '<:psychic_type:1406552310808576122>', 'Bug': '<:bug_type:1406555435980427358>', 'Rock': '<:rock_type:1406552394950512711>', 'Ghost': '<:ghost_type:1406553684887998484>', 'Dragon': '<:dragon_type:1406552069669916742>',
            'Dark': '<:dark_type:1406553165624774666>', 'Steel': '<:steel_type:1406552865291501629>', 'Fairy': '<:fairy_type:1406552167283691691>'
        }
        type_emoji = type_emojis.get(type_value, '❓')
        embed.add_field(name="Type", value=f"{type_emoji} {type_value}", inline=False)
        class_value = move_data['class']
        class_emojis = {
            'Physical': '<:physical:1407693919722012702>',
            'Special': '<:spiecal:1407693872557064192>',
            'Status': '<:status:1407693796787097672>'
        }
        class_emoji = class_emojis.get(class_value, '❓')
        embed.add_field(name="Class", value=f"{class_emoji} {class_value}", inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Move Not Found",
            description=f"Move '{move_name}' not found in the database. Please check the spelling and try again.",
            color=0xff0000
        )
        await ctx.send(embed=embed)

# Battle action commands  
@bot.command(name="switch")
async def switch_command(ctx, *, order_number=None):
    """Switch Pokemon during battle: @Pokékiro switch <order_number>"""
    if not order_number:
        await ctx.send("Usage: `@Pokékiro switch <order_number>`")
        return
    
    # Check if user is in an active battle
    battle_id = None
    for bid, battle_data in active_battles.items():
        if ctx.author.id in [battle_data.get("challenger_id"), battle_data.get("target_id")] and battle_data.get("battle_started"):
            battle_id = bid
            break
    
    if not battle_id:
        await ctx.send("❌ You are not currently in a battle!")
        return
    
    try:
        order = int(order_number)
        await ctx.send(f"Switched to Pokemon #{order} ✅")
    except ValueError:
        await ctx.send("❌ Please provide a valid Pokemon order number!")

@bot.command(name="flee")
async def flee_command(ctx):
    """Flee from battle: @Pokékiro flee"""
    # Check if user is in an active battle
    battle_id = None
    for bid, battle_data in active_battles.items():
        if ctx.author.id in [battle_data.get("challenger_id"), battle_data.get("target_id")] and battle_data.get("battle_started"):
            battle_id = bid
            break
    
    if not battle_id:
        await ctx.send("❌ You are not currently in a battle!")
        return
    
    await ctx.send("🏃 You fled from the battle!")

@bot.command(name="pass")
async def pass_command(ctx):
    """Pass turn during battle: @Pokékiro pass"""
    # Check if user is in an active battle
    battle_id = None
    for bid, battle_data in active_battles.items():
        if ctx.author.id in [battle_data.get("challenger_id"), battle_data.get("target_id")] and battle_data.get("battle_started"):
            battle_id = bid
            break
    
    if not battle_id:
        await ctx.send("❌ You are not currently in a battle!")
        return
    
    await ctx.send("⏭️ You passed your turn!")

bot.run(os.getenv('DISCORD_BOT_TOKEN'))