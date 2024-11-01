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
    role="Lost Civilizations and Ancient Tech Researcher",
    goal=f"Find the latest discoveries, theories, and discussions about lost civilizations and ancient technologies from the last 7 days (since {seven_days_ago})",
    backstory="Archaeologist with a passion for uncovering evidence of advanced ancient civilizations and their technologies",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool]
)

curator = Agent(
    role="Ancient Mysteries Content Curator",
    goal="Select and categorize the most intriguing findings and theories about lost civilizations and ancient technologies from the past week",
    backstory="Former museum curator specializing in controversial archaeological finds and theoretical ancient technologies",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool]
)

writer = Agent(
    role="Ancient Civilizations Content Writer",
    goal="Craft engaging summaries of discoveries and theories about lost civilizations and ancient technologies, presenting them in a balanced and thought-provoking manner",
    backstory="Science writer known for bridging mainstream archaeology with alternative theories about ancient civilizations",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool]
)

editor = Agent(
    role="Lost Civilizations Newsletter Editor",
    goal="Compile a cohesive newsletter that presents a range of discoveries, theories, and discussions about lost civilizations and ancient technologies from the past week",
    backstory="Seasoned editor with expertise in both conventional archaeology and alternative historical narratives",
    verbose=True,
    allow_delegation=True,
    tools=[search_tool, web_search_tool]
)

# Tasks

research_task = Task(
    description=f"Research and compile a list of 30-40 articles from reputable sources about lost civilizations, ancient technologies, mysterious archaeological finds, and related theories published in the last 7 days (since {seven_days_ago})",
    agent=researcher,
    expected_output="A list of 30-40 article URLs with brief notes on their content, relevance, and potential implications for our understanding of ancient history and technology"
)

curation_task = Task(
    description="Review the researched articles from the past week and select the top 15, ensuring a balanced representation of discoveries, theories, and discussions about lost civilizations and ancient technologies. Organize them into relevant subcategories.",
    agent=curator,
    expected_output="A list of 15 selected article URLs from the past 7 days, organized into subcategories (e.g., Recent Discoveries, Theoretical Ancient Technologies, Mysterious Artifacts, Alternative Interpretations)"
)

writing_task = Task(
    description="Write compelling and informative descriptions (2-3 sentences) for each of the 15 selected articles from the past week, presenting the discoveries, theories, or discussions about lost civilizations and ancient technologies in a balanced manner. Include the full URL for each article.",
    agent=writer,
    expected_output="15 engaging article descriptions with their corresponding full URLs, presenting discoveries and theories about lost civilizations and ancient technologies in a thought-provoking yet balanced way"
)

editing_task = Task(
    description=f"Compile the final lost civilizations and ancient technologies newsletter covering the period from {seven_days_ago} to today, ensuring a cohesive narrative that explores recent discoveries, intriguing theories, and ongoing discussions in the field. Add a brief introduction and conclusion to contextualize the week's content.",
    agent=editor,
    expected_output="A complete newsletter draft with 15 article links and descriptions from the past 7 days, organized into relevant subcategories, with an introductory overview and concluding thoughts on the week's developments in the study of lost civilizations and ancient technologies"
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
output_file = os.path.join(output_folder, f"ancient_technologies_newsletter_results_{timestamp}.txt")
with open(output_file, "w") as file:
    file.write("AI Newsletter Results\n")
    file.write("=====================\n\n")
    file.write(str(result))  # Convert result to string

print(f"\nResults have been written to {output_file}")