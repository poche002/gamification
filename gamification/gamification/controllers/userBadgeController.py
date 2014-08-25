from pecan.rest import RestController
from pecan import expose, request, response
from test_project.model import model

class UserBadgeController(RestController):

    @expose()
    def put(self, user_id, badge_id, cant_sum=1):
        try:
            body = request.json
            try:
                cant_sum=body['cant_sum']
                if model.set_user_badge(user_id, badge_id, cant_sum):
                    response.status = 200
                else:
                    response.status = 404
            except KeyError:
                response.status = 400
        except ValueError:
            if model.set_user_badge(user_id, badge_id, cant_sum):
                response.status = 200
            else:
                response.status = 404