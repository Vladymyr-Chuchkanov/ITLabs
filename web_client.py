import re

from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from client import Client

app= Flask(__name__)
client = Client()
TYPES = ["int","char","string","real","complexInteger","complexReal"]
@app.route('/<login>',methods=["POST","GET"])
@app.route('/',methods=["POST","GET"])
def index(login = None):
    if request.method=="POST":
        email = request.values["email"]
        print(email)
        res = client.log_in(email)
        if res == "OK":
            return redirect(url_for("account", login = email))
        return render_template("index.html", error = res)
    return render_template("index.html")

@app.route('/register', methods=["POST","GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method=="POST":
        email = request.values["email"]
        res = client.register(email)
        if res == "OK":
            return render_template("index.html", login = email)
        else:
            return render_template("register.html", error = res)
    return render_template("register.html")

@app.route("/logout", methods=["POST"])
def logout():
    client.log_out()
    return render_template("index.html")


@app.route('/account', methods=["POST","GET"])
@app.route('/account/<login>', methods=["POST","GET"])
def account(login=None):
    if login == None:
        login = client.get_login()
    if request.method == "GET":

        dbs = client.get_dbs()
        return render_template("account.html", login = login,dbs = dbs)
    dbs = client.get_dbs()

    return render_template("account.html", login = login,dbs = dbs)

@app.route('/add_db', methods=["POST"])
def add_db():
    if request.method=="POST":
        dbname = request.values["dbname"]
        dbs = client.get_dbs()
        if dbname not in dbs:
            client.add_db(dbname)
            dbs = client.get_dbs()
            return render_template("account.html", account=client.get_login(), dbs=dbs)

@app.route('/delete_db', methods=["POST"])
def delete_db():
    if request.method=="POST":
        dbname = request.values["dbs2"]
        dbs = client.get_dbs()
        if dbname in dbs:
            client.delete_db(dbname)
            dbs = client.get_dbs()
            return render_template("account.html", account=client.get_login(), dbs=dbs)
@app.route('/open_db', methods=["GET","POST"])
def open_db():
    if request.method=="GET":
        dbname = request.values["dbs3"]
        dbs = client.get_dbs()
        if dbname in dbs:
            client.add_selected_db(dbname)
            tbls = client.get_tables_names(dbname)
            return render_template("database.html", account=client.get_login(), db=dbname, tbls=tbls)
    if request.method == "POST":
        dbname = client.get_selected_db()
        tbls = client.get_tables_names(dbname)
        return render_template("database.html", account=client.get_login(), db=dbname, tbls=tbls)

@app.route('/add_tbl', methods=["POST"])
def add_tbl():
    if request.method=="POST":
        tblname = request.values["tblname"]
        tbls = client.get_tables_names(client.get_selected_db())
        if tblname not in tbls:
            client.add_table(client.get_selected_db(),tblname)
            tbls = client.get_tables_names(client.get_selected_db())
            return render_template("database.html", account=client.get_login(), tbls=tbls)

@app.route('/delete_tbl', methods=["POST"])
def delete_tbl():
    if request.method=="POST":
        tblname = request.values["tbls2"]
        tbls = client.get_tables_names(client.get_selected_db())
        if tblname in tbls:
            client.delete_table(client.get_selected_db(), tblname)
            tbls = client.get_tables_names(client.get_selected_db())
            return render_template("database.html", account=client.get_login(), tbls=tbls)

@app.route('/mult_tbl', methods=["POST"])
def mult_tbl():
    if request.method=="POST":
        tblname1 = request.values["tbls_left"]
        tblname2 = request.values["tbls_right"]
        tbls = client.get_tables_names(client.get_selected_db())
        data,headings = client.table_mult(client.get_selected_db(),tblname1,tblname2)
        return render_template("database.html", account=client.get_login(), tbls=tbls, data = data, head = headings)

@app.route('/open_tbl', methods=["GET"])
def open_tbl():
    if request.method=="GET":
        tblname = request.values["tbls3"]
        tbls = client.get_tables_names(client.get_selected_db())
        if tblname in tbls:
            client.add_selected_tbl(tblname)
            cols = client.get_columns_names_types(client.get_selected_db(),tblname)
            return render_template("table.html", account=client.get_login(), db=client.get_selected_db(), tbl=tblname, cols = cols, tps = TYPES)
    if request.method=="POST":
        tblname = client.get_selected_tbl()
        cols = client.get_columns_names_types(client.get_selected_db(),tblname)
        return render_template("table.html", account=client.get_login(), db=client.get_selected_db(), tbl=tblname, cols = cols, tps = TYPES)

@app.route('/add_col', methods=["POST"])
def add_col():
    if request.method=="POST":
        colname = request.values["colname"]
        type = request.values["type"]
        cols = client.get_columns_names_types(client.get_selected_db(),client.get_selected_tbl())
        if colname+"_"+type not in cols:
            client.add_column(client.get_selected_db(),client.get_selected_tbl(),colname,type)
            cols = client.get_columns_names_types(client.get_selected_db(),client.get_selected_tbl())
            return render_template("table.html", account=client.get_login(), db=client.get_selected_db(), tbl=client.get_selected_tbl(), cols = cols, tps = TYPES)

@app.route('/add_row', methods=["POST"])
def add_row():
    if request.method=="POST":
        data = request.values["values"]
        data = data.split(",")
        cols = client.get_columns_names_types(client.get_selected_db(), client.get_selected_tbl())
        res, text = client.add_row(client.get_selected_db(),client.get_selected_tbl(), data)
        if res == -1:
            return render_template("table.html", account=client.get_login(), db=client.get_selected_db(), tbl=client.get_selected_tbl(), cols = cols, tps = TYPES)
        else:
            return render_template("table.html", account=client.get_login(), db=client.get_selected_db(),
                                   tbl=client.get_selected_tbl(), cols=cols, tps=TYPES, error = text)

@app.route('/get_rows', methods=["GET"])
def get_rows():
    if request.method == "GET":
        n1 = request.values["n1"]
        n2 = request.values["n2"]
        if re.fullmatch(r"[0-9]+", str(n1)) and (re.fullmatch(r"[0-9]+", str(n2))or re.fullmatch(r"[&]",str(n2))):
            n1 = int(n1)
            if n2 != '&':
                n2 = int(n2)
            else:
                n2 = -2
            rows = client.get_rows(client.get_selected_db(),client.get_selected_tbl(),n1,n2)
            return render_template("table.html", account=client.get_login(), db=client.get_selected_db(),
                                   tbl=client.get_selected_tbl(), rws=rows, tps=TYPES)


if __name__=="__main__":
    app.run(debug=True)
