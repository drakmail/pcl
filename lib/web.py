# -*- coding: utf-8 -*-

# HTML renderer module.
import os
import sys
import codecs

from lib import common

import cgi
import cgitb
cgitb.enable(display = 1, logdir = os.path.join(common.TEMP_SETTINGS["PCL_PATH"], "logs"))

from thirdparty.tenjin import tenjin
from tenjin.helpers import *

class Web:
    """
    """
    def __init__(self):
        self.engine = tenjin.Engine(path = [os.path.join(common.TEMP_SETTINGS["PCL_PATH"], "public", "templates")], trace = True)
        # Force cache storage to memory, to keep clean templates directory.
        tenjin.Engine.cache = tenjin.MemoryCacheStorage()
        tenjin.set_template_encoding("utf-8")
        self.template_name = ""
        
    def print_output(self, data, template = "index.pyhtml"):
        """
        Print generated output as webpage.
        """
        try:
            # Variables.
            # Site name.
            if not "site_name" in data:
                data["site_name"] = common.SETTINGS["main"]["site_name"]
            # Page title, used for <TITLE> tag.
            if not "title" in data:
                data["title"] = common.SETTINGS["main"]["site_name"]
            # Sometimes we need to hide navigation bar.
            if not "hide_navbar_links" in data:
                data["hide_navbar_links"] = False
            # Login state.
            if not "logged_in" in data:
                data["logged_in"] = common.SESSION.get_login_state()
            # Will we require authorization? No by default!
            auth_required = False
            # IP address
            if not "ip_address" in data:
                data["ip_address"] = common.parse_parameters()[1]
            # Site root directory. In rare cases we have to override it.
            if not "root" in data:
                data["root"] = "/"
            # Current path.
            if not "current_path" in data:
                data["current_path"] = os.environ["REQUEST_URI"]
            # Version.
            if not "pcl_version" in data:
                data["pcl_version"] = common.TEMP_SETTINGS["PCL_VERSION"]
            if not "page_data_here" in data:
                data["page_data_here"] = False

            # Admin email.
            data["admin_email"] = common.SETTINGS["main"]["admin_email"]

            # Set template name for proper exceptions handling.
            self.template_name = template

            # We do not need links in errors templates.
            if not "error" in template:
                if not "action" in data:
                    if not common.parse_parameters()[0]["module"]:
                        link_action = "home"
                    else:
                        link_action = common.parse_parameters()[0]["module"]
                else:
                    link_action = data["action"]

                links = common.TEMP_SETTINGS["links_formatter"].get_links(link_action)
                data["links"] = links

            # Print "Not authorized" error if no authorization found and we require it.
            if not data["logged_in"][0] and common.TEMP_SETTINGS["AUTH_REQUIRED"]:
                # Set template name for proper exceptions handling.
                self.template_name = "not_authorized.pyhtml"
                # Modify TITLE tag.
                data["title"] = common.SETTINGS["main"]["site_name"] + " - 401 aka Authorization Required"
                html = self.engine.render("not_authorized.pyhtml", data)
                common.set_response(html)
                if os.getenv("PCL_SUPPRESS_PRINT_TO_CONSOLE") != "1":
                    sys.stdout.buffer.write(html.encode("utf-8"))
            else:
                # Trying to format page data
                if data["page_data_here"]:
                    try:
                        page_data = data["page_data"]
                        page_data = str(page_data).format(**data)
                        data["page_data"] = page_data.encode("utf-8")
                    except KeyError as e:
                        # This exception raises only when "page_data"
                        # item not found in "data" dictionary and
                        # if module's developer sets "page_data_here"
                        # variable to "True". This is really GENIOUS,
                        # but anyway we have to print eye-candy
                        # exception for this.
                        # Set template name for proper exceptions handling.
                        self.template_name = "generic_error.pyhtml"
                        error_data = {
                            "site_name"     : common.SETTINGS["main"]["site_name"] + " - We got an error!",
                            "template_name" : e.args[0].split(":")[0],
                            "error_header"  : "Page data not found",
                            "error_name"    : "PageDataNotFound",
                            "error_message" : "PCL failed to get '" + e.args[0] + "' for page '" + data["action"] + "'!"
                        }
                        data.update(error_data)
                        html = self.engine.render("generic_error.pyhtml", data)
                        common.set_response(html)
                        if os.getenv("PCL_SUPPRESS_PRINT_TO_CONSOLE") != "1":
                            sys.stdout.buffer.write(html.encode("utf-8"))

                # Print HTML page.
                html = self.engine.render(template, data)
                common.set_response(html)
                if os.getenv("PCL_SUPPRESS_PRINT_TO_CONSOLE") != "1":
                    sys.stdout.buffer.write(html.encode("utf-8"))
        except tenjin.TemplateNotFoundError as e:
            # This exception raises only when template file not found.
            # Set template name for proper exceptions handling.
            self.template_name = "template_error.pyhtml"
            error_data = {
                "site_name"     : common.SETTINGS["main"]["site_name"] + " - Templates not found!",
                "template_name" : e.args[0].split(":")[0],
                "error_name"    : "TemplateNotFound",
                "error_message" : e.args[0]
            }
            data.update(error_data)
            html = self.engine.render("template_error.pyhtml", data)
            common.set_response(html)
            if os.getenv("PCL_SUPPRESS_PRINT_TO_CONSOLE") != "1":
                sys.stdout.buffer.write(html.encode("utf-8"))
        except NameError as e:
            error_data = {
                "site_name" : common.SETTINGS["main"]["site_name"] + " - Templates error found!",
                "template_name" : self.template_name,
                "error_name"    : "NameError",
                "error_message" : e

            }
            data.update(error_data)
            html = self.engine.render("template_error.pyhtml", data)
            common.set_response(html)
            if os.getenv("PCL_SUPPRESS_PRINT_TO_CONSOLE") != "1":
                sys.stdout.buffer.write(html.encode("utf-8"))