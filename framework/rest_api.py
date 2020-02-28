# pylint: disable = too-many-branches
# pylint: disable = too-many-locals
# pylint: disable = no-member


"""Python module for initiating and executing commands via REST API.

Authors: Prasad Hegde
"""

#pylint

import time
import json
import requests


class Rest():
    """REST class for invoking REST calls GET, POST, PUT, DELETE.
      """

    # Constants representing REST API keys.
    HEADERS = "headers"
    DATA = "data"

    # Constants representing type of REST request
    GET = "get"
    POST = "post"
    DELETE = "delete"
    PUT = "put"

    #Constants representing response codes
    SUCCESS = 0
    FAILURE = 1

    def __init__(self, **kwargs):
        """This class defines methods to invoke REST calls.

        Args:
          base_uri(str,optional): URI for sending REST calls to.

        Returns
          Returns REST object instance.
        """
        self._base_uri = kwargs.get('base_uri', None)
        if self._base_uri is None:
            print("Base URI is not present in config")
            assert False

        #need to check this
        #auth = kwargs.get('auth', None)

    def get(self, relative_url=None, **kwargs):
        """This routine is used to invoke GET call for REST API.

        Args:
          relative_url: Relative URL for the particular API call.
          kwargs:
            headers(dict, optional): Custom headers for making the REST call.
              Default: {}
            data(dict, optional): Data to be send for making the REST call.
              Default: {}

        Returns:
          str: response text.
        """
        kwargs["operation"] = Rest.GET
        return self.__send_request(relative_url, **kwargs)

    def post(self, relative_url=None, **kwargs):
        """This routine is used to invoke POST call for REST API.

        Args:
          relative_url(str): Relative URL for the particular API call.
          kwargs:
            headers(str, optional): Custom headers for making the REST call.
              Default: {}
            data(str, optional): Data to be send for making the REST call.
              Default: {}

        Returns:
          str: response text.
        """
        kwargs["operation"] = Rest.POST
        return self.__send_request(relative_url, **kwargs)

    def delete(self, relative_url=None, **kwargs):
        """This routine is used to invoke DELETE call for REST API.

        Args:
          relative_url(str): Relative URL for the particular API call.
          kwargs:
            headers(str, optional): Custom headers for making the REST call.
              Default: {}.
            data(str, optional): Data to be send for making the REST call.
              Default: {}.

        Returns:
          str: response text.
        """
        kwargs["operation"] = Rest.DELETE
        return self.__send_request(relative_url, **kwargs)

    def put(self, relative_url=None, **kwargs):
        """This routine is used to invoke PUT call for REST API.

        Args:
          relative_url(str): Relative URL for the particular API call.
          kwargs:
            headers(str, optional): Custom headers for making the REST call.
              Default: {}
            data(str, optional): Data to be send for making the REST call.
              Default: {}

        Returns:
          str: response text.
        """
        kwargs["operation"] = Rest.PUT
        return self.__send_request(relative_url, **kwargs)

    def __send_request(self, relative_url, **kwargs):
        """
        Method which can be used to perform operations like post, get,
        patch, delete and put.

        Returns:
          http_response_obj : if kwargs['http_response'] is true else, str: Response text.


        """
        headers = kwargs.get(Rest.HEADERS, {"Content-Type": "application/json"})
        custom_data = kwargs.get(Rest.DATA, None)
        if not custom_data:
            custom_data = {}
        data = json.dumps(custom_data, indent=2)
        max_retries = kwargs.get('max_retires', 3)
        if not relative_url:
            main_uri = self._base_uri
        else:
            main_uri = "".join([self._base_uri, relative_url])
        req_type = kwargs.get("operation", None)
        if not req_type:
            raise ValueError("REST request type not specified.")
        timeout = kwargs.pop("timeout", 60)
        verify = kwargs.pop("verify", False)
        auth = kwargs.get('auth', None)

        retry_count = 1
        print(">> %s: %s, headers=%s, data=%s, authenticaion=%s" \
              % (req_type.upper(), main_uri, headers, data, auth))
        while retry_count <= max_retries:
            method_to_call = getattr(requests, req_type)
            response = method_to_call(main_uri, headers=headers, verify=verify,
                                      data=data, auth=auth, timeout=timeout)
            if response.status_code == requests.codes.OKAY:
                if kwargs.get("return_response_obj", True):
                    return response
                return_val = json.loads(response.text)
                print("<< %s" % json.dumps(return_val, indent=2))
                return return_val

            if kwargs.get("return_failure_response", False):
                return response

            if response.status_code == requests.codes.UNAUTHORIZED:
                print("UNAUTHORIZED ERROR(%s:%s). Please check given credentials: %s" \
                      % (response.status_code, response.text, auth))

            if response.status_code == requests.codes.BAD_REQUEST:
                api_used = "req_type= %s, url=%s, headers=%s, data=%s, auth=%s" \
                           % (req_type, main_uri, headers, data, auth)
                print("BAD REQUEST(%s): api = %s" % (response.status_code, api_used))

            if response.status_code == requests.codes.UNSUPPORTED_MEDIA_TYPE:
                message = "%s: Check if the request has been serialized before sending" \
                          % response.status_code
                print("UNSUPPORTED MEDIA TYPE %s" % message)

            if response.status_code == requests.codes.INTERNAL_SERVER_ERROR:
                message = "[%s:%s]." % (response.status_code, response.text)
                print("INTERNAL SERVER ERROR %s" % message)

            if retry_count == max_retries:
                print("RESTError: %s response: %s" % (req_type, response.text))
                print("Reached max retries: %s waiting for proper %s response. "\
                      "Response:[%s:%s] " %(max_retries, req_type, response.status_code,
                                            response.text))
                assert False
            retry_count = retry_count + 1
            time.sleep(5)
