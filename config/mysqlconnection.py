# a cursor is the object we use to interact with the database
from multiprocessing import connection
import pymysql.cursors

# this class will give us an instance of a connection to our database


class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='rootroot',
                                     db=db,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor,
                                     autocommit=True)
        self.connection = connection

    # the method to query the database
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print('Running query', query)
                cursor.execute(query, data)

                if query.lower().find('insert') >= 0:
                    # INSERT queries will return the ID number of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find('select') >= 0:
                    # SELECT queries will return the data from the database
                    # as a LIST of DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE or DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # IF the query fails the method will return False
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close()

# connectToMySQL receives the database we're using and uses it to create an
    # instance of MySQLConnection class


def connectToMySQL(db):
    return MySQLConnection(db)
