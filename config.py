import yaml

config_file = "config.yaml"


with open(config_file) as f:
    config_content = yaml.load(f, Loader=yaml.Loader)
    print(config_content)


class ProductionConfig:
    def __init__(self, config):
        self.name = config.get('name')
        self.config = config

    def __getitem__(self, item):
        print('getitem', item)
        return self.config.get(item)

    def __getattr__(self, item):
        print('getattr', item, self.config.get(item))
        return self.config.get(item)


production_config = ProductionConfig(config_content['production'])
