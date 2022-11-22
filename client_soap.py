import copy
import json
import requests
import suds.sax.text
from suds.client import Client

class Client_soap:
    def __init__(self):
        self.url = 'http://localhost:8001?wsdl'
        self.selected = ""
        self.c = Client('http://localhost:8001/?wsdl')
        self.help = self.c.service.helper()

    def save(self):
        self.c.service.Save(self.selected)

    def get_selected(self):
        return self.selected

    def add_db(self,name):
        self.c.service.add_db(self.selected,name)

    def get_dbs(self):
        res = self.c.service.get_dbs(self.selected)
        if res == "":
            return []
        response = list(res[0])
        return response

    def get_tables_names(self, name):
        res = self.c.service.get_tables_names(self.selected,name)
        if res == "":
            return []
        response = list(res[0])
        return response

    def delete_db(self,name):
        self.c.service.delete_db(self.selected,name)

    def delete_table(self,dbname, name):
        self.c.service.delete_table(self.selected,dbname,name)

    def get_columns_names_types(self,dbname,name):
        res = self.c.service.get_columns_names_types(self.selected,dbname,name)
        if res == "":
            return []
        response = list(res[0])
        return response

    def add_table(self,dbname,name):
        self.c.service.add_table(self.selected,dbname,name)

    def rename_table(self,dbname,name,newname):
        self.c.service.rename_table(self.selected,dbname,name,newname)

    def get_rows(self,dbname,name,n1,n2):
        res0 = self.c.service.get_rows(self.selected,dbname,name,n1,n2)
        if res0 == "":
            return []
        response = list(res0[0])
        res = []
        for el in response:
            res.append(el[0])
        return res

    def get_columns_names(self,dbname,name):
        res = self.c.service.get_columns_names(self.selected,dbname,name)
        if res == "":
            return []
        response = list(res[0])
        return response

    def get_rows_num(self,dbname,name):
        response = self.c.service.get_rows_num(self.selected,dbname,name)
        return response

    def add_column(self, dbname, tblname, name, type):
        self.c.service.add_column(self.selected,dbname,tblname,name,type)

    def rename_column(self,dbname,tblname,name,newname):
        self.c.service.rename_column(self.selected,dbname,tblname,name,newname)

    def table_mult(self,dbname,tbl1,tbl2):
        res = self.c.service.table_mult(self.selected,dbname,tbl1,tbl2)
        rows=[]
        cols = list(res[1][0])
        for el in res[0][0]:
            rows.append(list(el[0]))
        return rows,cols

    def add_row(self, dbname, tblname, data):
        temp = self.help
        tdata = data
        for i in range(0,len(tdata)):
            tdata[i]=suds.sax.text.Text(str(tdata[i]))
        temp["string"]=tdata
        res = self.c.service.add_row(self.selected,dbname,tblname,temp)
        if res == "":
            return [],[]
        response = res
        return response[0],response[1]

    def delete_row(self,dbname,tblname,n):
        self.c.service.delete_row(self.selected,dbname,tblname,n)

    def log_in(self, login):
        response = self.c.service.log_in(login)
        if response == "OK":
            self.selected=login
        return response

    def register(self,login):
        response = self.c.service.register(login)
        if response == "OK":
            self.selected=login
        return response

    def log_out(self):
        self.c.service.log_out(self.selected)