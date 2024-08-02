import sqlite3

class DataBase:
    """This class connect to Users Database"""

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()



# DataBase.cursor.execute("CREATE TABLE table1 (userid INTEGER , balance INTEGER , count INTEGER , warnings INTEGER)")