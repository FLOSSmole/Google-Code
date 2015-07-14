import MySQLdb
import datetime
import codecs

#Constants
datasourceid = 58459
linenum = 1

#Establishes connection to the database
db = MySQLdb.connect(host="", user="", passwd="", db="", use_unicode=True, charset = "utf8")
cursor = db.cursor()

lines = codecs.open("GCProjectList.txt", 'r', encoding='utf-8', errors='ignore')

for line in lines:
    print ("current line is %d", linenum)
    currentLine = line.split(',')
    print(currentLine[0])
    
    if len(currentLine) == 5: 
        try:
            cursor.execute("INSERT INTO `gc_projects`(`proj_name`, `datasource_id`,\
            `last_updated`, `code_license`, `activity_level`, \
            `project_summary`) VALUES (%s,%s,%s,%s,%s,%s)",
            (currentLine[0],datasource_id,datetime.datetime.now(),currentLine[3], currentLine[1], currentLine[4]))
            db.commit()
        except MySQLdb.Error as error:
            print(error)
            db.rollback()
    linenum += 1
cursor.close()
db.close()
