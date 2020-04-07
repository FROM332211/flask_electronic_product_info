from APP.ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(16), nullable=False)

    def save(self):  # 添加数据
        db.session.add(self)
        db.session.commit()


class commodity_info(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commodity_type = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    重量 = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_path = db.Column(db.String(30), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()
