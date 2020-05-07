from flask import request, make_response, jsonify
from flask.views import MethodView

from src import bcrypt, db


class BaseAPI(MethodView):
    """ Base class for other resources """

    def get(self, Class, fail_msg, query_kwargs, attributes):
        objects = list(Class.query.filter_by(**query_kwargs))
        responseCode = 200
        responseObject = {"status": "success", "data": {}}

        if len(objects) == 0:
            responseCode = 404
            responseObject["status"] = "failed"
            responseObject["message"] = fail_msg

        responseObject["data"] = []

        for class_object in objects:
            responseObject["data"].append(self.object_to_dict(class_object, attributes))
        return make_response(jsonify(responseObject)), responseCode

    def object_to_dict(self, class_object, attributes):
        """ Returns a dictionary representation of the object.
        :param None:
        :return: dict
        """
        return dict(
            (key, class_object.__dict__[key])
            for key in attributes
            if key in class_object.__dict__
        )