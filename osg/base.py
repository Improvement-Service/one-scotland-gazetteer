import configparser
from pathlib import Path


class Configuration:

    file_name = 'development.ini'

    def __init__(self):
        # The file path targeting the configuration file. The file path is converted to string so it can be used in
        # different Python 3.x versions.
        self.file_path = [str(path) for path in Path('../').iterdir() if path.name == self.file_name][0]

    def get_configuration_for(self, section, option):

        config = configparser.ConfigParser()
        config.read(self.file_path)

        return config.get(section, option)
