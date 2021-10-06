#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

date_format = ["%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"]
date_time_format = date_format[0]
date_time_format_momo = date_format[1]


def getDateTimeNow():
    return datetime.now()


def get_date_telegram():
    return datetime.now().strftime(date_time_format)


def getDateTimeMomo():
    return datetime.now().strftime(date_time_format_momo)


def getTimeStringFromTimeStamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime(date_time_format)


def getTimeStamp():
    now = datetime.now()
    return int(datetime.timestamp(now))


def convertDateToTimestamp(date):
    return int(datetime.timestamp(date))
