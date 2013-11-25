from app import db


class Master(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), index=True, unique=True)
    items = db.relationship('Detail', backref='master', lazy='dynamic')

    def __repr__(self):
        return '<Master %r>' % self.name


class Detail(db.Model):
    id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name  = db.Column(db.String(255))
    qty   = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0)
    master_id = db.Column(db.Integer, db.ForeignKey('master.id'))
    
    def __repr__(self):
        return '<Detail %r>' % self.name
