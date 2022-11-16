import copy
import re
import pandas as pd
import PySimpleGUI as sg
from accounts import Accounts
TYPES = ["int","char","string","real","complexInteger","complexReal"]
def register_page(accs):
    layout2 = [
        [sg.Text('Введіть почту'), sg.InputText()],
        [sg.Text('', key="enter_error_window", pad=((100, 0), (5, 5)), text_color="red")],
        [sg.Button('Зареєструватися', pad=((126, 0), (5, 5)))],
        [sg.Button('Повернутися', pad=((126, 0), (5, 5)))]

    ]
    window = sg.Window("Реєстрація", layout2)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Повернутися":
            window.close()
            return 0
        if event == 'Зареєструватися':
            result = accs.register(values[0])
            if result == "OK":
                window.close()
                return 1
            elif result == "Bad email":
                window["enter_error_window"].update("Некоректні дані!")

def start_page(accs):
    sg.theme('DarkAmber')
    layout = [[sg.Text('Введіть почту'), sg.InputText(accs.get_selected(), key= "email_input_field")],
              [sg.Text('', key="enter_error_window", pad=((100, 0), (5, 5)), text_color="red")],
              [sg.Button('Увійти', pad=((160, 0), (10, 5)))],
              [sg.Button('Зареєструватися', pad=((126, 0), (5, 5)))]
              ]
    window = sg.Window('Lab1', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            return -1
        if event == "Зареєструватися":
            tmp1 = register_page(accs)
            if tmp1 == 1:
                window["email_input_field"].update(accs.get_selected())
                window["enter_error_window"].update(accs.get_selected()+" зареєстрована!",text_color="green")
        if event == 'Увійти':
            result = accs.log_in(values["email_input_field"])
            if result == "OK":
                window.close()
                return 1
            elif result == "No email":
                window["enter_error_window"].update("Введена пошта не зареєстрована!",text_color="red")
            elif result == "Bad email":
                window["enter_error_window"].update("Некоректні дані!",text_color="red")

def db_create_page(accs, operation, name0=""):
    sg.theme('DarkAmber')
    dbs = accs.get_dbs()
    layout = [[sg.Text('Введіть назву'), sg.InputText("", key="db_name_input_field")],
              [sg.Text('', key="enter_error_window", pad=((100, 0), (5, 5)), text_color="red")],
              [sg.Button(operation, pad=((160, 0), (10, 5)))],
              [sg.Button('Повернутися', pad=((160, 0), (10, 5)))]
              ]
    window = sg.Window(operation+' базу', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Повернутися':
            window.close()
            return -1
        if operation == "Перейменувати":
            window["db_name_input_field"].update(name0)
        if event == operation:
            name = values["db_name_input_field"]
            if name in dbs and operation != "Перейменувати" or (operation == "Перейменувати" and name in dbs and name != name0):
                window["enter_error_window"].update("Введіть унікальну назву!", text_color="red")
            elif not re.fullmatch(r'[a-zA-Z_0-9!#$%.&\'*+\-=?^`{|}~\s]*',name):
                window["enter_error_window"].update("Лише символи: a-zA-Z_0-9!#$%&\'*+-=?^`{|}~\s!", text_color="red")
            else:
                if operation == "Створити":
                    accs.add_db(name)
                    window.close()
                    return 1
                elif operation == "Перейменувати" and name0!=name:
                    accs.rename(name)
                    window.close()
                    return name
                else:
                    window.close()
                    return name

def table_create_page(db,operation, name0=""):
    sg.theme('DarkAmber')
    tbls = db.get_tables_names()
    layout = [[sg.Text('Введіть назву'), sg.InputText("", key="tbl_name_input_field")],
              [sg.Text('', key="enter_error_window", pad=((100, 0), (5, 5)), text_color="red")],
              [sg.Button(operation, pad=((160, 0), (10, 5)))],
              [sg.Button('Повернутися', pad=((160, 0), (10, 5)))]
              ]
    window = sg.Window(operation + ' таблицю', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Повернутися':
            window.close()
            return -1
        if event == operation:
            name = values["tbl_name_input_field"]
            if name in tbls and operation != "Перейменувати" or (operation == "Перейменувати" and name in tbls and name != name0):
                window["enter_error_window"].update("Введіть унікальну назву!", text_color="red")
            elif not re.fullmatch(r'[a-zA-Z]{1}[a-zA-Z_0-9]*', name):
                window["enter_error_window"].update("Лише символи: a-zA-Z_0-9 починати з a-zA-Z", text_color="red")
            else:
                if operation == "Створити":
                    db.add_table(name)
                    window.close()
                    return 1
                elif operation == "Перейменувати" and name0!=name:
                    db.rename_table(name0,name)
                    window.close()
                    return name
                else:
                    window.close()
                    return name

def column_create_page(table, operation,name0=""):
    sg.theme('DarkAmber')
    cols = table.get_columns_names()
    row_n = table.get_rows_num()

    layout = [[sg.Text('Введіть назву'), sg.InputText("", key="tbl_name_input_field")],
              [sg.Text('Оберіть тип'), sg.Combo(TYPES,key="select_type")],
              [sg.Text('', key="enter_error_window", pad=((100, 0), (5, 5)), text_color="red")],
              [sg.Button(operation, pad=((160, 0), (10, 5)))],
              [sg.Button('Повернутися', pad=((160, 0), (10, 5)))]
              ]
    window = sg.Window(operation + ' таблицю', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Повернутися':
            window.close()
            return -1
        if event == operation:
            name = values["tbl_name_input_field"]
            """if operation =="Редагувати":
                type = name0.split(":")[1]
                if len(values["select_type"]) != 0:
                    if type != values["select_type"] and row_n>0 :
                        window["enter_error_window"].update("Неможливо змінити тип - кі-сть рядків більше 0!", text_color="red")
                        continue"""

            if name in cols and operation != "Редагувати" or (
                    operation == "Редагувати" and name in cols and name != name0):
                window["enter_error_window"].update("Введіть унікальну назву!", text_color="red")
            elif not re.fullmatch(r'[a-zA-Z]{1}[a-zA-Z_0-9]*', name):
                window["enter_error_window"].update("Лише символи: a-zA-Z_0-9 починати з a-zA-Z", text_color="red")
            else:
                if operation == "Створити":
                    if len(values["select_type"]) != 0:
                        table.add_column(name,values["select_type"])
                    else:
                        window["enter_error_window"].update("Оберіть тип!", text_color="red")
                        continue
                    window.close()
                    return 1
                elif operation == "Редагувати" and name0 != name:
                    table.rename_column(name0, name)
                    window.close()
                    return name
                else:
                    window.close()
                    return name

def show_table_page(data,head, n,n0=-1):
    sg.theme('DarkAmber')
    data = copy.deepcopy(data)
    head = copy.deepcopy(head)
    if n0>=0:
        i=0
        for el in data:
            el.insert(0,n0+i)
            i+=1
        head.insert(0,"index")

    layout = [[sg.Table(values=data,headings=head,num_rows=n)]]
    window = sg.Window('Таблиця', layout, resizable=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            return

def table_mult(db,name):
    sg.theme('DarkAmber')

    tables = db.get_tables_names()

    layout = [[sg.Text('База: '), sg.Text(name, key="db_name"), sg.Button("Повернутися")],
              [sg.Combo(tables,key="left_combo"),sg.Button("Добуток"),sg.Combo(tables,key="right_combo")],
              [sg.Text('', key="enter_error_window", pad=((100, 0), (5, 5)), text_color="red")],
              ]
    window = sg.Window('Добуток', layout, resizable=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Повернутися":
            window.close()
            return
        if event == "Добуток":
            if len(values["left_combo"]) == 0:
                window["enter_error_window"].update("оберіть ліву таблицю!", text_color="red")
                continue
            if len(values["right_combo"]) == 0:
                window["enter_error_window"].update("оберіть праву таблицю!", text_color="red")
                continue
            name1 = values["left_combo"]
            name2 = values["right_combo"]
            data,headings = db.table_mult(name1,name2)
            if len(data)==0:
                ev, vals = sg.Window('Попередження!',
                                     [[sg.Text("Добуток: 0 рядків - оберіть інші таблиці, або додайте нові рядки!")], [sg.OK()]],
                                     size=(450, 70)).read(close=True)
                continue
            n = len(data)
            if n > 50:
                n = 50
            show_table_page(data,headings,n)

def delete_row_page(table):
    sg.theme('DarkAmber')
    layout = [
        [sg.Text("Оберіть номер рядка, який потрібно видалити"),sg.InputText(key = "num")],
        [sg.Button("Видалити")]
              ]
    window = sg.Window('Таблиця', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            return
        if event == "Видалити":
            if len(values["num"]) == 0:
                ev, vals = sg.Window('Попередження!',
                                     [[sg.Text("Оберіть індекс \'від\'!")], [sg.OK()]],
                                     size=(300, 70)).read(close=True)
                continue
            num = values["num"][0]
            if not re.fullmatch(r"[0-9]+", str(num)):
                ev, vals = sg.Window('Попередження!',
                                     [[sg.Text("Індекс має бути цілим числом не менше 0!")], [sg.OK()]],
                                     size=(400, 70)).read(close=True)
                continue
            res = table.delete_row(num)
            ev, vals = sg.Window('!',
                                 [[sg.Text(res)], [sg.OK()]],
                                 size=(400, 70)).read(close=True)
            continue

def add_row_page(table):
    sg.theme('DarkAmber')
    cols = table.get_columns_names_types()
    layout = []
    i = 0
    for el in cols:
        layout.append([sg.Text("Введіть значення для поля "+str(el)),sg.InputText(key=str(i)+"field"),
                       sg.Text('', key=str(i)+"error", pad=((100, 0), (5, 5)), text_color="red")])
        i+=1
    layout.append([sg.Button("Ввести рядок")])
    window = sg.Window('Таблиця', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            return
        if event == "Ввести рядок":
            for a in range(0,i):
                window[str(a) + "error"].update("")
            data = []
            i = 0
            for el in cols:
                data.append(values[str(i)+"field"])
                i+=1
            res,text = table.add_row(data)
            if res == -1:
                ev, vals = sg.Window('Успіх!',
                                     [[sg.Text("Рядок "+str(data)+" успішно додано")], [sg.OK()]],
                                     size=(500, 70)).read(close=True)
                window.close()
                return
            else:
                window[str(res)+"error"].update(text)

def tbl_main_page(db,name):
    sg.theme('DarkAmber')
    tbl = db.get_table(name)
    columns = tbl.get_columns_names_types()
    col1 = sg.Column([[sg.Frame('Поля:', [
        [sg.Column([[sg.Listbox(columns, key='col_list', size=(60, 40)), ]], size=(200, 400))]])]], pad=(0, 0))
    col2 = sg.Column([
        [sg.Button("Змінити назву таблиці", size=(30, 1))],
        [sg.Button("Додати поле", size=(30, 1))],
        [sg.Button("Видалити поле", size=(30, 1))],
        [sg.Button("Редагувати поле", size=(30, 1))],
        [sg.Button("Додати рядок", size=(30, 1))],
        [sg.Button("Видалити рядок", size=(30, 1))]

    ])
    layout = [[sg.Text('Таблиця: '), sg.Text(name, key="tbl_name"), sg.Button("Повернутися")],
              [col1, col2],
              [sg.Text("Обрати рядки для перегляду"),sg.Text("Від"),sg.InputText("0",key="n1"),sg.Text("до"),sg.InputText("0",key="n2"),sg.Button("Показати")],

              ]
    window = sg.Window('Таблиця', layout, resizable=True)
    change = 0
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Повернутися":
            window.close()
            if change == 1:
                return 1
            return -1
        if event == "Змінити назву таблиці":
            name2 = table_create_page(db, "Перейменувати",name)
            if name2 != -1:
                window["tbl_name"].update(name2)
                change = 1
                name = name2
        elif event == "Показати":
            if len(values["n1"]) == 0:
                ev, vals = sg.Window('Попередження!',
                                     [[sg.Text("Оберіть індекс \'від\'!")], [sg.OK()]],
                                     size=(300, 70)).read(close=True)
                continue
            if len(values["n2"]) == 0:
                ev, vals = sg.Window('Попередження!',
                                     [[sg.Text("Оберіть індекс \'до\'!")], [sg.OK()]],
                                     size=(300, 70)).read(close=True)
                continue
            n1 = values["n1"][0]
            n2 = values["n2"][0]
            if not re.fullmatch(r"[0-9]+", str(n1)):
                ev, vals = sg.Window('Попередження!',
                                     [[sg.Text("Індекс \'від\' має бути цілим числом не менше 0!")], [sg.OK()]],
                                     size=(400, 70)).read(close=True)
                continue
            if not( re.fullmatch(r"[0-9]+", str(n2)) or re.fullmatch(r"[&]",str(n2))):
                ev, vals = sg.Window('Попередження!',
                                     [[sg.Text("Індекс \'до\' має бути цілим числом не менше 0 або символом & щоб обрати максимальный індекс!")], [sg.OK()]],
                                     size=(500, 70)).read(close=True)
                continue
            n1 = int(n1)
            if n2 != '&':
                n2 = int(n2)
                c = n2-n1
            else:
                n2 = -2
            data = tbl.get_rows(n1,n2)
            head = tbl.get_columns_names_types()
            show_table_page(data,head,len(data),n1)
        elif event == "Додати поле":
            res = column_create_page(tbl,"Створити")
            if res==1:
                columns = tbl.get_columns_names_types()
                window["col_list"].update(columns)
        elif event == "Редагувати поле":
            if len(values["col_list"])==0:
                ev, vals = sg.Window('Попередження!',
                                     [[sg.Text("Оберіть поле, яке ви хочете змінити!")], [sg.OK()]],
                                     size=(300, 70)).read(close=True)
                continue
            res = column_create_page(tbl, "Редагувати", values["col_list"][0])
            if len(str(res))>1:
                columns = tbl.get_columns_names_types()
                window["col_list"].update(columns)
        elif event == "Видалити рядок":
            delete_row_page(tbl)
        elif event == "Додати рядок":
            add_row_page(tbl)

def db_main_page(accs, name):
    sg.theme('DarkAmber')
    db = accs.get_db(name)

    tables = db.get_tables_names()
    col1 = sg.Column([[sg.Frame('Таблиці:', [[sg.Column([[sg.Listbox(tables,key='tbl_list', size=(40, 40)),]],size=(150, 400))]])]], pad=(0, 0))
    col2 = sg.Column([
        [sg.Button("Змінити назву бази", size=(30, 1))],
        [sg.Button("Видалити базу", size=(30, 1))],
        [sg.Button("Переглянути обрану таблицю", size=(30, 1))],
        [sg.Button("Створити таблицю", size=(30, 1))],
        [sg.Button("Видалити таблицю", size=(30, 1))],
        [sg.Button("Добуток таблиць", size=(30, 1))]
    ])
    layout = [[sg.Text('База: '), sg.Text(name, key="db_name"), sg.Button("Повернутися")],
              [col1, col2]
              ]
    window = sg.Window('Таблиці', layout, resizable=True)
    change = 0
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Повернутися":
            accs.save()
            window.close()
            if change == 1:
                return 1
            return -1
        if event == "Змінити назву бази":
            ev, vals = sg.Window('Попередження!', [[sg.Text("Тимчасово недоступно!")], [sg.OK()]],
                                 size=(300, 70)).read(close=True)
            continue
            name2 = db_create_page(accs, "Перейменувати",name)
            if name2 != -1:
                window["db_name"].update(name2)
                change = 1
                name = name2
        elif event == "Видалити базу":
            ev, vals = sg.Window('Видалити базу',[[ sg.OK("Так",size=(10,20)), sg.Cancel("Ні",size=(10,20))]],size=(250,50)).read(close=True)
            if ev == 'Так':
                accs.delete_db(name)
                window.close()
                return 1
        elif event == "Створити таблицю":
            res = table_create_page(db,"Створити")
            if res == 1:
                tables = db.get_tables_names()
                window["tbl_list"].update(tables)
        elif event == "Видалити таблицю":
            if len(values["tbl_list"])==0:
                ev, vals = sg.Window('Попередження!', [[sg.Text("Оберіть таблицю, яку ви хочете видалити!")],[sg.OK()]],
                                     size=(300, 70)).read(close=True)
                continue
            ev, vals = sg.Window('Видалити таблицю', [[sg.OK("Так", size=(15, 20)), sg.Cancel("Ні", size=(15, 20))]],
                                 size=(350, 50)).read(close=True)
            if ev == 'Так':
                db.delete_table(values["tbl_list"][0])
                tables = db.get_tables_names()
                window["tbl_list"].update(tables)
        elif event == "Добуток таблиць":
            table_mult(db,name)
        elif event == "Переглянути обрану таблицю":
            if len(values["tbl_list"])==0:
                ev, vals = sg.Window('Попередження!', [[sg.Text("Оберіть таблицю, яку ви хочете переглянути!")],[sg.OK()]],
                                     size=(300, 70)).read(close=True)
                continue

            res = tbl_main_page(db,values["tbl_list"][0])
            if res == 1:
                tables = db.get_tables_names()
                window["tbl_list"].update(tables)

def dbs_page(accs):
    sg.theme('DarkAmber')
    dbs = accs.get_dbs()

    col1 = sg.Column([[sg.Frame('Бази даних:', [[sg.Column([[sg.Listbox(dbs,key='db_list', size=(40, 40)),]],size=(150, 400))]])]], pad=(0, 0))
    col2 = sg.Column([
        [sg.Button("Завантажити обрану базу",size=(20,2))],
        [sg.Button("Створити базу",size=(20,2))]
    ])
    layout = [[sg.Text('Користувач: '), sg.Text(accs.get_selected()), sg.Button("Змінити користувача")],
                [col1,col2]
              ]
    window = sg.Window('Бази даних', layout,resizable=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            accs.save()
            window.close()
            return -1
        if event == "Змінити користувача":
            accs.save()
            window.close()
            return 0
        if event == "Завантажити обрану базу":
            if len(values["db_list"])==0:
                ev, vals = sg.Window('Попередження!', [[sg.Text("Оберіть базу, яку ви хочете завантажити!")],[sg.OK()]],
                                     size=(300, 70)).read(close=True)
                continue

            res2 = db_main_page(accs, values["db_list"][0])
            if res2 == 1:
                dbs = accs.get_dbs()
                window["db_list"].update(dbs)
        if event == "Створити базу":
            res = db_create_page(accs, "Створити")
            if res == 1:
                dbs = accs.get_dbs()
                window["db_list"].update(dbs)

if __name__ == '__main__':

    accs = Accounts()
    res = start_page(accs)
    if res == -1:
        accs.save()
        exit(0)
    while True:
        if res == -1:
            accs.save()
            exit(0)
        elif res == 0:
            res = start_page(accs)
        elif res == 1:
            res = dbs_page(accs)
        elif res == 2:
            res = db_create_page(accs)


