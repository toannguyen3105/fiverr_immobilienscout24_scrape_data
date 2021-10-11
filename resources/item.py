#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse

from models.item import ItemModel

from utils.date_format import getTimeStamp

STATUS_CODES = ['OK', 'INTERNAL_ERROR', 'DATABASE_ERROR']


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('price',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('absolute_link',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="This field cannot be blank."
                        )

    def get(self):
        items = [item.json() for item in ItemModel.find_all()]

        return {
                   "error": None,
                   "status": STATUS_CODES[0],
                   "result": [item for item in items],
                   "time": getTimeStamp()
               }, 200

    def post(self):
        data = self.parser.parse_args()
        name = data["name"]
        price = data["price"]
        absolute_link = data["absolute_link"]
        store_id = data["store_id"]

        item = ItemModel(name, price, absolute_link, store_id, getTimeStamp(), None, None, None)
        item.save_to_db()

        return {
                   "error": None,
                   "status": STATUS_CODES[0],
                   "result": item.json(),
                   "time": getTimeStamp()
               }, 200
