import argparse


parser = argparse.ArgumentParser(
    prog='python run2.py',
    description='Aykracy Gvt Builder, runs a gouvernement or a team for you, based on your choice',
    epilog='Have fun and contribute at https://github.com/scenaristeur/aykracy')


# parser.add_argument('filename')           # positional argument
parser.add_argument('-c', '--config', default='config/default.json')      # configuration file

parser.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag
# choose a gouvernement
parser.add_argument(
    '-t', '--team', choices=['autogenGvt', 'crewaiGvt'], default='crewaiGvt')
parser.add_argument('-b', '--backend', choices=['chatgpt3.5', 'chatgpt4', 'gcolab',
                    'replicate', 'llama_server', 'llama_internal'], default='llama_server')  # choose a gouvernement

args = parser.parse_args()
print(
    # args.filename,
    # args.count,
    args.config,
    args.verbose,
    args.team,
    args.backend
)
