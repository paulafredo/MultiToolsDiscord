import discord
from discord.ext import commands
import os
import json
from app import Seemu

CONFIG_FILE = "config.json"  # Fichier de configuration


class GoddbeyBot(commands.Cog):
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
    async def on_member_remove(self, member: discord.Member):
        config = self.load_config()

        # Assurez-vous que la clé existe avant de tenter d'accéder à l'ID du salon d'aurevoir
        goodbye_channel_id = config.get("goodbye_channel")

        if goodbye_channel_id:
            channel = self.bot.get_channel(int(goodbye_channel_id))

            if channel:
                embed = discord.Embed(
                    title="Un membre vient de partir… 😢",  # Titre du message d'aurevoir
                    description=f"À bientôt {member.mention} ! 👋 Nous espérons te revoir bientôt !",
                    color=discord.Color.red()  # Changer la couleur en rouge pour signifier le départ
                )
                # Ajouter l'image d'aurevoir (URL directe de l'image)
                embed.set_image(
                    url="https://i.ibb.co/fY8RV8fj/A-BIENTOT-1.gif")  # Remplace par l'URL directe de l'image
                # Ajouter l'avatar du membre en miniature
                embed.set_thumbnail(url=member.avatar.url)

                # Envoyer l'embed dans le salon d'aurevoir
                await channel.send(embed=embed)


# Ajouter cette commande pour configurer le bot
async def setup(bot: Seemu):
    await bot.add_cog(GoddbeyBot(bot))
