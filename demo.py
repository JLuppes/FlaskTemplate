from flask import Blueprint, render_template, request, redirect, url_for
from models import db

demo = Blueprint('demo', __name__)

@demo.route('/demo')
def crudPage():
    return render_template('demo.html')

@demo.route('/demo/create')
def create():
    return render_template('demoPages/create.html')
@demo.route('/demo/read')
def read():
    return render_template('demoPages/read.html')
@demo.route('/demo/update')
def update():
    return render_template('demoPages/update.html')
@demo.route('/demo/delete')
def delete():
    return render_template('demoPages/delete.html')