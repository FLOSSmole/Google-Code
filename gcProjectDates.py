# -*- coding: utf-8 -*-
"""
(c) megan squire for FLOSSmole
GPL v3 license applies
"""
import pymysql
from datetime import datetime as dt
import codecs

linenum = 1
datasource_id = 58459

db = pymysql.connect(host="",
                     user="",
                     passwd="",
                     db="google_code",
                     use_unicode=True,
                     charset="utf8",
                     autocommit=True)
cursor = db.cursor()

lines = codecs.open('gcProjectDates.txt',
                    'r',
                    encoding='utf-8',
                    errors='ignore')
next(lines)
for line in lines:
    #print(linenum)
    currentLine = line.split(',')
    print("working on:", currentLine[0])

    if len(currentLine) == 6:
        try:
            proj_name = currentLine[0]
            timestamp = currentLine[4]
            if timestamp != "[NULL]":
                convertDate = dt.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

                cursor.execute("INSERT INTO gc_project_creates(\
                proj_name, \
                datasource_id, \
                created, \
                convert_created, \
                last_updated) \
                VALUES (%s,%s,%s,%s,%s)",
                (proj_name,
                 datasource_id,
                 timestamp,
                 convertDate,
                 dt.now()))

        except pymysql.Error as error:
            print(error)
            db.rollback()
    linenum = linenum + 1
cursor.close()
db.close()
