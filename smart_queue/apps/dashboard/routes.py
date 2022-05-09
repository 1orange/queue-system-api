from flask import Blueprint, redirect, render_template, request

from smart_queue.db.database import (
    get_all_conditions,
    get_current_client,
    get_queue_status,
    insert_condition,
    next_patient,
)

Dash = Blueprint("dash", __name__)


@Dash.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        next_patient()

    return render_template(
        "base.html",
        queue=get_queue_status(),
        current_patient=get_current_client(),
        conditions=get_all_conditions(),
    )


@Dash.route("/conditions/add", methods=["POST", "GET"])
def condition_add_form():
    if request.method == "GET":
        return redirect("/")

    desc = None
    name = request.form["name"]
    burst_time = request.form["burst_time"]
    urgency = request.form["urgency"]

    if request.form["desc"]:
        desc = request.form["desc"]

    insert_condition(name=name, desc=desc, burst_time=burst_time, urgency=urgency)

    return redirect("/")
