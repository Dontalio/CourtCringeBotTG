from aiogram import Router
from aiogram.filters import CommandStart
from  aiogram.types import Message, CallbackQuery
from keyboards import inline_keyboards
from utility.main_utils import can_use_menu, get_user_data
from BD_work import BD_user as bd

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message : Message | CallbackQuery, text_from : str = ''):
    '''Стартовое меню бота'''
    user_id = message.from_user.id # извлекаем тг_ид
    if isinstance(message, CallbackQuery):
        message = message.message # извлекаем message
    text_from = text_from + '\n' if text_from else ''

    print(f" was start <start> with {message}")
    res = can_use_menu(user_tg_id= user_id)
    user_data = get_user_data(user_tg_id=user_id)
    if res is None:
        # сценарий первого запуска чата для нового пользователя
        bd.register_id(user_id) # регистрируем ИД.
        await message.answer('🫦 Вас приветсвует <b>бот кринжовых</b> подкатов 🫦\n'
                            'Так как вы новый пользователь, вам необходимо заполнить данные о вашем профиле:\n\n'
                            '<blockquote><i>Это позволит боту подбирать правильные шутки-подкаты для вас!</i></blockquote>',
                        reply_markup=inline_keyboards.register_kb(bd.check_info(user_id)))
    elif not res:
        # если ранее ид_тг пользователя было занесено в БД.
        await message.answer('🫦Неполная регистрация в <b>боте кринжовых</b> подкатов 🫦\n'
                            f'{text_from}Без заполненных данных о профиле функционал бота недоступен:\n\n'
                            '<blockquote><i>Для заполнения данных выбери необходимое ниже</i></blockquote>',
                            reply_markup=inline_keyboards.register_kb(user_data))
    elif res:
        await message.answer('🫦 <b>Бот кринжовых</b> подкатов 🫦\n'
                            f'{text_from}Все необходимые данные заполнены верно!\n\n'
                            'Для вызова основного меню введи команду /menu',
                            reply_markup=inline_keyboards.register_kb(user_data))




