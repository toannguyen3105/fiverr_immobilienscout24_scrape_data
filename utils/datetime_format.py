#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


def get_timestamp():
    now = datetime.now()
    return int(datetime.timestamp(now))
