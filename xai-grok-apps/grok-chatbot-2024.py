import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json

class GrokChatApp:
    def __init__(self, master):
        self.master = master
        master.title("Grok Chatbot GUI")
        
        # API Key Entry
        self.api_key_label = tk.Label(master, text="Enter your xAI API Key:")
        self.api_key_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.api_key_entry = tk.Entry(master, width=50)
        self.api_key_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        # Chat Log
        self.chat_log = scrolledtext.ScrolledText(master, width=60, height=20)
        self.chat_log.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        self.chat_log.config(state=tk.DISABLED)

        # User Input
        self.user_input = tk.Entry(master, width=40)
        self.user_input.grid(row=2, column=0, padx=5, pady=5)
        self.user_input.bind("<Return>", self.send_message)

        # Send Button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=2, column=1, padx=5, pady=5)

        # Initialize conversation history
        self.conversation = [
            {"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhiker's Guide to the Galaxy."}
        ]

    def send_message(self, event=None):
        user_text = self.user_input.get().strip()
        if user_text.lower() in ["exit", "quit", "bye"]:
            self.close_app()
            return

        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"You: {user_text}\n")
        self.chat_log.yview(tk.END)
        self.chat_log.config(state=tk.DISABLED)
        self.user_input.delete(0, tk.END)

        api_key = self.api_key_entry.get()
        if not api_key:
            messagebox.showerror("Error", "Please enter an API key.")
            return
        
        response = self.get_grok_response(api_key, user_text)
        if response:
            self.display_response(response)

    def get_grok_response(self, api_key, message):
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        self.conversation.append({"role": "user", "content": message})
        
        data = {
            "messages": self.conversation,
            "model": "grok-beta",
            "stream": False,
            "temperature": 0
        }
        
        try:
            response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            assistant_message = response_data['choices'][0]['message']['content']
            self.conversation.append({"role": "assistant", "content": assistant_message})
            return assistant_message
        except requests.RequestException as e:
            return f"Error: {e}"

    def display_response(self, response):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"Grok: {response}\n")
        self.chat_log.yview(tk.END)
        self.chat_log.config(state=tk.DISABLED)

    def close_app(self):
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GrokChatApp(root)
    root.mainloop()
