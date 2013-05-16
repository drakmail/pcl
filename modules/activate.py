# -*- coding: utf-8 -*-

# Activation module.

from lib.module import PCL_Module

class ActivateModule(PCL_Module):
    def __init__(self):
        PCL_Module.__init__(self)

    def execute(self):
        """
        Execute it!
        """
        activation_hash = self.parameters[0]["id"]
        if not activation_hash:
            self.no_activation_hash_supplied()
        else:
            # Get user_id for specified hash
            user_id = self.database.get_userid_by_activation_hash(activation_hash)
            if user_id == "ACTIVATION_HASH_NOT_FOUND":
                self.bad_activation_hash()
            else:
                user_name = self.database.get_username_by_id(user_id)
                self.database.set_user_activated(user_id)

                data = {
                    "title"     : self.config["main"]["site_name"] + " - User activation",
                    "user_name"   : user_name
                }

                self.renderer.print_output(data, template = "activate.pyhtml")

    def no_activation_hash_supplied(self):
        """
        Produces an error about insupplying activation hash.
        """
        data = {
            "site_name"     : self.config["main"]["site_name"] + " - We got an error!",
            "template_name" : "",
            "error_header"  : "Activation hash not supplied",
            "error_name"    : "ActivationHashNotSupplied",
            "error_message" : "You forgot to supply activation hash!"
        }
        self.renderer.print_output(data, template = "generic_error.pyhtml")

    def bad_activation_hash(self):
        """
        Produces an error about inability to find supplied activation
        hash.
        """
        data = {
            "site_name"     : self.config["main"]["site_name"] + " - We got an error!",
            "template_name" : "",
            "error_header"  : "Activation hash not found",
            "error_name"    : "ActivationHashNotFound",
            "error_message" : "PCL can't find supplied activation hash! \
                                Usually, that means next: you never \
                                register on this site. Or supplied hash \
                                has expired."
        }
        self.renderer.print_output(data, template = "generic_error.pyhtml")