import discord
from discord.ext import commands
import asyncio
import os
from openai import OpenAI
from flask import Flask
from threading import Thread

# 1. API Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

# 2. Flask Server (UptimeRobot සඳහා)
app = Flask(__name__)

@app.route('/')
def home():
    return "HAZA BOT is running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Flask එක පටන් ගන්නා ක්‍රමය
def start_server():
    server = Thread(target=run_flask)
    server.daemon = True
    server.start()

# 3. Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} ඔන්ලයින් මචං!')
    await bot.change_presence(activity=discord.Game(name="HAZA AI එක්ක චැට් කරන්න!"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # බොට්ව mention කළොත් විතරක් රිප්ලයි කරන්න
    if bot.user.mentioned_in(message):
        async with message.channel.typing():
            try:
                # OpenRouter API call
                def call_api():
                    return client.chat.completions.create(
                        model="z-ai/glm-4.5-air:free",
                        messages=[{"role": "user", "content": message.content}]
                    )
                
                loop = asyncio.get_event_loop()
                completion = await loop.run_in_executor(None, call_api)
                response = completion.choices[0].message.content
                await message.channel.send(response)
            except Exception as e:
                await message.channel.send("මචං, පොඩි අවුලක් වුණා, ආයෙත් ට්‍රයි කරන්න.")
                print(f"Error: {e}")

    await bot.process_commands(message)

# 4. වැඩේ පටන් ගැනීම
if __name__ == "__main__":
    start_server()
    # මෙතන ටෝකන් එක දාන්න (නැත්නම් secrets වල දාන්න)
    bot.run('MTQ4MDk4MzI4NjI0NjI3NzM0NA.Ggazpn.HRkOHauT_Ht_uLg8190J0VI4itxtEXcS3sy21U')
