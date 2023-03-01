from werkzeug.security import check_password_hash, generate_password_hash

USERNAME='shine'
PASSWORD='shine'

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.pw_hash = self._generate_pw_hash(self.password)

    def _generate_pw_hash(self, password: str):
        return generate_password_hash(password, 'pbkdf2:sha256:260000', 18)


    def __str__(self):
        return "User(id='%s')" % self.id


users = [
    User(1, USERNAME, PASSWORD), # shine:shine
]


username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and check_password_hash(user.pw_hash, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)
