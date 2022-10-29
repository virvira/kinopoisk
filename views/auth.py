import calendar
import datetime

from flask import request
from flask_restx import Resource, Namespace, abort

from dao.model.user import User
from implemented import user_service
from setup_db import db
import jwt

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        username = req_json.get('username')
        password = req_json.get('password')
        if None in [username, password]:
            abort(400)

        tokens = user_service.auth_user(username, password)

        if tokens is None:
            return {"error": "Неверные учётные данные"}, 401

        return tokens, 201


@auth_ns.route('/<int:aid>')
class AuthView(Resource):
    def put(self, uid):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(400)

        tokens = user_service.get_tokens(refresh_token)

        if tokens is None:
            return {"error": "Неверные учётные данные"}, 401

        return tokens, 201
