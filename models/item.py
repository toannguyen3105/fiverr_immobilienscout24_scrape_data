#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import db
from utils.date_format import getTimeStringFromTimeStamp
from sqlalchemy import desc


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False, comment="Item name")
    price = db.Column(db.String(100), nullable=False, comment="Item price")
    absolute_link = db.Column(db.String(300), nullable=False, unique=True, comment="Item link")
    created_at = db.Column(db.Integer, nullable=True, comment="Timestamp")
    created_by = db.Column(db.String(30), nullable=True, comment="Person create user")
    updated_at = db.Column(db.Integer, nullable=True, comment="Timestamp")
    updated_by = db.Column(db.String(30), nullable=True, comment="Person update user")

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False, comment="Store")

    def __init__(self, name, price, absolute_link, store_id, created_at, created_by, updated_at,
                 updated_by):
        self.name = name
        self.price = price
        self.absolute_link = absolute_link
        self.store_id = store_id
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'absolute_link': self.absolute_link,
            'store_id': self.store_id,
            'created_at': self.created_at,
            'created_at_string': None if self.created_at is None else getTimeStringFromTimeStamp(self.created_at),
            'created_by': self.created_by,
            'updated_at': self.updated_at,
            'updated_at_string': None if self.updated_at is None else getTimeStringFromTimeStamp(self.updated_at),
            'updated_by': self.updated_by
        }

    @classmethod
    def find_by_name(cls, name, _store_id):
        return cls.query.filter_by(name=name, store_id=_store_id).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_absolute_link(cls, absolute_link, _store_id):
        return cls.query.filter_by(absolute_link=absolute_link, store_id=_store_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.order_by(desc(cls.created_at)).all()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
