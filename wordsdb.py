import mysql.connector
import re

conn = mysql.connector.connect(
    host='localhost',
    user="root",
    password="sucram1002",
    database="vocab")

cursor = conn.cursor()
cursor.execute("SHOW DATABASES")
found = False
# Checks if database already exists. If it doesnt, it will create the database
for db in cursor:
    pattern = "[(,')]"
    db_string = re.sub(pattern, "", str(db))
    if db_string == 'vocab':
        found = True
        print("database vocab exists")
if not found:
    cursor.execute("CREATE DATABASE vocab")

sql = "DROP TABLE IF EXISTS vocab_table "
cursor.execute(sql)
sql = "CREATE TABLE vocab_table(word VARCHAR(255), definition VARCHAR(255))"
cursor.execute(sql)

# Read Data from a .csv file for insertion to MySQL
fh = open('Vocabulary_list.csv', "r")
wd_list = fh.readlines()
wd_list.pop(0)
vocab_list = []
for rawstring in wd_list:
    word, defenition = rawstring.split(',', 1)
    definition = defenition.rstrip()
    vocab_list.append({word, defenition})
    sql = "INSERT INTO vocab_table(word,definition) VALUES(%s,%s)"
    values = (word,definition)
    cursor.execute(sql,values)

    conn.commit()
    print("Inserted " + str(cursor.rowcount)+ " row into vocab table")

# Query 1: Selecting all rows
sql = "SELECT * from vocab_table" # selects everything
cursor.execute(sql) # Executes query
result = cursor.fetchall()
for row in result: # reiterates through each row and prints each row
    print(row)

print("----End of Query 1----")

# Query 2: Selecting a specific word from dictionary
sql = "SELECT * from vocab_table WHERE word = %s" # selects everything
value = ('boisterous',)
cursor.execute(sql,value) # Executes query
result = cursor.fetchall()
for row in result: # reiterates through each row and prints each row
    print(row)
print("----End of Query 2----")

# Updating a row
sql = "UPDATE  vocab_table SET definition = %s WHERE word = %s"
value = ("Spirited; lovely", "boisterous")
cursor.execute(sql,value)
conn.commit()
print("modified row count: ", cursor.rowcount)

# Query for updated definition
sql = "SELECT * from vocab_table WHERE word = %s" # selects everything
value = ('boisterous',)
cursor.execute(sql,value) # Executes query
result = cursor.fetchall()
for row in result:  # reiterates through each row and prints each row
    print(row)
