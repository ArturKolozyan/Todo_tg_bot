import datetime
from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.utils.formatting import as_list
from aiogram.fsm.context import FSMContext

from app.keyboards import *
from app.states import *
from db.db import *

router = Router()

# Хэндлеры команд
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Это бот для управления задачами.",
                         reply_markup=get_main_menu_keyboard())


# Хэндлеры для выбора пунктов меню
@router.message(F.text == "Мои задачи")
async def show_tasks(message: types.Message):
    user_id = message.from_user.id
    tasks = user_tasks.get(user_id, {})
    if tasks:
        task_list = as_list(*[f"{i + 1}. {task['task']} (Время: {task['time']})" for i, task in
                              enumerate(tasks)])  # Отображение времени в списке задач
        await message.answer(f"Ваши задачи:\n{task_list}", reply_markup=get_tasks_inline_keyboard(user_id))
    else:
        await message.answer("У вас пока нет задач.", reply_markup=get_main_menu_keyboard())


@router.message(F.text == "Редактировать задачи")
async def edit_tasks(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=get_edit_tasks_keyboard())


@router.message(F.text == "Время напоминания")
async def set_reminder_time(message: types.Message, state: FSMContext):
    await message.answer("Введите время напоминания в формате HH:MM (например, 10:30):")
    await state.set_state(TaskForm.waiting_for_reminder_time)


# Хэндлеры для подменю "Редактировать задачи"
@router.message(F.text == "Создать задачу")
async def create_task(message: types.Message, state: FSMContext):
    await message.answer("Введите текст задачи:")
    await state.set_state(TaskForm.waiting_for_task_text)


@router.message(F.text == "Удалить задачу")
async def delete_task(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    tasks = user_tasks.get(user_id, [])
    if tasks:
        task_list = "\n".join([f"{i + 1}. {task['task']}" for i, task in enumerate(tasks)])
        await message.answer(f"Выберите задачу для удаления (введите номер):\n{task_list}")
        await state.set_state(TaskForm.waiting_for_task_to_delete)
    else:
        await message.answer("У вас нет задач для удаления.", reply_markup=get_edit_tasks_keyboard())


@router.message(F.text == "Назад")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню:", reply_markup=get_main_menu_keyboard())


# Хэндлеры для ввода данных (Состояния)
@router.message(TaskForm.waiting_for_task_text)
async def process_task_text(message: types.Message, state: FSMContext):
    task_text = message.text
    await message.answer("Теперь введите время для напоминания в формате HH:MM (например, 10:30):")
    await state.set_state(TaskForm.waiting_for_task_time)
    await state.update_data(task_text=task_text)


@router.message(TaskForm.waiting_for_task_time)
async def process_task_time(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    time_str = message.text
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
    except ValueError:
        await message.answer("Неверный формат времени. Пожалуйста, введите время в формате HH:MM.")
        return

    data = await state.get_data()
    task_text = data.get("task_text")
    if not task_text:
        await message.answer("Ошибка: Текст задачи не найден.")
        await state.clear()
        return

    if user_id not in user_tasks:
        user_tasks[user_id] = []

    user_tasks[user_id].append({"task": task_text, "time": time_str})
    await message.answer("Задача успешно создана!", reply_markup=get_edit_tasks_keyboard())
    await state.clear()  # Сброс состояния


@router.message(TaskForm.waiting_for_task_to_delete)
async def process_task_to_delete(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        task_index = int(message.text) - 1
        if 0 <= task_index < len(user_tasks.get(user_id, [])):
            del user_tasks[user_id][task_index]
            await message.answer("Задача удалена.", reply_markup=get_edit_tasks_keyboard())
        else:
            await message.answer("Неверный номер задачи.", reply_markup=get_edit_tasks_keyboard())
    except ValueError:
        await message.answer("Пожалуйста, введите число.", reply_markup=get_edit_tasks_keyboard())
    finally:
        await state.clear()


@router.message(TaskForm.waiting_for_reminder_time)
async def process_reminder_time(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    time_str = message.text
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        user_reminder_times[user_id] = time_str
        await message.answer(f"Время напоминания установлено на {time_str}", reply_markup=get_main_menu_keyboard())
    except ValueError:
        await message.answer("Неверный формат времени. Пожалуйста, введите время в формате HH:MM.")
    finally:
        await state.clear()


# Callback для отображения подробностей о задаче (необязательно)
@router.callback_query(lambda c: c.data and c.data.startswith('task_details_'))
async def process_task_details_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    task_index = int(callback_query.data.split('_')[2])
    tasks = user_tasks.get(user_id, [])
    if 0 <= task_index < len(tasks):
        await callback_query.answer(
            text=f"Подробности задачи: {tasks[task_index]['task']} (Время: {tasks[task_index]['time']})",
            show_alert=True)
    else:
        await callback_query.answer(text="Ошибка: Задача не найдена", show_alert=True)
    await callback_query.message.edit_reply_markup(reply_markup=None)  # Remove the inline keyboard