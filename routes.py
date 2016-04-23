# -*- coding: utf-8 -*-

import re, logging, datetime
from flask import jsonify, Flask, request, redirect, render_template
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import fields

### import passwords
inFile = open('/home/sentinel/beermebot/.passwords.txt')
creds = inFile.read()
SECRET_KEY = re.findall('SECRET_KEY:\w+', creds)[0].strip('SECRET_KEY:')
DB_SECRET = re.findall('DB_SECRET:\w+', creds)[0].strip('DB_SECRET:')

##app config stuff
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://python:'+DB_SECRET+'@localhost/beermebot'

##set up the db and bootstrap
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


##set up class for submission form
 
class SubmitForm(Form):
    Beer_Name = fields.StringField()
    Beer_Class = fields.DateField()
    ABV = fields.DecimalField()
    IBU = fields.DecimalField()
    Tasting_Notes=fields.TextField()


@app.route("/")
def index():
	return render_template("index.html")

@app.route('/submit')
def submissionForm():
	submit_form = SubmitForm()
	return render_template("submission.html", submit_form = submit_form,)

if __name__ == '__main__':
  	app.run(debug=True)