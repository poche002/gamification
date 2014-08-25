from pecan.rest import RestController
from pecan import expose, request, response
from test_project.model import model
import json

class BadgesController(RestController):

    @expose('json')
    def get_one(self, badge_id):
        users = {}
        badge = model.get_badge(badge_id)
        if badge:
            for b in badge.badges:                              #lista de objetos user-badge
                if b.cant_act >= badge.amount_necessary:
                    users[b.user.user_id] = b.user.fullname
            badge_dict = {'badge_id':badge.badge_id,'amount_necessary':badge.amount_necessary,'description':badge.description, 'title':badge.title, 'image':badge.image, 'data1':badge.data1,'users':users}
            #badge_dict = {badge.badge_id:{'amount_necessary':badge.amount_necessary,'description':badge.description, 'title':badge.title, 'image':badge.image, 'data1':badge.data1,'users':users}}
            return badge_dict
        else:
            response.status = 404

    @expose('json')
    def get_all(self):
        badges = []

        for badge in model.get_all_badges():
            badges.append(self.get_one(badge.badge_id))
        return badges

    @expose()
    def post(self):
        try:
            body = request.json
            if model.get_badge(body['badge_id']):
                response.status = 409
            else:
                try:
                    model.create_badge(body['badge_id'], body['amount_necessary'], body['description'], body['image'], body['title'], body['data1'])
                except KeyError:
                    response.status = 400
        except KeyError:
            response.status = 400

    @expose()
    def delete(self, badge_id):
        if model.delete_badge(badge_id):
            response.status = 200
        else:
            response.status = 404

    @expose()
    def put(self, badge_id_old):
        try:
            body = request.json
            try:
                if model.set_badge(badge_id_old, body['badge_id'], body['amount_necessary'], body['description'], body['image'], body['title'], body['data1']):
                    response.status = 200
                else:
                    response.status = 404
            except KeyError:
                response.status = 400
        except ValueError:
            response.status = 400


