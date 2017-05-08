from flask import Flask, render_template, request, redirect, jsonify, url_for
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

app = Flask(__name__)

#Fake categories
category = {'name': 'Catagory', 'id': '0'}

categories = [{'name': 'Catagory1', 'id': '1'},
            {'name': 'Catagory2', 'id': '2'},
            {'name': 'Catagory3', 'id': '3'},
            {'name': 'Catagory4', 'id': '4'},
            {'name': 'Catagory5', 'id': '5'}]

items = [{'name': 'item1', 'id': '1', 'c_id': 1},
        {'name': 'item2', 'id': '2', 'c_id': 2},
        {'name': 'item3', 'id': '3', 'c_id': 1},
        {'name': 'item4', 'id': '4', 'c_id': 2},
        {'name': 'item5', 'id': '5', 'c_id': 1},
        {'name': 'item6', 'id': '6', 'c_id': 3}]

item = [{'name': 'item', 'id': '0', 'description': 'Some description'}]

@app.route('/')
@app.route('/catalog')
def homepage():
    return render_template('index.html', categories = categories)

@app.route('/catalog/<int:category_id>')
def category(category_id):

    return render_template('category.html', categories = categories, category_id = category_id, items = items)

@app.route('/catalog/<int:category_id>/<int:item_id>')
def item(category_id, item_id):
    return render_template('item.html', catagories = categories, category_id = category_id, item_id = item_id, item = item)

@app.route('/catalog/new')
def newItem():
    return render_template('new_item.html')

@app.route('/catalog/<int:category_id>/<int:item_id>/edit')
def editItem(category_id, item_id):
    return render_template('edit.html', catagories = categories, category_id = category_id, item_id = item_id)

@app.route('/catalog/<int:category_id>/<int:item_id>/delete')
def deleteItem(category_id, item_id):
    return render_template('delete.html', catagories = categories, category_id = category_id, item_id = item_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
