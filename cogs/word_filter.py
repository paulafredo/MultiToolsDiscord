import discord
from discord.ext import commands
import os
import json

FICHIER_MOTS = "mots_interdits.json"

def charger_mots_interdits():
    if os.path.exists(FICHIER_MOTS):
        with open(FICHIER_MOTS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def sauvegarder_mots_interdits(mots):
    with open(FICHIER_MOTS, "w", encoding="utf-8") as f:
        json.dump(mots, f, indent=4)

class WordFilter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.mots_interdits = charger_mots_interdits()

    @commands.command(name="setmotinterdit")
    async def set_mot_interdit(self, ctx: commands.Context, *, mot: str):
        """Ajoute un mot à la liste des mots interdits."""
        mot = mot.lower()
        self.mots_interdits[mot] = True
        sauvegarder_mots_interdits(self.mots_interdits)
        await ctx.send(f"✅ Mot interdit ajouté : `{mot}`")

    @commands.command(name="listemotsinterdits")
    async def liste_mots(self, ctx):
        if not self.mots_interdits:
            await ctx.send("🚫 Aucun mot interdit n'a été défini.")
        else:
            mots = ", ".join(f"`{mot}`" for mot in self.mots_interdits)
            await ctx.send(f"📌 Mots interdits actuels : {mots}")

    @commands.command(name="scanmessages")
    async def scan_messages(self, ctx: commands.Context, limit: int = 100):
        """Scanne les anciens messages pour tous les mots interdits."""
        if not self.mots_interdits:
            await ctx.send("❌ Aucun mot interdit défini.")
            return

        await ctx.send(f"🔍 Scan des **{limit}** derniers messages...")

        deleted_count = 0

        async for message in ctx.channel.history(limit=limit):
            if message.author.bot:
                continue

            for embed in message.embeds:
                contenu_embed = ""

                if embed.title:
                    contenu_embed += embed.title + " "
                if embed.description:
                    contenu_embed += embed.description + " "
                if embed.footer and embed.footer.text:
                    contenu_embed += embed.footer.text + " "
                for field in embed.fields:
                    contenu_embed += field.name + " " + field.value + " "

                contenu_embed = contenu_embed.lower()

                if any(mot in contenu_embed for mot in self.mots_interdits):
                    try:
                        await message.delete()
                        deleted_count += 1
                        break
                    except Exception as e:
                        print(f"Erreur suppression : {e}")

        await ctx.send(f"✅ **{deleted_count}** message(s) ont été supprimés.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not self.mots_interdits:
            return

        for embed in message.embeds:
            contenu_embed = ""

            if embed.title:
                contenu_embed += embed.title + " "
            if embed.description:
                contenu_embed += embed.description + " "
            if embed.footer and embed.footer.text:
                contenu_embed += embed.footer.text + " "
            for field in embed.fields:
                contenu_embed += field.name + " " + field.value + " "

            contenu_embed = contenu_embed.lower()

            if any(mot in contenu_embed for mot in self.mots_interdits):
                try:
                    await message.delete()
                    print("🔴 Message supprimé (mot interdit détecté).")
                except Exception as e:
                    print(f"Erreur suppression : {e}")
                return

        await self.bot.process_commands(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(WordFilter(bot))
