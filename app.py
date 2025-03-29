import discord
from discord.ext import commands
import dotenv
import os
import traceback

dotenv.load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# Validate environment variables
if not TOKEN:
    raise ValueError("DISCORD_TOKEN is not set in the .env file")

# List of cogs to load
exts = [
    "cogs.welcome",
    "cogs.sendmessage",
    "cogs.goodbey",
    "cogs.setting",
]

class Seemu(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix=command_prefix, intents=intents, **kwargs)

    async def setup_hook(self) -> None:
        # Load all extensions (cogs)
        for ext in exts:
            try:
                await self.load_extension(ext)
                print(f"{ext} loaded successfully.")
            except Exception as e:
                print(f"Failed to load {ext}: {e}")
                traceback.print_exc()

        print("All cogs are loaded.")
        await self.tree.sync()  # Syncing the command tree

    async def on_ready(self):
        # Changer le message d'activité avec un style "hacker" et terminal
        activity = discord.Game(
            name="⏳ Hacking into Discord...",
            details="Décryptage des données...",
            state="Accès en cours à la base de données... ⚡",
            emoji="💻"  # Emoji de hacker
        )
        await self.change_presence(activity=activity)
        print(f"Bot is ready as {self.user}")

# Run the bot
if __name__ == "__main__":
    intents = discord.Intents.all()  # Enable all intents

    bot = Seemu(command_prefix="!", intents=intents)

    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("Invalid Discord token provided. Please check your .env file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
