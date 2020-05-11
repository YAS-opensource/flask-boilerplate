from flask import request, make_response, jsonify
from flask.views import MethodView

from src import bcrypt, db


class BaseAPI(MethodView):
    """ Base class for other resources """

    def get(self, Class, attributes, status_kwargs, query_kwargs):
        objects = list(Class.query.filter_by(**query_kwargs))
        responseCode = status_kwargs["success_code"]
        responseObject = {"status": "success", "data": {}}

        if len(objects) == 0:
            responseCode = status_kwargs["fail_code"]
            responseObject["status"] = "fail"
            responseObject["message"] = status_kwargs["fail_msg"]

        responseObject["data"] = []

        for class_object in objects:
            responseObject["data"].append(self.object_to_dict(class_object, attributes))
        return make_response(jsonify(responseObject)), responseCode

    def post(self, Class, attributes, process_func, status_kwargs):
        post_data = request.get_json()
        responseCode = status_kwargs["success_code"]
        responseObject = {"status": "success", "data": {}}

        try:
            for key in post_data:
                if key not in attributes:
                    raise KeyError
            processed_data = process_func(request)
            if isinstance(processed_data, dict):
                class_object = Class(**processed_data)
                db.session.add(class_object)
                db.session.commit()
            else:
                status_kwargs["fail_code"] = processed_data[0]
                status_kwargs["fail_msg"] = processed_data[1]
                raise Exception()
        except Exception as e:
            responseCode = status_kwargs["fail_code"]
            responseObject["status"] = "failed"
            responseObject["message"] = status_kwargs["fail_msg"]

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
