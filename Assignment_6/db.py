import mysql.connector

def create_or_update_sql_db():
    db = mysql.connector.connect(
      host="localhost",
      user="root",
      password="root"
    )

    cursor = db.cursor()

    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print(databases)
    if(('chatbot_kb',) in databases):
        print('Updating existing SQL database chatbot_kb')
        cursor.execute("DROP TABLE terms")
    else:
        print('Creating new SQL database chatbot_kb')
        cursor.execute("CREATE DATABASE chatbot_kb")



if __name__ == '__main__':
    create_or_update_sql_db()