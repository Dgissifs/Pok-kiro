import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="pk!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "pk!register":
        embed = discord.Embed(
            title="Welcome to the world of Pokémon!",
            description="Choose your Character by Clicking Male or Female!",
            color=discord.Color.yellow()
        )
        embed.set_image(url="https://static.wikia.nocookie.net/ultimate-pokemon-fanon/images/c/c5/Ivy-Rye.jpg/revision/latest?cb=20201212225708")

        view = GenderSelectView()
        await message.channel.send(embed=embed, view=view)

    await bot.process_commands(message)

class GenderSelectView(discord.ui.View):
    @discord.ui.button(label="Male", style=discord.ButtonStyle.blurple)
    async def male_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        trainer_id = random.randint(100000, 999999)
        embed = discord.Embed(
            title="You chose Male",
            description=f"You have been registered ✅\nTrainer ID: `{trainer_id}`",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Female", style=discord.ButtonStyle.red)
    async def female_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        trainer_id = random.randint(100000, 999999)
        embed = discord.Embed(
            title="You chose Female",
            description=f"You have been registered ✅\nTrainer ID: `{trainer_id}`",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run("TOKEN")