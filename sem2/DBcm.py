import pymysql
class DBCconnection:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection=pymysql.connect(**self.config)
            self.cursor=self.connection.cursor()
            return self.cursor
        except Exception as e:
            print(e)
            return None
    def __exit__(self, exc_type, exc_val,exc_tb):
        if exc_type is not None:
            print(exc_val)
            if self.connection is not None:
                self.connection.commit()
                self.cursor.close()
                self.connection.close()
            return True
        self.connection.rollback()
        self.cursor.close()
        self.connection.close()
        return

class DBContextManager:





    db_config= {
    'host' : '127.0.0.1',
    'port' : 3306,
    'user' : 'root',
    'password' : '1590',
    'db' : 'MyShop'
    }
    result =[]
    with DBCconnection(db_config) as cursor:
        if cursor is None:
            raise ValueError("Cursor is None")
        cursor.execute(" select * from product limit 1")
        schema = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(schema,row)))
        print(result)