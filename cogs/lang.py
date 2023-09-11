import discord
from discord import app_commands
from discord.ext import commands
from languages import get_server_language, set_server_language, translate, get_user_language, set_user_language, clear_user_language


class Languages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Clear user language
    @commands.command()
    async def clearuserlang(self, ctx):
        user_id = ctx.author.id
        user_lang = get_user_language(user_id)
        if user_lang is not None:
            clear_user_language(user_id)
            await ctx.send("Your language preference has been cleared")
        else:
            await ctx.send("You don't have a language preference set.")

    # Set server/user language
    @commands.command()
    async def setlang(self, ctx, target=None, language=None):
        available_languages = ['en','pl']
        if target is None or language is None:
            languages_string = ', '.join(available_languages)
            await ctx.send(f"Please provide both target and language arguments. \n**Please select:** `user` or `server`\n**Available languages:** `{languages_string}`")
            return
        
        if target.lower() == 'server':
            if not ctx.author.guild_permissions.manage.guild:
                await ctx.send("You need the `manage_guilds` permission to set the server language.")
                return
            
            server_id = ctx.guild.id
            if language in available_languages:
                if set_server_language(server_id, language):
                    await ctx.send(f"Server language set to: **{language}**")
                else: 
                    await ctx.send("Invalid language. Please choose either 'en' or 'pl'.")
            else:
                await ctx.send("Invalid language. Please choose either 'en' or 'pl'.")
            return

        if target.lower() == 'user':
            user_id = ctx.author.id
            if language in available_languages:
                if set_user_language(user_id, language):
                    await ctx.send(f"Your language preference set to: **{language}**")
                else: 
                    await ctx.send("Invalid language. Please choose either 'en' or 'pl'.")
            else:
                await ctx.send("Invalid language. Please choose either 'en' or 'pl'.")
        else:
            await ctx.send("Invalid target. Please choose either 'user' or 'server'.")


async def setup(bot):
    await bot.add_cog(Languages(bot)) 