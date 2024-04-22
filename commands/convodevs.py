import discord
from discord import app_commands
from discord.ext import commands


class Cog8(commands.Cog):

  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="convodevs",
                        description="Information about ConvoAI and its team.")
  async def convodevs(self, interaction: discord.Interaction):
    embed = discord.Embed(
        title="ConvoAI Developer Team",
        description=
        "ConvoAI offers Free AI models. The bot uses ConvoAI's API. Join our community: [ConvoAI](https://discord.convoai.tech)",
        color=discord.Color.blue())

    founders_button = FoundersButton(embed)
    developers_button = DevelopersButton(embed)

    view = discord.ui.View()
    view.add_item(founders_button)
    view.add_item(developers_button)

    await interaction.response.send_message(embed=embed,
                                            view=view,
                                            ephemeral=True)


class TeamButton(discord.ui.Button):

  def __init__(self, label: str, embed: discord.Embed, role: str,
               description: str):
    super().__init__(label=label, style=discord.ButtonStyle.primary)
    self.embed = embed
    self.role = role
    self.description = description

  async def callback(self, interaction: discord.Interaction):
    self.embed.title = f"💻 {self.role}"
    self.embed.clear_fields()
    self.embed.add_field(name=f"👨‍💻 {self.role}",
                         value=f"```{self.description}```",
                         inline=False)
    await interaction.response.edit_message(embed=self.embed, view=self.view)


class FoundersButton(TeamButton):

  def __init__(self, embed: discord.Embed):
    super().__init__(
        "Founders", embed, "Founders",
        "Niklas manages the entire API system and the entire site. Werewolf does a great job in developing ConvoAI's site."
    )


class DevelopersButton(TeamButton):

  def __init__(self, embed: discord.Embed):
    super().__init__(
        "Developers", embed, "Developers",
        "Diboxa is the main developer of ConvoAI's github. BestCodes is the frontend developer for ConvoAI. Impact does a great job in writing code for the site."
    )


async def setup(client: commands.Bot) -> None:
  await client.add_cog(Cog8(client))
