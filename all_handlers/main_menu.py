import asyncio
import time

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from  aiogram.types import Message, CallbackQuery
from keyboards import reply_keyboards, inline_keyboards
from make_joke.user_jokes import make_joke_for_user
from utility.main_utils import *
from all_handlers.start_menu import cmd_start


main_router = Router()

@main_router.message(Command('test_upp'))
async def test_upp(message : Message):
    msg = await message.answer('пробный текст (1)', reply_markup= inline_keyboards.uppdate_kb())

@main_router.callback_query(F.data == 'del_call')
async def del_msg(callback : CallbackQuery):
    msg = callback.message
    await msg.delete()
    pass

@main_router.callback_query(F.data == 'update_call')
async def update_msg(callback : CallbackQuery):
    msg = callback.message # по факту это сообщение от БОТА, которое "зацеплено" к колбеку через клаву.

    await asyncio.sleep(0.5)
    text = ('Привет, давай попробуем сделать что-то вроде набора текста?\n'
            'Как тебе? Выглядит правдапободно?'
            '\n\n\n\n\n'
            'ну да мне без разницы. Тут много всякого!!!!❤️‍🔥❤️‍🔥❤️‍🔥')
    await ValidOutputText.out_text(message= msg, new_text= text,
                          keyboard= inline_keyboards.ease_link_kb(),
                          reset= False,
                          html_teg= 'i')


###################################################

@main_router.message(Command('menu'))
async def menu_from_command(message : Message):
    '''вызов основного меню с функционалом бота'''
    if not can_use_menu(message.from_user.id):
        await cmd_start(message, text_from = 'Без заполненного до конца профиля основное меню недоступно') # возвращаем назад!
    else:
        print('Было запущено главное меню!')
        await main_menu(message = message)


@main_router.callback_query(F.data.startswith('success_reg'))
async def menu_from_callback_reg(callback : CallbackQuery):
    await reset_inline_kb(callback)
    if not can_use_menu(callback.from_user.id):
        await rewrite_last_txt(callback, reset= False, new_text='\n\n<blockquote>Ошибка запуска меню!</blockquote>')
        await cmd_start(callback, text_from = 'Без заполненного до конца профиля основное меню недоступно') # возвращаем назад!
    else:
        print('Было запущено главное меню!')
        await main_menu(callback= callback)


async def main_menu(message : Message = None, callback : CallbackQuery = None):
    if callback:
        user_tg_id, name, adult, gender = bd.check_info(callback.from_user.id).values()
        text_menu = (f"💝💖💕 <b>{name}</b> 💝💖💕\n"
                     f"<blockquote>Выберите пункт меню!</blockquote>")
        await callback.answer()
        await callback.message.answer(text= text_menu,
                                      reply_markup=inline_keyboards.main_kb(user_telegram_id= user_tg_id))
    elif message:
        user_tg_id, name, adult, gender = bd.check_info(message.from_user.id).values()
        text_menu = (f"💝💖💕 <b>{name}</b> 💝💖💕\n"
                     f"<blockquote>Выберите пункт меню!</blockquote>")
        await message.answer(text=text_menu,
                                      reply_markup=inline_keyboards.main_kb(user_telegram_id=user_tg_id))


@main_router.callback_query(F.data == 'make_court')
async def make_court_one(callback : CallbackQuery):
    await reset_inline_kb(callback, dell_msg=True)
    tg_id = callback.from_user.id
    if not can_use_menu(tg_id):
        await cmd_start(callback, text_from =  'Никаких подкатов, ваш профиль не заполнен!') # возвращаем назад!
    else:
        print('запуск редактора подката')
        await callback.message.answer('Для кого мне придумать лучший в мире подкат?'
                            '\n❤️‍🔥', reply_markup= inline_keyboards.make_court_kb())


@main_router.callback_query(F.data == 'show_profile')
async def show_profile(callback : CallbackQuery):
    # d = {'id_tg': self.id_tg, 'name': self.name,
    #  'adult': self.adult, 'gender': self.gender}
    await reset_inline_kb(callback, dell_msg= True)
    tg_id, name, adult, gender = bd.check_info(callback.from_user.id).values()
    if gender == True:
        gender = "Мужской"
        suffix = 'ий'
    elif gender == False:
        gender = "Женский"
        suffix = 'яя'
    else:
        gender = '???'
        suffix = ''

    if adult == True:
        adult = 'Совершеннолетн'
    elif adult == False:
        adult = 'Несовершеннолетн'
    else:
        adult = '???'
    await callback.message.answer(f"<b>Информация о вашем профиле</b>:\n"

                        f"<blockquote>Имя : {name if name is not None else '???'}\n"
                        f"Возраст : {adult + suffix}\n"
                        f"Пол : {gender}\n</blockquote>",
                        reply_markup=inline_keyboards.profile_settings_kb())


@main_router.callback_query(F.data.startswith('get_jokes_user_'))
async def show_jokes_callback(callback : CallbackQuery):
    # если мы запускаем из меню (не повтор)
    await reset_inline_kb(callback, dell_msg= True if callback.data == 'get_jokes_user_first' else False)
    if can_use_menu(callback.from_user.id):
        joke = make_joke_for_user(callback.from_user.id)
        await callback.answer('подкат...')
        msg = await callback.message.answer(text= "<blockquote>Подбираю шутку</blockquote>\n")
        await asyncio.sleep(1)
        await ValidOutputText.out_text(message= msg, new_text= joke,
                          keyboard= inline_keyboards.jokes_menu(),
                          reset= True,
                          html_teg= "blockquote")
    else:
        await cmd_start(callback, text_from ='Никаких подкатов, ваш профиль не заполнен!')
