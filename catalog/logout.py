from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

from catalog import app

    # DISCONNECT - Revoke a current user's token and reset their session

@app.route('/logout')
def logout():
    provider = login_session.get('provider')
    if not provider:
        print "no provider!!!"
        return redirect(url_for('homepage'))
    if provider == 'google':
        return redirect(url_for('gdisconnect'))
    elif provider == 'facebook':
        return redirect(url_for('fbdisconnect'))


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    if access_token is None:
 	print 'Access Token is None'
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	del login_session['picture']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
        flash("Successfully disconnected")
    	return redirect(url_for('homepage'))
    else:

    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['user_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['facebook_id']
    flash("you have been logged out")
    return redirect(url_for('homepage'))
