



import os
import autogen
from autogen import AssistantAgent, UserProxyAgent

config_list_gpt4 = autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={
                "model": [
                    'Meta-Llama-3.1-8B-Instruct.Q4_K_M'
                    # 'Llama 3.2 1B Instruct' # no function
                    #"gpt-3.5-turbo-1106",
                    # 'ehartford_dolphin-2.2.1-mistral-7b'
                    #'mistral'
                    #"llama2-uncensored"
                    # "gpt-4",
                    # "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"
                ],
            },
        )
llm_config = {
            "cache_seed": 43,  # change the cache_seed for different trials
            "temperature": 0,
            "config_list": config_list_gpt4,
            "timeout": 120,
        }
# llm_config = {"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}
assistant = AssistantAgent("assistant", llm_config=llm_config)
user_proxy = UserProxyAgent("user_proxy", code_execution_config=False)

# Start the chat
user_proxy.initiate_chat(
    assistant,
    message="Tell me a joke about NVDA and TESLA stock prices.",
)