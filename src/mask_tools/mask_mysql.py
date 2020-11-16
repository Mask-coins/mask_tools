import mysql.connector
import datetime
import time

MIN_TIMEDELTA = datetime.datetime(1971,1,1,1,1,1,1)


class DuplicateEntryError(Exception):
    pass


def escape(text:str):
    text = text.replace('\\','\\\\')
    text = text.replace('\'','\\\'')
    text = text.replace('\"','\\\"')
    return text


def query_insert(db:str, table:str, d):
    if isinstance(d, dict):
        col = ""
        val = ""
        for key in d:
            col = col + "," + key
            if type(d[key]) == bool:
                val = val + "," + str(int(d[key]))
            elif type(d[key]) == str:
                val = val + ",'" + escape(d[key]) + "'"
            else:
                val = val + ",'" + escape(str(d[key])) + "'"
        query = "INSERT INTO `" + db + "`.`" + table + "` (" + col[1:] + ") VALUES (" + val[1:] + ");"
        return query
    if isinstance(d, (list,tuple)):
        val = ""
        for data in d:
            if type(data) == bool:
                val = val + "," + str(int(data))
            elif type(data) == str:
                val = val + ",'" + escape(data) + "'"
            else:
                val = val + ",'" + escape(str(data)) + "'"
        query = "INSERT INTO `" + db + "`.`" + table + "` VALUES (" + val[1:] + ");"
        return query
    print('')
    raise TypeError('dict,list,tuple型を入力してください')


class SQL(object):
    def __init__(self, host='localhost', port=3306, user='root', password='password', databese='databese', charset='utf8mb4'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.databese = databese
        self.charset = charset
        self.conn = None
        self.cur = None
        self.cur_dict = None
        self.set()

    def set(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.databese,
            charset=self.charset)
        self.cur = self.conn.cursor()
        self.cur_dict = self.conn.cursor(dictionary=True)

    def execute(self,query):
        self.set()
        try:
            self.cur.execute(query)
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            if '1062 (23000)' in str(e):
                raise DuplicateEntryError
        except mysql.connector.errors.DatabaseError as e:
            print(e)
            if "1064 (42000)" in str(e):
                raise
            timecount = 0
            while(timecount<12):
                time.sleep(5)
                timecount+=1
                print("sleep" + str(timecount*5))
            self.cur.execute(query)

    def commit(self):
        try:
            self.conn.commit()
        except mysql.connector.errors.DatabaseError as e:
            print(e)
            timecount = 0
            while(timecount<12):
                time.sleep(5)
                timecount+=1
                print("sleep" + str(timecount*5))
            try:
                self.conn.commit()
            except:
                self.conn.rollback()
        except:
            self.conn.rollback()

    def close(self):
        self.conn.close()

    def fetch(self,query:str,DBname:str):
        self.execute(query)
        r = self.cur.fetchall()
        self.conn.close()
        return r

    def fetch_dict(self,query:str,DBname:str):
        self.execute(query)
        r = self.cur_dict.fetchall()
        self.conn.close()
        return r

    def insert(self,db:str, table:str, d):
        query = query_insert(db,table,d)
        self.execute(query)
        self.commit()
        self.close()
