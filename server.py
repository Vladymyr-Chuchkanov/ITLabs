import json

from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable, String
from lxml import etree
from spyne.protocol.soap import Soap11
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

from accounts import Accounts

acc = Accounts()
accs = []
loged=[]

class Server(ServiceBase):

    @rpc(Unicode)
    def Save(self, login):
        accs[login].save()

    @rpc(Unicode)
    def log_out(self, login):
        loged.remove(login)
        for el in accs:
            if el.get_selected()==login:
                accs.remove(el)
                break

    @rpc(Unicode,_returns=Unicode)
    def get_dbs(self,login):
        return json.dumps(accs[loged.index(login)].get_dbs())

    @rpc(Unicode, Unicode)
    def add_db(self,login,name):
        accs[loged.index(login)].add_db(name)

    @rpc(Unicode,Unicode, _returns=Unicode)
    def get_tables_names(self, login,name):
        return json.dumps(accs[loged.index(login)].get_db(name).get_tables_names())

    @rpc(Unicode,Unicode)
    def delete_db(self,login,name):
        accs[loged.index(login)].delete_db(name)

    @rpc(Unicode,Unicode,Unicode)
    def delete_table(self,login,dbname,name):
        accs[loged.index(login)].get_db(dbname).delete_table(name)

    @rpc(Unicode,Unicode,Unicode)
    def add_table(self,login,dbname,name):
        accs[loged.index(login)].get_db(dbname).add_table(name)

    @rpc(Unicode,Unicode,Unicode,Unicode)
    def rename_table(self,login,dbname,name,newname):
        accs[loged.index(login)].get_db(dbname).rename_table(name,newname)

    @rpc(Unicode,Unicode,Unicode, _returns=Unicode)
    def get_columns_names_types(self,login,dbname, name):
        return json.dumps(accs[loged.index(login)].get_db(dbname).get_table(name).get_columns_names_types())

    @rpc(Unicode,Unicode,Unicode, _returns=Unicode)
    def get_columns_names(self,login,dbname, name):
        return json.dumps(accs[loged.index(login)].get_db(dbname).get_table(name).get_columns_names())

    @rpc(Unicode,Unicode,Unicode,Integer,Integer, _returns=Unicode)
    def get_rows(self,login,dbname,name,n1,n2):
        return json.dumps(accs[loged.index(login)].get_db(dbname).get_table(name).get_rows(n1,n2))

    @rpc(Unicode,Unicode,Unicode, _returns=Unicode)
    def get_rows_num(self,login,dbname,name):
        return json.dumps(accs[loged.index(login)].get_db(dbname).get_table(name).get_rows_num())

    @rpc(Unicode,Unicode,Unicode,Unicode,Unicode)
    def add_column(self,login,dbname,tblname,name,type):
        accs[loged.index(login)].get_db(dbname).get_table(tblname).add_column(name,type)

    @rpc(Unicode,Unicode,Unicode,Unicode,Unicode)
    def rename_column(self,login,dbname,tblname,name,newname):
        accs[loged.index(login)].get_db(dbname).get_table(tblname).rename_column(name,newname)

    @rpc(Unicode,Unicode,Unicode,Unicode, _returns=Unicode)
    def table_mult(self,login,dbname,tbl1,tbl2):
        return json.dumps(accs[loged.index(login)].get_db(dbname).table_mult(tbl1,tbl2))

    @rpc(Unicode,Unicode,Unicode,Iterable(String), _returns=Unicode)
    def add_row(self,login,dbname,tblname,data):
        return json.dumps(accs[loged.index(login)].get_db(dbname).get_table(tblname).add_row(data))

    @rpc(Unicode,Unicode,Unicode,Integer)
    def delete_row(self,login,dbname,tblname,n):
        accs[loged.index(login)].get_db(dbname).get_table(tblname).delete_row(n)

    @rpc(Unicode, _returns=Unicode)
    def log_in(self,login):
        if login in loged:
            return json.dumps("two emails")
        temp = acc.log_in(login)
        if temp == "OK":
            loged.append(login)
            tmp = Accounts()
            tmp.refresh(login)
            accs.append(tmp)
        return json.dumps(temp)

    @rpc(Unicode, _returns=Unicode)
    def register(self,login):
        return json.dumps(acc.register(login))




if __name__ == '__main__':
    app = Application([Server], tns='Server',
                      in_protocol=JsonDocument(validator='soft'),
                      out_protocol=JsonDocument())
    application = WsgiApplication(app)
    server = make_server('0.0.0.0', 8000, application)
    server.serve_forever()