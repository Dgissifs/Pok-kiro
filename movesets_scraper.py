import requests
from bs4 import BeautifulSoup
import asyncio
import time
import discord
from discord.ui import View, Button
from moves import get_move_by_name
BASE_URL = "https://pokemondb.net/pokedex/"
def get_all_moves_comprehensive(pokemon_name):
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
        "flabébé": "flabebe"
    }
    if url_name in url_replacements:
        url_name = url_replacements[url_name]
    else:
        url_name = url_name.replace(" ", "-")
    url = BASE_URL + url_name
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return {"error": f"❌ **Pokemon not found:** Could not fetch data for **{pokemon_name.title()}**. Please check the spelling and try again."}
        soup = BeautifulSoup(resp.text, "html.parser")
        move_data = {
            "level_up": [],
            "evolution": [],
            "egg": [],
            "tm": [],
            "pokemon_name": pokemon_name.title()
        }
        level_up_section = soup.find("h3", string="Moves learnt by level up")
        if not level_up_section:
            level_up_section = soup.find("h3", string=lambda text: text and "level up" in text.lower() if text else False)
        if not level_up_section:
            level_up_section = soup.find("h2", string="Moves learnt by level up")
        if not level_up_section:
            level_up_section = soup.find("h2", string=lambda text: text and "level up" in text.lower() if text else False)
        if level_up_section:
            table = level_up_section.find_next("table")
            if table:
                rows = table.find_all("tr")
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if len(cols) >= 4:
                        level = cols[0].get_text(strip=True)
                        move = cols[1].get_text(strip=True)
                        move_type = cols[2].get_text(strip=True)
                        category = cols[3].get_text(strip=True)
                        power = cols[4].get_text(strip=True) if len(cols) > 4 else "—"
                        accuracy = cols[5].get_text(strip=True) if len(cols) > 5 else "—"
                        move_data["level_up"].append({
                            "level": level,
                            "move": move,
                            "type": move_type,
                            "category": category,
                            "power": power,
                            "accuracy": accuracy
                        })
        evolution_section = soup.find("h3", string="Moves learnt on evolution")
        if not evolution_section:
            evolution_section = soup.find("h3", string=lambda text: text and "evolution" in text.lower() if text else False)
        if evolution_section:
            table = evolution_section.find_next("table")
            if table:
                rows = table.find_all("tr")
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if len(cols) >= 3:
                        move = cols[0].get_text(strip=True)
                        move_type = cols[1].get_text(strip=True)
                        category = cols[2].get_text(strip=True)
                        power = cols[3].get_text(strip=True) if len(cols) > 3 else "—"
                        accuracy = cols[4].get_text(strip=True) if len(cols) > 4 else "—"
                        move_data["evolution"].append({
                            "move": move,
                            "type": move_type,
                            "category": category,
                            "power": power,
                            "accuracy": accuracy
                        })
        egg_section = soup.find("h3", string="Egg moves")
        if not egg_section:
            egg_section = soup.find("h3", string=lambda text: text and "egg" in text.lower() if text else False)
        if egg_section:
            table = egg_section.find_next("table")
            if table:
                rows = table.find_all("tr")
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if len(cols) >= 3:
                        move = cols[0].get_text(strip=True)
                        move_type = cols[1].get_text(strip=True)
                        category = cols[2].get_text(strip=True)
                        power = cols[3].get_text(strip=True) if len(cols) > 3 else "—"
                        accuracy = cols[4].get_text(strip=True) if len(cols) > 4 else "—"
                        move_data["egg"].append({
                            "move": move,
                            "type": move_type,
                            "category": category,
                            "power": power,
                            "accuracy": accuracy
                        })
        tm_section = soup.find("h3", string="Moves learnt by TM")
        if not tm_section:
            tm_section = soup.find("h3", string=lambda text: text and "TM" in text if text else False)
        if tm_section:
            table = tm_section.find_next("table")
            if table:
                rows = table.find_all("tr")
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if len(cols) >= 4:
                        tm_number = cols[0].get_text(strip=True)
                        move = cols[1].get_text(strip=True)
                        move_type = cols[2].get_text(strip=True)
                        category = cols[3].get_text(strip=True)
                        power = cols[4].get_text(strip=True) if len(cols) > 4 else "—"
                        accuracy = cols[5].get_text(strip=True) if len(cols) > 5 else "—"
                        move_data["tm"].append({
                            "tm": tm_number,
                            "move": move,
                            "type": move_type,
                            "category": category,
                            "power": power,
                            "accuracy": accuracy
                        })
        return move_data
    except requests.RequestException as e:
        return {"error": f"❌ **Network error:** Could not fetch data from pokemondb.net. Please try again later."}
    except Exception as e:
        return {"error": f"❌ **Error processing data** for **{pokemon_name.title()}**: {str(e)}"}
class MovePaginationView(View):
    def __init__(self, move_data, user_id):
        super().__init__(timeout=300)
        self.move_data = move_data
        self.user_id = user_id
        self.current_page = 0
        self.pages = self._create_pages()
        self._update_buttons()
    def _create_pages(self):
        pages = []
        moves_per_page = 20
        type_emojis = {
            'normal': '<:normal_type:1406551478184706068>', 'fire': '<:fire_type:1406552697653559336>', 'water': '<:water_type:1406552467319029860>', 'electric': '<:electric_type:1406551930406436935>', 'grass': '<:grass_type:1406552601415122945>',
            'ice': '<:ice_type:1406553274584399934>', 'fighting': '<:fighting_type:1406551764483702906>', 'poison': '<:poison_type:1406555023382413343>', 'ground': '<:ground_type:1406552961253117993>', 'flying': '<:flying_type:1406553554897862779>',
            'psychic': '<:psychic_type:1406552310808576122>', 'bug': '<:bug_type:1406555435980427358>', 'rock': '<:rock_type:1406552394950512711>', 'ghost': '<:ghost_type:1406553684887998484>', 'dragon': '<:dragon_type:1406552069669916742>',
            'dark': '<:dark_type:1406553165624774666>', 'steel': '<:steel_type:1406552865291501629>', 'fairy': '<:fairy_type:1406552167283691691>'
        }
        category_emojis = {
            'physical': '<:physical:1407693919722012702>', 'special': '<:spiecal:1407693872557064192>', 'status': '<:status:1407693796787097672>'
        }
        def create_move_pages(moves, move_type, format_func):
            if not moves:
                return
            moves_per_page_display = 10
            for page_num in range(0, len(moves), moves_per_page_display):
                chunk = moves[page_num:page_num + moves_per_page_display]
                page_number = (page_num // moves_per_page_display) + 1
                total_pages = (len(moves) + moves_per_page_display - 1) // moves_per_page_display
                if move_type == "Level-up Movesets":
                    title = f"{self.move_data['pokemon_name']} — Moveset"
                else:
                    title = f"{self.move_data['pokemon_name']} — {move_type}"
                embed = discord.Embed(title=title, color=0xFFD700)
                moves_text = ""
                for i, move in enumerate(chunk):
                    move_number = page_num + i + 1
                    moves_text += format_func(move, move_number)
                total_moves = len(moves)
                start_num = page_num + 1
                end_num = min(page_num + moves_per_page_display, total_moves)
                moves_text += f"\nShowing {start_num}-{end_num} out of {total_moves}."
                embed.description = moves_text
                embed.set_footer(text="Data fetched from pokemondb.net")
                pages.append(embed)
        def format_level_move(move, move_number):
            move_type = move['type'].lower()
            move_category = move['category'].lower() if move['category'] else ''
            
            # Fallback to moves.py if category is missing or unclear
            if not move_category or move_category in ['—', '-', '']:
                move_data = get_move_by_name(move['move'])
                if move_data and 'class' in move_data:
                    move_category = move_data['class'].lower()
            
            type_emoji = type_emojis.get(move_type, '⚪')
            category_emoji = category_emojis.get(move_category, '🔹')
            return f"[{type_emoji}/{category_emoji}] {move['move']}\nLevel {move['level']}\n\n"
        def format_evolution_move(move, move_number):
            move_type = move['type'].lower()
            move_category = move['category'].lower() if move['category'] else ''
            
            # Fallback to moves.py if category is missing or unclear
            if not move_category or move_category in ['—', '-', '']:
                move_data = get_move_by_name(move['move'])
                if move_data and 'class' in move_data:
                    move_category = move_data['class'].lower()
            
            type_emoji = type_emojis.get(move_type, '⚪')
            category_emoji = category_emojis.get(move_category, '🔹')
            return f"[{type_emoji}/{category_emoji}] {move['move']}\nEvolution\n\n"
        def format_egg_move(move, move_number):
            move_type = move['type'].lower()
            move_category = move['category'].lower() if move['category'] else ''
            
            # Fallback to moves.py if category is missing or unclear
            if not move_category or move_category in ['—', '-', '']:
                move_data = get_move_by_name(move['move'])
                if move_data and 'class' in move_data:
                    move_category = move_data['class'].lower()
            
            type_emoji = type_emojis.get(move_type, '⚪')
            category_emoji = category_emojis.get(move_category, '🔹')
            return f"[{type_emoji}/{category_emoji}] {move['move']}\nEgg Move\n\n"
        def format_tm_move(move, move_number):
            move_type = move['type'].lower()
            move_category = move['category'].lower() if move['category'] else ''
            
            # Fallback to moves.py if category is missing or unclear
            if not move_category or move_category in ['—', '-', '']:
                move_data = get_move_by_name(move['move'])
                if move_data and 'class' in move_data:
                    move_category = move_data['class'].lower()
            
            type_emoji = type_emojis.get(move_type, '⚪')
            category_emoji = category_emojis.get(move_category, '🔹')
            return f"[{type_emoji}/{category_emoji}] {move['move']}\n{move['tm']}\n\n"
        create_move_pages(self.move_data["level_up"], "Level-up Movesets", format_level_move)
        create_move_pages(self.move_data["evolution"], "Evolution Moves", format_evolution_move)
        create_move_pages(self.move_data["egg"], "Egg Moves", format_egg_move)
        create_move_pages(self.move_data["tm"], "TM Moves", format_tm_move)
        return pages
    def _update_buttons(self):
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= len(self.pages) - 1
    def get_current_embed(self):
        if not self.pages:
            return discord.Embed(
                title="No Moves Found",
                description="No movesets were found for this Pokémon.",
                color=0xff0000
            )
        return self.pages[self.current_page]
    @discord.ui.button(emoji="◀️", style=discord.ButtonStyle.secondary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You cannot interact with this moveset browser.", ephemeral=True)
            return
        if self.current_page > 0:
            self.current_page -= 1
            self._update_buttons()
            await interaction.response.edit_message(embed=self.get_current_embed(), view=self)
        else:
            await interaction.response.defer()
    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You cannot interact with this moveset browser.", ephemeral=True)
            return
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self._update_buttons()
            await interaction.response.edit_message(embed=self.get_current_embed(), view=self)
        else:
            await interaction.response.defer()
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
async def get_all_moves_comprehensive_async(pokemon_name):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, get_all_moves_comprehensive, pokemon_name)
def get_level_up_moves(pokemon_name):
    url_name = pokemon_name.lower().strip()
    url_replacements = {
        "mr. mime": "mr-mime",
        "mime jr.": "mime-jr",
        "mr. rime": "mr-rime",
        "farfetch'd": "farfetchd",
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
        "type: null": "type-null"
    }
    if url_name in url_replacements:
        url_name = url_replacements[url_name]
    else:
        url_name = url_name.replace(" ", "-")
    url = BASE_URL + url_name
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
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
if __name__ == "__main__":
    test_pokemon = ["pikachu", "charizard", "bulbasaur"]
    for pokemon in test_pokemon:
        print(f"Testing {pokemon}...")
        result = get_level_up_moves(pokemon)
        print(result[:200] + "..." if len(result) > 200 else result)
        print("\n" + "="*50 + "\n")
        time.sleep(1)