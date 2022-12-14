import pymysql.cursors
from env import db_pw

class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(host = 'localhost',
                #this is the only section we'll have to edit User/password
                user = 'root',
                password = db_pw,
                db = db,
                charset = 'utf8mb4',
                cursorclass = pymysql.cursors.DictCursor,
                autocommit = True)
        self.connection = connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    #INSERT queries return id number of row inserted.
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    #SELECT queries return all data
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong!", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)