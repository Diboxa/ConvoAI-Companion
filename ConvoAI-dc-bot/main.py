import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time
import platform
import os

bot_token = os.getenv('BOT_TOKEN')
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command('help')


class Client(commands.Bot):

  def __init__(self):
    super().__init__(command_prefix=commands.when_mentioned_or('.'),
                     intents=discord.Intents().all())

    self.cogslist = [
        "commands.chat", "commands.imagine", "commands.help", "commands.gif",
        "commands.fact", "commands.summarize", "commands.convodevs"
    ]

  async def setup_hook(self):
    for ext in self.cogslist:
      await self.load_extension(ext)

  async def on_ready(self):
    prfx = (Back.BLACK + Fore.GREEN +
            time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET +
            Fore.WHITE + Style.BRIGHT)
    print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
    print(prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
    print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
    print(prfx + " Python Version " + Fore.YELLOW +
          str(platform.python_version()))
    synced = await self.tree.sync()
    print(prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) +
          " Commands")


client = Client()

client.run(bot_token or "")
