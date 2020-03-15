from APP.ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(16), nullable=False)

    def save(self):#添加数据
        db.session.add(self)
        db.session.commit()
