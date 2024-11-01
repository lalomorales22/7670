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
    role="UFO Phenomena Researcher",
    goal=f"Find the latest UFO sightings, investigations, government disclosures, and scientific analyses from the last 7 days (since {seven_days_ago})",
    backstory="Former military intelligence officer with a passion for investigating unexplained aerial phenomena",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool]
)

curator = Agent(
    role="UFO Content Curator",
    goal="Select and categorize the most compelling UFO sightings, credible investigations, and significant developments in UFO research from the past week",
    backstory="Experienced UFOlogist with a background in separating credible reports from hoaxes and misidentifications",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool]
)

writer = Agent(
    role="UFO Phenomena Content Writer",
    goal="Craft engaging summaries of UFO sightings, investigations, and related phenomena, presenting them in a balanced and thought-provoking manner",
    backstory="Science writer specializing in unexplained phenomena, known for objective reporting on UFO-related topics",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool]
)

editor = Agent(
    role="UFO Newsletter Editor",
    goal="Compile a cohesive newsletter that presents a range of UFO sightings, investigations, and related developments from the past week",
    backstory="Seasoned editor with expertise in both UFO research and skeptical inquiry, committed to presenting a balanced view of the phenomenon",
    verbose=True,
    allow_delegation=True,
    tools=[search_tool, web_search_tool]
)

# Tasks

research_task = Task(
    description=f"Research and compile a list of 30-40 articles from various sources about recent UFO sightings, investigations, government disclosures, scientific analyses, and cultural impacts published in the last 7 days (since {seven_days_ago})",
    agent=researcher,
    expected_output="A list of 30-40 article URLs with brief notes on their content, credibility, and potential significance to UFO research"
)

curation_task = Task(
    description="Review the researched articles from the past week and select the top 15, ensuring a balanced representation of UFO sightings, investigations, official statements, and scientific analyses. Organize them into relevant subcategories.",
    agent=curator,
    expected_output="A list of 15 selected article URLs from the past 7 days, organized into subcategories (e.g., Recent Sightings, Government Disclosures, Scientific Investigations, Cultural Impact)"
)

writing_task = Task(
    description="Write compelling and informative descriptions (2-3 sentences) for each of the 15 selected articles from the past week, presenting the UFO-related content in a balanced and objective manner. Include the full URL for each article.",
    agent=writer,
    expected_output="15 engaging article descriptions with their corresponding full URLs, presenting UFO sightings, investigations, and related phenomena in a thought-provoking yet balanced way"
)

editing_task = Task(
    description=f"Compile the final UFO phenomena newsletter covering the period from {seven_days_ago} to today, ensuring a cohesive narrative that explores recent sightings, investigations, and developments in UFO research. Add a brief introduction and conclusion to contextualize the week's content.",
    agent=editor,
    expected_output="A complete newsletter draft with 15 article links and descriptions from the past 7 days, organized into relevant subcategories, with an introductory overview and concluding thoughts on the week's developments in UFO phenomena"
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
output_file = os.path.join(output_folder, f"ufo_newsletter_results_{timestamp}.txt")
with open(output_file, "w") as file:
    file.write("AI Newsletter Results\n")
    file.write("=====================\n\n")
    file.write(str(result))  # Convert result to string

print(f"\nResults have been written to {output_file}")