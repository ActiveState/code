import yaml

def yaml_include(loader, node):
    with file(node.value) as inputfile:
        return yaml.load(inputfile)

yaml.add_constructor("!include", yaml_include)
