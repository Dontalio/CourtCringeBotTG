from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from decouple import config


# список супер юзеров из env.
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

def ease_link_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Мой хабр", url='https://habr.com/ru/users/yakvenalex/')],
        [InlineKeyboardButton(text="Мой Telegram", url='tg://resolve?domain=yakvenalexx')],
        [InlineKeyboardButton(text="Веб приложение", web_app=WebAppInfo(url="https://tg-promo-bot.ru/questions"))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def uppdate_kb():
    bt_lst = [[InlineKeyboardButton(text='📝 Удалить', callback_data='del_call')],
              [InlineKeyboardButton(text='📄 Обновить', callback_data='update_call')]]
    return InlineKeyboardMarkup(inline_keyboard=bt_lst)
#№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№#

def register_kb(user_data : dict):
    # {'id_tg': self.id_tg, 'name': self.name,
    #  'adult': self.adult, 'gender': self.gender}
    user_tg_id = user_data['id_tg']
    user_name = user_data['name']
    user_adult = user_data['adult']
    user_gender = user_data['gender']
    inline_kb_list = []
    # inline_kb_list = [
    #     [InlineKeyboardButton(text='Указать имя', callback_data=f'<user_id>{user_tg_id}</user_id>_name')],
    #     [InlineKeyboardButton(text='Указать возвраст', callback_data=f'<user_id>{user_tg_id}</user_id>_age')],
    #     [InlineKeyboardButton(text='Указать свой гендер', callback_data=f'<user_id>{user_tg_id}</user_id>_gender')]
    # ]
    # inline_kb_list.append([InlineKeyboardButton(text='Пробник_тест',
    #                                             callback_data=f'test_')])
    if user_name is None:
        inline_kb_list.append([InlineKeyboardButton(text='Указать имя',
                                                    callback_data=f'name_')])
    if user_adult is None:
        inline_kb_list.append([InlineKeyboardButton(text='Указать возвраст',
                                                    callback_data=f'age_')])
    if user_gender is None:
        inline_kb_list.append([InlineKeyboardButton(text='Указать свой гендер',
                                                    callback_data=f'gender_')])
    if not inline_kb_list:
        inline_kb_list.append([InlineKeyboardButton(text='Запустить меню', callback_data='success_reg_reg')])
    print(f"register_kb : was set like {inline_kb_list}")
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def main_kb(user_telegram_id: int):
    bt_lst  = [
        [InlineKeyboardButton(text="❤️ Создать подкат", callback_data= 'make_court'),
         InlineKeyboardButton(text="👤 Профиль", callback_data= 'show_profile')]
    ]
    if user_telegram_id in admins: # при создании клавы для юзера - проверяем кто он.
        bt_lst .append([InlineKeyboardButton(text="⚙️ Админ панель", callback_data= 'admin_menu'),])
    return InlineKeyboardMarkup(inline_keyboard=bt_lst) # вернём готовую сгенерированную клавиатуру


def profile_settings_kb():
    bt_lst = [[InlineKeyboardButton(text = '📝 Обновить информацию о себе', callback_data='update_info')],
              #[InlineKeyboardButton(text = '📑 Ваш пресет...', callback_data='preset_info')],
              [InlineKeyboardButton(text = '📄 Назад в меню', callback_data="success_reg_profile")]]
    return InlineKeyboardMarkup(inline_keyboard=bt_lst)

def make_court_kb():
    button_lst = [
        [InlineKeyboardButton(text='🍓 Подкат для себя 🍓', callback_data= f'get_jokes_user_first')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=button_lst)

def jokes_menu():
    button_lst = [
        [InlineKeyboardButton(text= "❤️ Повторить подкат" , callback_data="get_jokes_user_repet")],
        [InlineKeyboardButton(text ="📄 Назад в меню" ,callback_data="success_reg_court")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=button_lst)