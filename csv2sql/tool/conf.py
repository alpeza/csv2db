import yaml
class Config(object):
    """docstring for Config."""
    def __init__(self, file='config.yaml'):
        super(Config, self).__init__()
        self.configfile = file
        self.config = {}
        self.load()

    def load(self):
        with open(self.configfile) as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)

    def print(self):
        print(self.config)

    def getConfig(self):
        return self.config


class SQLConfig(Config):
    """Configuracion especifica para sql"""
    def __init__(self, file='config.yaml'):
        super(SQLConfig, self).__init__(file=file)
        try:
            self.db = self.config['db']
            self.table=self.config['table']
            self.preferences=self.config['preferences']
            self.table=self.config['table']
            self.mapping=self.config['mapping']
        except Exception as e:
            print("Error to load something in config file")
