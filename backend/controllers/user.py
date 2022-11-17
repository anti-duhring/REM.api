
class UserController:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection
        print('Initialize user controller')
    
    def create(self, data):
        token = data['token']
        admin = data['admin']
        access = data['access']
        name = data['name']

        command = f'INSERT INTO Users (token, admin, access, name) VALUES ("{token}", {admin}, {access}, "{name}")'

        self.cursor.execute(command)
        self.connection.commit()
    
    def read(self, data):
        token = data['token']
        admin = data['admin']
        access = data['access']
        name = data['name']

        command = f'SELECT * FROM Users'

        self.cursor.execute(command)
        result = self.cursor.fetchall()
        return result

    def update(self, data):
        token = data['token']
        admin = data['admin']
        access = data['access']
        name = data['name']
        user_id = data['id']

        command = f'UPDATE Users SET name = "{name}" WHERE id = {user_id}'

        self.cursor.execute(command)
        self.connection.commit()
    
    def delete(self, data):
        user_id = data['id']

        command = f'DELETE FROM Users WHERE id = {user_id}'

        self.cursor.execute(command)
        self.connection.commit()