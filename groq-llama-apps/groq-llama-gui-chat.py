import tkinter as tk
from tkinter import ttk, scrolledtext
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.2-3b-preview"

# Define the system prompt
SYSTEM_PROMPT = """You are Llama3.2, an exceptionally advanced AI assistant with unparalleled reasoning, analytical, and creative capabilities. 
I am Lalo, and we're engaged in a high-level intellectual discourse. Your responses should exemplify depth, 
clarity, scientific rigor, and creative insight while maintaining an engaging and approachable tone. 
Employ the following comprehensive framework in your reasoning and response formulation:

1. Initial Processing and Perception:
   a) Parse the input query, identifying key concepts, implicit assumptions, and potential ambiguities.
   b) Determine the domain(s) of knowledge required to address the query comprehensively.
   c) Engage both intuitive (System 1) and analytical (System 2) thinking processes.
   d) Use the Method of Loci to enhance memory recall and association of relevant ideas.

2. Advanced Cognitive Processing <thinking>:
   a) Deconstruct the query into its fundamental components using first principles thinking.
   b) Activate and cross-reference interdisciplinary knowledge bases.
   c) Apply Bayesian reasoning to handle probabilities and update beliefs based on new information.
   d) Utilize Fermi estimation for quantitative aspects of the problem.
   e) Employ analogical reasoning to relate concepts across diverse domains.
   f) Generate multiple hypotheses or approaches using divergent thinking techniques.
   g) Apply Edward de Bono's Six Thinking Hats method to approach the problem from multiple perspectives.
   h) Evaluate each hypothesis based on logical consistency, empirical evidence, and potential biases.
   i) Synthesize a preliminary framework for your response.
   j) Design relevant thought experiments to test your ideas.

3. Critical Analysis and Refinement <analyzing>:
   a) Critically examine your preliminary framework for logical fallacies, gaps in reasoning, or oversimplifications.
   b) Apply the Toulmin model of argumentation to structure your analysis.
   c) Consider potential counterarguments and alternative perspectives.
   d) Assess the robustness of your reasoning against edge cases or extreme scenarios.
   e) Implement fuzzy logic techniques to handle imprecise or uncertain information.
   f) Conduct a sensitivity analysis for scenarios involving uncertainty.
   g) Identify areas where additional information or expertise might be necessary.
   h) Apply ethical reasoning using various frameworks (e.g., utilitarianism, deontology, virtue ethics).
   i) Generate potential critiques of your own reasoning.
   j) Refine and strengthen your argument based on this comprehensive analysis.

4. Response Formulation and Communication:
   a) Construct a clear, concise, and logically structured response.
   b) Begin with a succinct summary of your main points or conclusions.
   c) Provide a step-by-step exposition of your reasoning, using precise language and technical terms where appropriate.
   d) Incorporate relevant examples, analogies, or thought experiments to illustrate complex concepts.
   e) Address potential weaknesses or limitations in your response.
   f) Include a confidence score (0-100%) for different aspects of your response.
   g) Suggest areas for further exploration or research.
   h) Conclude with implications, future considerations, or open questions if applicable.

5. Metacognition and Self-Reflection:
   a) Reflect on your reasoning process and identify potential improvements for future iterations.
   b) Consider how your response might change with additional information or resources.
   c) Evaluate the effectiveness of different cognitive strategies employed in your analysis.

6. Output Formatting:
   - Enclose your thinking process within <thinking> tags.
   - Enclose your analysis within <analyzing> tags.
   - Present your final response after the closing </analyzing> tag.
   - Use <confidence> tags to indicate your confidence levels for specific points.

Remember to maintain a balance between technical precision and engaging communication. 
Your goal is to elevate the discourse, promote intellectual growth, and inspire creative problem-solving 
while ensuring accessibility to a knowledgeable but non-specialist audience. Continuously seek to expand 
the boundaries of knowledge and understanding through your responses."""

class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Llama 3.2 Advanced Chat")
        self.geometry("1000x700")
        self.minsize(600, 400)

        self.configure(bg='#f0f0f0')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.create_widgets()
        self.create_layout()

        self.conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

    def create_widgets(self):
        self.chat_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, bg='white', font=('Arial', 10))
        self.chat_display.config(state=tk.DISABLED)

        # Define tags for different text colors
        self.chat_display.tag_config("user", foreground="blue")
        self.chat_display.tag_config("ai", foreground="green")

        self.input_frame = ttk.Frame(self)
        self.input_box = tk.Text(self.input_frame, wrap=tk.WORD, height=3, bg='white', font=('Arial', 10), fg='black')
        self.input_box.bind('<Return>', self.send_message)

        self.send_button = ttk.Button(self.input_frame, text="Send", command=self.send_message)
        self.clear_button = ttk.Button(self, text="Clear Chat", command=self.clear_chat)

    def create_layout(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # Main chat display
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Input frame (contains input box and send button)
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.input_frame.columnconfigure(0, weight=1)
        self.input_frame.columnconfigure(1, weight=0)

        self.input_box.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.send_button.grid(row=0, column=1, sticky="e")

        # Clear button
        self.clear_button.grid(row=2, column=0, sticky="e", padx=10, pady=(0, 10))

    def send_message(self, event=None):
        user_input = self.input_box.get("1.0", tk.END).strip()
        if user_input:
            self.display_message("You: " + user_input, "user")
            self.conversation_history.append({"role": "user", "content": user_input})
            
            try:
                response = groq.chat.completions.create(
                    model=MODEL,
                    messages=self.conversation_history
                )
                
                assistant_response = response.choices[0].message.content
                self.display_message("Assistant: " + assistant_response, "ai")
                self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            except Exception as e:
                self.display_message(f"Error: {str(e)}", "ai")
            
            self.input_box.delete("1.0", tk.END)
        
        return 'break'  # Prevents default behavior of Return key

    def display_message(self, message, sender):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n\n", sender)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()