import jwt
from flask import request
from flask_restx import Resource, Namespace, abort

from constants import PWD_HASH_SALT
from dao.model.user import UserSchema
from decorators import auth_required
from implemented import user_service

user_ns = Namespace('user')


@user_ns.route('/')
class UserView(Resource):
    @auth_required
    def get(self):
        req_header = request.headers['Authorization']

        user_email = user_service.get_user_email_from_header(req_header)

        if user_email is None:
            abort(401)

        user = user_service.get_by_email(user_email)

        if user is None:
            return {"error": "User not found"}, 404

        return UserSchema().dump(user), 200

    @auth_required
    def patch(self):
        req_json = request.json
        req_header = request.headers['Authorization']

        user_email = user_service.get_user_email_from_header(req_header)

        if user_email is None:
            abort(401)

        user = user_service.get_by_email(user_email)

        if "id" not in req_json:
            req_json['id'] = user.id
        user_service.update(req_json)

        return "", 204


@user_ns.route('/password')
class UserView(Resource):
    @auth_required
    def put(self):
        req_json = request.json
        req_header = request.headers['Authorization']

        user_email = user_service.get_user_email_from_header(req_header)

        if user_email is None:
            abort(401)

        user = user_service.get_by_email(user_email)

        if "id" not in req_json:
            req_json['id'] = user.id
        if "password_1" not in req_json or "password_2" not in req_json:
            return {"error": "Поля password_1 и password_2 обязательны"}, 400

        user_service.update_password(req_json)

        return "", 204
