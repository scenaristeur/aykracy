import json
from aykracy.autogen.autogen_gvt import AutogenGvt
from aykracy.crewai.crewai_gvt import CrewaiGvt
#from aykracy.crewai.crewai_gvt_manager import CrewaiGvt

lancement = {
    AutogenGvt: False,
    CrewaiGvt: True
}

with open('data/gouvernement.json', encoding="utf-8") as f:
    d = json.load(f)
    # print(d)
    # for mini in d['ministres']:
    #     print(f"mini {mini}")

options = {
    "debug": False,
    "verbose": False,
    "composition": d,
    "OPENAI_API_BASE_URL": "http://127.0.0.1:5678/v1",
    "OPENAI_API_KEY": "Are you crazy ????",
    "MODEL_NAME": "ehartford_dolphin-2.2.1-mistral-7b"

    # "ollama_url": "https://855d-34-138-9-225.ngrok-free.app" , # without trailing slash !
    # "ollama_model": "mistral", #"llama2-uncensored"
}


def main():
    if lancement[AutogenGvt]:
        autogenGvt = AutogenGvt(options)
    if lancement[CrewaiGvt]:
        crewaiGvt = CrewaiGvt(options)


main()
