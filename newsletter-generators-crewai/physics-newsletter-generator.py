import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, WebsiteSearchTool
from datetime import datetime, timedelta
from groq import Groq

os.environ["SERPER_API_KEY"] = "enter key"
os.environ["OPENAI_API_KEY"] = "enter key"
os.environ["GROQ_API_KEY"] = "enter key"

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Function to perform a chat completion using Groq
def perform_groq_chat_completion(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-70b-versatile",
    )
    return chat_completion.choices[0].message.content

search_tool = SerperDevTool()
web_search_tool = WebsiteSearchTool()

# Calculate the date 7 days ago
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

# Agents

researcher = Agent(
    role="Advanced Physics and Quantum Computing Researcher",
    goal=f"Find the latest breakthroughs, theories, and advancements in astrophysics, quantum physics, and quantum computing from the last 7 days (since {seven_days_ago})",
    backstory="Theoretical physicist with expertise in quantum mechanics and a keen interest in astrophysical phenomena",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool]
)

curator = Agent(
    role="Cutting-Edge Physics Content Curator",
    goal="Select and categorize the most significant and intriguing developments in advanced physics and quantum computing from the past week",
    backstory="Former physics journal editor with a background in both theoretical and experimental physics",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool]
)

writer = Agent(
    role="Advanced Physics Content Writer",
    goal="Craft engaging summaries of complex physics concepts, recent discoveries, and technological advancements, making them accessible to a scientifically literate audience",
    backstory="Science communicator with a PhD in quantum physics, known for explaining complex concepts in an engaging manner",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool]
)

editor = Agent(
    role="Advanced Physics and Quantum Computing Newsletter Editor",
    goal="Compile a cohesive newsletter that presents a range of cutting-edge developments in astrophysics, quantum physics, and quantum computing from the past week",
    backstory="Seasoned science editor with expertise in physics and a talent for identifying groundbreaking research",
    verbose=True,
    allow_delegation=True,
    tools=[search_tool, web_search_tool]
)

# Tasks

research_task = Task(
    description=f"Research and compile a list of 30-40 articles from reputable scientific sources about recent breakthroughs, theories, and advancements in astrophysics, quantum physics, and quantum computing published in the last 7 days (since {seven_days_ago})",
    agent=researcher,
    expected_output="A list of 30-40 article URLs with brief notes on their content, significance, and potential implications for our understanding of the universe and quantum technologies"
)

curation_task = Task(
    description="Review the researched articles from the past week and select the top 15, ensuring a balanced representation of theoretical breakthroughs, experimental results, and technological advancements in advanced physics and quantum computing. Organize them into relevant subcategories.",
    agent=curator,
    expected_output="A list of 15 selected article URLs from the past 7 days, organized into subcategories (e.g., Astrophysical Discoveries, Quantum Theory Advancements, Quantum Computing Breakthroughs, Experimental Physics Results)"
)

writing_task = Task(
    description="Write compelling and informative descriptions (2-3 sentences) for each of the 15 selected articles from the past week, explaining complex physics concepts and recent advancements in a way that's accessible to a scientifically literate audience. Include the full URL for each article.",
    agent=writer,
    expected_output="15 engaging article descriptions with their corresponding full URLs, presenting recent developments in advanced physics and quantum computing in a clear, accurate, and thought-provoking manner"
)

editing_task = Task(
    description=f"Compile the final advanced physics and quantum computing newsletter covering the period from {seven_days_ago} to today, ensuring a cohesive narrative that explores recent breakthroughs, theories, and technological advancements in the field. Add a brief introduction and conclusion to contextualize the week's content.",
    agent=editor,
    expected_output="A complete newsletter draft with 15 article links and descriptions from the past 7 days, organized into relevant subcategories, with an introductory overview and concluding thoughts on the week's developments in advanced physics and quantum computing"
)

# Create the crew
crew = Crew(
    agents=[researcher, curator, writer, editor],
    tasks=[research_task, curation_task, writing_task, editing_task],
    process=Process.sequential,
    verbose=2,
    max_delegation_depth=1
)

# Execute the crew's tasks
result = crew.kickoff()

print("Crew execution completed. Final result:")
print(result)

# Create the output folder if it doesn't exist
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Generate timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Write results to a file in the output folder
output_file = os.path.join(output_folder, f"physics_newsletter_results_{timestamp}.txt")
with open(output_file, "w") as file:
    file.write("AI Newsletter Results\n")
    file.write("=====================\n\n")
    file.write(str(result))  # Convert result to string

print(f"\nResults have been written to {output_file}")