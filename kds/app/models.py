from . import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.String(10))
    served = db.Column(db.Boolean, default=False)

    items = db.relationship('OrderItem', backref='order', lazy=True)

    @property
    def is_completed(self):
        return all(item.status == 'done' for item in self.items)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    name = db.Column(db.String(100))
    section = db.Column(db.String(50))
    status = db.Column(db.String(20), default='cooking')
