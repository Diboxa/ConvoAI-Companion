import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from utils.model import text_model_choices
from utils.openai import generate_chat

class Cog1(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="chat", description="Chat with a model!")
    @app_commands.choices(model=text_model_choices)
    async def ask(self, interaction: discord.Interaction, prompt: str, model: Choice[str]):
        await interaction.response.defer()
        completion_message = f"{interaction.user.display_name}: {prompt}"

        try:
            chat_completion = await generate_chat(completion_message, model.value)
            if chat_completion:
                if len(chat_completion) > 1024:
                  response_header = discord.Embed(title=f"👥 {interaction.user.display_name}",
                                        description=f"```{prompt}```",
                                        color=discord.Color.blue())
                  response_header.add_field(name="🔮 Text Generation Model",
                                      value=f"```{model.name}```",
                                      inline=False)
                  if len(chat_completion) > 4000:
                      response = discord.Embed(title="🧠 AI's response",
                                                  description=f"```{chat_completion[:4000:]}```",
                                                  color=discord.Color.blue())
                  else:
                      response = discord.Embed(title="🧠 AI's response",
                                                  description=f"```{chat_completion}```",
                                                  color=discord.Color.blue())
                  await interaction.followup.send(embed=response_header)
                  await interaction.followup.send(embed=response)
                else:
                    embed = discord.Embed(title=f"👥 {interaction.user.display_name}",
                                          description=f"```{prompt}```",
                                          color=discord.Color.blue())
                    embed.add_field(name="🧠 AI's response",
                                    value=f"```{chat_completion}```",
                                    inline=True)
                    embed.add_field(name="🔮 Text Generation Model",
                                    value=f"```{model.name}```",
                                    inline=True)
                    avatar_url = interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url
                    embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=avatar_url)
                    await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(
                    "No response from the text generation model, might be caused because of model not being available for you."
                )
        except Exception as e:
            await interaction.followup.send(
                f"An error occurred while processing your request: {e}")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Cog1(client))