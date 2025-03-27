from aiogram.fsm.state import State, StatesGroup


class TaskForm(StatesGroup):
    waiting_for_task_text = State()
    waiting_for_task_time = State()
    waiting_for_task_to_delete = State()
    waiting_for_reminder_time = State()