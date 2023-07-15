from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
# from decorators import auth_required
from implemented import movie_service
from constants import ITEMS_PER_PAGE

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    # @auth_required
    def get(self):
        page = request.args.get('page')
        status = request.args.get('status')
        filters = {
            'status': status
        }
        all_movies = movie_service.get_all(filters)
        res = MovieSchema(many=True).dump(all_movies)
        if page:
            page = int(page)-1
            res = res[page*ITEMS_PER_PAGE:(page+1)*ITEMS_PER_PAGE]

        return res, 200

    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return '', 201, {'location': f'/movies/{movie.id}'}


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    # @auth_required
    def get(self, bid):
        b = movie_service.get_one(bid)
        sm_d = MovieSchema().dump(b)
        return sm_d, 200

    def put(self, bid):
        req_json = request.json
        if 'id' not in req_json:
            req_json['id'] = bid
        movie_service.update(req_json)
        return '', 204

    def delete(self, bid):
        movie_service.delete(bid)
        return '', 204
