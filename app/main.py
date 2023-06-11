from base64 import b64decode  # Used to encode binary data as printable text.
import os  # is imported to handle operating system-related functionalities

from Fortuna import random_int, random_float
from MonsterLab import Monster
from flask import Flask, render_template, request  # is imported to create a Flask web application.
from pandas import DataFrame

from app.data import Database
from app.graph import chart
from app.machine import Machine

SPRINT = 3
APP = Flask(__name__)


@APP.route("/")  # home route specifies the URL endpoint ("/") that corresponds to the home page.
#  The home() function is the view function for the home page. It returns the rendered template
#  "home.html" with some context variables.
def home():
    return render_template(
        "home.html",
        sprint=f"Sprint {SPRINT}",
        monster=Monster().to_dict(),
        password=b64decode(b"VGFuZ2VyaW5lIERyZWFt"),
    )


@APP.route("/data")  # data route specifies the URL endpoint ("/data") that corresponds to the data page.
# The data() function is the view function for the data page. It returns the rendered template "data.html"
# with some context variables.
def data():
    if SPRINT < 1:
        return render_template("data.html")
    db = Database("monster")
    return render_template(
        "data.html",
        count=db.count(),
        table=db.html_table(),
    )


@APP.route("/view", methods=["GET", "POST"])
def view():
    if SPRINT < 2:
        return render_template("view.html")
    db = Database("monster")
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    x_axis = request.values.get("x_axis") or options[1]
    y_axis = request.values.get("y_axis") or options[2]
    target = request.values.get("target") or options[4]
    graph = chart(
        df=db.dataframe(),
        x=x_axis,
        y=y_axis,
        target=target,
    ).to_json()
    # "view.html" is returned with some context variables.
    return render_template(
        "view.html",
        options=options,
        x_axis=x_axis,
        y_axis=y_axis,
        target=target,
        count=db.count(),
        graph=graph,
    )


@APP.route("/model", methods=["GET", "POST"])
def model():
    if SPRINT < 3:
        return render_template("model.html")
    db = Database("monster")
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]  # This is a list of our headers/keys
    filepath = os.path.join("app", "model.joblib")
    if not os.path.exists(filepath):
        df = db.dataframe()
        machine = Machine(df[options])
        machine.save(filepath)
    else:
        machine = Machine.open(filepath)
    stats = [round(random_float(1, 250), 2) for _ in range(3)]
    level = request.values.get("level", type=int) or random_int(1, 20)
    health = request.values.get("health", type=float) or stats.pop()
    energy = request.values.get("energy", type=float) or stats.pop()
    sanity = request.values.get("sanity", type=float) or stats.pop()
    prediction, confidence = machine(DataFrame(
        [dict(zip(options, (level, health, energy, sanity)))]
    ))
    info = machine.info()
    return render_template(
        "model.html",
        info=info,
        level=level,
        health=health,
        energy=energy,
        sanity=sanity,
        prediction=prediction,
        confidence=f"{confidence:.2%}",
    )


if __name__ == '__main__':
    APP.run()
