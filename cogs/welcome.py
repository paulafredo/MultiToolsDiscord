import discord
from discord.ext import commands
from discord import app_commands
import os
from app import Seemu
import json

CONFIG_FILE = "config.json"

class WelcomeBot(commands.Cog):
    def __init__(self, bot: Seemu):
        self.bot = bot

    def load_config(self):
        # Charger la configuration si elle existe
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Erreur lors de la lecture du fichier de configuration.")
                return {}
        return {}  # Retourne un dictionnaire vide si aucune configuration n'est trouvée

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        config = self.load_config()
        welcome_channel_id = config.get("welcome_channel")
        # channel = self.bot.get_channel(1355533113022746826)  # ID du salon de bienvenue
        if welcome_channel_id:
            channel = self.bot.get_channel(int(welcome_channel_id))
            if channel:
                embed = discord.Embed(
                    title="Ho ! Encore un nouveau membre !",  # Correction du titre
                    description=f"Bienvenue {member.mention} ! 🎉",
                    color=discord.Color.green()
                )
                # Ajouter l'image de bienvenue
                embed.set_image(url="https://i.ibb.co/WWJxwhpJ/BIENVENUE-2.gif?quality=lossless")
                # Ajouter l'avatar du membre en miniature
                embed.set_thumbnail(url=member.avatar.url)

                # Envoyer l'embed dans le salon de bienvenue
                await channel.send(embed=embed)

# Ajouter cette commande pour configurer le bot
async def setup(bot: Seemu):
    await bot.add_cog(WelcomeBot(bot))
