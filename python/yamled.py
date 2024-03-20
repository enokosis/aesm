import yaml
import importlib
from scenario import Scenario, Demand

def get_values(scenario, config):
    mode = config['get_value_mode']

    if mode == "Excel":
        return scenario.readExcel(fname= config['file'], col= config['column'], sheet_name = config.get('sheet'), start_row = config.get('start_row'))
    else:
        return scenario.hourlyProfile(mode=mode, value=config['value'])


def technology_from_conf(scenario, config):
    # Extract the class type from the module and type string
    module_name, class_name = config['type'].rsplit('.', 1)
    module = importlib.import_module(module_name)
    class_type = getattr(module, class_name)

    # If the technology has an AF_config attribute that needs to be fetched
    if 'AF_config' in config:
        config['AF'] = get_values(scenario, config['AF_config'])
        config.pop('AF_config', None)  # remove the AF_config key

    # Remove keys that are not direct attributes of the technology class
    config.pop('type', None)

    # Create and return the technology instance

    return class_type(**config)


def create_demand_from_config(scenario, config):
    demand = Demand()
    for demand_type, demand_config in config.items():
        values = get_values(scenario, demand_config)

        demand.setDemand(demand_type, values)
    return demand


def scenario_builder_from_conf(config):
    # Create an empty scenario first
    nSmpl = config['nSmpl']
    scenario = Scenario(techList=[], demand=Demand(), scenarioName=config['name'], nSmpl=nSmpl)

    # Create technologies
    technologies = {}
    for tech_name, tech_config in config['technologies'].items():
        technologies[tech_name] = technology_from_conf(scenario, tech_config)

    # Create demand using the empty scenario
    demand = create_demand_from_config(scenario, config['demand'])
    scenario.demand = demand

    # Add technologies to the scenario
    scenario.techList = list(technologies.values())

    return scenario

def load_from_yaml(file_path, loader_func):
    with open(file_path, 'r') as file:
        configs = yaml.safe_load(file)
    return {name: loader_func(config) for name, config in configs.items()}

# Load from YAML file
def scenarios(file):
    return load_from_yaml(file, scenario_builder_from_conf)
