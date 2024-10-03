#!/usr/bin/env python
import sys
from crewai_gvt.crew import CrewaiGvtCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
# Proposer des solutions réalistes et les moyens de mise en oeuvre détaillés pour améliorer la vie des citoyens.
# Donnez votre avis sur 5 des dossiers récents de l'assemblée https://www.nosdeputes.fr/dossiers/date

# topic= """En France, depuis la dissolution de l'Assemblée du 09 juin 2024 par le président Macron, le gouvernement est à l'arrêt.
# Analyser la situation et les événements des élections qui ont entraîné cette dissolution.
# Comment la France peut-elle sortir de cette crise?
# Comment la France peut-elle evoluer?
# Peut-on remplacer les ministres et le gouvernement par un système Multi-agents (Crewai, Autogen ou un système de pilotage approprié) et si oui, comment ?
# """

# topic = """
# Generer des crew de LLM via crewAi pour épauler les commissions permanentes de l'assemblée nationale. """

topic = "https://www2.assemblee-nationale.fr/documents/liste/(type)/projets-loi/(legis)/16"

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': topic
    }
    CrewaiGvtCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": topic
    }
    try:
        CrewaiGvtCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CrewaiGvtCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": topic
    }
    try:
        CrewaiGvtCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
