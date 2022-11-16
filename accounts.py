import openpyxl
import os
import pandas as pd
import numpy as np
import re
from database import Database
class Accounts:
    def __init__(self):
        self.__accounts,self.__selected_acc = self.load()
        self.__selected_dbs = self.__get_dbs()
        self.__DB = None


    def get_acc(self):
        return self.__accounts

    def get_selected(self):
        return self.__selected_acc

    def get_dbs(self):
        return self.__selected_dbs

    def __get_dbs(self):
        res = []
        temp = self.__accounts[self.__selected_acc].notna()
        i0 = -1
        for i in self.__accounts[self.__selected_acc]:
            i0+=1
            if i and temp[i0] and temp[i0]!="":
                res.append(str(i))
        res.sort()
        return res

    def load(self):
        if os.path.exists("files/accounts.xlsx"):
            excel_data = pd.read_excel("files/accounts.xlsx")
            data = pd.DataFrame(excel_data)
            data = data.fillna("")
            data = pd.DataFrame(data,dtype=str)
        else:
            data = pd.DataFrame()
        if os.path.exists("files/recent.txt"):
            file = open("files/recent.txt")
            data2 = file.readline()
        else:
            data2 = ""
        data.astype(str)
        return data,data2

    def log_in(self, mail):
        if re.fullmatch(r'[a-zA-Z_0-9!#$%&\'*+\-/=?^`{|}~.]*[@]{1}[a-zA-Z0-9-]*[.]{1}[a-zA-Z0-9-]*', mail):
            for el in self.__accounts:
                if el == mail:
                    self.__selected_acc = mail
                    self.__selected_dbs = self.__get_dbs()
                    return "OK"
            return "No email"
        else:
            return "Bad email"
    def register(self, mail):
        if re.fullmatch(r'[a-zA-Z_0-9!#$%&\'*+\-/=?^`{|}.~]*[@]{1}[a-zA-Z0-9-]*[.]{1}[a-zA-Z0-9-]*', mail):
            for el in self.__accounts:
                if el == mail:
                    return "No email"
            self.__selected_acc = mail
            if not os.path.exists("files/accounts.xlsx"):
                df = pd.DataFrame([mail])
                df.to_excel("files/accounts.xlsx")
            else:
                temp = []
                for i in range(0,len(self.__accounts)):
                    temp.append("")
                self.__accounts.insert(0,mail,temp)

                pass
            return "OK"
        else:
            return "Bad email"

    def save(self):
        if self.__DB is not None:
            self.save_db()
        self.__accounts.to_excel("files/accounts.xlsx",index = False)
        file = open("files/recent.txt","w")
        file.write(self.__selected_acc)
        file.close()

    def save_db(self):
        db_path = "files/"+self.__selected_acc+self.__DB.get_name()+".db"
        self.__DB.save(db_path)
        self.__DB = None

    def add_db(self,name):
        length0 = 0
        for el in self.__accounts:
            temp = len(self.__accounts[el].dropna())
            if temp > length0:
                length0 = temp
        if len(self.__accounts[self.__selected_acc]) == length0:
            row = {self.__selected_acc: name}
            self.__accounts = self.__accounts.append(row,ignore_index=True)
        else:
            ind = self.__accounts.index[self.__accounts[self.__selected_acc].isna()].tolist()[0]
            self.__accounts.loc[ind,self.__selected_acc]=name
        self.__selected_dbs.append(name)


    def rename(self,name):
        prev_name = self.__DB.get_name()

        temp = self.__accounts.index[self.__accounts[self.__selected_acc]==prev_name]
        ind = temp.tolist()[0]
        self.__accounts.loc[ind,self.__selected_acc] = name
        self.__selected_dbs = self.__get_dbs()
        self.__DB.rename(name)

    def get_db(self,name):
        db_path = "files/" + self.__selected_acc + name + ".db"
        db = Database(name)
        db.load(db_path, name)
        self.__DB = db
        return self.__DB

    def delete_db(self,name):
        ind = self.__accounts.index[self.__accounts[self.__selected_acc] == name].tolist()[0]
        self.__accounts.loc[ind, self.__selected_acc] = np.nan
        self.__selected_dbs = self.__get_dbs()
        self.__DB.delete()
        self.__DB = None

