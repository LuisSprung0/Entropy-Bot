import os
import random
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Load .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    try:
        await bot.tree.sync()
        print("Slash commands synced!")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="entropy", description="Returns a random number between range")
async def entropy(interaction: discord.Interaction, max: int, min: int = 1):
    if max < min:
        await interaction.response.send_message("⚠️ Max must be greater than or equal to Min!", ephemeral=True)
        return

    number = random.randint(min, max)

    middle = f"║  min: {min}   max: {max}  │ [{number}] ║"

    inner_width = len(middle) - 2  
    top = f"╔{'═' * inner_width}╗"
    bottom = f"╚{'═' * inner_width}╝"

    box = f"```\n{top}\n{middle}\n{bottom}\n```"
    await interaction.response.send_message(box)
    

@bot.tree.command(name="roll", description="Returns a random as if it were a dice roll")
async def roll(interaction: discord.Interaction, max: int, mod: str = "0"):
    """
    max: maximum value of dice roll
    mod: modifier, can be +1, 1, -1, etc.
    """
    # convert mod string to int, handle + sign
    try:
        mod_value = int(mod)
    except ValueError:
        if mod.startswith("+") and mod[1:].isdigit():
            mod_value = int(mod[1:])
        else:
            await interaction.response.send_message(
                "⚠️ Invalid modifier! Use a number like -1, 0, +1.", ephemeral=True
            )
            return

    number = random.randint(1, max)
    number += mod_value

    middle = f"║  max: {max}   modifier: {mod_value}  │ [{number}] ║"
    inner_width = len(middle) - 2
    top = f"╔{'═' * inner_width}╗"
    bottom = f"╚{'═' * inner_width}╝"

    box = f"```\n{top}\n{middle}\n{bottom}\n```"
    await interaction.response.send_message(box)

bot.run(TOKEN)
