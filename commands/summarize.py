import discord
from discord.ext import commands
from discord import app_commands
from utils.openai import openai_client


class cog7(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="summarize", description="Summarize your ideas in brief.")
    async def ask(self, interaction: discord.Interaction, paragraph: str):
        await interaction.response.defer()
        completion_message = f"{interaction.user.display_name}: Please summarize: {paragraph}"

        try:
            chat_completion = await openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Hello, I would like you to act as summarizer, you summarize people's paragraphs and messages, your summarization should be concise and informative."},
                    {"role": "user", "content": completion_message}
                ],
            )

            if chat_completion.choices and chat_completion.choices[0].message:
                embed = discord.Embed(title=f"📰 Paragraph", description=(f"```{paragraph}```"), color=discord.Color.blue())
                embed.add_field(name="📜 Summarization",
                                value=(f"```{chat_completion.choices[0].message.content}```"),
                                inline=True)
                avatar_url = interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url
                embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=avatar_url)


                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send("No response from the text generation model, might be caused because of model not being available for you.")
        except Exception as e:
            await interaction.followup.send(f"An error occurred while processing your request: {e}")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(cog7(client))
