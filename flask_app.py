import pandas
from flask import Flask, request, redirect, make_response, render_template_string
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

THIS_FOLDER = Path(__file__).parent.resolve()

def stringinserter(string, insertables):
    array = string.split("@")
    outputarray = []
    for x in range(len(array)):
        outputarray.append(array[x])
        if x < len(insertables):
            outputarray.append(insertables[x])
    return(("").join(outputarray))

class Adder(FlaskForm):
    personname = StringField()
    occupation = StringField()
    submitter = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'REDACTED_SECRET_KEY'

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="REDACTED_DB_USER",
    password="REDACTED_DB_PASS",
    hostname="REDACTED_DB_HOST",
    databasename="REDACTED_DB_NAME",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

datasource = SQLAlchemy(app)

with open(THIS_FOLDER / "page1.txt") as f:
    lines1 = f.readlines()
lines1 = (" ").join(lines1)

with open(THIS_FOLDER / "page2.txt") as f:
    lines2 = f.readlines()
lines2 = (" ").join(lines2)

@app.route("/", methods = ["GET","POST"])
def login():

    personform = Adder()

    selected_name = 'nothing'
    if (personform.validate_on_submit() and personform.submitter.data):
        if((len(personform.personname.data)>1) and (personform.occupation.data in ["tourist","explorer","landowner"])):
            selected_name = personform.personname.data
            selected_occ = personform.occupation.data
            personform.personname.data = ""
            personform.occupation.data = ""
        else:
            personform.personname.data = ""
            personform.occupation.data = ""

    if(selected_name == 'nothing'):
        return render_template_string(lines1, personform=personform)

    if(request.cookies.get('User_Name') is None):
        response_object = make_response(lines1)
        response_object.set_cookie("User_Name", value = selected_name, max_age = 31536000, expires = None, path = '/', domain = None, secure = None, httponly = False)
        response_object.set_cookie("User_Occupation", value = selected_occ, max_age = 31536000, expires = None, path = '/', domain = None, secure = None, httponly = False)
        return response_object
    else:
        return redirect("https://restore-thomasappmaker.pythonanywhere.com/main")
    
@app.route("/main", methods = ["GET","POST"])
def home():

    if(request.cookies.get('User_Name') is None):
        return redirect("https://restore-thomasappmaker.pythonanywhere.com")
    else:
        return(stringinserter(lines2,[request.cookies.get('User_Name'),request.cookies.get('User_Occupation')]))