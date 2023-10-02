from typing import List
from pydantic import BaseModel
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData


from tgbot.config import TGBOT_USERNAME

# Sructure of callback buttons
class SimpleCbFactory(CallbackData, prefix="B"):
    question: str
    answer: Optional[str] = None
    data: int


async def make_inline_keyboard(question_name: str, answers: list, data=0):
    """Возвращает клавиатуру для сообщений"""
    if not answers:
        return None

    keyboard = InlineKeyboardBuilder()

    for answer in answers:  # make a botton for every answer
        cb_data = SimpleCbFactory(
            question=question_name,
            answer=answer,
            data=data)
        keyboard.button(
            text=answer, callback_data=cb_data
        )    
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()


async def make_button_for_add_bot_to_chat():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton(
        text="Добавить бота в группу",
        url=f"https://t.me/{TGBOT_USERNAME}?startgroup="))

    return keyboard


async def make_button_link_to_bot():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton(
        text="Перейти в бота",
        url=f"https://t.me/{TGBOT_USERNAME}"))

    return keyboard


class ButtonItem(BaseModel):
    text: str
    item_id: int

async def make_multiple_choice_keyboard(
        buttons_list: List[ButtonItem],
        question: str,
        chosen_id: list = None,
        pressed_answer: str = None,
        pressed_data: int = None) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру c мультивыбором

    Args:
        buttons_list (List[ButtonItem]): список кнопок
        question (str): вопрос
        chosen_id (list, optional): список id уже выбранных элементов.
        pressed_answer (str, optional): нажатая кнопка.
        pressed_data (int, optional): нажатая кнопка.

    Returns:
        InlineKeyboardMarkup: keyboard
        list: chosen_id
    """
    if pressed_answer is None:
        pass
    elif pressed_answer == 'next_step':
        if chosen_id:
            return None, chosen_id
    elif pressed_answer == 'scroll':
        pass
    else:
        item_id = int(pressed_answer)
        if item_id not in chosen_id:
            chosen_id.append(item_id)
        else:
            chosen_id.remove(item_id)

    keyboard = InlineKeyboardMarkup()
    first_num = pressed_data

    if first_num:
        buttons_list = buttons_list[first_num:first_num+10]
        privios_first_num = max(first_num-10, 0)

        if len(buttons_list) < 10:
            next_first_num = first_num
        else:
            next_first_num = first_num + 10
    else:
        buttons_list = buttons_list[:10]
        first_num = 0
        privios_first_num = 0
        next_first_num = min(len(buttons_list), 10)

    if not chosen_id:
        chosen_id = []

    for button in buttons_list:
        if button.item_id not in chosen_id:
            text = f'⬜ {button.text}'
        else:
            text = f'🔳 {button.text}'

        cb_data = SimpleCbFactory(
            question=question,
            answer=button.item_id,
            data=first_num)
        keyboard.row(InlineKeyboardButton(
            text=text,
            callback_data=cb_data
        ))
    
    privios_first_num_cb_data = SimpleCbFactory(
        question=question,
        answer='scroll',
        data=privios_first_num)
    next_first_num_cb_data = SimpleCbFactory(
        question=question,
        answer='scroll',
        data=next_first_num)
    next_step_cb_data = SimpleCbFactory(
        question=question,
        answer='next_step',
        data=0)
    keyboard.row(
        InlineKeyboardButton(
            text='<',
            callback_data=privios_first_num_cb_data
        ),
        InlineKeyboardButton(
            text='✔️ Продолжить',
            callback_data=next_step_cb_data
        ),
        InlineKeyboardButton(
            text='>',
            callback_data=next_first_num_cb_data
        )
    )

    return keyboard, chosen_id


async def make_keyboard_with_scroll(
        buttons_list: List[ButtonItem],
        question: str,
        pressed_answer: str = None,
        pressed_data: int = None) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру c мультивыбором

    Args:
        buttons_list (List[ButtonItem]): список кнопок
        question (str): вопрос
        pressed_answer (str, optional): нажатая кнопка.
        pressed_data (int, optional): нажатая кнопка.

    Returns:
        InlineKeyboardMarkup: keyboard
        int: chosen_id
    """
    if pressed_answer is None:
        chosen_id = None
    elif pressed_answer == 'scroll':
        chosen_id = None
    else:
        chosen_id = int(pressed_answer)

    keyboard = InlineKeyboardMarkup()
    first_num = pressed_data

    if first_num:
        buttons_list = buttons_list[first_num:first_num+10]
        privios_first_num = max(first_num-10, 0)

        if len(buttons_list) < 10:
            next_first_num = first_num
        else:
            next_first_num = first_num + 10
    else:
        buttons_list = buttons_list[:10]
        first_num = 0
        privios_first_num = 0
        next_first_num = min(len(buttons_list), 10)

    for button in buttons_list:
        text = f'{button.text}'
        cb_data = SimpleCbFactory(
            question=question,
            answer=button.item_id,
            data=first_num)
        keyboard.row(InlineKeyboardButton(
            text=text,
            callback_data=cb_data
        ))

    privios_first_num_cb_data = SimpleCbFactory(
        question=question,
        answer='scroll',
        data=privios_first_num)
    next_first_num_cb_data = SimpleCbFactory(
        question=question,
        answer='scroll',
        data=next_first_num)
    keyboard.row(
        InlineKeyboardButton(
            text='<',
            callback_data=privios_first_num_cb_data
        ),
        InlineKeyboardButton(
            text='>',
            callback_data=next_first_num_cb_data
        )
    )

    return keyboard, chosen_id
