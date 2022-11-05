import calendar
import datetime

from flask import request
from flask_restx import Resource, Namespace, abort

from dao.model.user import User
from implemented import user_service
from setup_db import db
import jwt

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthView(Resource):
    """Создаём пользователя по переданным данным"""
    def post(self):
        req_json = request.json
        try:
            user = user_service.create(req_json)
            return "", 201, {"location": f"/users/{user.id}"}
        except Exception as e:
            return {"error": f"{e}"}, 400


@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get('email')
        password = req_json.get('password')
        if None in [email, password]:
            abort(400)

        tokens = user_service.auth_user(email, password)

        if tokens is None:
            return {"error": "Неверные учётные данные"}, 401

        return tokens, 201

    def put(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(400)

        tokens = user_service.check_refresh_token(refresh_token)

        if tokens is None:
            return {"error": "Неверные учётные данные"}, 401

        return tokens, 201


# @auth_ns.route('/<int:aid>')
# class AuthView(Resource):
#     def put(self, uid):
#         req_json = request.json
#         refresh_token = req_json.get("refresh_token")
#         if refresh_token is None:
#             abort(400)
#
#         tokens = user_service.check_refresh_token(refresh_token)
#
#         if tokens is None:
#             return {"error": "Неверные учётные данные"}, 401
#
#         return tokens, 201
