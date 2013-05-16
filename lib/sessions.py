# -*- coding: utf-8 -*-

# Session controller. Generates and checks sessions.
import hashlib
import os

from http import cookies

from lib import common

class Session:
    def __init__(self):
        if "HTTP_COOKIE" in os.environ:
            self.cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
        else:
            self.cookie = cookies.SimpleCookie()

        common.set_session(self)

    def get_cookie(self):
        """
        Returns cookie contents.
        """
        return self.cookie

    def generate_session(self, username, password_hash, ip_address, user_agent, expiration_timeout):
        """
        Generates a sha256 hash of username, password, ip address and
        browser string.
        """
        # Okay, here we go. Let's generate sha256 of each parameter
        # we got.
        username = hashlib.sha256(username.encode()).hexdigest()
        password_hash = hashlib.sha256(password_hash.encode()).hexdigest()
        ip_address = hashlib.sha256(ip_address.encode()).hexdigest()
        user_agent = hashlib.sha256(user_agent.encode()).hexdigest()
        expiration_timeout = hashlib.sha256(expiration_timeout.encode()).hexdigest()
        # Making a one big line wish hashes and HASH THEM!
        # Look at "doc/session_generator.png" for complete
        # diagram of this process.
        the_string = username + password_hash + ip_address + user_agent + expiration_timeout
        session_string = hashlib.sha256(the_string.encode()).hexdigest()
        return session_string

    def put_session_in_cookie(self, username, session_hash, expiration_timeout):
        """
        Generate cookies list for later inclusion in templates. Nuff said.
        """
        self.cookie = ["name={name}; domain=.{domain}; path=/; expires={expires}".format(domain = common.SETTINGS["main"]["cookie_domain"], expires = expiration_timeout, name = username), "hash={hash}; domain=.{domain}; path=/; expires={expires}".format(domain = common.SETTINGS["main"]["cookie_domain"], expires = expiration_timeout, hash = session_hash)]
        return self.cookie

    def get_login_state(self):
        """
        Checks for login state and return list:
        [login_state (boolean), username, user id]
        """
        try:
            # Get cookie data.
            user_id = self.cookie["name"].value
            session_hash = self.cookie["hash"].value
            user_ip = os.environ["REMOTE_ADDR"]
            user_agent = os.environ["HTTP_USER_AGENT"]
            # Check cookie information for validness.
            stored_session = common.DATABASE.get_session_data(user_id)
            if stored_session[2] == session_hash and stored_session[3] == user_ip and stored_session[4] == user_agent:
                username = common.DATABASE.get_username_by_id(user_id)
                print("Session confirmed for", username)
                # Avatar.
                data = common.DATABASE.get_specified_user(user_id)
                avatar = "http://gravatar.com/avatar/" + hashlib.md5(data[2].encode()).hexdigest()
                return (True, username, user_id, avatar)
            else:
                return (False, "Not logged in", 0, None)
        except:
            # Raises when no cookie data present.
            return (False, "Not logged in", 0, None)

    def remove_session_by_user_id(self, user_id):
        """
        Remove session from database for given user ID.
        """
        common.DATABASE.remove_session_by_user_id(user_id)