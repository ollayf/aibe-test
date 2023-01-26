from werkzeug.security import check_password_hash


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


users = [
    User(1, 'shine', 'pbkdf2:sha256:260000$jh8EnTtgkY07IJsj$8d33ccd601237cc5f9b331df02d62e035b3bff46ccab1408b3d34a035df5912d'), # shine:shine
]


username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and check_password_hash(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)
