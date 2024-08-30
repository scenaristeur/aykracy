# https://github.com/joaomdmoura/crewAI/blob/main/docs/how-to/Hierarchical.md

from langchain_openai import ChatOpenAI
from crewai import Crew, Process, Agent

from crewai import Agent, Task, Crew
from langchain.agents import Tool
from langchain_community.tools import DuckDuckGoSearchRun


from langchain_community.llms import LlamaCpp
#from langchain.callbacks.manager import CallbackManager
#from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# GCP_PROJECT_ID = 
# os.environ["OPENAI_API_KEY"] = os.getenv('GCP_PROJECT_ID')

# Callbacks support token-wise streaming
#callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])



llm = LlamaCpp(
    # model_path="/Users/rlm/Desktop/Code/llama.cpp/models/openorca-platypus2-13b.gguf.q4_0.bin",
    model_path="../models/openhermes-2.5-mistral-7b.Q2_K.gguf",
    temperature=0.75,
    max_tokens=32000,
    n_ctx = 32768,
    top_p=1,
    #callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
)


# Define your agents, no need to define a manager
# researcher = Agent(
# 	role='Researcher',
# 	goal='Conduct in-depth analysis',
#     llm=llm
# 	# tools = [...]
# )
writer = Agent(
	role='Writer',
	goal='Create engaging content',
    backstory="""You're a writer at a large company.
    You're responsible for writing blog posts based on researcher insights.""",
    llm=llm,
    verbose=True
	# tools = [...]
)

researcher = Agent(
    role='Researcher',
    goal='Find and summarize the latest AI news',
    backstory="""You're a researcher at a large company.
    You're responsible for analyzing data and providing insights
    to the business.""",
    llm=llm,
    verbose=True
)

# Install duckduckgo-search for this example:
# !pip install -U duckduckgo-search
search_tool = DuckDuckGoSearchRun()

task = Task(
  description='Find and summarize the latest AI news',
    expected_output='A bullet list summary of the top 5 most important AI news',
    #agent=research_agent,
  tools=[search_tool]
)

post = Task(
  description='Create engaging content for a blog post in french',
    expected_output='A blog post in french with the top 5 most important AI news',
    #agent=research_agent,

)


# Form the crew with a hierarchical process
crew = Crew(
	tasks=[task, post], # Tasks that that manager will figure out how to complete
	agents=[researcher, writer],
	manager_llm=llm, #ChatOpenAI(temperature=0, model="gpt-4"), # The manager's LLM that will be used internally
	process=Process.hierarchical  # Designating the hierarchical approach
)

        # Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)