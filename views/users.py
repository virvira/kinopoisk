from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from decorators import auth_required
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self):
        all_users = user_service.get_all()
        res = UserSchema(many=True).dump(all_users)
        return res, 200


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid):
        user = user_service.get_one(uid)

        if user is None:
            return {"error": "User not found"}, 404

        return UserSchema().dump(user), 200

    @auth_required
    def patch(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json['id'] = uid
        user_service.update(req_json)

        return "", 204

    # def put(self, uid):
    #     req_json = request.json
    #     req_json['id'] = uid
    #     user_service.update(req_json)
    #
    #     required_fields = [
    #             'username',
    #             'password',
    #             'role'
    #         ]
    #
    #     for field in required_fields:
    #         if field not in req_json:
    #             return {"error": f"Поле {field} обязательно"}, 400
    #
    #     return "", 204

    def delete(self, uid):
        user = user_service.get_one(uid)

        if user is None:
            return {"error": "Пользователь не найден"}, 404

        user_service.delete_one(uid)

        return "", 204


@user_ns.route('/<int:uid>/password')
class UserView(Resource):
    @auth_required
    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json['id'] = uid
        if "password_1" not in req_json or "password_2" not in req_json:
            return {"error": "Поля password_1 и password_2 обязательны"}, 400

        user_service.update_password(req_json)

        return "", 204
