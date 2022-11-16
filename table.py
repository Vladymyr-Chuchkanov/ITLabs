from column import Column

class Table:
    def __init__(self,name, conn):
        self.__name = name
        self.__conn = conn
        cur = self.__conn.cursor()
        cur.execute("Select * from " + str(self.__name) + ";")
        res = cur.fetchall()
        self.__rows=[]
        t = 0
        for el in res:
            if t ==0:
                t = 1
                continue
            self.__rows.append(list(el[1:]))
        cur.execute("pragma table_info(" + self.__name + ");")
        cols = cur.fetchall()
        self.__columns = []
        t = 0
        for el in cols:
            if t == 0:
                t = 1
                continue
            self.__columns.append(el[1])
        cur.close()


    def get_name(self):
        return self.__name

    def get_rows(self,n1=0,n2=-2):
        n2+=1
        if n2 == -1:
            n2 = len(self.__rows)
        if n2 > len(self.__rows):
            n2 = len(self.__rows)
        if n1 > len(self.__rows):
            n1 = len(self.__rows)
        return self.__rows[n1:n2]

    def get_rows_num(self):
        return len(self.__rows)

    def get_columns_names(self):
        res = []
        for el in self.__columns:
            res.append(el.split("_")[0])
        return res

    def get_col_type(self,name):
        for el in self.__columns:
            if el.split("_")[0]==name:
                return el.split("_")[1]

    def get_columns_names_types(self):
        return self.__columns

    def add_row(self, args):
        if len(self.__columns)==0:
            return -1, "Немає полів!"

        for i in range(0,len(self.__columns)):
            nm = self.__columns[i].split("_")[0]
            tp = self.__columns[i].split("_")[1]
            col = Column(nm,tp)
            check = col.check_type(args[i])
            if check == 1:
                if tp == "int":
                    if args[i]=="":
                        args[i]=None
                        continue
                    args[i]=int(args[i])
                if tp == "real":
                    if args[i]=="":
                        args[i]=None
                        continue
                    args[i]=float(args[i])
                continue
            else:
                return i,check
        cur = self.__conn.cursor()
        n = len(self.__columns)
        str0 = ""
        for i in range(0,n):
            str0+="?, "
        str0+="?"
        args.insert(0,0)
        cur.execute("INSERT INTO "+self.__name+
                    " VALUES("+str0+");",args)
        self.__conn.commit()
        cur.execute("Select * from " + str(self.__name) + ";")
        res = cur.fetchall()
        self.__rows = []
        t = 0
        for el in res:
            if t == 0:
                t = 1
                continue
            self.__rows.append(list(el[1:]))
        cur.close()
        return -1,"Ok"

    def add_column(self,name, type):
        cur = self.__conn.cursor()

        tp = "TEXT"
        if type == "int":
            tp="INT"
        if type == "real":
            tp="REAL"
        cur.execute("ALTER TABLE "+self.__name+" ADD COLUMN "+name+"_"+type+" "+tp+";")
        self.__columns.append(name+"_"+type)
        self.__conn.commit()
        cur.close()

    def delete_row(self, n):
        cur = self.__conn.cursor()
        n = int(n)
        if n >= len(self.__rows):
            return "Видалено 0 рядків - індекс поза межами!"
        temp = self.__rows.pop(n)
        str0="DELETE FROM "+self.__name+" WHERE "
        for i in range(0,len(self.__columns)-1):
            str0+= self.__columns[i]+" = \""+str(temp[i])+"\" AND "
        str0+= self.__columns[len(self.__columns)-1]+" = \""+str(temp[len(self.__columns)-1])+"\";"
        cur.execute(str0)
        self.__conn.commit()
        cur.close()
        return "Видалено рядок "+str(temp)

    def update_column(self, name, new_name, type):
        for i in range(0,len(self.__columns)):
            nm = self.__columns[i].split("_")[0]
            tp = self.__columns[i].split("_")[1]
            if nm == name:
                if tp!=type:
                    if len(self.__rows)>0:
                        return -1,"У таблиці вже є рядки, змінити тип неможливо!"
                    #else:
                        #col.change_type(type)
                #col.change_name(new_name)
                return 1,"Ok"
    def delete_column(self,name):
        cur = self.__conn.cursor()
        cur.execute("ALTER TABLE "+self.__name+
                    " DROP COLUMN "+name+";")
        cur.execute("Select * from " + str(self.__name) + ";")
        self.__rows = cur.fetchall()
        cur.execute("pragma table_info(" + self.__name + ");")
        cols = cur.fetchall()
        self.__columns = []
        for i in range(1, len(cols)):
            self.__columns.append(cols[i][1])
        cur.close()


    def rename_column(self,name,new_name):
        cur = self.__conn.cursor()
        for i in range(0, len(self.__columns)):
            nm = self.__columns[i].split("_")[0]
            tp = self.__columns[i].split("_")[1]
            if nm==name:
                cur.execute("ALTER TABLE "+self.__name+" "
                            "RENAME COLUMN "+self.__columns[i]+" TO "+new_name+"_"+tp+";")