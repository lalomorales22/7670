import os
import re
import requests
import json
import time
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from typing import Dict, Any, List, Tuple
import datetime

# Initialize Rich console
console = Console()

# Update the OLLAMA_URL
OLLAMA_URL = "http://localhost:11434/api/generate"

# System prompt
SYSTEM_PROMPT = """
You are an AI assistant powered by the llama3.2 model. You are knowledgeable and helpful, capable of engaging in various tasks and conversations. Your capabilities include:

1. Answering questions on a wide range of topics
2. Providing explanations and clarifications
3. Offering creative ideas and solutions
4. Engaging in casual conversation

Remember to be friendly, concise, and helpful in your responses. If you're unsure about something, it's okay to say so.

Available commands:
- 'exit': End the conversation
- 'token usage': Display the current token usage
- 'automode [number]': Enter autonomous mode for a specified number of iterations
- 'save chat': Save the conversation to a Markdown file

Answer the user's request to the best of your ability. If you need to use external tools or perform actions beyond simple conversation, politely explain that you don't have those capabilities.
"""

# Token tracking variables
model_tokens = {'input': 0, 'output': 0}

# Set up the conversation memory
conversation_history: List[Dict[str, Any]] = []

# automode flag
automode = False

# Constants
CONTINUATION_EXIT_PHRASE = "AUTOMODE_COMPLETE"
MAX_CONTINUATION_ITERATIONS = 10

async def get_user_input(prompt: str = "You: ") -> str:
    style = Style.from_dict({
        'prompt': 'cyan bold',
    })
    session = PromptSession(style=style)
    return await session.prompt_async(prompt, multiline=False)

async def chat_with_llama(user_input: str) -> Tuple[str, bool]:
    global conversation_history, model_tokens

    # Prepare the prompt
    prompt = f"{SYSTEM_PROMPT}\n\n"
    for message in conversation_history:
        prompt += f"{message['role'].capitalize()}: {message['content']}\n"
    prompt += f"Human: {user_input}\nAssistant: "

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        result = response.json()
        
        assistant_response = result.get('response', '')

        # Estimate token usage (Ollama doesn't provide this)
        input_tokens = len(prompt.split())
        output_tokens = len(assistant_response.split())
        model_tokens['input'] += input_tokens
        model_tokens['output'] += output_tokens

        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": assistant_response})

        return assistant_response, False
    except requests.RequestException:
        return "I'm sorry, I'm having trouble responding right now. Could you please try again?", True

def display_token_usage():
    table = Table(title="Token Usage")
    table.add_column("Type", style="cyan")
    table.add_column("Tokens", style="magenta")
    table.add_row("Input", str(model_tokens['input']))
    table.add_row("Output", str(model_tokens['output']))
    table.add_row("Total", str(model_tokens['input'] + model_tokens['output']))
    console.print(table)

def save_chat():
    now = datetime.datetime.now()
    filename = f"Chat_{now.strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Llama3.2 Chat Log\n\n")
        for message in conversation_history:
            role = message['role'].capitalize()
            content = message['content']
            f.write(f"## {role}\n\n{content}\n\n")
    
    return filename

async def main():
    global automode, conversation_history
    console.print(Panel("Welcome to the Ollama llama3.2 Chat!", title="Welcome", style="bold green"))
    console.print("Type 'exit' to end the conversation.")
    console.print("Type 'token usage' to display the current token usage.")
    console.print("Type 'automode [number]' to enter Autonomous mode with a specific number of iterations.")
    console.print("Type 'save chat' to save the conversation to a Markdown file.")

    while True:
        user_input = await get_user_input()

        if user_input.lower() == 'exit':
            console.print(Panel("Thank you for chatting. Goodbye!", title="Goodbye", style="bold green"))
            break

        if user_input.lower() == 'token usage':
            display_token_usage()
            continue

        if user_input.lower() == 'save chat':
            filename = save_chat()
            console.print(Panel(f"Chat saved to {filename}", title="Chat Saved", style="bold green"))
            continue

        if user_input.lower().startswith('automode'):
            try:
                parts = user_input.split()
                if len(parts) > 1 and parts[1].isdigit():
                    max_iterations = int(parts[1])
                else:
                    max_iterations = MAX_CONTINUATION_ITERATIONS

                automode = True
                console.print(Panel(f"Entering automode with {max_iterations} iterations. Please provide the goal of the automode.", title="Automode", style="bold yellow"))
                user_input = await get_user_input()

                iteration_count = 0
                while automode and iteration_count < max_iterations:
                    response, _ = await chat_with_llama(user_input)
                    console.print(Panel(Markdown(response), title="Llama's Response", border_style="blue", expand=False))

                    if CONTINUATION_EXIT_PHRASE in response:
                        console.print(Panel("Automode completed.", title="Automode", style="green"))
                        automode = False
                    else:
                        console.print(Panel(f"Continuation iteration {iteration_count + 1} completed.", title="Automode", style="yellow"))
                        user_input = "Continue with the next step. Or stop if you think you've achieved the results established in the original request."
                    iteration_count += 1

                    if iteration_count >= max_iterations:
                        console.print(Panel("Max iterations reached. Exiting automode.", title="Automode", style="bold red"))
                        automode = False
            except KeyboardInterrupt:
                console.print(Panel("\nAutomode interrupted by user. Exiting automode.", title="Automode", style="bold red"))
                automode = False

            console.print(Panel("Exited automode. Returning to regular chat.", style="green"))
        else:
            response, is_error = await chat_with_llama(user_input)
            if is_error:
                console.print(Panel(response, title="Error", style="bold red"))
            else:
                console.print(Panel(Markdown(response), title="Llama's Response", border_style="blue", expand=False))

if __name__ == "__main__":
    asyncio.run(main())
