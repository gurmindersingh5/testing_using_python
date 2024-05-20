from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    data = db.Column(db.String(120))

    def __repr__(self):
        return f'Name: {self.name}, email: {self.email}'
