import sqlite3


def info_search(table_name):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    search_list = []
    search_list.append('Информация актуально по состоянию на:')
    if table_name == 'FilialJobs':
        cursor.execute(f'SELECT num_app, date_app, vincod, text_app FROM {table_name}')
        total_search = cursor.fetchall()
        count = 1
        for search_add in total_search:
            search_list.append(
                f'{count}. ID заявки: {search_add[0]}, Дата: {search_add[1]}, Объект: {search_add[2]}, Описание: {search_add[3]}')
            count += 1
    if table_name == 'Objects':
        cursor.execute(f'SELECT vincod, title, resident, phone_num FROM {table_name}')
        total_search = cursor.fetchall()
        count = 1
        for search_add in total_search:
            search_list.append(
                f'{count}. Код объекта: {search_add[0]}, Объект: {search_add[1]}, Имя агента: {search_add[2]}, '
                f'Телефон агента: {search_add[3]}')
            count += 1
    if table_name == 'FilialWorker':
        cursor.execute(f'SELECT name, post, phone_num, tlg_id FROM {table_name}')
        total_search = cursor.fetchall()
        count = 1
        for search_add in total_search:
            search_list.append(
                f'{count}. Имя сотрудника: {search_add[0]}, Должность: {search_add[1]}, '
                f'Номер телефона: {search_add[2]}, ID сотрудника {search_add[3]}')
            count += 1
    connection.commit()
    connection.close()
    return search_list


def info_detail(id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT date_app, vincod, system_app, text_app FROM FilialJobs WHERE num_app = ?',
                   (f'{id}',))
    total_jobs = cursor.fetchone()
    connection.commit()
    connection.close()
    return total_jobs


def obj_info(id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT title, resident, phone_num FROM Objects WHERE vincod = ?',
                   (f'{id}',))
    total_obj = cursor.fetchone()
    connection.commit()
    connection.close()
    return total_obj


# Проверка, сколько администраторов в системе
def check_count():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM FilialWorker WHERE role=?', ('True',))
    count = cursor.fetchone()
    connection.commit()
    connection.close()
    if count[0] == 1:
        return False
    else:
        return True


def fio_search(id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM FilialWorker WHERE tlg_id=?', (f'{id}',))
    fio = cursor.fetchone()
    connection.commit()
    connection.close()
    return fio


# Проверяем роль пользователя
def role_search(id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    role = {0: 'False'}
    cursor.execute('SELECT COUNT(*) FROM FilialWorker WHERE tlg_id=?', (f'{id}',))
    count = cursor.fetchone()
    if count[0] != 0:
        cursor.execute('SELECT role FROM FilialWorker WHERE tlg_id=?', (f'{id}',))
        role = cursor.fetchone()
    connection.commit()
    connection.close()
    return role


# Выводим список наших агентов
def agents_search():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    agents_list = []
    cursor.execute('SELECT vincod, title, resident, phone_num FROM Objects')
    total_agents = cursor.fetchall()
    count = 1
    for agents_add in total_agents:
        agents_list.append(
            f'{count}. Код объекта: {agents_add[0]}, Название объекта: {agents_add[1]}, '
            f'Имя агента: {agents_add[2]}, Телефон агента: {agents_add[3]}')
        count += 1
    connection.commit()
    connection.close()
    return agents_list


# Проверка наличия кода объекта в таблице
def check_data(vincod, table_name):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    if table_name == 'FilialWorker':
        cursor.execute(f'SELECT COUNT(*) FROM {table_name} WHERE tlg_id=?', (f'{vincod}',))
    else:
        cursor.execute(f'SELECT COUNT(*) FROM {table_name} WHERE vincod=?', (f'{vincod}',))
    count = cursor.fetchone()
    connection.commit()
    connection.close()
    if count[0] != 0:
        return True
    else:
        return False


# Обновляем данные об агенте
def agent_update(vincod, resident, phone_num):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Objects SET resident = ?, phone_num = ? WHERE vincod = ?',
                   (f'{resident}', f'{phone_num}', f'{vincod}'))
    connection.commit()
    connection.close()


# Вносим данные нового агента
def agent_new(vincod, title, resident, phone_num):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Objects(vincod, title, resident, phone_num) VALUES(?, ?, ?, ?)',
                   (f'{vincod}', f'{title}', f'{resident}', f'{phone_num}'))
    connection.commit()
    connection.close()


# Удаляем агента
def agent_del(vincod):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Objects WHERE vincod = ?', (f'{vincod}',))
    connection.commit()
    connection.close()


# Вносим данные нового сотрудника
def worker_new(name, post, phone_num, role, tlg_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO FilialWorker(name, post, phone_num, role, tlg_id) VALUES(?, ?, ?, ?, ?)',
                   (f'{name}', f'{post}', f'{phone_num}', f'{role}', f'{tlg_id}'))
    connection.commit()
    connection.close()


# Обновляем данные о сотруднике
def worker_update(name, post, phone_num, role, tlg_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE FilialWorker SET name = ?, post = ?, phone_num = ?, role = ?'
                   ' WHERE tlg_id = ?', (f'{name}', f'{post}', f'{phone_num}', f'{role}', f'{tlg_id}'))
    connection.commit()
    connection.close()


# Удаляем сотрудника
def worker_del(tlg_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM FilialWorker WHERE tlg_id = ?', (f'{tlg_id}',))
    connection.commit()
    connection.close()


""" Данный блок находится в разработке, будет 
    необходим в дальнейшем для заливки заданий, приходящих из ЦА 
import datetime    
from openpyxl import load_workbook
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS FilialJobs(
#     id INTEGER PRIMARY KEY,
#     num_app INTEGER,
#     date_app DATE,
#     obj_app TEXT,
#     applicant TEXT,
#     email TEXT,
#     system_app TEXT,
#     text_app TEXT,
#     stat_app TEXT,
#     type_app TEXT
#     )
# ''')
# cursor.execute("DELETE FROM Filialjobs")
#
# file_name = '09-Oct-2024.xlsx'
# str_jobs = load_workbook(file_name)
# sheet = str_jobs.get_sheet_by_name('Worksheet')
#
# date_file = (file_name[0:11])


# count = 2
# while sheet[f'A{count}'].value is not None:
#     cursor.execute("INSERT INTO Filialjobs (num_app, date_app, obj_app, applicant, email, system_app, "
#                    "text_app, stat_app, type_app) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (sheet[f'A{count}'].value,
#                                                                                        datetime.datetime.date(
#                                                                                            sheet[f'B{count}'].value),
#                                                                                        sheet[f'C{count}'].value,
#                                                                                        sheet[f'D{count}'].value,
#                                                                                        sheet[f'F{count}'].value,
#                                                                                        sheet[f'G{count}'].value,
#                                                                                        sheet[f'H{count}'].value,
#                                                                                        sheet[f'I{count}'].value,
#                                                                                        sheet[f'J{count}'].value
#                                                                                        ))
#     count += 1
#
# connection.commit()
# connection.close()
"""
