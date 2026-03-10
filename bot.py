import discord
from discord.ext import commands
import asyncio
from openai import OpenAI
from flask import Flask
from threading import Thread

# 1. API Client එක හදන්න (ඔයාගේ Key එකත් එක්කම)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

# 2. Flask සර්වර් එක (Render එකේ 24/7 නොමිලේ දුවන්න මේක ඕනේ)
app = Flask(__name__)

@app.route('/')
def home():
    return "HAZA BOT is running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# 3. Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} ඔන්ලයින් මචං!')
    # බොට්ගේ ස්ටේටස් එක ලස්සනට පේන්න
    await bot.change_presence(activity=discord.Game(name="HAZA AI එක්ක චැට් කරන්න!"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if bot.user.mentioned_in(message):
        # typing status එක පටන් ගන්නවා
        async with message.channel.typing():
            # AI එකෙන් උත්තරේ ගන්නවා (මේක වැඩ කරනකම් typing පෙන්නයි)
            try:
                loop = asyncio.get_event_loop()
                # API call එක වෙනම තැනක රන් කරනවා
                completion = await loop.run_in_executor(None, lambda: client.chat.completions.create(
                    model="z-ai/glm-4.5-air:free",
                    messages=[{"role": "user", "content": message.content}]
                ))
                response = completion.choices[0].message.content
                await message.channel.send(response)
            except Exception as e:
                await message.channel.send("මචං, පොඩි අවුලක් වුණා, ආයෙත් ට්‍රයි කරන්න.")
                print(e)

    await bot.process_commands(message)

# 4. වැඩේ පටන් ගැනීම (Flask එකයි Bot එකයි දෙකම රන් කිරීම)
if __name__ == "__main__":
    # Flask සර්වර් එක වෙනම Thread එකක පටන් ගන්නවා
    t = Thread(target=run_flask)
    t.start()
    
    # බොට්ව රන් කරනවා ඔයාගේ ටෝකන් එකෙන්

    bot.run('MTQ4MDk4MzI4NjI0NjI3NzM0NA.Ggazpn.HRkOHauT_Ht_uLg8190J0VI4itxtEXcS3sy21U')
