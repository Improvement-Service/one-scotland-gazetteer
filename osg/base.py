import configparser
from pathlib import Path


class Configuration:

    file_name = 'development.ini'

    def __init__(self):
        self.file_path = [x for x in Path('../').iterdir() if x.name == self.file_name][0]

    def get_configuration_for(self, section, option):

        config = configparser.ConfigParser()
        config.read(self.file_path)

        return config.get(section, option)
