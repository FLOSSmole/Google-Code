# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 10:44:35 2016

@author: eashwell2
"""
import re
import sys
import pymysql
import datetime

datasource_id = sys.argv[1]
password = sys.argv[2]


if datasource_id:
    # =======
    # Collector
    # =======
    try:
        dbh1 = pymysql.connect(host='grid6.cs.elon.edu',
                               database='test',
                               user='eashwell',
                               password=password,
                               charset='utf8')
    except pymysql.Error as err:
        print(err)
    cursor1 = dbh1.cursor()
    cursor2 = dbh1.cursor()
    # ======
    # LOCAL
    # ======
    try:
        dbh2 = pymysql.connect(host='grid6.cs.elon.edu',
                               database='test',
                               user='eashwell',
                               password=password,
                               charset='utf8')
    except pymysql.Error as err:
        print(err)
    cursor3 = dbh2.cursor()

    # =======
    # REMOTE
    # =======
    try:
        dbh3 = pymysql.connect(host='flossdata.syr.edu',
                               database='test',
                               user='test',
                               password=password,
                               charset='utf8')
    except pymysql.Error as err:
        print(err)
    cursor4 = dbh3.cursor()

    selectQuery1 = 'SELECT `proj_name` FROM `gc_projects`'

    insertQuery = 'INSERT INTO `gc_project_links`(`proj_name`, `datasource_id`\
    , `link_title`, `link`, `last_updated`) VALUES (%s,%s,%s,%s,%s)'

    cursor1.execute(selectQuery1)

    codeParser = cursor1.fetchall()

    for code in codeParser:
        code = str(code)[2:-3]

        selectQuery2 = 'SELECT `homehtml` FROM `gc_project_indexes` where\
        `unixname` = "' + code + '"'

        cursor2.execute(selectQuery2)

        html = cursor2.fetchall()

        for links in html:
            links = str(links)

            website = re.search('.+<li class="psmeta"><b>External links</b>' +
                                '</li>\\\\n \\\\n <li class="psmeta">\\\\n ' +
                                '<a href="(.+?)" rel="nofollow">(.+?)' +
                                '</a>.+', links)
            blog = re.search('<li class="psmeta"><b>Blogs</b></li>\\\\n ' +
                             '\\\\n <li class="psmeta">\\\\n <a href="(.+?)"' +
                             ' rel="nofollow">(.+?)</a>\\\\n', links)
            if website:
                url = website.group(2)
                url_description = website.group(1)
                print(url_description)
                print(url)

                # ======
                # LOCAL
                # ======
                try:
                    cursor2.execute(insertQuery, (code, datasource_id, url,
                                                  url_description,
                                                  datetime.datetime.now()))
                    dbh2.commit()
                except pymysql.Error as error:
                    print(error)
                    dbh2.rollback()
                # =======
                # REMOTE
                # =======
                try:
                    cursor4.execute(insertQuery, (code, datasource_id, url,
                                                  url_description,
                                                  datetime.datetime.now()))
                    dbh3.commit()
                except pymysql.Error as error:
                    print(error)
                    dbh3.rollback()

            if blog:
                url = blog.group(2)
                url_description = blog.group(1)
                print(url_description)
                print(url)

                # ======
                # LOCAL
                # ======
                try:
                    cursor2.execute(insertQuery, (code, datasource_id, url,
                                                  url_description,
                                                  datetime.datetime.now()))
                    dbh2.commit()
                except pymysql.Error as error:
                    print(error)
                    dbh2.rollback()
                # =======
                # REMOTE
                # =======
                try:
                    cursor4.execute(insertQuery, (code, datasource_id, url,
                                                  url_description,
                                                  datetime.datetime.now()))
                    dbh3.commit()
                except pymysql.Error as error:
                    print(error)
                    dbh3.rollback()
cursor1.close()
cursor2.close()
cursor3.close()
cursor4.close()


dbh1.close()
dbh2.close()
dbh3.close()
