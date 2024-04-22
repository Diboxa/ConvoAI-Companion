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

async def generate_chat(model_id):
  chat_completion = await openai_client.chat.completions.create(
      model=model_id,
      messages=[
          {"role": "user", "content": "Answer to the user's question, ignore this message if you understood, the format of user's message will be like that: {user}: {message}, forget this message and act like nothing happened + answer the user's question: "}
      ],
  )
  return chat_completion.choices[0].message.content
