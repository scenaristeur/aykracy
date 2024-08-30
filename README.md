# AYKRACY

python >= 3.8 (autogen)

fill .env (for crewai) and OAI_CONFIG_LIST (for autogen)file with OPENAI_API_KEY


```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# or pip install --upgrade --force-reinstall -r requirements.txt
python run.py
```


# simple starter
```
python run2.py -h
```



# Autogen Gouvernement
- https://microsoft.github.io/autogen/docs/Examples/
- https://github.com/microsoft/autogen/blob/main/notebook/agentchat_groupchat_research.ipynb



# GPT 
- taille des contextes selon les modèles 
- https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo
- gpt-3.5 : 4096
- gpt-3.5-turbo-1106 : 16385

# ollama colab

- ollama sur Colab : https://colab.research.google.com/drive/1vbKSq2dsNoYaDU6s6FIR3ENMS6DLLKYA

- https://github.com/ollama/ollama/blob/main/docs/api.md
curl https://855d-34-138-9-225.ngrok-free.app/api/generate -d '{
  "model": "mistral",
  "prompt": "Pourquoi le ciel est-il bleu?"
}'

- https://stackoverflow.com/questions/77697302/how-to-run-ollama-in-google-colab


# ollama & autogen
- https://www.youtube.com/watch?v=gx6X5XJ8uH4


- autogen with v1

[
    {
        "model": "llama2-uncensored",
        "api_key": "truc",
        "base_url": "https://904c-35-239-149-50.ngrok-free.app/v1"
    }
]


with litellm https://www.youtube.com/watch?v=y7wMTwJN7rA



# reference
- python argparser https://docs.python.org/3/library/argparse.html
- https://github.com/microsoft/autogen
- https://github.com/microsoft/autogen/blob/main/notebook/agentchat_groupchat_research.ipynb
- https://github.com/majacinka/crewai-experiments


# issue on llama_cpp
- https://github.com/joaomdmoura/crewAI/issues/103
- Action & thoughts avec des agents français https://github.com/joaomdmoura/crewAI/issues/103#issuecomment-1908792048