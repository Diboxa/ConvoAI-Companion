from discord import app_commands, Embed
from discord.ext import commands
import aiohttp


class Cog4(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name="gif", description="Search for a GIF online.")
  @app_commands.choices(category=[
      app_commands.Choice(name=category.capitalize(), value=category)
      for category in [
          'baka', 'bite', 'blush', 'bored', 'cry', 'cuddle', 'dance',
          'facepalm', 'feed', 'handhold', 'happy', 'highfive', 'hug', 'kick',
          'kiss', 'laugh', 'nod', 'nom', 'nope', 'pat', 'poke', 'pout',
          'punch', 'shoot', 'shrug'
      ]
  ])
  async def gif(self, interaction, category: app_commands.Choice[str]):
    base_url = "https://nekos.best/api/v2/"
    url = base_url + category.value

    async with aiohttp.ClientSession() as session:
      async with session.get(url) as response:
        if response.status != 200:
          await interaction.response.send_message("Failed to fetch the image.")
          return

        json_data = await response.json()
        results = json_data.get("results")
        if not results:
          await interaction.response.send_message("No image found.")
          return

        image_url = results[0].get("url")
        embed = Embed(color=0x2b2d31)
        embed.set_image(url=image_url)
        await interaction.response.send_message(embed=embed)


async def setup(client: commands.Bot) -> None:
  await client.add_cog(Cog4(client))
