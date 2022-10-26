from column import Column

class Table:
    def __init__(self,name):
        self.__name = name
        self.__columns = []
        self.__rows = []

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

    def get_columns(self):
        return self.__columns

    def get_rows_num(self):
        return len(self.__rows)

    def get_columns_names(self):
        res = []
        for col in self.__columns:
            res.append(col.get_name())
        return res

    def get_col_type(self,name):
        for el in self.__columns:
            if el.get_name() == name:
                return el.get_type()

    def get_columns_names_types(self):
        res = []
        for col in self.__columns:
            res.append(col.get_name()+":"+col.get_type())
        return res
    def add_row(self, args):
        if len(self.__columns)==0:
            return -1, "Немає полів!"
        for i in range(0,len(self.__columns)):
            check = self.__columns[i].check_type(args[i])
            if check == 1:
                continue
            else:
                return i,check
        self.__rows.append(args)
        return -1,"Ok"
    def add_column(self,name,type):
        col = Column(name,type)
        self.__columns.append(col)
        for el in self.__rows:
            el.append("")
    def delete_row(self, n):
        n = int(n)
        if n >= len(self.__rows):
            return "Видалено 0 рядків - індекс поза межами!"
        temp = self.__rows.pop(n)
        return "Видалено рядок "+str(temp)

    def update_column(self, name, new_name, type):
        for col in self.__columns:
            if col.get_name()== name:
                if col.get_type()!=type:
                    if len(self.__rows)>0:
                        return -1,"У таблиці вже є рядки, змінити тип неможливо!"
                    else:
                        col.change_type(type)
                col.change_name(new_name)
                return 1,"Ok"
    def delete_column(self,name):
        ind = self.get_columns_names().index(name)
        self.__columns.pop(ind)
        for el in self.__rows:
            el.pop(ind)
    def rename(self,name):
        self.__name=name

    def rename_column(self,name,new_name):
        for el in self.__columns:
            if el.get_name() == name.split(":")[0]:
                el.rename(new_name)