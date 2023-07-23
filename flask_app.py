import pandas
from flask import Flask, request, redirect, make_response
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy

THIS_FOLDER = Path(__file__).parent.resolve()

def stringinserter(string, insertables):
    array = string.split("@")
    outputarray = []
    for x in range(len(array)):
        outputarray.append(array[x])
        if x < len(insertables):
            outputarray.append(insertables[x])
    return(("").join(outputarray))

app = Flask(__name__)
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
def home():

    if(request.cookies.get('User_Name') is None):
        return redirect("https://restore-thomasappmaker.pythonanywhere.com/login")
    else:
        return(lines2)

@app.route("/login", methods = ["GET","POST"])
def login():

    # if(your_data is None):
    #     response_object = make_response(lines1)
    #     response_object.set_cookie("User_Name", value = next_available_id, max_age = 31536000, expires = None, path = '/', domain = None, secure = None, httponly = False)
    #     return response_object
    
    return lines1