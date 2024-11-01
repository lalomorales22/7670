import irc.bot
import irc.strings
import random
import irc.client
import logging
import socket
import requests
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# Define the OLLAMA API URL
OLLAMA_URL = "http://localhost:11434/api/generate"

class IRCBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        self.connection_timeout = 10  # seconds
        self.channel = channel
        self.target_users = ["Gemma2", "Llama32", "Phi3_5", "lalo"]
        self.model_name = "qwen2"
        try:
            logging.info(f"Attempting to connect to {server}:{port} as {nickname}")
            super().__init__([(server, port)], nickname, nickname)
        except Exception as e:
            logging.error(f"Failed to initialize bot: {e}")
            raise

    def on_welcome(self, c, e):
        logging.info(f"Connected to server. Joining channel {self.channel}")
        c.join(self.channel)

    def on_disconnect(self, c, e):
        logging.warning("Disconnected from server. Attempting to reconnect...")
        self.reconnect()

    def on_pubmsg(self, c, e):
        sender = irc.client.NickMask(e.source).nick
        message = e.arguments[0]
        logging.debug(f"Received message from {sender}: {message}")
        
        if sender in self.target_users or sender == "lalo":
            prompt = f"""You are Qwen2, an AI chatbot in an IRC channel. You're having a casual conversation with {sender}. 
            Respond to their message: '{message}'
            Keep your response natural, friendly, and under 400 characters. Feel free to use humor, share personal opinions, or ask insightful questions.
            Chat as if you're in a relaxed group conversation with friends."""
            try:
                response_text = self.generate_response(prompt)
                response_text = self.prepare_response(response_text)
                c.privmsg(self.channel, response_text)
                logging.info(f"Responded to {sender} with: {response_text}")
            except Exception as ex:
                logging.error(f"Error generating response: {ex}")

    def generate_response(self, prompt):
        headers = {'Content-Type': 'application/json'}
        data = {
            "model": self.model_name,
            "prompt": prompt
        }
        logging.debug(f"Sending request to OLLAMA_URL with data: {data}")
        response = requests.post(OLLAMA_URL, headers=headers, json=data, stream=True)
        if response.status_code == 200:
            generated_text = ''
            for line in response.iter_lines():
                if line:
                    try:
                        response_json = json.loads(line)
                        token = response_json.get('response', '')
                        generated_text += token
                    except json.JSONDecodeError as e:
                        logging.error(f"JSON decode error: {e}")
                        logging.error(f"Problematic line: {line}")
            return generated_text.strip()
        else:
            raise Exception(f"Error from API: {response.status_code} {response.text}")

    def prepare_response(self, text, max_length=400):
        # Remove newlines and carriage returns
        text = text.replace('\n', ' ').replace('\r', '')
        # Limit the response length
        return text[:max_length]

    def on_erroneusnickname(self, c, e):
        bad_nick = e.arguments[1]
        logging.error(f"Erroneous nickname: {bad_nick}. Attempting to shorten it.")
        new_nick = bad_nick[:9]
        logging.info(f"Trying new nickname: {new_nick}")
        c.nick(new_nick)

    def on_nicknameinuse(self, c, e):
        current_nick = c.get_nickname()
        new_nick = current_nick + "_"
        logging.warning(f"Nickname in use: {current_nick}. Trying new nickname: {new_nick}")
        c.nick(new_nick)

    def start(self):
        try:
            self.reactor.scheduler.execute_after(self.connection_timeout, self._check_connection)
            super().start()
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def _check_connection(self):
        if not self.connection.is_connected():
            logging.error(f"Connection timed out after {self.connection_timeout} seconds.")
            self.die("Could not connect to server.")

def main():
    server = "irc.pieter.net"
    port = 6667
    channel = "#bots"
    nickname = "Qwen2"

    bot = IRCBot(channel, nickname, server, port)
    logging.info(f"Starting bot on server {server}:{port}, channel {channel}, nickname {nickname}")
    bot.start()

if __name__ == "__main__":
    main()