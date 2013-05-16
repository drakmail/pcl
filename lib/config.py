# -*- coding: utf-8 -*-

# Configuration library. Parses all config files and expose
# their data to the rest of script.

import os
import sys
import configparser

from lib import common

class Configuration:
    def __init__(self):
        # Create configparser instance.
        self.config = configparser.ConfigParser()
        # Load all configuration files from "config" directory.
        config_list = os.listdir(os.path.join(common.TEMP_SETTINGS["PCL_PATH"], "config"))
        config_list.sort()
        for item in config_list:
            if ".conf" in item:
                self.config.read(os.path.join(common.TEMP_SETTINGS["PCL_PATH"], "config", item))
            
    def get_config(self):
        """
        Return config dictitonary (configparser instance).
        """
        return self.config