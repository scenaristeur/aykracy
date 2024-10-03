print("crewai_gvt.py")
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
import os, json
from dotenv import load_dotenv
#from langchain_community.llms import Ollama
from langchain.chat_models.openai import ChatOpenAI
from langchain_community.llms import LlamaCpp
load_dotenv()
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# GCP_PROJECT_ID = 
# os.environ["OPENAI_API_KEY"] = os.getenv('GCP_PROJECT_ID')

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

class CrewaiGvt:
    def __init__(self, options):
        print("crewaiGvt", options)
        self.buildGvt(options)

    def buildGvt(self, options):
        print("buildGvt")

        # You can choose to use a local model through Ollama for example. See ./docs/how-to/llm-connections.md for more information.

        # llm = Ollama(model="openhermes")
        #llm = Ollama(base_url=options['ollama_url'], model=options['ollama_model'])

        # Install duckduckgo-search for this example:
        # !pip install -U duckduckgo-search
        # llm = ChatOpenAI(openai_api_base=options["OPENAI_API_BASE_URL"],
        #          openai_api_key=options["OPENAI_API_KEY"],
        #          model_name=options["MODEL_NAME"]
        # )

        llm = LlamaCpp(
    # model_path="/Users/rlm/Desktop/Code/llama.cpp/models/openorca-platypus2-13b.gguf.q4_0.bin",
    model_path="../aykracy/models/openhermes-2.5-mistral-7b.Q2_K.gguf",
    temperature=0.1 , # 0.75, https://github.com/joaomdmoura/crewAI/issues/103#issuecomment-1894100634
    max_tokens=32000,
    n_ctx = 32768,
    top_p=1,
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
)


# from langchain.chat_models.openai import ChatOpenAI
# from dotenv import load_dotenv

# load_dotenv()

# llm = ChatOpenAI(openai_api_base=os.environ.get("OPENAI_API_BASE_URL"),
#                  openai_api_key=os.environ.get("OPENAI_API_KEY"),
#                  model_name=os.environ.get("MODEL_NAME")


        search_tool = DuckDuckGoSearchRun()

        # Define your agents with roles and goals
        researcher = Agent(
        role='Analyste de recherche principal',
        goal="""Découvrez les actualités pertinentes sur les problèmes en France en ce moment""",
        backstory="""Vous travaillez dans un groupe de réflexion technologique de premier plan.
        Votre expertise réside dans l’identification des tendances émergentes et des actualités pertinentes.
        Vous avez le don de disséquer des données complexes et de présenter des informations exploitables.""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        # You can pass an optional llm attribute specifying what mode you wanna use.
        # It can be a local model through Ollama / LM Studio or a remote
        # model like OpenAI, Mistral, Antrophic or others (https://python.langchain.com/docs/integrations/llms/)
        #
        # Examples:
        #
        # from langchain_community.llms import Ollama
         llm=llm # was defined above in the file
        #
        # from langchain_openai import ChatOpenAI
        # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
        )
        writer = Agent(
        role='Stratège de contenu technique et politique',
        goal='Créez du contenu convaincant sur les avancées technologiques et les problème sociétaux',
        backstory="""Vous êtes un stratège de contenu renommé, connu pour vos articles perspicaces et engageants.
        Vous transformez des concepts complexes en récits convaincants.""",
        verbose=True,
        allow_delegation=True,
        # (optional) 
        llm=llm
        )




        agents=[researcher, writer]

                # Gouvernement

        for mini in options['composition']['ministres']:
            print(f"mini {mini}")
            if mini['active']:
                ministre = Agent(
                    role=mini['role'],
                    goal="Tu dois tout mettre en oeuvre en fonction de ton rôle pour arranger les choses",
                    backstory=f"Tu es la/le {mini['role']} de la France, connu pour tes engagements et tes actions.",
                    # goal='Craft compelling content on tech advancements',
                    # backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
                    # You transform complex concepts into compelling narratives.""",
                    verbose=True,
                    allow_delegation=True,
                    llm=llm
                )
                print(f"ajout {mini['role']}")
                agents.append(ministre)

        print(f"-----------------------------------  {len(agents)} agents")


        # Create tasks for your agents
        task1 = Task(
        description="""La France traverse actuellement une grave crise de la démocratie, le parlement a été dissolu par le président Macron au début de l'été.
        Et la France est sans ministre depuis cette date.
        Vous êtes les nouveaux ministres de la France.
        Récupérez les dernières infos sur ce qui se passe en ce moment en France sur des sites d'informations comme 
              sur https://news.google.com/home?hl=fr&gl=FR&ceid=FR:fr ou tout autre site pertinent. et faites des propositions. pour rétablir un état stable,
              un équilibre et une transition.""",
        # description="""Vous êtes les ministres de la France. Récupérez les dernières infos sur ce qui se passe ne ce moment en France
        #       sur https://news.google.com/home?hl=fr&gl=FR&ceid=FR:fr """,
        agent=researcher,
        expected_output="""Un bullet list avec les dernières informations politiques""",
        )

        task2 = Task(
        description="""
              Vous devez rédiger un rapport détaillé des actualités, les problèmes à résoudre, les enjeux, les actions et les recommandations.
        Votre réponse finale DOIT être un rapport proposant des solutions avec au moins 4 paragraphes, au format PDF ou markdown.""",
        agent=writer,
        expected_output="""Un rapport.""",
        )

        task3 = Task(
        description="""
              Vous devez prendre des décisions en fonctions des rapports qui vous sont transmis""",
        agent=agents[3],
        expected_output="""Des décisions.""",
        )
        

        # Instantiate your crew with a sequential process
        crew = Crew(
        agents=agents,
        tasks=[task1, task2, task3],
        #verbose=2, # You can set it to 1 or 2 to different logging levels
        #process=Process.sequential,
        #full_output=True,
        verbose=True,
        )

        print("crew", crew.agents)

        # Get your crew to work!
        #result = crew.kickoff()

        # print("######################")
        # print(result)
        crew_output = crew.kickoff()

# Accessing the crew output
        print(f"Raw Output: {crew_output.raw}")
        if crew_output.json_dict:
            print(f"JSON Output: {json.dumps(crew_output.json_dict, indent=2)}")
        if crew_output.pydantic:
            print(f"Pydantic Output: {crew_output.pydantic}")
        print(f"Tasks Output: {crew_output.tasks_output}")
        print(f"Token Usage: {crew_output.token_usage}")