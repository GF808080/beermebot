# -*- coding: utf-8 -*-

import re, logging, datetime
from flask import jsonify, Flask, request, redirect, render_template, flash
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import fields

### import passwords
inFile = open('.passwords.txt')
creds = inFile.read()
SECRET_KEY = re.findall('SECRET_KEY:\w+', creds)[0][10:]
DB_SECRET = re.findall('DB_SECRET:\w+', creds)[0][10:]

##app config stuff
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://beermebot:'+DB_SECRET+'@localhost/beermebot'

##set up the db and bootstrap
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class MasterList(db.Model):
  __tablename__ = 'MasterList'
  beer_name = db.Column(db.String(100), primary_key = True)
  beer_class = db.Column(db.String(100))
  abv = db.Column(db.Integer)
  ibu = db.Column(db.Integer)
  tasting_notes=db.Column(db.String(200))
##set up class for submission form
 

class SubmitForm(Form):
    beer_name= fields.StringField()
    beer_class = fields.StringField()
    abv = fields.DecimalField()
    ibu = fields.DecimalField()
    tasting_notes=fields.TextField()


@app.route("/")
def index():
	return render_template("index.html")

@app.route('/submit', methods = ("GET", "POST"))
def submissionForm():
	form = SubmitForm()
	if form.validate_on_submit():
		beer = Masterlist()
		form.populate_obj(beer)
		db.session.add(beer)
		flash("Added the beer you requested ")
		return render_template("submission.html", submit_form = form)
	else:
		flash("Something went wrong!")
		return render_template("submission.html", submit_form = form)


@app.route("/MasterList", methods = ("GET", "POST"))
def Master_List_Display():
    query = MasterList.query.filter()
    data = query_to_list(query)
    #data = [next(data)] + [[_make_link(cell) if i == 0 else cell for i, cell in enumerate(row)] for row in data]
    return render_template("masterlist.html", data=data, type="MasterList")

def query_to_list(query, include_field_names=True):
    """Turns a SQLAlchemy query into a list of data values."""
    column_names = []
    for i, obj in enumerate(query.all()):
        if i == 0:
            column_names = [c.name for c in obj.__table__.columns]
            if include_field_names:
                yield column_names
        yield obj_to_list(obj, column_names)


def obj_to_list(sa_obj, field_order):
    """Takes a SQLAlchemy object - returns a list of all its data"""
    return [getattr(sa_obj, field_name, None) for field_name in field_order]

if __name__ == '__main__':
  	app.run(debug=True)