from flask import render_template
from flask import render_template
from main import clients_queue

def render_dashboard():
    clients = clients_queue.get_iterable()

    return render_template('base.html', clients=clients)