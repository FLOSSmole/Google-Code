import MySQLdb
import datetime
import os
import codecs
import sys

#Constants
#datasourceid = int(sys.argv[1])
linenum = 1

#Establishes connection to the database
db = MySQLdb.connect(host="grid6.cs.elon.edu", user="groth", passwd="Monsterhunter12", db="test", use_unicode=True, charset = "utf8")
cursor = db.cursor()
cursor.execute('SET NAMES utf8mb4')
cursor.execute('SET CHARACTER SET utf8mb4')
cursor.execute('SET character_set_connection=utf8mb4')



#pulls all the files in the given directory and stors them
lines= codecs.open("C:/Users/groth/Desktop/googlecode/GCProjectList.txt", 'r', encoding='utf-8', errors='ignore')

for line in lines:
    print ("current line is %d", linenum)
    currentLine = line.split(',')
    print(currentLine[0])
    
    if len(currentLine) == 5: 
        try:
            cursor.execute("INSERT INTO `gc_projects`(`proj_name`, `datasource_id`,\
            `last_updated`, `code_license`, `activity_level`, \
            `project_summary`) VALUES (%s,%s,%s,%s,%s,%s)",
            (currentLine[0],58459,datetime.datetime.now(),currentLine[3], currentLine[1], currentLine[4]))
            db.commit()
        except MySQLdb.Error as error:
            print(error)
            db.rollback()
    linenum = linenum + 1
cursor.close()
db.close()
