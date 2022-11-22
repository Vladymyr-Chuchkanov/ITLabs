import json
import requests


class Client:
    def __init__(self):
        self.url = 'http://localhost:8000?wsdl'
        self.selected = ""

    def save(self):
        data = {"Save": {"login":self.selected}}
        requests.post(self.url, data=json.dumps(data), verify=False)

    def get_selected(self):
        return self.selected

    def add_db(self,name):
        data = {"add_db": {"login": self.selected, "name": name}}
        requests.post(self.url, data=json.dumps(data), verify=False)

    def get_dbs(self):
        data = {"get_dbs": {"login":self.selected}}
        answer = requests.post(self.url, data=json.dumps(data), verify=False)
        response = json.loads(answer.json())
        return response

    def get_tables_names(self, name):
        data = {"get_tables_names": {"login":self.selected,"name":name}}
        answer = requests.post(self.url, data=json.dumps(data), verify=False)
        response = json.loads(answer.json())
        return response

    def delete_db(self,name):
        data = {"delete_db": {"login":self.selected,"name": name}}
        requests.post(self.url, data=json.dumps(data), verify=False)

    def delete_table(self,dbname, name):
        data = {"delete_table": {"login":self.selected,"dbname":dbname,"name":name}}
        requests.post(self.url, data=json.dumps(data), verify=False)

    def get_columns_names_types(self,dbname,name):
        data = {"get_columns_names_types": {"login":self.selected,"dbname":dbname,"name": name}}
        answer = requests.post(self.url, data=json.dumps(data), verify=False)
        response = json.loads(answer.json())
        return response

    def add_table(self,dbname,name):
        data = {"add_table": {"login":self.selected,"dbname": dbname, "name": name}}
        requests.post(self.url, data=json.dumps(data), verify=False)

    def rename_table(self,dbname,name,newname):
        data = {"rename_table": {"login":self.selected,"dbname": dbname, "name": name,"newname":newname}}
        requests.post(self.url, data=json.dumps(data), verify=False)

    def get_rows(self,dbname,name,n1,n2):
        data = {"get_rows": {"login":self.selected,"dbname": dbname, "name": name,"n1":n1,"n2":n2}}
        answer = requests.post(self.url, data=json.dumps(data), verify=False)
        response = json.loads(answer.json())
        return response

    def get_columns_names(self,dbname,name):
        data = {"get_columns_names": {"login":self.selected,"dbname": dbname, "name": name}}
        answer = requests.post(self.url, data=json.dumps(data), verify=False)
        response = json.loads(answer.json())
        return response

    def get_rows_num(self,dbname,name):
        data = {"get_rows_num": {"login":self.selected,"dbname": dbname, "name": name}}
        answer = requests.post(self.url, data=json.dumps(data), verify=False)
        response = json.loads(answer.json())
        return response

    def add_column(self,dbname,tblname,name,type):
        data = {"add_column": {"login":self.selected,"dbname": dbname,"tblname":tblname, "name": name,"type":type}}
        requests.post(self.url, data=json.dumps(data), verify=False)

    def rename_column(self,dbname,tblname,name,newname):
        data = {"rename_column": {"login":self.selected,"dbname": dbname, "tblname": tblname, "name": name, "newname": newname}}
        requests.post(self.url, data=json.dumps(data), verify=False)

    def table_mult(self,dbname,tbl1,tbl2):
        data = {"table_mult": {"login":self.selected,"dbname": dbname, "tbl1": tbl1,"tbl2":tbl2}}
        answer = requests.post(self.url, data=json.dumps(data), verify=False)
        response = json.loads(answer.json())
        return response

    def add_row(self, dbname, tblname, data):
        data = {"add_row": {"login":self.selected,"dbname": dbname, "tblname": tblname,  "data": data}}
        answer = requests.post(self.url, data=json.dumps(data), verify=False)
        response = json.loads(answer.json())
        return response

    def delete_row(self,dbname,tblname,n):
        data = {"delete_row": {"login":self.selected,"dbname": dbname, "tblname": tblname, "n": n}}
        requests.post(self.url, data=json.dumps(data), verify=False)

    def log_in(self, login):
        data = {"log_in": {"login": login}}
        answer = requests.post(self.url, data=json.dumps(data), verify=False)
        response = json.loads(answer.json())
        if response == "OK":
            self.selected=login
        return response

    def register(self,login):
        data = {"register": {"login": login}}
        answer = requests.post(self.url, data=json.dumps(data), verify=False)
        response = json.loads(answer.json())
        if response == "OK":
            self.selected=login
        return response
    def log_out(self):
        data = {"log_out": {"login":self.selected}}
        requests.post(self.url, data=json.dumps(data), verify=False)