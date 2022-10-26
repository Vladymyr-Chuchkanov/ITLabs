import re

from table import Table
import pickle
import os

class Database:
    def __init__(self,name):
        self.__name = name
        self.__tables = []
        self.__path = None

    def get_name(self):
        return self.__name

    def get_path(self):
        return self.__path

    def add_table(self,name):
        tbl = Table(name)
        self.__tables.append(tbl)

    def get_tables(self):
        return self.__tables

    def get_tables_names(self):
        res = []
        for el in self.__tables:
            res.append(el.get_name())
        return res

    def rename_table(self, name, new_name):
        for el in self.__tables:
            if el.get_name() == name:
                el.rename(new_name)
                break

    def get_table(self,name):
        for el in self.__tables:
            if el.get_name() == name:
                return el

    def delete_table(self,name):
        for el in self.__tables:
            if el.get_name() == name:
                self.__tables.remove(el)
                break

    def save(self,path):
        self.__path = path
        pickle.dump(self,open(path,"wb"),protocol=pickle.HIGHEST_PROTOCOL)

    def load(self,path):
        if os.path.exists(path):
            db = pickle.load(open(path,'rb'))
            self.__name = db.get_name()
            self.__tables = db.get_tables()
            self.__path = db.get_path()

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
        os.remove(self.__path)

    def table_mult(self,name1, name2):
        rows1 = []
        rows2 = []
        cols1 = []
        cols2 = []
        for el in self.__tables:
            if el.get_name()==name1:
                tbl1 = el
                rows1 = tbl1.get_rows()
                cols1 = tbl1.get_columns_names_types()
            if el.get_name()==name2:
                tbl2 = el
                rows2 = tbl2.get_rows()
                cols2 = tbl2.get_columns_names_types()

        cols = cols1+cols2
        rows = []
        for el1 in rows1:
            for el2 in rows2:
                rows.append((el1+el2))
        return rows,cols