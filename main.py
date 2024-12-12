from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import *
from db import *

from aiogram.contrib.fsm_storage.memory import MemoryStorage

API = ''
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message):
    user_id = message.from_user.id
    name = fio_search(user_id)
    if name != None:
        await message.answer(f'Здравствуйте, {name[0]}!', reply_markup=kb_start)
    else:
        await message.answer(f'Здравствуйте, {user_id}!', reply_markup=kb_start)


@dp.message_handler(text=['Информация о боте'])
async def set_age(message):
    await message.answer('Бот для навигации по заявкам и облегчения коммуникации между исполнителями,'
                         'контролирующими сотрудниками и агентами на объектах! \n'
                         'С пожеланиями по внесению изменений обращайтесь к @nApTu3aH82 \n'
                         'Для администрирования тапните "/admin"')


'''Блок запросов на списковые значения'''


@dp.message_handler(text=['Текущие заявки'])
async def main_menu(message):
    list_jobs = info_search('FilialJobs')
    for jobs in list_jobs:
        await message.answer(f'{jobs}')
    await message.answer('Выберите дальнейшее действия:', reply_markup=kb_jobs_inline)


@dp.callback_query_handler(text='agents_list')
async def agents_list(call):
    list_agents = info_search('Objects')
    for agents in list_agents:
        await call.message.answer(f'{agents}')
    await call.answer()


@dp.message_handler(text=['Список объектов и агентов'])
async def agents_list(message):
    list_agents = info_search('Objects')
    for agents in list_agents:
        await message.answer(f'{agents}')


@dp.callback_query_handler(text='workers_list')
async def workers_list(call):
    list_workers = info_search('FilialWorker')
    for workers in list_workers:
        await call.message.answer(f'{workers}')
    await call.answer()


@dp.message_handler(text=['Список наших доблестных сотрудников'])
async def workers_list(message):
    list_workers = info_search('FilialWorker')
    for workers in list_workers:
        await message.answer(f'{workers}')


'''Конец блока запросов'''

'''Блок получения подробной информации о заявке'''


class JobsStat(StatesGroup):
    id_jobs = State()


@dp.callback_query_handler(text='detail')
async def get_detail(call):
    await call.message.answer('Введите id заявки:')
    await JobsStat.id_jobs.set()
    await call.answer()


@dp.message_handler(state=JobsStat.id_jobs)
async def get_detail_print(message, state):
    await state.update_data(id_text=message.text)
    data = await state.get_data()
    check = int(data['id_text'])
    detail_list = info_detail(int(data['id_text']))
    if detail_list != None:
        check_obj = detail_list[1]
        obj_list = obj_info(check_obj)
        await message.answer(f'По заявке есть следующие данные: \nдата обращения: {detail_list[0]} '
                             f'\nобъект: {obj_list[0]} \nсистема: {detail_list[2]} '
                             f'\nописание: {detail_list[3]} \n'
                             f'Контакты нашего агента: \n Имя: {obj_list[1]} \n '
                             f'Номер телефона: {obj_list[2]}')
    else:
        await message.answer(f'Вы ввели неверный ID заявки {check}')
    await state.finish()


'''Конец блока получения подробной информации о заявке'''

'''Блок администрирования данных'''


@dp.message_handler(commands=['admin'])
async def admin_start(message):
    user_id = message.from_user.id
    check_role = role_search(user_id)
    if check_role[0] != 'True':
        await message.answer('Извините, у вас нет прав на администрирование бота!')
    else:
        await message.answer(f'Что будем администрировать:', reply_markup=kb_admin_start)


# Администрирование данных об агентах
@dp.callback_query_handler(text='agents')
async def set_agens(call):
    await call.message.answer('Редактирование блока агентов. \nКакие действия предпримем:',
                              reply_markup=kb_agents_admin)
    await call.answer()


# Администрирование данных о сотрудниках
@dp.callback_query_handler(text='workers')
async def set_agens(call):
    await call.message.answer('Редактирование блока сотрудников. \nКакие действия предпримем:',
                              reply_markup=kb_workers_admin)
    await call.answer()


# Администрирование данных о заданиях
@dp.callback_query_handler(text='jobs_list')
async def set_jobs(call):
    await call.message.answer('Данный блок находится в разработке. Извините...')
    await call.answer()


'''Конец блока администрирования данных'''

'''Блок обновления данных агентов'''


class AgentsUpdate(StatesGroup):
    vincod = State()
    resident = State()
    phone_num = State()


@dp.callback_query_handler(text='agents_update')
async def set_vincod(call):
    await call.message.answer('Введите код объекта или тапните "/cancel" для отмены:')
    await AgentsUpdate.vincod.set()
    await call.answer()


@dp.message_handler(state=AgentsUpdate.vincod)
async def set_resident(message, state):
    await state.update_data(vincod_text=message.text)
    data = await state.get_data()
    if data['vincod_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        check_vin = check_data(data['vincod_text'], 'Objects')
        if check_vin == False:
            await message.answer('Введен несуществующий код объекта')
        else:
            await message.answer('Введите имя агента или тапните "/cancel" для отмены:')
            await AgentsUpdate.resident.set()


@dp.message_handler(state=AgentsUpdate.resident)
async def set_phone_num(message, state):
    await state.update_data(resident_text=message.text)
    data = await state.get_data()
    if data['resident_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        await message.answer('Введите номер телефона или тапните "/cancel" для отмены:')
        await AgentsUpdate.phone_num.set()


@dp.message_handler(state=AgentsUpdate.phone_num)
async def update_agent(message, state):
    await state.update_data(phone_text=message.text)
    data = await state.get_data()
    data = await state.get_data()
    if data['phone_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        agent_update(data['vincod_text'], data['resident_text'], data['phone_text'])
        await message.answer('Данные об агенте изменены!')
        await state.finish()


'''Конец блока обновления данных об агентах'''

'''Блок ввода нового агента'''


class AgentsNew(StatesGroup):
    vincod = State()
    title = State()
    resident = State()
    phone_num = State()


@dp.callback_query_handler(text='agents_add')
async def new_vincod(call):
    await call.message.answer('Введите код объекта или тапните "/cancel" для отмены:')
    await AgentsNew.vincod.set()
    await call.answer()


@dp.message_handler(state=AgentsNew.vincod)
async def new_resident(message, state):
    await state.update_data(vincod_text=message.text)
    data = await state.get_data()
    if data['vincod_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        check_vin = check_data(data['vincod_text'], 'Objects')
        if check_vin == True:
            await message.answer('Такой код объекта уже существует. Введите другой!')
        else:
            await message.answer('Введите место дислокации агента или тапните "/cancel" для отмены:')
            await AgentsNew.title.set()


@dp.message_handler(state=AgentsNew.title)
async def new_resident(message, state):
    await state.update_data(title_text=message.text)
    data = await state.get_data()
    if data['title_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        await message.answer('Введите имя агента или тапните "/cancel" для отмены:')
        await AgentsNew.resident.set()


@dp.message_handler(state=AgentsNew.resident)
async def new_phone_num(message, state):
    await state.update_data(resident_text=message.text)
    data = await state.get_data()
    if data['resident_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        await message.answer('Введите номер телефона агента или тапните "/cancel" для отмены:')
        await AgentsNew.phone_num.set()


@dp.message_handler(state=AgentsNew.phone_num)
async def new_agent(message, state):
    await state.update_data(phone_text=message.text)
    data = await state.get_data()
    agent_new(data['vincod_text'], data['title_text'], data['resident_text'], data['phone_text'])
    await message.answer('Данные нового агента внесены!!')
    await state.finish()


'''Конец блока ввода нового агента'''

"""Блок удаления данных об агенте"""


class AgentsDel(StatesGroup):
    vincod = State()


@dp.callback_query_handler(text='agents_del')
async def del_vincod(call):
    await call.message.answer('Введите код объекта или тапните "/cancel" для отмены:')
    await AgentsDel.vincod.set()
    await call.answer()


@dp.message_handler(state=AgentsDel.vincod)
async def del_resident(message, state):
    await state.update_data(vincod_text=message.text)
    data = await state.get_data()
    if data['vincod_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        check_vin = check_data(data['vincod_text'], 'FilialJobs')
        if check_vin == True:
            await message.answer('Агент связан с заданиями. Удаление невозможно! Разрешено ТОЛЬКО редактирование')
            await state.finish()
        else:
            agent_del(data['vincod_text'])
            await message.answer('Агент удален!')
            await state.finish()


"""Конец блока удаления данных об агенте"""

'''Блок ввода нового сотрудника'''


class WorkersNew(StatesGroup):
    tlg_id = State()
    name = State()
    post = State()
    phone_num = State()
    role = State()


@dp.callback_query_handler(text='workers_add')
async def new_tlg_id(call):
    await call.message.answer('Введите ID сотрудника (автоматически присваивается аккаунту telegram)'
                              ' или тапните "/cancel" для отмены:')
    await WorkersNew.tlg_id.set()
    await call.answer()


@dp.message_handler(state=WorkersNew.tlg_id)
async def new_name(message, state):
    await state.update_data(tlg_id_text=message.text)
    data = await state.get_data()
    if data['tlg_id_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        check_id = check_data(data['tlg_id_text'], 'FilialWorker')
        if check_id == True:
            await message.answer('Такой ID уже существует. Введите другой!')
        else:
            await message.answer('Введите имя сотрудника или тапните "/cancel" для отмены:')
            await WorkersNew.name.set()


@dp.message_handler(state=WorkersNew.name)
async def new_post(message, state):
    await state.update_data(name_text=message.text)
    data = await state.get_data()
    if data['name_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        await message.answer('Введите должность сотрудника или тапните "/cancel" для отмены:')
        await WorkersNew.post.set()


@dp.message_handler(state=WorkersNew.post)
async def new_phone_num(message, state):
    await state.update_data(post_text=message.text)
    data = await state.get_data()
    if data['post_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        await message.answer('Введите номер телефона сотрудника или тапните "/cancel" для отмены:')
        await WorkersNew.phone_num.set()


@dp.message_handler(state=WorkersNew.phone_num)
async def new_role(message, state):
    await state.update_data(phone_num_text=message.text)
    data = await state.get_data()
    if data['phone_num_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        await message.answer('Введите роль сотрудника (True - роль администратора) или тапните "/cancel" для отмены:')
        await WorkersNew.role.set()


@dp.message_handler(state=WorkersNew.role)
async def new_worker(message, state):
    await state.update_data(role_text=message.text)
    data = await state.get_data()
    worker_new(data['name_text'], data['post_text'], data['phone_num_text'], data['role_text'], data['tlg_id_text'])
    await message.answer('Данные нового сотрудника внесены!!')
    await state.finish()


'''Конец блока ввода нового сотрудника'''
'''Блок обновления данных сотрудников'''


class WorkersUpdate(StatesGroup):
    tlg_id = State()
    name = State()
    post = State()
    phone_num = State()
    role = State()


@dp.callback_query_handler(text='workers_update')
async def upd_tlg_id(call):
    await call.message.answer('Введите ID сотрудника или тапните "/cancel" для отмены:')
    await WorkersUpdate.tlg_id.set()
    await call.answer()


@dp.message_handler(state=WorkersUpdate.tlg_id)
async def upd_name(message, state):
    await state.update_data(tlg_id_text=message.text)
    data = await state.get_data()
    if data['tlg_id_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        check_id = check_data(data['tlg_id_text'], 'FilialWorker')
        check_admin = check_count()
        if check_id == False:
            await message.answer('Введен несуществующий ID сотрудника')
        else:
            if check_admin == False:
                check_role = role_search(data['tlg_id_text'])
                if check_role[0] == 'True':
                    await message.answer('Вы единственный администратор! Ваше редактирование запрещено!')
                    await state.finish()
                else:
                    await message.answer('Введите имя сотрудника или тапните "/cancel" для отмены:')
                    await WorkersUpdate.name.set()
            else:
                await message.answer('Введите имя сотрудника или тапните "/cancel" для отмены:')
                await WorkersUpdate.name.set()


@dp.message_handler(state=WorkersUpdate.name)
async def upd_post(message, state):
    await state.update_data(name_text=message.text)
    data = await state.get_data()
    if data['name_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        await message.answer('Введите должность сотрудника или тапните "/cancel" для отмены:')
        await WorkersUpdate.post.set()


@dp.message_handler(state=WorkersUpdate.post)
async def upd_phone_num(message, state):
    await state.update_data(post_text=message.text)
    data = await state.get_data()
    if data['post_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        await message.answer('Введите номер телефона или тапните "/cancel" для отмены:')
        await WorkersUpdate.phone_num.set()


@dp.message_handler(state=WorkersUpdate.phone_num)
async def upd_phone_num(message, state):
    await state.update_data(phone_num_text=message.text)
    data = await state.get_data()
    if data['phone_num_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        await message.answer('Введите роль сотрудника (True - администратор) или тапните "/cancel" для отмены:')
        await WorkersUpdate.role.set()


@dp.message_handler(state=WorkersUpdate.role)
async def update_role(message, state):
    await state.update_data(role_text=message.text)
    data = await state.get_data()
    if data['role_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        worker_update(data['name_text'], data['post_text'], data['phone_num_text'],
                      data['role_text'], data['tlg_id_text'])
        await message.answer('Данные о сотруднике изменены!')
        await state.finish()


'''Конец блока обновления данных о сотрудниках'''
"""Блок удаления данных о сотруднике"""


class WorkersDel(StatesGroup):
    tlg_id = State()


@dp.callback_query_handler(text='workers_del')
async def del_tlg_id(call):
    await call.message.answer('Введите ID сотрудника или тапните "/cancel" для отмены:')
    await WorkersDel.tlg_id.set()
    await call.answer()


@dp.message_handler(state=WorkersDel.tlg_id)
async def del_worker(message, state):
    await state.update_data(tlg_id_text=message.text)
    data = await state.get_data()
    if data['tlg_id_text'] == '/cancel':
        await message.answer('Вы отменили действие!')
        await state.finish()
    else:
        check_admin = check_count()
        check_id = check_data(data['tlg_id_text'], 'FilialWorker')
        if check_id == True and check_admin == False:
            await message.answer('Вы единственный администратор. Удаление невозможно! '
                                 'Перед удалением, назначьте роль администратора другому сотруднику')
            await state.finish()
        else:
            worker_del(data['tlg_id_text'])
            await message.answer('Сотрудник удален!')
            await state.finish()


"""Конец блока удаления данных о сотруднике"""

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

''' Данный блок находится в разработке, будет предназначен просто для того, чтобы сотрудники 
    могли снять напряжение, поулыбаться
    В будущем будет также завязан на таблицу.
# list_answer = ['Не чихай', 'Будьте здоровы', 'Кто здесь?']    

# @dp.message_handler(text=['апчхи'])
# async def set_new_age(message):
#     i = random.randrange(1, len(list_answer) + 1)
#     await message.answer(f'{list_answer[i - 1]}')


# class Lerne(StatesGroup):
#     new_answer = State()
#
#
# @dp.message_handler(text=['учись!'])
# async def set_new_age2(call):
#     await call.answer('И как мне желать здоровья?')
#     await Lerne.new_answer.set()
#     await call.answer()
#
# @dp.message_handler(state=Lerne.new_answer)
# async def set_list_answer(state):
#     await state.message()
#     #new_answer = Lerne.new_answer
#     list_answer.append(state.message())
#     await state.finish()
'''
