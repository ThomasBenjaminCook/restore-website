import pandas
from flask import Flask, request, redirect, render_template_string, after_this_request
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

class Regi(FlaskForm):
    title = StringField()
    description = StringField()
    submitagain = SubmitField('Submit')

with open(THIS_FOLDER / "page1.txt") as f:
    lines1 = f.readlines()
lines1 = (" ").join(lines1)

with open(THIS_FOLDER / "page2.txt") as f:
    lines2 = f.readlines()
lines2 = (" ").join(lines2)

with open(THIS_FOLDER / "register_land_form.txt") as f:
    lines3 = f.readlines()
lines3 = (" ").join(lines3)

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

    if(selected_name == 'nothing' and request.cookies.get('User_Name') is None):
        return render_template_string(lines1, personform=personform)

    if(request.cookies.get('User_Name') is None):

        @after_this_request
        def add_cookie(response_object):
            response_object.set_cookie("User_Name", value = selected_name, max_age = 31536000, expires = None, path = '/', domain = None, secure = None, httponly = False)
            response_object.set_cookie("User_Occupation", value = selected_occ, max_age = 31536000, expires = None, path = '/', domain = None, secure = None, httponly = False)
            return response_object
        
        return redirect("https://restore-thomasappmaker.pythonanywhere.com/browse")
    else:
        return redirect("https://restore-thomasappmaker.pythonanywhere.com/browse")
    
@app.route("/browse", methods = ["GET","POST"])
def browse():
    if(request.cookies.get('User_Name') is None):
        return redirect("https://restore-thomasappmaker.pythonanywhere.com")
    
    else:
        insertables = [request.cookies.get('User_Name'),request.cookies.get('User_Occupation')]

        islandowner = False
        if(request.cookies.get('User_Occupation') == "landowner"):
            insertables.append(lines3)
            islandowner = True
            regform = Regi()
        else:
            insertables.append("</br>")

        if(islandowner):
            return render_template_string(stringinserter(lines2,insertables), regform = regform)
        else:
            return(stringinserter(lines2,insertables))