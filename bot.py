import discord
from discord import app_commands
from discord.ext import commands

import time
import credentials
import config

class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

idk = (colors.GREEN + time.strftime("%a, %d %b %Y %I:%M %p") + colors.ENDC)

class Client(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents, **kwargs)
    
    async def setup_hook(self):
        for cog in config.cogs:
            try:
                await self.load_extension(cog) # Don't do that if you restart your bot non stop.
                print(idk + colors.CYAN + f"     Loaded {cog}" + colors.ENDC)
            except Exception as exc:
                print(f"Could not load extension {cog} due to {exc.__class__.__name__}: {exc}")

    async def on_ready(self):
        sync = await client.tree.sync()
        print(idk + colors.CYAN + F"     Bot is online" + colors.ENDC)
        print(idk + colors.BOLD + colors.BLUE + f"     Synced {len(sync)} commands" + colors.ENDC)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
client = Client(intents=intents)
ownerId = 614807913302851594 # Your id basically.

@client.tree.command(name = "reload", description = "Reloads the extension (Dev only)")
@app_commands.describe(extension = "cogs.(extension name)")
async def reload(interaction: discord.Interaction, extension: str):
    ext = f"cogs.{extension}"
    if interaction.user.id == ownerId:
        try: 
            await client.reload_extension(ext)
            await interaction.response.send_message(f"Reloaded {ext}", ephemeral=True)
        except Exception as exc:
            await interaction.response.send_message(f"Could not reload extension {exc} due to {exc.__class__.__name__}: {exc}", ephemeral=True)
    else:
        await interaction.response.send_message("You are not allowed to use this command")


@client.command(aliases=["sd"])
async def shutdown(ctx):
    if ctx.author.id == ownerId:
        await ctx.send("Shutting down...")
        raise SystemExit("Bot shutdown")
    else:
        await ctx.send("You are not allowed to use this command")

client.run(credentials.token)