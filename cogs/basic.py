import discord
from discord import app_commands
from discord.ext import commands
from languages import get_server_language, set_server_language, translate, get_user_language, set_user_language, clear_user_language

class Basic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="avatar", description="Fetches user's avatar")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
        if user is None:
            user = interaction.user
        embed = discord.Embed(color = user.color)
        embed.set_author(name = f"{user.name}'s avatar")
        embed.set_image(url = user.avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # slash command
    @app_commands.command(name="hello", description="testing")
    async def hello(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_lang = get_user_language(user_id)
        server_lang = get_server_language(interaction.guild.id)
        lang = user_lang if user_lang else server_lang
        await interaction.response.send_message(translate("hello", lang))

    # text command
    @commands.command()
    async def hello1(self, ctx):
        user_id = ctx.author.id
        user_lang = get_user_language(user_id)
        server_lang = get_server_language(ctx.guild.id)
        lang = user_lang if user_lang else server_lang
        await ctx.send(translate("hello", lang))


async def setup(bot):
    await bot.add_cog(Basic(bot))