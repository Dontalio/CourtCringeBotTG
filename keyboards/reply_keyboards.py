from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import Message, CallbackQuery

def reg_name_jb(call : CallbackQuery | Message):
    first_name = call.from_user.first_name.title()
    kb_list = [[KeyboardButton(text= f'{first_name}')]]
    return ReplyKeyboardMarkup(keyboard=kb_list,
                               resize_keyboard=True,
                               input_field_placeholder='Или отправьте напишите своё имя в чате...'
                               )

def reg_adult_kb(call : CallbackQuery | Message):
    kb_list = [[KeyboardButton(text=f'Мужской 🙎‍♂️')], [KeyboardButton(text=f'Женский 🙎‍♀️')]]
    return ReplyKeyboardMarkup(keyboard=kb_list,
                               resize_keyboard=True,
                               input_field_placeholder='Выберите пол'
                               )
def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="❤️ Создать подкат"), KeyboardButton(text="👤 Профиль")]
    ]
    if user_telegram_id in admins: # при создании клавы для юзера - проверяем кто он.
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list,
                                   resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder='Основное меню бота...')
    return keyboard # вернём готовую сгенерированную клавиатуру

def jokes_menu():
    kb_list = [
        [KeyboardButton(text="❤️ Повторить подкат")],
        [KeyboardButton(text="📄 Назад в меню")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list,
                                   resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder='I so love u')
    return keyboard  # вернём готовую сгенерированную клавиатуру

def get_spec_info():
    kb_list = [
        [KeyboardButton(text='CONTACT', request_contact=True), KeyboardButton(text='GEO', request_location=True)]
    ]
    keboard = ReplyKeyboardMarkup(keyboard= kb_list,
                                  resize_keyboard=True,
                                 # one_time_keyboard=True,
                                  input_field_placeholder='Рассказать о себе...'
                                  )
    return keboard


#################################################################################
def auto_generate_kb(to_button : list[str]):
    builder = ReplyKeyboardBuilder()
    for item in to_button[0:10]:
        builder.button(text=item)
    builder.button(text='Назад')
    builder.adjust(3, 3, 3)
    return builder.as_markup(resize_keyboard=True, input_field_placeholder='1- 10..')

#№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№#




