import MySQLdb
import datetime
import codecs

linenum = 1
datasource_id = 58459

db = MySQLdb.connect(host="", 
                    user="",
                    passwd="",
                    db="",
                    use_unicode=True,
                    charset = "utf8")
cursor = db.cursor()

lines= codecs.open("gcProjectDates.txt", 'r', encoding='utf-8', errors='ignore')
next (lines)
for line in lines:
    print ("current line is %d", linenum)
    currentLine = line.split(',')
    print(currentLine[0])
    
    if len(currentLine) == 6: 
        try:
            proj_name = currentLine[0]
            timestamp = currentLine[4]
            print timestamp
            if timestamp != "[NULL]":
                convertDate = datetime.datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
            
                cursor.execute("INSERT INTO gc_project_creates(\
                proj_name, \
                datasource_id, \
                timestamp, \
                convert_date, \
                last_updated) \
                VALUES (%s,%s,%s,%s,%s)",
                (proj_name, 
                datasource_id, 
                timestamp, 
                convertDate, 
                datetime.datetime.now(),))
                db.commit()
        except MySQLdb.Error as error:
            print(error)
            db.rollback()
    linenum = linenum + 1
cursor.close()
db.close()
