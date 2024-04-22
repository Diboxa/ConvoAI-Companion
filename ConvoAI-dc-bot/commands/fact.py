import discord
from discord.ext import commands
from discord import app_commands
from utils.openai import openai_client

class FactButton(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction

    @discord.ui.button(label="Request Again", 
                       style=discord.ButtonStyle.primary, 
                       emoji="🤖")
    async def request_again(self, 
                            interaction: discord.Interaction, 
                            button: discord.ui.Button):
        await interaction.response.defer()
        completion_message = f"{interaction.user.display_name}: Tell me a fact"

        try:
            chat_completion = await openai_client.chat.completions.create(
                model="claude-3-haiku",
                messages=[
                    {"role": "system", "content": "I want you to act as a random fact generator, your facts should be always safe for work, so no bad stuff, only positive random facts, your message should start as Hello! Did you knew that: {here you put your fact}"},
                    {"role": "user", "content": completion_message}
                ],
            )

            if chat_completion.choices and chat_completion.choices[0].message:
                new_fact = chat_completion.choices[0].message.content
                embed = discord.Embed(title=f"📜 Facts", 
                                      description=(f"```Made with ❤️ by ConvoAI```"), 
                                      color=discord.Color.blue())
                embed.add_field(name="❓ Random Fact", 
                                value=(f"```{new_fact}```"), 
                                inline=True)
                avatar_url = interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url
                embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=avatar_url)


                await self.interaction.edit_original_response(embed=embed)
            else:
                await interaction.followup.send("No response from the text generation model, might be caused because of model not being available for you.")
        except Exception as e:
            await interaction.followup.send(f"An error occurred while processing your request: {e}")

class cog6(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="fact", description="Get a random fact from AI.")
    async def ask(self, 
                  interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        completion_message = f"{interaction.user.display_name}: Tell me a fact"

        try:
            chat_completion = await openai_client.chat.completions.create(
                model="claude-3-haiku",
                messages=[
                    {"role": "system", "content": "I want you to act as a random fact generator, your facts should be always safe for work, so no bad stuff, only positive random facts, your message should start as Hello! Did you knew that: {here you put your fact}"},
                    {"role": "user", "content": completion_message}
                ],
            )

            if chat_completion.choices and chat_completion.choices[0].message:
                fact = chat_completion.choices[0].message.content
                embed = discord.Embed(title=f"📜 Facts", 
                                      description=(f"Requested by {interaction.user.display_name}"), 
                                      color=discord.Color.blue())
                embed.add_field(name="❓ Random Fact", 
                                value=(f"```{fact}```"), 
                                inline=True)
                embed.set_footer(text=f"Made with ❤️ by ConvoAI")

                await interaction.followup.send(embed=embed, view=FactButton(interaction))
            else:
                await interaction.followup.send("No response from the text generation model, might be caused because of model not being available for you.")
        except Exception as e:
            await interaction.followup.send(f"An error occurred while processing your request: {e}")

async def setup(client:commands.Bot) -> None:
    await client.add_cog(cog6(client))