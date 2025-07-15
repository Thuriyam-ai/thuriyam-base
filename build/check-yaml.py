import yaml
import sys

with open("./build/prod_values.yml", "r") as stream:
    try:
        body = yaml.safe_load(stream)
        sys.exit(0)
    except yaml.YAMLError as e:
        print(e)
        sys.exit(-1)
