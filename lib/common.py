# -*- coding: utf-8 -*-

# Common module. Contains configuration settings and something
# more.
import os
import sys

# Parsed configuration.
SETTINGS = {}

TEMP_SETTINGS = {}

HTML_RESPONSE = ""

DATABASE = ""

SESSION = ""

def set_settings_dict(settings):
    """
    Set settings dictionary (configparser instance). Nuff said.
    """
    global SETTINGS
    SETTINGS = settings
    
def set_pcl_path(path):
    """
    Sets script-wide accessible path of script.
    """
    global TEMP_SETTINGS
    TEMP_SETTINGS["PCL_PATH"] = path

def set_version(version_string):
    """
    Sets PCL version.
    """
    global TEMP_SETTINGS
    TEMP_SETTINGS["PCL_VERSION"] = version_string

def set_linksformatter(lf_instance):
    """
    Sets links_formatter instance for easy access from "web" module.
    """
    global TEMP_SETTINGS
    TEMP_SETTINGS["links_formatter"] = lf_instance

def set_response(response):
    """
    Sets script-wide accessible response for usage in (u)WSGI.
    """
    global HTML_RESPONSE
    HTML_RESPONSE = response

def set_database(database):
    """
    Sets database module instance for libraries usage.
    """
    global DATABASE
    DATABASE = database

def set_session(session):
    """
    Sets session module instance for libraries usage.
    """
    global SESSION
    SESSION = session

def set_temp_setting(option, value):
    """
    Sets temporary option.
    """
    global TEMP_SETTINGS
    TEMP_SETTINGS[option] = value

def parse_parameters():
    """
    Parse parameters.
    """
    global TEMP_SETTINGS
    if "REQUEST_URI" in os.environ:
        params = os.environ["REQUEST_URI"].split("/")
        ipaddr = os.environ["REMOTE_ADDR"]
    else:
        # Looks like, we starting PCL from commandline.
        # As a program. In debugging purposes. GENIOUS! But we
        # have to FAKE these parameters. Sorry.
        params = sys.argv
        ipaddr = "127.0.0.1"

    if len(params) > 1:
        module = params[1]
    else:
        module = None
    if len(params) > 2:
        id = params[2]
    else:
        id = None
    if len(params) > 3:
        operation = params[3]
    else:
        operation = None

    if module == None:
        module = "home"

    TEMP_SETTINGS["REQUESTED_URL"] = {
        "module"    : module,
        "id"        : id,
        "operation" : operation
    }

    TEMP_SETTINGS["REMOTE_ADDR"] = ipaddr
    #print(TEMP_SETTINGS["REQUESTED_URL"])

    # Returning a tuple of "REQUESTED_URI" and "REMOTE_ADDR".
    return(TEMP_SETTINGS["REQUESTED_URL"], TEMP_SETTINGS["REMOTE_ADDR"])