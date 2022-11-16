import re

from table import Table
import pickle
import os
import sqlite3


class Database:
    def __init__(self,name):
        self.__name = name
        self.__tables = []
        self.__path = None
        self.__conn = None

    def get_name(self):
        return self.__name

    def get_path(self):
        return self.__path

    def add_table(self,name):
        cur = self.__conn.cursor()
        cur.execute("CREATE TABLE "+name+" (id INT);")
        self.__tables.append(name)

    def get_tables_names(self):
        return self.__tables

    def rename_table(self, name, new_name):
        cur = self.__conn.cursor()
        cur.execute("ALTER TABLE "+str(name)+
                    " RENAME TO "+str(new_name)+";")
        for i in range(0,len(self.__tables)):
            if self.__tables[i] == name:
                self.__tables[i] = new_name
                break
        cur.close()
        self.__conn.commit()

    def get_table(self,name):
        tbl = Table(name, self.__conn)
        return tbl

    def delete_table(self, name):
        cur = self.__conn.cursor()
        cur.execute("DROP TABLE "+str(name))
        for el in self.__tables:
            if el == name:
                self.__tables.remove(el)
                break
        cur.close()
        self.__conn.commit()

    def save(self,path):
        self.__path = path
        self.__conn.commit()
        self.__conn.close()

    def load(self,path,name):
        if os.path.exists(path):
            self.__conn = sqlite3.connect(path)
            cur = self.__conn.cursor()
            tbls = cur.execute("SELECT name FROM sqlite_master WHERE TYPE='table'")
            self.__tables = []
            for el in tbls:
                self.__tables.append(str(el[0]))
            self.__name = name
            self.__path = path
            cur.close()
        else:
            self.__conn = sqlite3.connect(path)
            self.__name = name
            self.__tables = []
            self.__path = path

    def rename(self,name):
        if self.__path is not None:
            temp = self.__path
            temp2 = re.split(self.__name,temp)
            repl = temp2[0]
            for i in range(1,len(temp2)-1):
                repl+=self.__name+temp2[i]
            repl+=name+temp2[len(temp2)-1]
            self.__path = repl
            os.rename(temp,self.__path)
        self.__name=name

    def delete(self):
        self.__conn.close()
        if self.__path is not None:
            os.remove(self.__path)

    def table_mult(self,name1, name2):
        rows1 = []
        rows2 = []
        cols1 = []
        cols2 = []
        for el in self.__tables:
            if el==name1:
                tbl1 = Table(el,self.__conn)
                rows1 = tbl1.get_rows()
                cols1 = tbl1.get_columns_names_types()
            if el==name2:
                tbl2 = Table(el,self.__conn)
                rows2 = tbl2.get_rows()
                cols2 = tbl2.get_columns_names_types()

        cols = cols1+cols2
        rows = []
        for el1 in rows1:
            for el2 in rows2:
                rows.append((el1+el2))
        return rows,cols