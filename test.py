import os.path

import pytest
from accounts import Accounts
from database import Database
from table import Table

class Test_Class:
    def setup(self):
        self.account = Accounts()
        self.db1 = Database("test")


    def test_register(self):
        assert self.account.register("not_emeil") == "Bad email"
        assert self.account.register("still.not-email@not_email") == "Bad email"
        assert self.account.register("email.=+*@test.com") == "OK"
        assert self.account.register("email.=+*@test.com") == "No email"

    def test_log_in(self):
        assert self.account.log_in("not_emeil") == "Bad email"
        assert self.account.log_in("still.not-email@not_email") == "Bad email"
        assert self.account.log_in("email.=+*@test.com")=="No email"
        assert self.account.register("email.=+*@test.com") == "OK"
        assert self.account.log_in("email.=+*@test.com") == "OK"

    def test_add_save_del_db(self):
        self.account.register("email@test.com")
        self.account.log_in("email@test.com")
        self.account.add_db("test")
        assert self.account.get_db("test").get_name() == self.db1.get_name()
        assert self.account.get_db("test").get_tables_names() == self.db1.get_tables_names()
        self.account.save_db()
        assert os.path.exists("files/email@test.comtest.pkl")==True
        self.account.get_db("test")
        self.account.rename("test2")
        self.account.save_db()
        assert os.path.exists("files/email@test.comtest2.pkl") == True
        self.account.get_db("test2")
        self.account.delete_db("test2")
        assert os.path.exists("files/email@test.comtest2.pkl") == False

    def test_table_mult(self):
        self.db1.add_table("tbl1")
        self.db1.add_table("tbl2")
        self.tbl1 = self.db1.get_table("tbl1")
        self.tbl2 = self.db1.get_table("tbl2")
        self.tbl1.add_column("col11", "int")
        self.tbl1.add_column("col12", "string")
        self.tbl1.add_row(['1', 'fgh'])
        self.tbl1.add_row(['2', 'fgh2'])
        self.tbl2.add_column("col21", "real")
        self.tbl2.add_column("col22", "char")
        self.tbl2.add_row(['2.2', '&'])
        self.tbl2.add_row(['2.1', 'b'])
        data,head = self.db1.table_mult("tbl1","tbl2")
        assert len(data) == 4
        assert head == ['col11:int','col12:string','col21:real','col22:char']
        assert ['1','fgh','2.1','b'] in data