'''
Created on 28.07.2016

@author: Jonas
'''
import json

from flask import request
from flask.wrappers import Response, Request
from pkg_resources import Requirement, resource_string, resource_filename
import yaml

config_path = "son_editor/config.yaml"
CONFIG = yaml.safe_load(resource_string(Requirement.parse("upb-son-editor-backend"), config_path))


def update_config(config):
    """
    Update the configuratiion file
         
    :param config: The new configuration
    :return: Message if successful
    """
    global CONFIG
    CONFIG = config
    filename = resource_filename(Requirement.parse("upb-son-editor-backend"), config_path)
    # write changed config
    with open(filename, "w") as stream:
        yaml.safe_dump(CONFIG, stream, default_flow_style=False)
    return {"message": "update successful"}


def get_config():
    """ Returns the current configuration"""
    return CONFIG


def prepare_response(data=None, code=200) -> Response:
    """
    Sets the necessary headers and status code on the response

    :param data: The data to be returned to the client
    :param code: the status code. 200 by default
    :return: The Response object with the headers set according to the input data
    """
    response = Response()
    headers = response.headers
    if _is_allowed_origin():
        headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    headers['Access-Control-Allow-Methods'] = "GET,POST,PUT,DELETE,OPTIONS"
    headers['Access-Control-Allow-Headers'] = "Content-Type, Authorization, X-Requested-With"
    headers['Access-Control-Allow-Credentials'] = "true"
    headers['Access-Control-Max-Age'] = 1000
    if data is not None:
        if isinstance(data, dict) or isinstance(data, list):
            response.set_data(json.dumps(data))
            headers['Content-Type'] = 'application/json'
        else:
            response.set_data(data)
            headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.status_code = code
    return response


def prepare_error(data=None, code=500) -> tuple:
    """
    Prepares the error response and returns it as a tuple
    to accommodate for flask_restplus's way to deal with errors

    :param data: The error message
    :param code: the http error code, 500 by default
    :return: A tuple of the data, the status code and the headers
    """
    response = Response()
    headers = response.headers
    if _is_allowed_origin():
        headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    headers['Access-Control-Allow-Methods'] = "GET,POST,PUT,DELETE,OPTIONS"
    headers['Access-Control-Allow-Headers'] = "Content-Type, Authorization, X-Requested-With"
    headers['Access-Control-Allow-Credentials'] = "true"
    headers['Access-Control-Max-Age'] = 1000
    return data, code, headers


def _is_allowed_origin():
    """Checks if the request originates from a known origin"""
    if 'Origin' in request.headers:
        # strip the http method because we are only interested in the host
        origin = request.headers['Origin'].replace("http://", "").replace("https://", "")
        # strip the port
        origin_parts = origin.split(":")
        if len(origin_parts) > 1:
            origin = origin_parts[0]
        return origin in CONFIG['allowed-hosts']
    return False


def get_json(request: Request) -> dict:
    """
    Helper function to get a json dict out of a request

    :param request: Request to get the json data from
    :return: json data as dict
    """
    json_data = request.get_json()
    if json_data is None:
        json_data = request.form
    if json_data is None:
        json_data = json.loads(request.get_data().decode("utf8"))
    return json_data


def rreplace(s, old, new, occurrence):
    """
    Replaces 'occurences' occurences of string 'old' in the given string 's' from right by 'new'

    :param s: String that contains the replacing string
    :param old: String that gets replaced
    :param new: New string that replaces the old string
    :param occurrence: How many occurences get replaced
    :return: String that has replaced strings
    """
    li = s.rsplit(old, occurrence)
    return new.join(li)
