import sys
import mysql.connector
from mysql.connector import Error
import pandas as pd

#！ls
# Change the following 3 to your settings.
my_username='root'
my_password='password'
my_database='lyrics'
my_db_server='8.209.74.127'

filename = sys.argv[1]


try:
    # Connect to the MySQL database.
    connection = mysql.connector.connect(user=my_username, password=my_password, host=my_db_server, database=my_database)
    cursor = connection.cursor()
    # filename = "df2.csv"
    df = pd.read_csv(filename)
    all_list = df.values.tolist()

    for i in range(df.shape[0]):
        sql = "INSERT INTO Song (id, singer, song_name, content) VALUES (%s, %s, %s, %s)"
        val = tuple(all_list[i])


        cursor.execute(sql,val)

        connection.commit()

except Error as e:
    print(e)

finally:
    cursor.close()
    connection.close()


print(filename + " done!")
