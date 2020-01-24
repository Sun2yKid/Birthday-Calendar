import yaml

config_file = "config.yaml"


with open(config_file) as f:
    config_content = yaml.load(f, Loader=yaml.Loader)


class ProductionConfig:
    def __init__(self, config):
        self.name = config.get('name')
        self.config = config

    def __getitem__(self, item):
        return self.config.get(item)

    def __getattr__(self, item):
        return self.config.get(item)


production_config = ProductionConfig(config_content['production'])
