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
    role="Consciousness and Psychedelics Researcher",
    goal=f"Find the latest research, studies, and accounts related to consciousness exploration, psychedelic experiences, and reported spiritual connections from the last 7 days (since {seven_days_ago})",
    backstory="Neuroscientist with a background in consciousness studies and an interest in the effects of psychedelics on perception and spirituality",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool]
)

curator = Agent(
    role="Spiritual Experiences Content Curator",
    goal="Select and categorize the most insightful and significant reports, studies, and discussions about altered states of consciousness, psychedelic experiences, and spiritual connections from the past week",
    backstory="Anthropologist specializing in comparative religion and entheogens, with experience in both academic research and shamanic traditions",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool]
)

writer = Agent(
    role="Consciousness and Spirituality Content Writer",
    goal="Craft engaging and respectful summaries of research, personal accounts, and scientific discussions related to consciousness exploration, psychedelic experiences, and spiritual connections",
    backstory="Science writer with a deep interest in consciousness studies, known for bridging scientific research with philosophical and spiritual inquiries",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool]
)

editor = Agent(
    role="Consciousness and Spirituality Newsletter Editor",
    goal="Compile a cohesive newsletter that presents a range of perspectives on consciousness exploration, psychedelic experiences, and reported spiritual connections from the past week",
    backstory="Former psychology professor with expertise in altered states of consciousness, committed to presenting a balanced view of these profound experiences",
    verbose=True,
    allow_delegation=True,
    tools=[search_tool, web_search_tool]
)

# Tasks

research_task = Task(
    description=f"Research and compile a list of 30-40 articles from various sources about recent studies, personal accounts, and scientific discussions related to consciousness exploration, psychedelic experiences (e.g., DMT, psilocybin, LSD), and reported spiritual or 'divine' connections published in the last 7 days (since {seven_days_ago})",
    agent=researcher,
    expected_output="A list of 30-40 article URLs with brief notes on their content, scientific rigor, and potential significance to understanding consciousness and spiritual experiences"
)

curation_task = Task(
    description="Review the researched articles from the past week and select the top 15, ensuring a balanced representation of scientific studies, personal accounts, philosophical discussions, and cultural perspectives on consciousness, psychedelics, and spiritual experiences. Organize them into relevant subcategories.",
    agent=curator,
    expected_output="A list of 15 selected article URLs from the past 7 days, organized into subcategories (e.g., Neuroscience of Consciousness, Psychedelic Research, Spiritual Experiences, Philosophical Implications)"
)

writing_task = Task(
    description="Write compelling and informative descriptions (2-3 sentences) for each of the 15 selected articles from the past week, presenting the content related to consciousness, psychedelic experiences, and spiritual connections in a balanced, respectful, and thought-provoking manner. Include the full URL for each article.",
    agent=writer,
    expected_output="15 engaging article descriptions with their corresponding full URLs, presenting research, accounts, and discussions about consciousness exploration and spiritual experiences in an objective yet sensitive way"
)

editing_task = Task(
    description=f"Compile the final consciousness and spirituality newsletter covering the period from {seven_days_ago} to today, ensuring a cohesive narrative that explores recent research, personal accounts, and scientific discussions about consciousness, psychedelic experiences, and reported spiritual connections. Add a brief introduction and conclusion to contextualize the week's content.",
    agent=editor,
    expected_output="A complete newsletter draft with 15 article links and descriptions from the past 7 days, organized into relevant subcategories, with an introductory overview and concluding thoughts on the week's developments in consciousness research and spiritual experiences"
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
output_file = os.path.join(output_folder, f"consciousness_newsletter_results_{timestamp}.txt")
with open(output_file, "w") as file:
    file.write("AI Newsletter Results\n")
    file.write("=====================\n\n")
    file.write(str(result))  # Convert result to string

print(f"\nResults have been written to {output_file}")