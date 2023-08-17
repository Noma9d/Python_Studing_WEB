from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-a", "--action", dest="action")
parser.add_argument("-m", "--model", dest="model")

arg = parser.parse_args()

print(arg.action, arg.model)
