from pecan import expose, request, response
from pecan.rest import RestController
from pecan.secure import secure
from test_project.model import model
import userBadgeController


@secure('check_permissions')
class UsersController(RestController):

    badges = userBadgeController.UserBadgeController()

    @expose('json')
    def get_one(self, user_id):
        badges = []
        user = model.get_user(user_id)
        if user:
            for u in user.users:
                badges.append({'badge_id':u.badge.badge_id,'amount_necessary':u.badge.amount_necessary,'cant_act':u.cant_act ,'description':u.badge.description, 'title':u.badge.title, 'image':u.badge.image, 'data1':u.badge.data1})
            user_dict = {'user_id':user.user_id, 'fullname':user.fullname,'email':user.email,'password':user.password, 'badges':badges}
            return user_dict
        else:
            response.status = 404

    @expose('json')
    def get_all(self):
        users = []
        for user in model.get_all_users():
            users.append(self.get_one(user.user_id))
        return users

    @expose()
    def post(self):

        try:
            body = request.json
            if model.get_user(body['user_id']):
                response.status = 409
            else:
                if (body['user_id'] and body['fullname'] and body['password'] and body['email']):
                    model.create_user(body['user_id'], body['fullname'], body['password'], body['email'])
                    response.status = 201
                else:
                    response.status = 400
        except ValueError:
            response.status = 400

    @expose()
    def delete(self, user_id='none'):
        if model.delete_user(user_id):
            response.status = 200
        else:
            response.status = 404

    @expose('json')
    def put(self, user_id_old):
        try:
            body = request.json
            if model.set_user(user_id_old, body['user_id'], body['fullname'], body['password'], body['email']):
                response.status = 200
            else:
                response.status = 404
        except ValueError:
            response.status = 400