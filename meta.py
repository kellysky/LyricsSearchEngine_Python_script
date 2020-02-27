# import sys
import mysql.connector
from mysql.connector import Error
import pandas as pd

#！ls
# Change the following 3 to your settings.
my_username='test'
my_password='test'
my_database='lyrics'
my_db_server='8.209.74.127'



connection = mysql.connector.connect(user=my_username, password=my_password, host=my_db_server, database=my_database)
cursor = connection.cursor(buffered=True)


cursor.execute("Select * FROM Song")
myresult = cursor.fetchall()


cursor.close()
connection.close()



string = ""

total = 0
for t1 in myresult:
    
    tid = str(t1[0])
    length = len(t1[-2].split(","))
    total += length
                 
    string += tid +  " "+ str(length) + "\n"
                 
string += "CORPUS_SIZE " + str(len(myresult))
string += "\nTOTAL_NO_OF_TOKENS " + str(total)
                 
                 

with open("MetaData_index", 'w', encoding='gb18030') as f:
    f.write(string)
f.close()    
    