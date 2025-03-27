from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from db.db import user_tasks

def get_main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton(text="Мои задачи")],
            [KeyboardButton(text="Редактировать задачи")],
            [KeyboardButton(text="Время напоминания")]
        ])
    return keyboard

def get_edit_tasks_keyboard():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Создать задачу")],
            [KeyboardButton(text="Удалить задачу")],
            [KeyboardButton(text="Назад")]
        ])
    return keyboard

def get_tasks_inline_keyboard(user_id):
    tasks = user_tasks.get(user_id, [])
    for i, task_data in enumerate(tasks):
        # Добавим callback data для каждой задачи
        inline_keyboard.append([InlineKeyboardButton(text=f"{task_data['task']}", callback_data=f"task_details_{i}")])
    keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=inline_keyboard)
    return keyboard
