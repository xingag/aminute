#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: dateutils.py 
@time: 2018/8/21 23:20 
@description：时间日期工具类
"""

import datetime
import time
import locale

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"

DATE_FORMAT = "%Y年%m月%d日"


# 当前毫秒数
def curMilis():
	return int(time.time() * 1000)


# 当前秒数
def curSeconds():
	return int(time.time())


# 当前日期  格式%Y-%m-%d %H:%M:%S
def curDatetime():
	return datetime.datetime.strftime(datetime.datetime.now(), DATETIME_FORMAT)


# 当前日期  格式%Y-%m-%d
def curDate():
	return datetime.date.today()


def curDateWithFormat():
	# locale.setlocale(locale.LC_CTYPE, 'chinese')
	# return datetime.date.today().strftime(DATE_FORMAT)
	current = datetime.datetime.now()
	return str(current.year) + "年" + str(current.month) + "月" + str(current.day) + "日"


# 当前时间  格式%Y-%m-%d
def curTime():
	return time.strftime(TIME_FORMAT)


# 秒转日期
def secondsToDatetime(seconds):
	return time.strftime(DATETIME_FORMAT, time.localtime(seconds))


# 毫秒转日期
def milisToDatetime(milix):
	return time.strftime(DATETIME_FORMAT, time.localtime(milix // 1000))


# 日期转毫秒
def datetimeToMilis(datetimestr):
	strf = time.strptime(datetimestr, DATETIME_FORMAT)
	return int(time.mktime(strf)) * 1000


# 日期转秒
def datetimeToSeconds(datetimestr):
	strf = time.strptime(datetimestr, DATETIME_FORMAT)
	return int(time.mktime(strf))


# 当前年
def curYear():
	return datetime.datetime.now().year


# 当前月
def curMonth():
	return datetime.datetime.now().month


# 当前日
def curDay():
	return datetime.datetime.now().day


# 当前时
def curHour():
	return datetime.datetime.now().hour


# 当前分
def curMinute():
	return datetime.datetime.now().minute


# 当前秒
def curSecond():
	return datetime.datetime.now().second


# 星期几
def curWeek():
	return datetime.datetime.now().weekday()


# 几天前的时间
def nowDaysAgo(days):
	daysAgoTime = datetime.datetime.now() - datetime.timedelta(days=days)
	return time.strftime(DATETIME_FORMAT, daysAgoTime.timetuple())


# 几天后的时间
def nowDaysAfter(days):
	daysAgoTime = datetime.datetime.now() + datetime.timedelta(days=days)
	return time.strftime(DATETIME_FORMAT, daysAgoTime.timetuple())


# 某个日期几天前的时间
def dtimeDaysAgo(dtimestr, days):
	daysAgoTime = datetime.datetime.strptime(dtimestr, DATETIME_FORMAT) - datetime.timedelta(days=days)
	return time.strftime(DATETIME_FORMAT, daysAgoTime.timetuple())


# 某个日期几天前的时间
def dtimeDaysAfter(dtimestr, days):
	daysAgoTime = datetime.datetime.strptime(dtimestr, DATETIME_FORMAT) + datetime.timedelta(days=days)
	return time.strftime(DATETIME_FORMAT, daysAgoTime.timetuple())


def get_week_day(date):
	week_day_dict = {
		0: '星期一',
		1: '星期二',
		2: '星期三',
		3: '星期四',
		4: '星期五',
		5: '星期六',
		6: '星期天',
	}
	day = date.weekday()
	return week_day_dict[day]

# secondStamp = curSeconds()
# print("当前秒：", secondStamp)
# milisStamp = curMilis()
# print("当前毫秒：", milisStamp)
#
# curdTime = curDatetime()
# print("当前时间：", curdTime)
# curDate = curDate()
# print("当前日期：", curDate)
# curT = curTime()
# print("当前时刻：", curT)
#
# stdtime = secondsToDatetime(secondStamp)
# print("秒转时间：", stdtime)
# mtdtime = milisToDatetime(milisStamp)
# print("毫秒转时间：", mtdtime)
# dtimetm = datetimeToMilis(mtdtime)
# print("时间转毫秒：", dtimetm)
# dtimets = datetimeToSeconds(mtdtime)
# print("时间转秒：", dtimets)
#
# year = curYear()
# print("年：", year)
# month = curMonth()
# print("月：", month)
# day = curDay()
# print("日：", day)
# hour = curHour()
# print("时：", hour)
# minute = curMinute()
# print("分：", minute)
# second = curSecond()
# print("秒：", second)
# week = curWeek()
# print("星期：", week)
