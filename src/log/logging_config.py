import logging.config
import os

import yaml

dir_path = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(dir_path, "logging_config.yaml")


with open(config_file, "rt") as f:
    config = yaml.safe_load(f.read())


logging.config.dictConfig(config)
logger = logging.getLogger("development")
