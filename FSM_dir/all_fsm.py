from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from pyexpat.errors import messages
from utility.main_utils import *

from keyboards import reply_keyboards, inline_keyboards
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utility.main_utils import reset_inline_kb, rewrite_last_txt
from all_handlers.start_menu import cmd_start
from BD_work import BD_user as bd

fsm_router = Router()


class Register(StatesGroup):
    GENDER = State()
    NAME = State()
    ADULT = State()
    TEST = State()
    UPDATE =  State()


# router
async def get_info():
    '''Запуск всех трёх функций получения данных последовательно'''
    # в текущей реализации не имеет смысла
    pass


@fsm_router.callback_query(F.data == 'name_')
async def get_name(call: CallbackQuery, state: FSMContext):
    '''получение имени пользователя'''
    print('was start get_name')
    print('callback : ',call)
    print('state : ', state)
    await reset_inline_kb(call)
    await call.answer()
    await state.set_state(Register.NAME)
    await call.message.answer('Введите ваше имя самостоятельно или используйте кнопку!',
                              reply_markup=reply_keyboards.reg_name_jb(call))


@fsm_router.message(F.text, Register.NAME)
async def set_name(message: Message, state: FSMContext):
    print('was start set_name')
    print('message : ',message)
    print('state : ', state)
    name_to = message.text.title()
    if not (1 < len(name_to) < 51):
        await message.reply(text='Имя не может быть такого размера!\n'
                                 '<blockquote>Если ваше имя действительно звучит так, то отправьте более подходящую кличку или прозвище.</blockquote>',
                            reply_markup= reply_keyboards.reg_name_jb(message))
        return
    user_tg_id = message.from_user.id
    text_to = 'Такое замечательное имя, от него все без ума?\n' \
              f'<blockquote>Я запомнил вас, {name_to}!</blockquote>'
    bd.insert_info(user_tg_id, name=name_to)
    await state.clear()
    await cmd_start(message, text_to)


@fsm_router.callback_query(F.data == 'age_')
async def get_adult(call: CallbackQuery, state: FSMContext):
    await reset_inline_kb(call)
    await call.answer()
    await state.set_state(Register.ADULT)
    await call.message.answer('Укажите ваш возврат в формате числа (например так, <i>27</i>)')
    # а если белеберду отправит? Нужно перепроверять!


@fsm_router.message(F.text, Register.ADULT)
async def set_adult(message: Message, state: FSMContext):
    try:
        adult_from : int =  int(message.text)
    except:
        await  message.reply(text=f'Возраст должен быть числом! Отправьте целое число в чат'
                                  f'\n<blockquote>Вы отправили <b>{message.text[:15]}</b>... и это не похоже на число, <i>например, на 27</i></blockquote>')
        return


    if  not (3 < adult_from < 130):
        await  message.reply(text=f'Вам не может быть столько лет! Отправьте реальный возраст'
                                  f'\n<blockquote>Какие <b>{adult_from}</b> - серьёзно?</blockquote>')
        return
        #################################
    user_tg_id = message.from_user.id
    name = ''
    data = bd.check_info(user_tg_id) # попытка обратиться к имени (если есть)
    if data:
        name = data.get('name', '')
    ##################################
    adult_to = True if adult_from >= 18 else False
    text_to = f'Что-ж, возраст узнали! Вы {'уже выросли' if adult_to else 'Маловаты, я буду повежливее'} \n' \
              f'<blockquote>Я узнал ваш возраст, {name if name else 'пользователь'}!</blockquote>'
    bd.insert_info(user_tg_id, adult= adult_to)
    await state.clear()
    await cmd_start(message, text_to)


@fsm_router.callback_query(F.data == 'gender_')
async def get_gender(call: CallbackQuery, state: FSMContext):
    await reset_inline_kb(call)
    await call.answer()
    await state.set_state(Register.GENDER)
    await call.message.answer('деликатный вопрос. Какого ты пола? Выбери его!',
                              reply_markup= reply_keyboards.reg_adult_kb(call))


@fsm_router.message(F.text, Register.GENDER)
async def set_gender(message: Message, state: FSMContext):
    user_tg_id = message.from_user.id
    gender_from = message.text
    if gender_from not in ("Мужской 🙎‍♂️" ,"Женский 🙎‍♀️"):
        await message.reply(text='Ты отправил что-то не то..\n'
                                 '<blockquote>Используй кнопки в чате!</<blockquote>>',
                            reply_markup= reply_keyboards.reg_adult_kb(message))
        return
    gender_to = True if "Мужской 🙎‍♂️" == gender_from else False
    #################################
    name = ''
    data = bd.check_info(user_tg_id)  # попытка обратиться к имени (если есть)
    if data:
        name = data.get('name', '')
    ##################################
    gender_edit = 'ой' if gender_to else 'ая'
    text_to = f'Приятно узнать, что у вас ниже (или выше?), Дорог{gender_edit} {name if name else '!'}\n' \
              f'<blockquote>А что же дальше?</blockquote>'
    bd.insert_info(user_tg_id, gender=gender_to)
    await state.clear()
    await cmd_start(message, text_to)

@fsm_router.callback_query(F.data == 'update_info')
async def update_info_delete(callback : CallbackQuery):
    await rewrite_last_txt(callback, reset=True,
                           new_text=f"<b>Информация о вашем профиле</b>:\n"

                                    f"<blockquote>Имя : ???\n"
                                    f"Возраст : ???\n"
                                    f"Пол : ???</blockquote>\n"
                                    f"<i>UPD: информация сброшена</i>", )
    await reset_inline_kb(callback)
    tg_id = callback.from_user.id
    bd.delete_info(tg_id)
    await callback.answer(text='Информация сброшена - обновите данные', show_alert= True)
    await cmd_start(callback, 'Заполните данные профиля заново!\n')
    print(f"for user id : {tg_id} - info was clear")
