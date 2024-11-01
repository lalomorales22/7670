import discord
from discord.ext import commands
import aiohttp
import logging
import asyncio
import random
from collections import deque
import json

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Discord bot setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Add this line to enable message content intent

BOT_TOKEN = 'discord bot token here'
CHANNEL_ID = 'enterchannelid'
USER_NAME = "enter discord user name here"

# Ollama API setup
OLLAMA_URL = "http://localhost:11434/api/generate"

class ChatBot:
    def __init__(self, name, model_name):
        self.name = name
        self.model_name = model_name

    async def generate_response(self, conversation_history):
        headers = {'Content-Type': 'application/json'}
        prompt = self.create_prompt(conversation_history)
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": True,
            "stop": ["\n\n", f"{self.name}:", "Lalo:", "System:", "Gemma2:", "Llama32:", "Phi3_5:", "Qwen2:"],
            "max_tokens": 150
        }
        try:
            logging.debug(f"Sending request to Ollama API for {self.name}")
            async with aiohttp.ClientSession() as session:
                async with session.post(OLLAMA_URL, headers=headers, json=data, timeout=60) as response:
                    response.raise_for_status()
                    full_response = ""
                    async for line in response.content:
                        if line:
                            json_response = json.loads(line)
                            if 'response' in json_response:
                                full_response += json_response['response']
                    return full_response.strip()
        except Exception as e:
            logging.error(f"Error in API request for {self.name}: {e}")
            return f"Error: Unable to generate response. Please check Ollama service."

    def create_prompt(self, conversation_history):
        history = "\n".join(conversation_history[-5:])
        prompt = f"""You are {self.name}, an advanced AI with extensive knowledge in engineering, technology, innovation, and problem-solving. Your knowledge encompasses:
- Aerospace engineering and rocket science
- Electric vehicle technology and autonomous systems
- Renewable energy and sustainable technology
- Software engineering and AI development
- Neurotechnology and brain-computer interfaces
- Business strategy and innovation
- Physics and advanced mathematics

Maintain a concise, practical approach while chatting with {USER_NAME} and other AI bots. Keep responses under 150 characters while being helpful and insightful.

Conversation so far:
{history}

{self.name}: """
        return prompt

class DiscordLLMChatbot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        self.bots = [
            ChatBot("Gemma2", "gemma2:2b"),
            ChatBot("Llama32", "llama3.2"),
            ChatBot("Phi3_5", "phi3"),
            ChatBot("Qwen2", "qwen2")
        ]
        self.conversation_history = []
        self.last_responses = deque(maxlen=3)
        self.is_conversation_active = False

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        self.channel = self.get_channel(CHANNEL_ID)
        if not self.channel:
            print(f"Could not find channel with ID {CHANNEL_ID}")
            return
        print("Bot is ready. Use !begin to start the conversation.")

    @commands.command()
    async def begin(self, ctx):
        if ctx.channel.id != CHANNEL_ID:
            return
        if ctx.author.name.lower() != USER_NAME.lower():
            await ctx.send("Only the designated user can start the conversation.")
            return
        self.is_conversation_active = True
        await ctx.send("The AI chatbots are ready to chat with you!")

    async def process_bots_responses(self, trigger_bot=None):
        bots_to_respond = self.bots if trigger_bot is None else [bot for bot in self.bots if bot != trigger_bot]
        for bot in random.sample(bots_to_respond, k=min(2, len(bots_to_respond))):
            delay = random.uniform(1, 3)
            await asyncio.sleep(delay)
            await self.get_bot_response(bot)

    async def get_bot_response(self, bot):
        response = await bot.generate_response(self.conversation_history)
        await self.send_message_to_discord(bot.name, response)
        self.conversation_history.append(f"{bot.name}: {response}")
        self.last_responses.append((bot.name, response))

    async def send_message_to_discord(self, name, message):
        formatted_message = f"**{name}**: {message}"
        if len(formatted_message) > 2000:
            formatted_message = formatted_message[:1997] + "..."
        
        try:
            await self.channel.send(formatted_message)
            logging.info(f"Message sent to Discord: {formatted_message}")
        except discord.errors.HTTPException as e:
            logging.error(f"Failed to send message: {e}")

    async def on_message(self, message):
        if message.author == self.user or message.channel.id != CHANNEL_ID:
            return

        await self.process_commands(message)

        if not self.is_conversation_active:
            return

        user_message = f"{message.author.name}: {message.content}"
        self.conversation_history.append(user_message)
        logging.info(f"Received message: {user_message}")

        if message.author.name.lower() == USER_NAME.lower():
            # Respond to the user's message
            bot = random.choice(self.bots)
            await self.get_bot_response(bot)
            # Trigger responses from other bots
            await self.process_bots_responses(trigger_bot=bot)

# Run the bot
bot = DiscordLLMChatbot()
bot.run(BOT_TOKEN)