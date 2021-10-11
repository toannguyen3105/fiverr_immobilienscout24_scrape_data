#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse

from models.cookie import CookieModel

from utils.date_format import getTimeStamp

STATUS_CODES = ['OK', 'INTERNAL_ERROR', 'DATABASE_ERROR']


class Cookie(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("cookie",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    def post(self):
        data = self.parser.parse_args()
        cookie = data["cookie"]

        cookie_item = CookieModel(cookie, getTimeStamp(), None, None, None)
        cookie_item.save_to_db()

        return {
                   "error": None,
                   "status": STATUS_CODES[0],
                   "result": cookie_item.json(),
                   "time": getTimeStamp()
               }, 200


class CookieItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("cookie",
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        )

    def get(self, cookie_id: int):
        item = CookieModel.find_by_id(cookie_id)
        if not item:
            return {
                       "error": 1,
                       "status": STATUS_CODES[0],
                       "result": None,
                       "time": getTimeStamp()
                   }, 404

        return {
                   "error": 1,
                   "status": STATUS_CODES[0],
                   "result": item.json(),
                   "time": getTimeStamp()
               }, 200

    def put(self, cookie_id: int):
        item = CookieModel.find_by_id(cookie_id)

        if item is None:
            return {
                       "error": 1,
                       "status": STATUS_CODES[0],
                       "result": None,
                       "time": getTimeStamp()
                   }, 404

        data = self.parser.parse_args()
        cookie = data["cookie"]

        item.cookie = cookie
        item.updated_at = getTimeStamp()
        item.updated_by = "ADMIN"

        item.save_to_db()

        return {
                   "error": None,
                   "status": STATUS_CODES[0],
                   "result": cookie,
                   "time": getTimeStamp()
               }, 200
