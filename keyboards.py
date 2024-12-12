from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Детализация заявок

kb_jobs_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подробности', callback_data='detail')
            # InlineKeyboardButton(text='Вернуться', callback_data='back')
        ]
    ], resize_keyboard=True
)

# Стартовая клавиатура
kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Текущие заявки'),
            KeyboardButton(text='Информация о боте')],
        [
            KeyboardButton(text='Список объектов и агентов')
        ],
        [
            KeyboardButton(text='Список наших доблестных сотрудников')
        ]
    ], resize_keyboard=True
)

# Начальная клавиатура администрирования
kb_admin_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Агентов', callback_data='agents'),
            InlineKeyboardButton(text='Сотрудников', callback_data='workers'),
            InlineKeyboardButton(text='Задания', callback_data='jobs_list')
        ]
    ], resize_keyboard=True
)

# Клавиатура администрирования агентов
kb_agents_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Изменить', callback_data='agents_update'),
            InlineKeyboardButton(text='Добавить', callback_data='agents_add'),
            InlineKeyboardButton(text='Удалить', callback_data='agents_del')
        ],
        [
            InlineKeyboardButton(text='Список агентов', callback_data='agents_list')
        ]
    ], resize_keyboard=True
)

# Клавиатура администрирования сотрудников
kb_workers_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Изменить', callback_data='workers_update'),
            InlineKeyboardButton(text='Добавить', callback_data='workers_add'),
            InlineKeyboardButton(text='Удалить', callback_data='workers_del')
        ],
        [
            InlineKeyboardButton(text='Список сотрудников', callback_data='workers_list')
        ]
    ], resize_keyboard=True
)
