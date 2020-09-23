# region - Imports
import re
from collections import namedtuple
# endregion

# region - Classes
class configHandler:
    # region - Dunder methods

    """
    Config settings: dict(configName : (regex, requestMessage))
    Filepath: The path of the configuration file
    """
    def __init__(self, configSettings: dict, filepath: str = "config.cfg", keyValueSeparator: str = "="):
        configSet = namedtuple("configSet", "regex requestMessage")
        self.filepath = filepath
        self.keyValueSeparator = keyValueSeparator
        # Convert the tuples to namedtuples for easy and readable access
        try:
            self.configSettings = {}
            for key, value in configSettings.items():
                self.configSettings[key] = configSet(*value)
        except:
            raise Exception("Invalid configuration settings given")
        self.cfg = {}

    """
    def __iter__(self):
        return iter(self.cfg)

    def __next__(self):
        return next(self.cfg)

    def items(self):
        return self.cfg.items()

    def get(self, key: str, default = None):
        return self.cfg.get(key, default)
    """

    # endregion

    # region - Methods

    # Requests the user to set all the configuration values properly if not given
    def setUserConfigs(self):
        # Set all the config values to None
        # If cfg[key] remains None then request that from the user
        for key in self.configSettings.keys():
            self.cfg[key] = None

        # Read correct data into the cfg storage
        try:
            with open(self.filepath, "r") as f:
                # [[key, value], [key, value], ...]
                configs = [line.split(self.keyValueSeparator, 1) for line in f.readlines()]

                # Checks the key and the value against configuration requirements
                for config in configs:
                    try:
                        key, value = (x.strip() for x in config)
                        if re.match(self.configSettings[key].regex , value):
                            self.cfg[key] = value
                    except:
                        # If fails then something is not in the right format so leave the config value None
                        pass
        except:
            # If the file open fails then every config value should remain None
            pass

        for key, value in self.cfg.items():
            # If the value is not set get it from the user
            if value is None:
                while not re.match(self.configSettings[key].regex, "" if value == None else value):
                    value = input(self.configSettings[key].requestMessage)
                self.cfg[key] = value

        # Rewrite the config file with the correct values in the configuration object
        with open(self.filepath, "w") as f:
            for key, value in self.cfg.items():
                f.write(f"{key}{self.keyValueSeparator}{value}\n")
        
        # Set attributes for easy access (like cfg.monitoredFolder)
        for key, value in self.cfg.items():
            try:
                setattr(self, key, float(value))
            except:
                setattr(self, key, value)

    # endregion

# endregion
