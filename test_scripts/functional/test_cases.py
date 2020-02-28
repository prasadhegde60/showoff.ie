"""Python module for Rest API verification test cases.

Authors: Prasad Hegde
"""
import json
from workflows.workflows import Workflows
from framework.rest_api import Rest


class TestCases(Workflows):

    def setup_class(self):
        """
        Class level setup routine
        :return: None
        """
        pass

    def setup_method(self, test_method):
        """
        Test level setup routine
        :param test_method: Test method instance
        :return: None
        """
        self.wo_obj = TestCases()
        self.global_config, self.test_args = self.wo_obj.get_config_data(test_method=test_method.__name__)

    def teardown_method(self, test_method):
        """
        Test level teardown routine
        :param test_method: Test method instance
        :return: None
        """
        self.wo_obj = None
        self.config_data = None

    def test_check_email_endpoint(self, **kwargs):
        """
        This test is used to verify check email emdpoint - positive scenario
        :param kwargs: email_id, client_id, client_secret, url
        :return: HTTP Response obj if return_response_obj is True
        """
        email_id = kwargs.get('email_id', Workflows.generate_new_email(suffix=self.global_config["email_id_suffix"]))
        client_id = kwargs.get('client_id', self.global_config["client_id"])
        client_secret = kwargs.get('client_secret', self.global_config["client_secret"])
        relative_url = kwargs.get('url', self.test_args["relative_url"]).format(email_id, client_id, client_secret)

        restapi = Rest(base_uri=self.global_config["base_url"])
        response = restapi.get(relative_url=relative_url, **kwargs)
        if kwargs.get("return_response_obj", False):
            return response

        print("Verify Response body")
        assert json.loads(response.text)["data"]["available"] == self.test_args["expected_result"], "Test Failed"
        return None

    def test_check_email_endpoint_existing_email(self):
        """
        This test is used to verify check email endpoint for an exisisting email - Negative scenario
        :return: None
        """
        print("Create a new user")
        kwargs= {'return_response_obj': True}
        response = self.test_create_user_endpoint(**kwargs)
        email_id = json.loads(response.text)["data"]["user"]["email"]

        kwargs = {'email_id': email_id}
        response = self.test_check_email_endpoint(**kwargs)
        print("Response : {0}".format(response))

        print("Verify Response body")
        assert json.loads(response.text) == self.test_args["expected_result"], "Test Failed"

    def test_check_email_endpoint_incorrect_client_id_and_client_secret(self):
        """
        This test is used to verify check email endpoint when client_id ans client secret is incorrect - Negative
        :return: None
        """
        print("Incorrect Client ID")
        kwargs = {"client_id": self.test_args["client_id"], "return_response_obj": True, "return_failure_response": True}
        response = self.test_check_email_endpoint(**kwargs)

        print("Verify Response body")
        expected_result = self.test_args["expected_result"]
        actual_result = json.loads(response.text)
        assert actual_result == expected_result, "Test Failed.. Expected: {0}.. Actual: {1}".format(expected_result,
                                                                                                    actual_result)

        print("Incorrect Client Secret")
        kwargs = {"client_secret": self.test_args["client_secret"], "return_response_obj": True,
                  "return_failure_response": True}
        response = self.test_check_email_endpoint(**kwargs)

        print("Verify Response body")
        expected_result = self.test_args["expected_result"]
        actual_result = json.loads(response.text)
        assert actual_result == expected_result, "Test Failed.. Expected: {0}.. Actual: {1}".format(expected_result,
                                                                                                    actual_result)

        print("Incorrect Client id and client secret")
        kwargs = {"client_id": self.test_args["client_id"], "client_secret": self.test_args["client_secret"],
                  "return_response_obj": True, "return_failure_response": True}
        response = self.test_check_email_endpoint(**kwargs)

        print("Verify Response body")
        expected_result = self.test_args["expected_result"]
        actual_result = json.loads(response.text)
        assert actual_result == expected_result, "Test Failed.. Expected: {0}.. Actual: {1}".format(expected_result,
                                                                                                    actual_result)

    def test_check_email_endpoint_with_blank_values(self):
        """
        This test is used to verify check email endpoint by passing blank values to mandatory fields - Negative
        :return: None
        """
        print("Blank email id")
        kwargs = {"email_id": "", "return_response_obj": True, "return_failure_response": True}

        response = self.test_check_email_endpoint(**kwargs)

        print("Verify Response body")
        expected_result = self.test_args["expected_result"]
        actual_result = json.loads(response.text)["message"]
        assert actual_result == expected_result, "Test Failed.. Expected: {0}.. Actual: {1}".format(expected_result,
                                                                                                    actual_result)

        print("Blank client id")
        kwargs = {"client_id": "", "return_response_obj": True, "return_failure_response": True}
        response = self.test_check_email_endpoint(**kwargs)

        print("Verify Response body")
        expected_result = self.test_args["expected_result"]
        actual_result = json.loads(response.text)["message"]
        assert actual_result == expected_result, "Test Failed.. Expected: {0}.. Actual: {1}".format(expected_result,
                                                                                                    actual_result)

        print("Blank client secret")
        kwargs = {"client_secret": "", "return_response_obj": True, "return_failure_response": True}
        response = self.test_check_email_endpoint(**kwargs)

        print("Verify Response body")
        expected_result = self.test_args["expected_result"]
        actual_result = json.loads(response.text)["message"]
        assert actual_result == expected_result, "Test Failed.. Expected: {0}.. Actual: {1}".format(expected_result,
                                                                                                    actual_result)

    def test_create_user_endpoint(self, **kwargs):
        """
        This test is used to verify create user endpoint - Positive scenario
        :param kwargs: first_name, last_name, password, email
        :return: HTTPresponse obj if return_response_obj is set to True
        """
        first_name = kwargs.get('first_name', self.test_args["user_details"]["first_name"])
        last_name = kwargs.get('last_name', self.test_args["user_details"]["last_name"])
        password = kwargs.get('password', self.test_args["user_details"]["password"])
        email = kwargs.get('email', Workflows.generate_new_email(suffix=self.global_config["email_id_suffix"]))
        custom_data = {"first_name": first_name, "last_name": last_name, "password": password, "email": email}
        kwargs["data"] = {"user": custom_data, "client_id": self.global_config["client_id"],
                                  "client_secret": self.global_config["client_secret"]}

        restapi = Rest(base_uri=self.global_config["base_url"])
        response = restapi.post(**kwargs)

        if kwargs.get("return_response_obj", False):
            return response

        print("Verify Response body")
        assert json.loads(response.text)["message"] == self.test_args["expected_result"], "Test Failed"
        return None

    def test_create_user_endpoint_duplicate_user(self):
        """
        This test is used to verify create user endpoint by passing an already existing user email - Negative
        :return: None
        """
        kwargs = {'return_response_obj': True}
        response = self.test_create_user_endpoint(**kwargs)
        email = json.loads(response.text)["data"]["user"]["email"]

        kwargs = {"return_response_obj": True, "return_failure_response": True, "email": email}
        response = self.test_create_user_endpoint(**kwargs)

        print("Verify Response body")
        assert json.loads(response.text)["message"] == self.test_args["expected_result"], "Test Failed"

    def test_create_user_missing_mandatory_field_values(self):
        """
        This test is used to verify create user endpoint with missing mandatory field values - Negative
        :return: None
        """
        print("Missing First Name")
        kwargs = {"first_name":"", "return_response_obj": True, "return_failure_response": True}
        response = self.test_create_user_endpoint(**kwargs)

        print("Verify Response body")
        expected_result = self.test_args["expected_result"]["missing_first_name"]
        actual_result = json.loads(response.text)["message"]
        assert actual_result == expected_result, "Test Failed.. Expected: {0}.. Actual: {1}".format(expected_result,
                                                                                                    actual_result)

        print("Missing Last Name")
        kwargs = {"last_name": "", "return_response_obj": True, "return_failure_response": True}
        response = self.test_create_user_endpoint(**kwargs)

        print("Verify Response body")
        expected_result = self.test_args["expected_result"]["missing_last_name"]
        actual_result = json.loads(response.text)["message"]
        assert actual_result == expected_result, "Test Failed.. Expected: {0}.. Actual: {1}".format(expected_result,
                                                                                                    actual_result)

        print("Missing Password Name")
        kwargs = {"password": "", "return_response_obj": True, "return_failure_response": True}
        response = self.test_create_user_endpoint(**kwargs)

        print("Verify Response body")
        expected_result = self.test_args["expected_result"]["missing_password"]
        actual_result = json.loads(response.text)["message"]
        assert actual_result == expected_result, "Test Failed.. Expected: {0}.. Actual: {1}".format(expected_result,
                                                                                                    actual_result)

        print("Missing Email id")
        kwargs = {"email": "", "return_response_obj": True, "return_failure_response": True}
        response = self.test_create_user_endpoint(**kwargs)

        print("Verify Response body")
        expected_result = self.test_args["expected_result"]["missing_email"]
        actual_result = json.loads(response.text)["message"]
        assert actual_result == expected_result, "Test Failed.. Expected: {0}.. Actual: {1}".format(expected_result,
                                                                                                    actual_result)

    def test_update_user_endpoint(self, **kwargs):
        """
        This test is used to verify update user endpoint - Positive scenario
        :param kwargs: return_response_obj
        :return: HTTPresponse obj if return_response_obj is set to True
        """
        print("Create a new user")
        kwargs['return_response_obj'] = True
        response = self.test_create_user_endpoint(**kwargs)
        response = json.loads(response.text)

        print("Capture Authorization token")
        token_type = response["data"]["token"]["token_type"]
        access_token = response["data"]["token"]["access_token"]
        headers = {"Content-Type": "application/json", "Authorization": "{0} {1}".format(token_type, access_token)}
        kwargs['headers'] = headers

        print("Update the User")
        custom_data = Workflows.update_user_details(test_args=self.test_args, **kwargs)
        kwargs["data"] = {"user": custom_data}

        restapi = Rest(base_uri=self.global_config["base_url"])
        response = restapi.put(relative_url=self.test_args["relative_url"], **kwargs)

        if kwargs.get("return_response_obj", False):
            return response

        print("Verify Response body")
        assert json.loads(response.text)["message"] == self.test_args["expected_result"], "Test Failed"
        return None

    def test_update_user_endpoint_new_email(self):
        """
        This test is used to verify update user endpoint by passing a inactive email id - Negative
        :return: None
        """
        print("Generate a new email and check if email is not allocated")
        email_id = Workflows.generate_new_email(suffix=self.global_config["email_id_suffix"])
        kwargs = {'email_id': email_id, 'return_response_obj': True,
                  'url': self.test_args["relative_url_check_email"]}
        response = self.test_check_email_endpoint(**kwargs)
        assert json.loads(response.text)["data"]["available"] is True, "Unable to generate a new email id"

        print("Update email id")
        response = self.test_update_user_endpoint(**kwargs)

        print("Verify Response body")
        assert json.loads(response.text)["message"] == self.test_args["expected_result"], "Test Failed"

    def test_update_user_endpoint_existing_email(self, **kwargs):
        """
        This test is used to verify update user endpoint with existing email
        :param kwargs:
        :return: None
        """
        print("Create a new user and capture the email")
        kwargs['return_response_obj'] = True
        response = self.test_create_user_endpoint(**kwargs)
        email_id = json.loads(response.text)["data"]["user"]["email"]
        kwargs = {'email_id': email_id, 'return_response_obj': True, "return_failure_response": True,
                  'url': self.test_args["relative_url_check_email"]}

        print("Update email id")
        response = self.test_update_user_endpoint(**kwargs)

        print("Verify Response body")
        assert json.loads(response.text)["message"] == self.test_args["expected_result"], "Test Failed"

    def test_reset_password_endpoint(self, **kwargs):
        """
        This test is used to verify reset password endpoint - Positive scenario
        :param kwargs: email_id, client_id, client_secret
        :return: HTTPresponse if return_response_obj is set to True
        """
        email_id = kwargs.get("email_id", None)
        if not email_id:
            print("Create a new user and capture the email")
            things_to_edit= {"return_response_obj": True}
            response = self.test_create_user_endpoint(**things_to_edit)
            email_id = json.loads(response.text)["data"]["user"]["email"]

        client_id = kwargs.get("client_id", self.global_config["client_id"])
        client_secret = kwargs.get("client_secret", self.global_config["client_secret"])
        kwargs["data"] = {"user": {"email": email_id}, "client_id": client_id, "client_secret": client_secret}

        restapi = Rest(base_uri=self.global_config["base_url"])
        response = restapi.post(relative_url=self.test_args["relative_url"], **kwargs)

        if kwargs.get("return_response_obj", False):
            return response

        print("Verify Response body")
        expected_result = self.test_args["expected_result"].format(email_id)
        actual_result = json.loads(response.text)["message"]
        assert actual_result == expected_result, "Test Failed.. Expected: {0}.. Actual: {1}".format(expected_result,
                                                                                                    actual_result)
        return None

    def test_reset_password_endpoint_invalid_email(self):
        """
        This test is used to verify reset password endpoint by passing invalid email id
        :return: None
        """
        kwargs = {"email_id": self.test_args["invalid_email"], "return_response_obj": True,
                  "return_failure_response": True}
        response = self.test_reset_password_endpoint(**kwargs)

        print("Verify Response body")
        expected_result = self.test_args["expected_result"].format(self.test_args["invalid_email"])
        actual_result = json.loads(response.text)["message"]
        assert actual_result == expected_result, "Test Failed.. Expected: {0}.. Actual: {1}".format(expected_result,
                                                                                                    actual_result)

    def test_change_password_endpoint(self, **kwargs):
        """
        This test is used to verify change password endpoint - Positive scenario
        :param kwargs: current_password, new_password, return_response_obj
        :return: HTTPresponse obj if return_response_obj is set to True
        """
        print("Create a new user")
        things_to_edit = {"return_response_obj": True}
        response = self.test_create_user_endpoint(**things_to_edit)
        response = json.loads(response.text)

        print("Capture Authorization token")
        token_type = response["data"]["token"]["token_type"]
        access_token = response["data"]["token"]["access_token"]
        headers = {"Content-Type": "application/json", "Authorization": "{0} {1}".format(token_type, access_token)}
        kwargs['headers'] = headers

        current_password = kwargs.get("current_password", self.test_args["user_details"]["password"])
        new_password = kwargs.get("new_password", self.test_args["user_details"]["new_password"])
        kwargs["data"] = {"user": {"current_password": current_password, "new_password": new_password}}

        restapi = Rest(base_uri=self.global_config["base_url"])
        response = restapi.post(relative_url=self.test_args["relative_url"], **kwargs)

        if kwargs.get("return_response_obj", False):
            return response

        print("Verify Response body")
        expected_result = self.test_args["expected_result"]
        actual_result = json.loads(response.text)["message"]
        assert actual_result == expected_result, "Test Failed.. Expected: {0}.. Actual: {1}".format(expected_result,
                                                                                                    actual_result)
        return None

    def test_change_password_invalid_current_password(self):
        """
        This test is used to verify change password endpoint by passing invalid current password
        :return: None
        """
        kwargs = {"current_password": self.test_args["invalid_current_password"], "return_response_obj": True,
                  "return_failure_response": True}
        response = self.test_change_password_endpoint(**kwargs)

        print("Verify Response body")
        expected_result = self.test_args["expected_result"]
        actual_result = json.loads(response.text)["message"]
        assert actual_result == expected_result, "Test Failed.. Expected: {0}.. Actual: {1}".format(expected_result,
                                                                                                    actual_result)