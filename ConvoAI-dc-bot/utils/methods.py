import discord.ui
import random
import io
import requests
import time
from utils.openai import generate_image

class ImageButtons(discord.ui.View):
  def __init__(self, prompt, model_id, model_name, seed=None, private=False, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.prompt = prompt
      self.model_id = model_id
      self.model_name = model_name
      self.seed = seed
      self.private = private
      self.original_message = None
      self.generation_time = None


  @discord.ui.button(label="Regenerate", style=discord.ButtonStyle.grey, emoji="🔨")
  async def regenerate_button(self, interaction: discord.Interaction, button: discord.ui.Button):
      await interaction.response.defer()
      try:
          new_seed = random.randint(10000, 99999)
          while new_seed == self.seed:
              new_seed = random.randint(10000, 99999)

          start_time = time.time()
          new_image_url = await generate_image(self.prompt, self.model_id)
          end_time = time.time()
          self.generation_time = end_time - start_time

          if not new_image_url:
              await interaction.followup.send("No image generated.", ephemeral=True)
              return

          response = requests.get(new_image_url)
          new_image_data = response.content

          new_image_bytes = io.BytesIO(new_image_data)

          new_image_file = discord.File(new_image_bytes, filename="regenerated_image.png")

          embed = discord.Embed(title="ConvoAI Image Regeneration", color=discord.Color.blue())
          embed.set_image(url="attachment://regenerated_image.png")
          embed.add_field(name="👤 User", value=f'```{interaction.user.display_name}```', inline=True)
          embed.add_field(name="🌱 Seed", value=f'```{new_seed}```', inline=True)
          embed.add_field(name="🔒 Privacy", value="```Private```" if self.private else "```Public```", inline=True)
          embed.set_footer(text="Made with ❤️ by ConvoAI team")

          if self.private:
              await interaction.followup.send(file=new_image_file, embed=embed, view=self, ephemeral=True)
          else:
              new_message = await interaction.followup.send(file=new_image_file, embed=embed, view=self)
              self.seed = new_seed
              self.original_message = new_message
      except Exception as e:
          await interaction.followup.send(f"An error occurred while regenerating the image: {e}", ephemeral=True)

  @discord.ui.button(label="Image Generation Model", style=discord.ButtonStyle.grey, emoji="🤖")
  async def model_name_button(self, interaction: discord.Interaction, button: discord.ui.Button):
      embed = discord.Embed(
          title="Image Generation Model Information",
          description=f"The model used for image generation was: {self.model_name}",
          color=discord.Color.blue()
      )
      await interaction.response.defer(ephemeral=True)
      await interaction.followup.send(embed=embed, ephemeral=True)

  @discord.ui.button(label="Generation Time", style=discord.ButtonStyle.grey, emoji="⏰")
  async def generation_time_button(self, interaction: discord.Interaction, button: discord.ui.Button):
      if self.generation_time is not None:
          embed = discord.Embed(
              title="Image Generation Time",
              description=f"The image was generated in {self.generation_time:.2f} seconds.",
              color=discord.Color.blue()
          )
          await interaction.response.send_message(embed=embed, ephemeral=True)
      else:
          await interaction.response.send_message("The generation time is not available.", ephemeral=True)

  @discord.ui.button(label="Prompt", style=discord.ButtonStyle.grey, emoji="🖍️")
  async def prompt_button(self, interaction: discord.Interaction, button: discord.ui.Button):
      embed = discord.Embed(
          title="🖍️ Prompt",
          description=f"```{self.prompt}```",
          color=discord.Color.blue()
      )
      await interaction.response.send_message(embed=embed, ephemeral=True)