# mkdir froshims_flask_app
# cd froshims_flask_app
# cp ../my_flask_app/requirements.txt .
# . ../../bin/activate (. _Git/_test/bin/activate)
# pip install -r requirements.txt
# touch app.py
# mkdir templates
# touch layout.html index.html
# flask run

from flask import Flask, render_template, request
import sqlite3
from collections import namedtuple
import os

app = Flask(__name__)

DB = "froshims.db"

SPORTS = [
    "Basketball",
    "Soccer",
    "Ultimate Frisbee",
]

SEX = {1: 'Male', 0: 'Female', None: 'N/A'}

REGISTRANTS = [
    {'id': 1, 'name': 'já', 'sport': 'fotbal'},
    {'id': 2, 'name': 'ty', 'sport': 'hokej'},
]

def namedtuple_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    cls = namedtuple("Row", fields)
    return cls._make(row)

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS, pwd=os.getcwd())

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    if not name:
        return render_template("error.html", message="Missing name")
    sport = request.form.get("sport")
    if not sport:
        return render_template("error.html", message="Missing sport")
    if sport not in SPORTS:
        return render_template("error.html", message="Invalid sport")
    sex = next(filter(lambda x: SEX[x]==request.form.get("sex"), SEX.keys()), None)
    con = sqlite3.connect(DB)
    with con:
        con.execute("INSERT INTO registrants (name, sport, sex) VALUES (?, ?, ?)", [name, sport, sex])
    con.close()
    return render_template("success.html")

@app.route("/registrants")
def registrants():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.execute("SELECT * from registrants")
    registrants = cur.fetchall()
    con.close()
    return render_template("registrants.html", registrants=registrants, SEX=SEX)