"""Python module for common workflows and library methods.

Authors: Prasad Hegde
"""

import os
import json
import pathlib
import inspect
import random
import string


class Workflows():
    """
    Common Workflows and library methods
    """
    def get_config_data(self, test_method):
        """
        This routine retuns the config data specific to the test case
        :param test_method: Name of the test method
        :return: tuple containing global_config and test_args
        """
        path = pathlib.Path(inspect.getfile(self.__class__)).parent.absolute()
        config_path = os.path.join(path, "config.json")
        with open(config_path) as f_in:
            config_data = json.load(f_in)
            return config_data["global_config"], config_data["test_args"][self.__class__.__name__]\
                                                            [test_method]

    @staticmethod
    def generate_new_email(length=16, suffix=None):
        """
        This routine generates a new email id
        :param length: Length of the email(int)
        :param suffix: domain(str)
        :return: email id (str)
        """
        retval = ''.join(random.choice(string.ascii_lowercase + string.digits) \
                         for i in range(length))
        return retval + suffix if suffix else retval

    @staticmethod
    def verify_response_header(expected_header, actual_header):
        """
        This routine is used to validate expected response header against actual
        :param expected_header: dict
        :param actual_header: dict
        :return: Boolean
        """
        if not any(item in actual_header.items() for item in expected_header.items()):
            return False
        return True

    @staticmethod
    def verify_response_time(expected_response_time, actual_response_time):
        """
        This routine is used to verify response time of api call
        :param actual_response_time: sec
        :return: Boolean
        """
        if actual_response_time <= expected_response_time:
            return True
        return False

    @staticmethod
    def update_user_details(test_args, **kwargs):
        """
        This Routine is used to build user details
        :param test_args: test args of the test method
        :param kwargs: first_name, last_name, dob, image_url, email_id
        :return: user data (dict)
        """
        first_name = kwargs.get('first_name', test_args["updated_user_details"]["first_name"])
        last_name = kwargs.get('last_name', test_args["updated_user_details"]["last_name"])
        dob = kwargs.get('dob', test_args["updated_user_details"]["dob"])
        image_url = kwargs.get('image_url', test_args["updated_user_details"]["image_url"])
        email = kwargs.get('email_id', None)
        user_data = {"first_name": first_name, "last_name": last_name, "date_of_birth": dob,
                     "image_url": image_url}
        if email:
            user_data["email"] = email

        return user_data
