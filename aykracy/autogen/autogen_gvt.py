import autogen
#from autogen.agentchat.contrib.capabilities import context_handling
from autogen.agentchat.contrib.web_surfer import WebSurferAgent  # noqa: E402
print("autogen")


class AutogenGvt:
    def __init__(self, options):
        # print("autogenGvt", options)
        self.buildGvt(options)

    def buildGvt(self, options):
        print("build Autogen Gvt")
        config_list_gpt4 = autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={
                "model": [
                    #"gpt-3.5-turbo-1106",
                    'ehartford_dolphin-2.2.1-mistral-7b'
                    #'mistral'
                    #"llama2-uncensored"
                    # "gpt-4",
                    # "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"
                ],
            },
        )
        gpt4_config = {
            "cache_seed": 43,  # change the cache_seed for different trials
            "temperature": 0,
            "config_list": config_list_gpt4,
            "timeout": 120,
        }

        summarizer_llm_config = {
            "timeout": 600,
            "cache_seed": 44,  # change the seed for different trials
            "config_list": config_list_gpt4,
            "temperature": 0,
        }
        # user_proxy = autogen.UserProxyAgent(
        #     name="Admin",
        #     system_message="Un administrateur humain. Interagissez avec le planificateur pour discuter du plan. L'exécution du plan doit être approuvée par cet administrateur.",
        #     code_execution_config=False,
        # )

        # user proxy NEVER
        user_proxy = autogen.UserProxyAgent(
            "user_proxy",
            human_input_mode="NEVER",
            is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
            code_execution_config={
                "work_dir": "coding",
                "use_docker": True,
            },
            max_consecutive_auto_reply=10,
        )

        assistant = autogen.AssistantAgent(
            "assistant",
            llm_config=gpt4_config
        )

        web_surfer = WebSurferAgent(
            "web_surfer",
            llm_config=gpt4_config,
            summarizer_llm_config=summarizer_llm_config,
            browser_config={"viewport_size": 4096,
                            #"bing_api_key": bing_api_key
                            },
        )

        engineer = autogen.AssistantAgent(
            name="Engineer",
            llm_config=gpt4_config,
            system_message="""Ingénieur. Vous suivez un plan approuvé. Vous écrivez du code python/shell pour résoudre des tâches. Enveloppez le code dans un bloc de code qui spécifie le type de script. L'utilisateur ne peut pas modifier votre code. Ne suggérez donc pas de code incomplet qui nécessite que d’autres personnes le modifient. N'utilisez pas de bloc de code s'il n'est pas destiné à être exécuté par l'exécuteur.
        N'incluez pas plusieurs blocs de code dans une seule réponse. Ne demandez pas aux autres de copier et coller le résultat. Vérifiez le résultat de l'exécution renvoyé par l'exécuteur.
        Si le résultat indique qu'il y a une erreur, corrigez l'erreur et générez à nouveau le code. Suggérez le code complet au lieu d’un code partiel ou de modifications de code. Si l'erreur ne peut pas être corrigée ou si la tâche n'est pas résolue même après l'exécution réussie du code, analysez le problème, revisitez votre hypothèse, collectez les informations supplémentaires dont vous avez besoin et réfléchissez à une approche différente à essayer.        """,
        )
        scientist = autogen.AssistantAgent(
            name="Scientist",
            llm_config=gpt4_config,
            system_message="""Scientifique. Vous suivez un plan approuvé. Vous êtes en mesure de classer les articles après avoir vu leurs résumés imprimés. Vous n'écrivez pas de code. Vous êtes au service des ministres.""",
        )
        planner = autogen.AssistantAgent(
            name="Planner",
            system_message="""Planificateur. Proposez un plan. Révisez le plan en fonction des commentaires de l'administrateur et des critiques, jusqu'à l'approbation de l'administrateur.
        Le plan peut impliquer un ingénieur capable d’écrire du code et un scientifique qui n’écrit pas de code.
        Expliquez d'abord le plan. Soyez clair quelle étape est effectuée par un ingénieur et quelle étape est effectuée par un scientifique. Vous êtes au service des ministres.
        """,
            llm_config=gpt4_config,
        )
        executor = autogen.UserProxyAgent(
            name="Executor",
            system_message="Exécuteur. Exécutez le code écrit par l'ingénieur et rapportez le résultataux ministres. Vous êtes au service des ministres.",
            human_input_mode="NEVER",
            code_execution_config={
                "last_n_messages": 3,
                "work_dir": "paper",
                "use_docker": True,
            },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
        )
        critic = autogen.AssistantAgent(
            name="Critic",
            system_message="""Critique. Vérifiez à nouveau le plan, les réclamations, le code des autres agents et fournissez des commentaires. 
            Vérifiez si le plan inclut l'ajout d'informations vérifiables telles que l'URL source.
            Ne vous perdez pas dans les politesse, l'efficacité est le maître mot!""",
            llm_config=gpt4_config,
        )

        # pb de longueur de contexte avec gpt3.5 , 4097 tokens max
        # https://github.com/microsoft/autogen/blob/a52f52a1b556f76383c1908c3197f9583c3c383f/notebook/agentchat_capability_long_context_handling.ipynb#L7
        # Instantiate the capability to manage chat history
        manage_chat_history = context_handling.TransformChatHistory(
            max_tokens_per_message=50, max_messages=5, max_tokens=1000)
        # Add the capability to the assistant
        manage_chat_history.add_to_agent(assistant)

        agents = [assistant, web_surfer,user_proxy, engineer,
                  scientist, planner, executor, critic]

        # Gouvernement

        for mini in options['composition']['ministres']:
            print(f"mini {mini}")
            if mini['active']:
                ministre = autogen.AssistantAgent(
                    name=mini['name'],
                    system_message="tu es le/la " +
                    mini['role'] + " et tu dois agir comme tel.",
                    llm_config=gpt4_config,
                )
                print(f"ajout {mini['role']}")
                agents.append(ministre)

        print(f"-----------------------------------  {len(agents)} agents")

        groupchat = autogen.GroupChat(
            agents=agents, messages=[], max_round=50
        )
        manager = autogen.GroupChatManager(
            groupchat=groupchat, llm_config=gpt4_config)
        # start chat
        user_proxy.initiate_chat(
            manager,
            # message="""find papers on LLM applications from arxiv in the last week, create a markdown table of different domains.""",
            # message="""Détermine quels sont les plus gros problèmes de la France en ce moment, et créé un tableau markdown de ces différents problèmes avec les enjeux et les solutions possibles.""",
            # message="""Récupère dans l'actualité les dernières informations sur les plus récents problèmes de la France, classe les par ordre d'importance
            # pour le bien-être de la population et expose les dans un tableau Markdown.
            # Créé un rapport en français d'une page sur le problème des agriculteurs en ce moment en France, et la présente dans un fichier PDF, avec un chapitre sur les enjuex
            # et un autre avec les solutions envisageables.""",
            message="""Vous êtes les ministres de la France. Récupérez les dernières infos sur ce qui se passe ne ce moment
              sur https://news.google.com/home?hl=fr&gl=FR&ceid=FR:fr et analysez-les dans un tableau. 
              Evitez les redites et les redondances. Ne perdez pas votre temps et votre énergie en politesse, l'important est l'efficacité !
              Les ministres doivent pouvoir prendre des décisions en fonction de ces informations."""
        )
