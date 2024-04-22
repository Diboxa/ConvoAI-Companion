import discord
from discord.ext import commands
from discord import app_commands


class HelpView(discord.ui.View):

  def __init__(self, bot_id):
    super().__init__()
    invite_url = f"https://discord.com/api/oauth2/authorize?client_id={bot_id}&permissions=8&scope=bot%20applications.commands"
    self.add_item(discord.ui.Button(label="Invite", url=invite_url))
    self.add_item(
        discord.ui.Button(label="Support", url="https://discord.convoai.tech"))


class Cog3(commands.Cog):

  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="help", description="List of all commands.")
  async def help_command(self, interaction: discord.Interaction):
    embed = discord.Embed(title="📜 ConvoAI Help Command",
                          color=discord.Color.blurple())
    for command in self.client.tree.get_commands():
      embed.add_field(name=f"```📰 /{command.name}```",
                      value=f"```{command.description}```",
                      inline=True)
    await interaction.response.send_message(embed=embed,
                                            view=HelpView(self.client.user.id))


async def setup(client: commands.Bot) -> None:
  await client.add_cog(Cog3(client))
