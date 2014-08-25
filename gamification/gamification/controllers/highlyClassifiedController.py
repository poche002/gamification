

class HighlyClassifiedController(object):
    def check_permissions(self, user_id, user_pass):
        try:
            return True
        except KeyError:
            return False