
TYPES = ["int","char","string","real","complexInteger","complexReal"]
import re
class Column:
    def __init__(self,name,type):
        self.__name = name
        self.__type = type

    def get_name(self):
        return self.__name
    def get_type(self):
        return self.__type
    def change_type(self,type):
        self.__type=type
    def change_name(self,new_name):
        self.__name = new_name
    def check_type(self,value):
        if str(value) == "":
            return 1
        if self.__type=="int":
            if re.fullmatch(r'[-]?[0-9]+',str(value)):
                return 1
            else:
                return "дані типу int можуть бути лише цілим числом, наприклад: -1,0,105"
        elif self.__type=="char":
            if len(str(value))==1:
                return 1
            else:
                return "дані типу char можуть бути лише одним символом, наприклад: С А 7 ?"
        elif self.__type=="string":
            return 1
        elif self.__type=="real":
            if re.fullmatch(r'[-]?[0-9]+([.][0-9]+)?',str(value)):
                return 1
            else:
                return "дані типу real можуть бути лише дійсним числом, наприклад: 6 6.89 -0.54"
        elif self.__type=="complexReal":
            if re.fullmatch(r'[-]?[0-9]+([.][0-9]+)?(\s?[+-]?[0-9]+([.][0-9]+)?[*]?[i])?',str(value)):
                return 1
            else:
                return "дані типу complexReal можуть бути комплексним числом, записаним у виді: а+-bi"
        elif self.__type=="complexInteger":
            if re.fullmatch(r'[-]?[0-9]+(\s?[+-]?[0-9]+[*]?[i])?',str(value)):
                return 1
            else:
                return "дані типу complexInteger можуть бути комплексним цілим числом, записаним у виді: а+-bi"

    def rename(self,name):
        self.__name=name
