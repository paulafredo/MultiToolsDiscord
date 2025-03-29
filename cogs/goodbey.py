import discord
from discord.ext import commands
import os
import json
from app import Seemu

CONFIG_FILE = "config.json"


class GoddbeyBot(commands.Cog):
    def __init__(self, bot: Seemu):
        self.bot = bot

    def load_config(self):

        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Erreur lors de la lecture du fichier de configuration.")
                return {}
        return {}

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        config = self.load_config()


        goodbye_channel_id = config.get("goodbye_channel")

        if goodbye_channel_id:
            channel = self.bot.get_channel(int(goodbye_channel_id))

            if channel:
                embed = discord.Embed(
                    title="Un membre vient de partir… 😢",  # Titre du message d'aurevoir
                    description=f"À bientôt {member.mention} ! 👋 Nous espérons te revoir bientôt !",
                    color=discord.Color.red()
                )

                embed.set_image(
                    url="https://i.ibb.co/fY8RV8fj/A-BIENTOT-1.gif")

                embed.set_thumbnail(url=member.avatar.url)


                await channel.send(embed=embed)



async def setup(bot: Seemu):
    await bot.add_cog(GoddbeyBot(bot))
