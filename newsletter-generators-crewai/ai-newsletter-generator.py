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
    role="AI News Researcher",
    goal=f"Find the latest and most impactful AI news from the last 7 days (since {seven_days_ago})",
    backstory="Experienced tech journalist with a strong background in AI developments and computer engineering, known for staying on top of breaking news",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool],
)

curator = Agent(
    role="AI Content Curator",
    goal="Select and categorize the most relevant and groundbreaking AI stories from the past week",
    backstory="Former tech editor with a keen eye for emerging trends and breakthrough discoveries in AI, specializing in identifying the most newsworthy recent developments",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool],
)

writer = Agent(
    role="AI Content Writer",
    goal="Craft engaging summaries of the week's top AI stories, highlighting their immediate importance and potential future impact",
    backstory="Tech communicator specializing in making complex AI topics accessible to a broad audience, with a talent for explaining the significance of recent developments",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, web_search_tool],
)

editor = Agent(
    role="AI Newsletter Editor",
    goal="Compile a cohesive newsletter that presents a comprehensive view of the AI landscape from the past week",
    backstory="Seasoned AI publication editor with a talent for creating informative and engaging content, known for producing timely and relevant weekly roundups",
    verbose=True,
    allow_delegation=True,
    tools=[search_tool, web_search_tool],
)

# Tasks

research_task = Task(
    description=f"Research and compile a list of 30-40 news articles from reputable sources about AI, AI software companies, and AI technologies published in the last 7 days (since {seven_days_ago})",
    agent=researcher,
    expected_output="A list of 30-40 article URLs with brief notes on their content, relevance, and potential impact in the AI sector, all from the past week"
)

curation_task = Task(
    description="Review the researched articles from the past week and select the top 15, ensuring a balanced representation of recent AI news. Organize them into relevant subcategories.",
    agent=curator,
    expected_output="A list of 15 selected article URLs from the past 7 days, organized into subcategories (e.g., Recent AI advancements, AI software company news, emerging AI technologies)"
)

writing_task = Task(
    description="Write compelling and informative descriptions (2-3 sentences) for each of the 15 selected articles from the past week, highlighting their significance in the current AI landscape. Include the full URL for each article.",
    agent=writer,
    expected_output="15 engaging article descriptions with their corresponding full URLs, emphasizing the importance and potential impact of each AI story from the last 7 days"
)

editing_task = Task(
    description=f"Compile the final AI newsletter covering the period from {seven_days_ago} to today, ensuring a cohesive narrative that showcases the most recent developments in AI. Add a brief introduction and conclusion to contextualize the week's content.",
    agent=editor,
    expected_output="A complete newsletter draft with 15 article links and descriptions from the past 7 days, organized into relevant subcategories, with an introductory overview and concluding thoughts on the week's AI developments"
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
output_file = os.path.join(output_folder, f"ai_newsletter_results_{timestamp}.txt")
with open(output_file, "w") as file:
    file.write("AI Newsletter Results\n")
    file.write("=====================\n\n")
    file.write(str(result))  # Convert result to string

print(f"\nResults have been written to {output_file}")
