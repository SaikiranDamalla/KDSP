from flask import Blueprint, render_template, request, redirect
from .models import Order, OrderItem
from . import db, socketio


main = Blueprint('main', __name__)


SECTIONS = ['fry', 'grill', 'salad', 'dessert', 'beverage', 'pizza']


@main.route('/')
def expedite():
    orders = Order.query.filter_by(served=False).all()
    orders.sort(key=lambda o: not o.is_completed)
    return render_template('expedite.html', orders=orders)


@main.route('/section/<name>')
def section(name):
    items = OrderItem.query.filter_by(section=name, status='cooking').all()
    return render_template('section.html', items=items, section=name)


@main.route('/order', methods=['POST'])
def create_order():
    data = request.json
    order = Order(table_number=data['table'])
    db.session.add(order)
    db.session.commit()


    for item in data['items']:
        db.session.add(OrderItem(
            order_id=order.id,
                name=item['name'],
                section=item['section']
            ))
        db.session.commit()


    socketio.emit('new_order')
    return redirect('/order') #return jsonify({'status': 'ok'})

@main.route('/order')
def order_page():
    return render_template('order.html')


@main.route('/order-form', methods=['POST'])
def order_form_submit():
    table = request.form['table']
    names = request.form.getlist('name[]')
    sections = request.form.getlist('section[]')

    order = Order(table_number=table)
    db.session.add(order)
    db.session.commit()

    for name, section in zip(names, sections):
        db.session.add(OrderItem(
            order_id=order.id,
            name=name,
            section=section
        ))

    db.session.commit()
    socketio.emit('new_order')

    return redirect('/order')

@main.route('/item/<int:item_id>/done', methods=['POST'])
def mark_done(item_id):
    item = OrderItem.query.get(item_id)
    item.status = 'done'
    db.session.commit()
    socketio.emit('update')
    return '', 204


@main.route('/order/<int:order_id>/served', methods=['POST'])
def serve_order(order_id):
    order = Order.query.get(order_id)
    order.served = True
    db.session.commit()
    socketio.emit('update')
    return '', 204
