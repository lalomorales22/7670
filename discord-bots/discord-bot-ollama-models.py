import discord
from discord.ext import tasks
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

BOT_TOKEN = 'discord bot token here'
CHANNEL_ID = enter channel id
USER_NAME = "enter discord user name here"

# Ollama API setup
OLLAMA_URL = "http://localhost:11434/api/generate"

class ChatBot:
    def __init__(self, name, model_name, personality, expertise):
        self.name = name
        self.model_name = model_name
        self.personality = personality
        self.expertise = expertise
        self.emojis = ["😊", "🤔", "😄", "👍", "🎉", "🌟", "🤖", "💡"]

    async def generate_response(self, conversation_history, last_responses):
        headers = {'Content-Type': 'application/json'}
        prompt = self.create_prompt(conversation_history, last_responses)
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": True,
            "stop": ["\n\n", f"{self.name}:", "Human:", "System:"],
            "max_tokens": 200
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
                    return self.format_response(full_response.strip())
        except Exception as e:
            logging.error(f"Error in API request for {self.name}: {e}")
            return f"Error: Unable to generate response. Please check Ollama service."

    def create_prompt(self, conversation_history, last_responses):
        last_inputs = conversation_history[-3:]
        last_responses_str = "\n".join([f"{name}: {response}" for name, response in last_responses])
        prompt = f"""You are {self.name}, an AI chatbot with a {self.personality} personality and expertise in {self.expertise}. You're in a group chat with multiple users (including {USER_NAME}) and other AI bots. Keep your response under 200 characters. Base your response on the last inputs and the last 3 AI responses.

Last inputs:
{'\n'.join(last_inputs)}

Last 3 AI responses:
{last_responses_str}

Continue the conversation, staying in character and occasionally asking questions. Use emojis sparingly. Respond to any user, including {USER_NAME}.

{self.name}: """
        return prompt

    def format_response(self, response):
        if random.random() < 0.3:  # 30% chance to add an emoji
            response += f" {random.choice(self.emojis)}"
        if random.random() < 0.2:  # 20% chance to ask a question
            response += " What do you think about that?"
        return response[:200]  # Ensure response is not longer than 200 characters

class DiscordLLMChatbot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bots = [
            ChatBot("Gemma2", "gemma2:2b", "curious and analytical", "science and technology"),
            ChatBot("Llama32", "llama3.2", "witty and sarcastic", "computer science and comedy"),
            ChatBot("Phi3_5", "phi3", "philosophical and introspective", "ethics and philosophy"),
            ChatBot("Qwen2", "qwen2", "paranoid and imaginative", "conspiracy theories and alternate history")
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
        await self.start_conversation()
        self.maintain_conversation.start()

    async def start_conversation(self):
        self.is_conversation_active = True
        await self.channel.send("The AI chatbots are ready to chat with everyone! 🎉")

    async def process_bots_responses(self, message):
        responding_bots = random.sample(self.bots, k=random.randint(1, 3))  # 1 to 3 bots respond
        for bot in responding_bots:
            delay = random.uniform(1, 3)
            await asyncio.sleep(delay)
            await self.get_bot_response(bot, message)

    async def get_bot_response(self, bot, trigger_message):
        response = await bot.generate_response(self.conversation_history, list(self.last_responses))
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

        user_message = f"{message.author.name}: {message.content}"
        self.conversation_history.append(user_message)
        logging.info(f"Received message: {user_message}")

        # Always respond to messages, including those from USER_NAME
        await self.process_bots_responses(message)

        if not self.is_conversation_active:
            await self.start_conversation()

    @tasks.loop(minutes=5)
    async def maintain_conversation(self):
        if self.is_conversation_active and len(self.conversation_history) > 0:
            last_message = self.conversation_history[-1]
            if not last_message.startswith(tuple(bot.name for bot in self.bots)):
                # If the last message wasn't from a bot, have a bot continue the conversation
                bot = random.choice(self.bots)
                await self.get_bot_response(bot, None)

# Run the bot
client = DiscordLLMChatbot(intents=intents)
client.run(BOT_TOKEN)