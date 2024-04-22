import discord
from discord.ext import commands
from discord import app_commands
from utils.model import image_model_choices
import random
import time
import requests
import io
from utils.methods import ImageButtons
from utils.openai import generate_image

class Cog2(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="imagine", description="Create an image with words.")
    @app_commands.describe(prompt="The prompt for the image generation")
    @app_commands.describe(model="The model to use for image generation")
    @app_commands.describe(seed="The seed for the random number generator (optional)")
    @app_commands.describe(private="Whether the image should be private or not")
    @app_commands.choices(model=image_model_choices)
    async def imagine(self, interaction: discord.Interaction, prompt: str, model: app_commands.Choice[str], seed: int = 0, private: bool = False):
        await interaction.response.defer(ephemeral=private)
        try:
            start_time = time.time()

            seed = seed or random.randint(1, 100000)

            image_url = await generate_image(prompt, model.value)
            if not image_url:
                await interaction.followup.send("No image generated.", ephemeral=True)
                return

            response = requests.get(image_url)
            image_data = response.content

            image_bytes = io.BytesIO(image_data)
            image_file = discord.File(image_bytes, filename="generated_image.png")

            end_time = time.time()
            generation_time = end_time - start_time

            embed = discord.Embed(title="ConvoAI Image Generation", color=discord.Color.blue())
            embed.set_image(url="attachment://generated_image.png")
            embed.add_field(name="👤 User", value=f'```{interaction.user.display_name}```', inline=True)
            embed.add_field(name="🌱 Seed", value=f'```{seed}```', inline=True)
            embed.add_field(name="🔒 Privacy", value="```Private```" if private else "```Public```", inline=True)
            embed.set_footer(text="Made with ❤️ by ConvoAI team")
          
            view = ImageButtons(prompt, model.value, model.name, seed, private)
            view.generation_time = generation_time

            if private:
                await interaction.followup.send(file=image_file, embed=embed, view=view, ephemeral=True)
            else:
                message = await interaction.followup.send(file=image_file, embed=embed, view=view)
                view.original_message = message
        except Exception as e:
            await interaction.followup.send(f"An error occurred while generating the image: {e}", ephemeral=True)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Cog2(client))
