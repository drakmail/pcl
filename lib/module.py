# -*- coding: utf-8 -*-

# Modules metaclass
import os
import sys
import cgi

from lib import common
from lib import database
from lib import sessions
from lib import web

class PCL_Module:
    def __init__(self):
        self.renderer = web.Web()
        self.parameters = common.parse_parameters()
        self.config = common.SETTINGS
        self.temp_config = common.TEMP_SETTINGS
        self.pcl_version = common.TEMP_SETTINGS["PCL_VERSION"]
        self.database = database.Database(self.config)
        self.session = sessions.Session()
        
        if not "PCL_IN_WSGI_MODE" in os.environ:
            self.fields = cgi.FieldStorage(keep_blank_values = True)
        else:
            self.fields = cgi.parse_qs(os.environ["wsgi.input"], keep_blank_values = True)
        
        try:
            self.language = os.environ["HTTP_ACCEPT_LANGUAGE"].split("-")[0]
        except:
            self.language = "en"

        # By default we don't need authorization.
        self.set_temp_setting("AUTH_REQUIRED", False)

    def read_file(self, path):
        """
        Read file by path and return it's contents.

        Note: there is language-specific behaviour, e.g. we will try
        to read file 'file.ru', if your system language - Russian.
        If we can't - we will read 'file.en'.
        """
        file_data = open(path, "rb").read().decode("utf-8")

        return file_data

    def get_field_value(self, field):
        """
        Returns value of field.
        """
        if not "PCL_IN_WSGI_MODE" in os.environ:
            return self.fields.getvalue(field)
        else:
            return self.fields[field][0]

    def set_temp_setting(self, option, value):
        """
        Sets temporary option.
        """
        common.set_temp_setting(option, value)