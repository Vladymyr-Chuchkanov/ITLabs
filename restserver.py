import json

from bson import json_util
from flask import Flask, request, jsonify

from accounts import Accounts
from column import TYPES

app = Flask(__name__)
acc = Accounts()
accs = []
loged=[]


@app.post("/account/login/<login>")
def login(login):
    if login in loged:
        return json.dumps("two emails")
    temp = acc.log_in(login)
    if temp == "OK":
        loged.append(login)
        tmp = Accounts()
        tmp.refresh(login)
        accs.append(tmp)
    acc.log_in(login)
    return json.dumps(temp)


@app.get("/account/login")
def get_logined():
    return json.dumps(loged)


@app.post("/account/register/<login>")
def register(login):
    return json.dumps(acc.register(login))


@app.delete("/account/login/<login>")
def log_out(login):
    if login not in loged:
        return json.dumps("no such email!")
    loged.remove(login)
    for el in accs:
        if el.get_selected() == login:
            accs.remove(el)
            break
    return json.dumps("success")


@app.get("/database/<login>")
def get_dbs(login):
    return json.dumps(accs[loged.index(login)].get_dbs())


@app.post("/database/<login>/<dbname>")
def add_db( login, dbname):
    if login not in loged:
        return json.dumps("no such email!")
    temp = accs[loged.index(login)].get_dbs()
    if dbname not in temp:
        accs[loged.index(login)].add_db(dbname)
        return json.dumps("success")
    return json.dumps(dbname+" already in use!")


@app.delete("/database/<login>/<dbname>")
def delete_db(login, dbname):
    if login not in loged:
        return json.dumps("no such email!")
    temp = accs[loged.index(login)].get_dbs()
    if dbname not in temp:
        return json.dumps("no such database!")
    no = accs[loged.index(login)].get_db(dbname)
    accs[loged.index(login)].delete_db(dbname)
    return json.dumps("success")


@app.get("/table/<login>/<dbname>")
def get_tables_names(login, dbname):
    if login not in loged:
        return json.dumps("no such email!")
    temp = accs[loged.index(login)].get_dbs()
    if dbname not in temp:
        return json.dumps("no such database!")
    return json.dumps(accs[loged.index(login)].get_db(dbname).get_tables_names())


@app.post("/table/<login>/<dbname>/<name>")
def add_table(login, dbname, name):
    if login not in loged:
        return json.dumps("no such email!")
    temp = accs[loged.index(login)].get_dbs()
    if dbname not in temp:
        return json.dumps("no such database!")
    temp2 = accs[loged.index(login)].get_db(dbname).get_tables_names()
    if name in temp2:
        return json.dumps(name+" already in use!")
    accs[loged.index(login)].get_db(dbname).add_table(name)
    return json.dumps("success")

@app.delete("/table/<login>/<dbname>/<name>")
def delete_table(login, dbname, name):
    if login not in loged:
        return json.dumps("no such email!")
    temp = accs[loged.index(login)].get_dbs()
    if dbname not in temp:
        return json.dumps("no such database!")
    temp2 = accs[loged.index(login)].get_db(dbname).get_tables_names()
    if name not in temp2:
        return json.dumps("no such table!")
    accs[loged.index(login)].get_db(dbname).delete_table(name)
    return json.dumps("success")




@app.get("/col/<login>/<dbname>/<tblname>")
def get_cols(login, dbname,tblname):
    if login not in loged:
        return json.dumps("no such email!")
    temp = accs[loged.index(login)].get_dbs()
    if dbname not in temp:
        return json.dumps("no such database!")
    tbls = accs[loged.index(login)].get_db(dbname).get_tables_names()
    if tblname not in tbls:
        return json.dumps("no such table!")
    return json.dumps(accs[loged.index(login)].get_db(dbname).get_table(tblname).get_columns_names_types())


@app.post("/col/<login>/<dbname>/<tblname>/<colname>/<type>")
def add_col(login, dbname,tblname,colname, type):
    if login not in loged:
        return json.dumps("no such email!")
    temp = accs[loged.index(login)].get_dbs()
    if dbname not in temp:
        return json.dumps("no such database!")
    temp2 = accs[loged.index(login)].get_db(dbname).get_tables_names()
    if tblname not in temp2:
        return json.dumps("no such table!")
    if type not in TYPES:
        return json.dumps("no such type!")
    temp3 = accs[loged.index(login)].get_db(dbname).get_table(tblname).get_columns_names_types()
    if colname+"_"+type in temp3:
        return json.dumps(colname+"_"+type+ " already in use!")
    accs[loged.index(login)].get_db(dbname).get_table(tblname).add_column(colname,type)
    return json.dumps("success")

@app.get("/row/<login>/<dbname>/<tblname>")
def get_rows(login, dbname,tblname):
    if login not in loged:
        return json.dumps("no such email!")
    temp = accs[loged.index(login)].get_dbs()
    if dbname not in temp:
        return json.dumps("no such database!")
    temp2 = accs[loged.index(login)].get_db(dbname).get_tables_names()
    if tblname not in temp2:
        return json.dumps("no such table!")
    return json.dumps(accs[loged.index(login)].get_db(dbname).get_table(tblname).get_rows(0,-2))


@app.post("/row/<login>/<dbname>/<tblname>/<data>")
def add_row(login, dbname, tblname, data):
    data = data.split(",")
    if login not in loged:
        return json.dumps("no such email!")
    temp = accs[loged.index(login)].get_dbs()
    if dbname not in temp:
        return json.dumps("no such database!")
    temp2 = accs[loged.index(login)].get_db(dbname).get_tables_names()
    if tblname not in temp2:
        return json.dumps("no such table!")
    res,msg = accs[loged.index(login)].get_db(dbname).get_table(tblname).add_row(data)
    if msg =="Ok":
        return json.dumps("success")
    return msg

@app.delete("/row/<login>/<dbname>/<tblname>/<id>")
def del_row(login, dbname, tblname, id):
    if login not in loged:
        return json.dumps("no such email!")
    temp = accs[loged.index(login)].get_dbs()
    if dbname not in temp:
        return json.dumps("no such database!")
    temp2 = accs[loged.index(login)].get_db(dbname).get_tables_names()
    if tblname not in temp2:
        return json.dumps("no such table!")
    res = accs[loged.index(login)].get_db(dbname).get_table(tblname).delete_row(id)
    return res


@app.get("/all")
def get_all():
    res = []
    result = ""
    for el in loged:
        dbs = accs[loged.index(el)].get_dbs()
        res1 = []
        for el0 in dbs:
            tbls = accs[loged.index(el)].get_db(el0).get_tables_names()
            res2=[]
            for el1 in tbls:
                cols = accs[loged.index(el)].get_db(el0).get_table(el1).get_columns_names_types()
                rows = accs[loged.index(el)].get_db(el0).get_table(el1).get_rows(0,-2)
                res2.append({"table "+el1+" cols":cols,"table "+el1+" rows":rows})
            res1.append({"database "+el0:res2})

        res.append({"user "+el:res1})
    return json.dumps(res)

@app.get("/mult/<login>/<dbname>/<tbl1>/<tbl2>")
def mult(login,dbname,tbl1,tbl2):
    if login not in loged:
        return json.dumps("no such email!")
    temp = accs[loged.index(login)].get_dbs()
    if dbname not in temp:
        return json.dumps("no such database!")
    temp2 = accs[loged.index(login)].get_db(dbname).get_tables_names()
    if tbl1 not in temp2 or tbl2 not in temp2:
        return json.dumps("no such table!")
    return json.dumps(accs[loged.index(login)].get_db(dbname).table_mult(tbl1,tbl2))

if __name__ == '__main__':
    app.run(debug=True)