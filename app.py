#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_apscheduler import APScheduler
from datetime import datetime

from db import db

from resources.cookie import Cookie, CookieItem
from resources.store import Store, StoreItem
from resources.item import Item

from main import update_latest_product

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)


# set configuration values
class Config(object):
    SCHEDULER_API_ENABLED = True


app.config.from_object(Config())

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Cookie, '/cookies')
api.add_resource(CookieItem, '/cookies/<int:cookie_id>')
api.add_resource(StoreItem, '/stores/<int:store_id>')
api.add_resource(Store, '/stores')
api.add_resource(Item, '/items')


@scheduler.task('interval', id='fiverr_immobile_update_latest_product', minutes=5, misfire_grace_time=900,
                next_run_time=datetime.now())
def ScheduledTask():
    with app.app_context():
        update_latest_product()


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, use_reloader=False, debug=True)
