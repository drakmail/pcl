# -*- coding: utf-8 -*-

# Database module.
import os
import time

from lib import common

try:
    import pymysql
except:
    print("No pymysql module found<br>")
    print("Please, install pymysql with:<br><br>")
    print("<code>    # pip install pymysql</code><br><br>")
    print("Or use your package manager. Or even you can get source of pymysql here:")
    print("<a href='https://github.com/petehunt/PyMySQL/'>https://github.com/petehunt/PyMySQL/</a>")
    exit()

class Database:
    def __init__(self, config):
        self.hostname = config["mysql"]["host"]
        self.username = config["mysql"]["username"]
        self.password = config["mysql"]["password"]
        self.database = config["mysql"]["database"]
        self.database_prefix = config["mysql"]["database_prefix"]

        # Sometimes we need it. Really.
        common.set_database(self)
        
        try:
            self.connection = pymysql.connect(host = self.hostname, user = self.username, passwd = self.password, db = self.database, use_unicode = True, charset = "utf8")
        except pymysql.err.OperationalError as e:
            print("Can't connect to {0}@{1} (111).".format(self.username, self.hostname))

        self.cursor = self.connection.cursor()

    def add_user(self, username, password_hash, email):
        """
        Inserts user into "users" database.
        Also inserts entry into "notifications" database for
        user activation.
        """
        # Inserting into users database
        try:
            self.cursor.execute("INSERT INTO `users` (login, password, email, register_date, activated) VALUES (%s, %s, %s, %s, %s)", (username, password_hash, email, int(time.time()), 0))
            user_id = self.cursor.lastrowid
            # Generating random string for activation.
            self.connection.commit()
            return user_id
        except pymysql.err.IntegrityError:
            return "USER_EXISTS"

    def add_activation(self, user_id, activation_hash):
        """
        Adds activation to database.
        """
        self.cursor.execute("INSERT INTO `activations` (user_id, hash) VALUES (%s, %s)", (user_id, activation_hash))
        self.connection.commit()

    def get_userid_by_activation_hash(self, activation_hash):
        """
        Returns user id and user name by activation hash.
        """
        self.cursor.execute("SELECT user_id FROM `activations` WHERE hash=%s", activation_hash)
        try:
            return self.cursor.fetchone()[0]
        except:
            return "ACTIVATION_HASH_NOT_FOUND"

    def get_userid_by_login(self, login):
        """
        Returns user ID for specified login.
        """
        self.cursor.execute("SELECT id FROM `users` WHERE login=%s", login)
        try:
            return self.cursor.fetchone()[0]
        except:
            return "USERNAME_NOT_EXIST"

    def get_username_by_id(self, user_id):
        """
        Returns username by id.
        """
        self.cursor.execute("SELECT login FROM `users` WHERE id=%s", user_id)
        return self.cursor.fetchone()[0]

    def set_user_activated(self, user_id):
        """
        Set user activation state to "1" (activated).
        """
        self.cursor.execute("UPDATE `users` SET activated=1 WHERE id=%s", user_id)
        self.cursor.execute("DELETE FROM `activations` WHERE user_id=%s", user_id)
        self.connection.commit()

    def get_all_users(self):
        """
        Returns complete list of users.
        """
        self.cursor.execute("SELECT * FROM `users`")
        return self.cursor.fetchall()

    def get_specified_user(self, user_id):
        """
        Returns complete info about user, selected by id.
        """
        self.cursor.execute("SELECT * FROM `users` WHERE id=%s", user_id)
        return self.cursor.fetchone()

    def get_password(self, username):
        """
        Returns username's password in hash.
        """
        self.cursor.execute("SELECT password FROM `users` WHERE login=%s", username)
        return self.cursor.fetchone()[0]

    def get_activation_status(self, username):
        """
        Returns activation status of specified user.
        """
        self.cursor.execute("SELECT activated FROM `users` WHERE login=%s", username)
        return self.cursor.fetchone()[0]

    def put_session_for_user_id(self, user_id, session_hash, ip_address, user_agent, expiration_timestamp):
        """
        Put new session for user.
        """
        # Lets try to delete previous user session.
        try:
            self.cursor.execute("DELETE FROM `user_sessions` WHERE user_id=%s", user_id)
            self.connection.commit()
        except:
            pass

        self.cursor.execute("INSERT INTO `user_sessions` (user_id, session_hash, ip_address, browser, expire) VALUES (%s, %s, %s, %s, %s)", (user_id, session_hash, ip_address, user_agent, expiration_timestamp))
        self.connection.commit()

    def remove_session_by_user_id(self, user_id):
        """
        Remove session from database for given user ID.
        """
        self.cursor.execute("DELETE FROM `user_sessions` WHERE user_id=%s", user_id)
        self.connection.commit()

    def get_session_data(self, user_id):
        """
        Returns session hash for given user ID.
        """
        self.cursor.execute("SELECT * from `user_sessions` WHERE user_id=%s", user_id)
        return self.cursor.fetchall()[0]