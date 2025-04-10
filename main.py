import discord
import os
from openai import OpenAI

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

client_ai = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

@client.event
async def on_ready():
    print(f"Blaivutis prisijungė kaip {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        user_input = message.content.replace(f'<@{client.user.id}>', '').strip()

        try:
            response = client_ai.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=[
                    {"role": "system", "content": "Atsakinėk aiškia, suprantama lietuvių kalba. Tavo tonas – šmaikštus, bet atsakymai turi būti faktiški, be išgalvotų žodžių. Nerašyk bet ko – atsakyk prasmingai."}
                    {"role": "user", "content": user_input}
                ]
            )
            await message.channel.send(response.choices[0].message.content)
        except Exception as e:
            await message.channel.send(f"Blaivutis užsikniso: {e}")

client.run(os.getenv("DISCORD_TOKEN"))
