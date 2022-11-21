import json

from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable, String
from lxml import etree
from spyne.protocol.soap import Soap11
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

from accounts import Accounts

acc = Accounts()
loged=[]

class Server(ServiceBase):

    @rpc()
    def Save(self):
        acc.save()

    @rpc(_returns=Unicode)
    def get_selected(self):
        return acc.get_selected()

    @rpc(_returns=Unicode)
    def get_dbs(self):
        return json.dumps(acc.get_dbs())

    @rpc(Unicode, _returns=Unicode)
    def get_tables_names(self, name):
        return json.dumps(acc.get_db(name).get_tables_names())

    @rpc(Unicode)
    def delete_db(self,name):
        acc.delete_db(name)

    @rpc(Unicode,Unicode)
    def delete_table(self,dbname,name):
        acc.get_db(dbname).delete_table(name)

    @rpc(Unicode,Unicode)
    def add_table(self,dbname,name):
        acc.get_db(dbname).add_table(name)

    @rpc(Unicode,Unicode,Unicode)
    def rename_table(self,dbname,name,newname):
        acc.get_db(dbname).rename_table(name,newname)

    @rpc(Unicode,Unicode, _returns=Unicode)
    def get_columns_names_types(self,dbname, name):
        return json.dumps(acc.get_db(dbname).get_table(name).get_columns_names_types())

    @rpc(Unicode,Unicode, _returns=Unicode)
    def get_columns_names(self,dbname, name):
        return json.dumps(acc.get_db(dbname).get_table(name).get_columns_names())

    @rpc(Unicode,Unicode,Integer,Integer, _returns=Unicode)
    def get_rows(self,dbname,name,n1,n2):
        return json.dumps(acc.get_db(dbname).get_table(name).get_rows(n1,n2))

    @rpc(Unicode,Unicode, _returns=Unicode)
    def get_rows_num(self,dbname,name):
        return json.dumps(acc.get_db(dbname).get_table(name).get_rows_num())

    @rpc(Unicode,Unicode,Unicode,Unicode)
    def add_column(self,dbname,tblname,name,type):
        acc.get_db(dbname).get_table(tblname).add_column(name,type)

    @rpc(Unicode,Unicode,Unicode,Unicode)
    def rename_column(self,dbname,tblname,name,newname):
        acc.get_db(dbname).get_table(tblname).rename_column(name,newname)

    @rpc(Unicode,Unicode,Unicode, _returns=Unicode)
    def table_mult(self,dbname,tbl1,tbl2):
        return json.dumps(acc.get_db(dbname).table_mult(tbl1,tbl2))

    @rpc(Unicode,Unicode,Iterable(String), _returns=Unicode)
    def add_row(self,dbname,tblname,data):
        return json.dumps(acc.get_db(dbname).get_table(tblname).add_row(data))

    @rpc(Unicode,Unicode,Integer)
    def delete_row(self,dbname,tblname,n):
        acc.get_db(dbname).get_table(tblname).delete_row(n)

    @rpc(Unicode, _returns=Unicode)
    def log_in(self,login):
        if login in loged:
            return json.dumps("two emails")
        return json.dumps(acc.log_in(login))

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