import json
from aykracy.autogen.autogen_gvt import AutogenGvt
from aykracy.crewai.crewai_gvt import CrewaiGvt

with open('data/gouvernement.json', encoding="utf-8") as f:
    d = json.load(f)
    #print(d)
    # for mini in d['ministres']:
    #     print(f"mini {mini}")

options = {
    "debug": False,
    "verbose": False,
    "composition": d
}



def main():
    autogenGvt = AutogenGvt(options)
   # crewaiGvt = CrewaiGvt(options)


main()
