import discord
from discord.ext import commands
import dotenv
import os
import traceback
from app import Seemu
from discord import app_commands

# Charger les variables d'environnement à partir du fichier .env
dotenv.load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

class PersonalMessageBot(commands.Cog):
    def __init__(self, bot: Seemu):
        self.bot = bot
        self.authorized_user_ids = os.getenv("AUTHORIZED_USER_IDS")  # Identifiants des utilisateurs autorisés

    @app_commands.command(name="envoyermessages", description="Envoyer un message personnel à tous les membres du serveur.")
    async def send_personal_msg(self, interaction: discord.Interaction, message: str, link: str):
        # Vérifier si l'utilisateur est autorisé
        if str(interaction.user.id) not in self.authorized_user_ids:
            await interaction.response.send_message("Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
            return

        # Déférer la réponse pour éviter le délai d'attente
        await interaction.response.defer(thinking=True)

        # Itérer à travers tous les membres et envoyer le message privé
        for member in interaction.guild.members:
            if member.bot:
                continue  # Ignorer les bots
            try:
                await member.send(f"{message}\n{link}")
            except discord.Forbidden:
                print(f"Impossible d'envoyer un DM à {member.display_name}. Ils ont peut-être désactivé les DMs.")
            except Exception as e:
                print(f"Une erreur est survenue lors de l'envoi du DM à {member.display_name}: {e}")

        await interaction.followup.send("Les messages ont été envoyés à tous les membres !", ephemeral=True)

# Fonction de configuration pour ajouter le Cog au bot
async def setup(bot: Seemu):
    await bot.add_cog(PersonalMessageBot(bot))
