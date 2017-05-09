from flask import Flask, render_template, request, redirect, jsonify, url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/catalog')
def homepage():
    categories = session.query(Category).all()
    return render_template('index.html', categories = categories)

@app.route('/catalog/<int:category_id>')
def categoryList(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id)
    return render_template('category.html', category = category, category_id = category_id, items = items)

@app.route('/catalog/<int:category_id>/<int:item_id>')
def itemDescription(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html',  category_id = category_id, item_id = item_id, item = item)

@app.route('/catalog/<int:category_id>/new', methods=['GET', 'POST'])
def newItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id)
    print request.method
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'], description=request.form[
                           'description'], category_id=category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('categoryList', category_id = category_id))
    else:
        return render_template('new_item.html', category_id = category_id)

@app.route('/catalog/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('itemDescription', category_id = category_id, item_id = item_id))
    else:
        return render_template('edit.html', category_id = category_id, item_id = item_id, item = editedItem)

@app.route('/catalog/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    deleteItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        return redirect(url_for('categoryList', category_id = category_id))
    else:
        return render_template('delete.html', category_id = category_id, item_id = item_id)

@app.route('/catalog/<int:category_id>/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])

@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
