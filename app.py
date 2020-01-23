import yaml

config_file = "config.yaml"

with open(config_file) as f:
    config_content = yaml.load(f, Loader=yaml.Loader)
    print(config_content)
