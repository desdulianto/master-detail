from flask import render_template, jsonify, request

from app import app
from app import db
from app import models


@app.route('/', endpoint='index')
def index():
    return render_template('index.html')


@app.route('/master.json', endpoint='master_list')
def master_list():
    items = models.Master.query.all()
    return jsonify(objects=[dict(id=item.id, name=item.name) for item in items])


@app.route('/master.json', methods=['POST'], endpoint='new_master')
def new_master():
    data = request.get_json()
    try:
        entry = models.Master(name=data['name'])
        map(lambda item: entry.items.append(models.Detail(name=item['name'],
            qty=item['qty'], price=item['price'])), data['items'])
        db.session.add(entry)
        db.session.commit()
    except Exception as e:
        print e
        db.session.rollback()
        return jsonify(status='Server Error'), 500

    return jsonify(status='OK'), 201


@app.route('/master/<int:master_id>.json', methods=['GET'],
        endpoint='master_detail')
def master_detail(master_id):
    master = models.Master.query.get_or_404(master_id)
    return jsonify(id=master.id, name=master.name, items=[dict(id=item.id,
        name=item.name, qty=item.qty, price=item.price) for item in
        master.items])

@app.route('/master/<int:master_id>.json', methods=['POST'],
        endpoint='update_master_detail')
def update_master_detail(master_id):
    master = models.Master.query.get_or_404(master_id)
    data = request.get_json()
    if data['id'] != master.id:
        return jsonify(status='Error'), 400

    try:
        master.name = data['name']
        for item in data['items']:
            if item.get('id', None):
                old_item = master.items.filter_by(id=item['id']).first_or_404()
                old_item.name = item['name']
                old_item.qty = item['qty']
                old_item.price = item['price']
            else:
                new_item = models.Detail(name=item['name'],
                        qty=item['qty'], price=item['price'])
                master.items.append(new_item)
        db.session.add(master)
        db.session.commit()
    except Exception as e:
        print e
        db.session.rollback()
        return jsonify(status='Error'), 500

    return jsonify(status='OK'), 200
