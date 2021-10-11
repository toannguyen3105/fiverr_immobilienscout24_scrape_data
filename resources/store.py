#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse

from models.store import StoreModel

from utils.date_format import getTimeStamp

STATUS_CODES = ['OK', 'INTERNAL_ERROR', 'DATABASE_ERROR']


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("url",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )
    parser.add_argument("description",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    def get(self):
        stores = [store.json() for store in StoreModel.find_all()]

        return {
                   "status": 200,
                   "message": "Get success list",
                   "data": [store for store in stores],
                   "total": len(StoreModel.find_all())
               }, 200

    def post(self):
        data = self.parser.parse_args()
        url = data["url"]
        description = data["description"]

        store = StoreModel(url, description, getTimeStamp(), None, None, None)
        store.save_to_db()

        return {
                   "error": None,
                   "status": STATUS_CODES[0],
                   "result": store.json(),
                   "time": getTimeStamp()
               }, 200


class StoreItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("url",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )
    parser.add_argument("description",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    def get(self, store_id: int):
        store = StoreModel.find_by_id(store_id)

        if not store:
            return {
                       "error": 1,
                       "status": STATUS_CODES[0],
                       "result": None,
                       "time": getTimeStamp()
                   }, 404

        return {
                   "error": 1,
                   "status": STATUS_CODES[0],
                   "result": store.json(),
                   "time": getTimeStamp()
               }, 200

    def put(self, store_id: int):
        store = StoreModel.find_by_id(store_id)

        if store is None:
            return {
                       "error": 1,
                       "status": STATUS_CODES[0],
                       "result": None,
                       "time": getTimeStamp()
                   }, 404

        data = self.parser.parse_args()
        url = data["url"]
        description = data["description"]

        store.url = url
        store.description = description
        store.updated_at = getTimeStamp()
        store.updated_by = "ADMIN"

        store.save_to_db()

        return {
                   "error": None,
                   "status": STATUS_CODES[0],
                   "result": store.json(),
                   "time": getTimeStamp()
               }, 200
