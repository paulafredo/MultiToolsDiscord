import discord
from discord.ext import commands
import json
import os
from app import Seemu

CONFIG_FILE = "config.json"  # Fichier de configuration pour stocker les salons de bienvenue et d'aurevoir


class SettingBot(commands.Cog):
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

    def save_config(self, config):
        # Sauvegarder la configuration dans un fichier JSON
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

    @commands.command(name="setWelcomeSalon", help="Définir le salon de bienvenue")
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        config = self.load_config()

        if not channel.permissions_for(ctx.guild.me).send_messages:
            await ctx.send("Je n'ai pas la permission d'envoyer des messages dans ce salon.")
            return

        # Sauvegarder l'ID du salon de bienvenue dans le fichier de configuration
        config['welcome_channel'] = str(channel.id)
        self.save_config(config)

        await ctx.send(f"Salon de bienvenue configuré : {channel.mention}")

    @commands.command(name="setGoodbyeSalon", help="Définir le salon d'aurevoir")
    async def set_goodbye_channel(self, ctx, channel: discord.TextChannel):
        config = self.load_config()

        if not channel.permissions_for(ctx.guild.me).send_messages:
            await ctx.send("Je n'ai pas la permission d'envoyer des messages dans ce salon.")
            return

        # Sauvegarder l'ID du salon d'aurevoir dans le fichier de configuration
        config['goodbye_channel'] = str(channel.id)
        self.save_config(config)

        await ctx.send(f"Salon d'aurevoir configuré : {channel.mention}")


# Ajouter cette commande pour configurer le bot
async def setup(bot: Seemu):
    await bot.add_cog(SettingBot(bot))
