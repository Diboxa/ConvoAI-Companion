from openai import AsyncOpenAI
import os

API_KEY = os.getenv('API_KEY')

openai_client = AsyncOpenAI(       
  api_key=API_KEY,        
  base_url="https://api.convoai.tech/v1/"
)

async def generate_image(prompt, model_id):
  response = await openai_client.images.generate(
      model=model_id,
      prompt=prompt,
      n=1,
      size="1024x1024",
  )
  return response.data[0].url

async def generate_chat(prompt, model_id):
  chat_completion = await openai_client.chat.completions.create(
      model=model_id,
      messages=[
          {"role": "user", "content": f"Hello, you are currently talking to a discord user: "}
      ],
  )
  return chat_completion.choices[0].message.content
