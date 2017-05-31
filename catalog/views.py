
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session

from catalog import app

engine = create_engine('sqlite:///catalogUser.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog')
def homepage():
    '''
    Main page view
    '''
    categories = session.query(Category).all()
    # Check if user is logged in
    if 'username' not in login_session:
        return render_template('base.html', categories = categories)
    else:
        return render_template('base.html', categories = categories, username = login_session['username'])

@app.route('/catalog/<int:category_id>')
def categoryList(category_id):
    '''
    returns list of items with catagory_id
    '''
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id)
    item = session.query(Category).filter_by(id=category_id).one()
    creator = session.query(User).filter_by(id=category.user_id).one()
    # Check if user is logged
    if 'username' not in login_session:
        return render_template('category-public.html', category = category, category_id = category_id, items = items, categories = categories)
    # Check is logged in user is the owner
    elif creator.id != login_session['user_id']:
        return render_template('category.html', category = category, category_id = category_id, items = items, categories = categories, username = login_session['username'])
    else:
        return render_template('category-owner.html', category = category, category_id = category_id, items = items, categories = categories, username = login_session['username'])

@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategory():
    '''
    Creates new category
    '''
    categories = session.query(Category).all()
    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('login')
    category = session.query(Category)
    print request.method
    if request.method == 'POST':
        newCategory = Category(
            name=request.form['name'],
                           user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash("new category created.")
        return redirect(url_for('homepage', categories = categories, username = login_session['username']))
    else:
        return render_template('new_category.html', categories = categories, username = login_session['username'])


@app.route('/catalog/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    '''
    Delete Category
    '''
    categories = session.query(Category).all()
    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    deleteCategory = session.query(Category).filter_by(id=category_id).one()
    if deleteCategory.user_id != login_session['user_id']:
        return "<script> function myFunction() {alert('You are not ]authorized to delete this item!');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deleteCategory)
        session.commit()
        flash("Category deleted.")
        return redirect(url_for('homepage', category_id = category_id, categories = categories, username = login_session['username']))
    else:
        return render_template('delete-category.html', category_id = category_id, categories = categories, username = login_session['username'])

@app.route('/catalog/<int:category_id>/<int:item_id>')
def itemDescription(category_id, item_id):
    '''
    returns description of item
    '''
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id)
    item = session.query(Item).filter_by(id=item_id).one()
    creator = session.query(User).filter_by(id=item.user_id).one()
    # Check if user loggedin in and is the owner
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('item-public.html',  category_id = category_id, item_id = item_id, item = item, creator = creator, categories = categories, items = items, category = category)
    else:
        return render_template('item.html',  category_id = category_id, item_id = item_id, item = item, categories = categories, items = items, category = category, username = login_session['username'])

@app.route('/catalog/<int:category_id>/new', methods=['GET', 'POST'])
def newItem(category_id):
    '''
    Creates new item
    '''
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    creator = session.query(User).filter_by(id=category.user_id).one()
    # Check if user loggedin in and is the owner
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return redirect('login')
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id)
    print request.method
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'], description=request.form[
                           'description'], category_id=category_id,
                           user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("new item created.")
        return redirect(url_for('categoryList', category_id = category_id, categories = categories, username = login_session['username']))
    else:
        return render_template('new_item.html', category_id = category_id, categories = categories, category = category, username = login_session['username'])

@app.route('/catalog/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    '''
    Edit Item
    '''
    categories = session.query(Category).all()
    editedItem = session.query(Item).filter_by(id=item_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    creator = session.query(User).filter_by(id=item.user_id).one()
    # Check if user loggedin in and is the owner
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return redirect('/login')
    if editedItem.user_id != login_session['user_id']:
        return "<script> function myFunction() {alert('You are not authorized to edit this item!');} </script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash("Item edited.")
        return redirect(url_for('itemDescription', category_id = category_id, item_id = item_id, categories = categories, username = login_session['username']))
    else:
        return render_template('edit.html', category_id = category_id, item_id = item_id, item = editedItem, categories = categories, username = login_session['username'])

@app.route('/catalog/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    '''
    Deletes Item
    '''
    categories = session.query(Category).all()
    item = session.query(Item).filter_by(id=item_id).one()
    creator = session.query(User).filter_by(id=item.user_id).one()
    # Check if user loggedin in and is the owner
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return redirect('/login')
    deleteItem = session.query(Item).filter_by(id=item_id).one()
    if deleteItem.user_id != login_session['user_id']:
        return "<script> function myFunction() {alert('You are not ]authorized to delete this item!');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash("Item deleted.")
        return redirect(url_for('categoryList', category_id = category_id, categories = categories, username = login_session['username']))
    else:
        return render_template('delete.html', category_id = category_id, item_id = item_id, categories = categories, username = login_session['username'])


@app.route('/catalog/<int:category_id>/JSON')
def categoryJSON(category_id):
    '''
    Creates JSON data fot category page
    '''
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    '''
    Creates JSON data for item page
    '''
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)
