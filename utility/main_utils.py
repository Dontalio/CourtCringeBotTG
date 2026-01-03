import asyncio
import time


from  aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from BD_work import BD_user as bd
from aiogram.utils.chat_action import ChatActionSender
from create_bot import court_bot


###########################
class ValidOutputText:
    '''класс, который контролирует набор текста'''
    all_chat_act = set()
    work_sms = 0

    def __new__(cls, *args, **kwargs):
        print(f'попытка создать объект класса {cls.__name__}.. запрещено!')
        return
    @classmethod
    async def out_text(cls, *args, **kwargs):
        msg = kwargs.get('message', None)
        if not isinstance(msg, Message):
            return

        chat_id = msg.chat.id
        if chat_id not in cls.all_chat_act and cls.work_sms < 4:
            cls.all_chat_act.add(chat_id)
            cls.work_sms += 1
            print(f'набор текста активен для чата : {chat_id} | активных наборов = {cls.work_sms}')
            try:
                # имитация печати ботом
                async with  ChatActionSender.typing(bot= court_bot, chat_id=chat_id):
                    await output_text_bot(*args, **kwargs)
                    print(f'набор текста закончен активен для чата : {chat_id} | активных наборов = {cls.work_sms}')
            except:
                await output_text_error_bot(*args, **kwargs)
                print(f'Ошибка при попытке набора текста : {chat_id} | Error')
            finally:
                cls.work_sms -= 1
                if chat_id in cls.all_chat_act:
                    cls.all_chat_act.remove(chat_id)
        else:
            print(f'набор текста на паузе для чата : {chat_id} | активных наборов = {cls.work_sms}')
            await asyncio.sleep(2.0)
            await ValidOutputText.out_text(*args, **kwargs)


    pass
async def output_text_bot(message : Message = None, new_text : str = 'Что-то пошло не так???',
                          keyboard = None, reset : bool = False, html_teg : str = None):
    '''
    имитирует набор new_text у сообщения. Если нужно сбросить его, выберите параметр reset = True
    не поддерживает html-теги. Но можно передать html-тег для всего текста (нового) в параметре html_teg в виде текста
    '''
    if message is None:
        print(f'Пустое поле message для метода output_text_bot')
        return
    teg_one, teg_two = '', ''
    if html_teg is not None:
        teg_one, teg_two = f'<{html_teg}>', f'</{html_teg}>'
    text_old = message.text if not reset else '' # текущий текст, берём при верном флаге старый текст от смс.
    text_in = ''
    letters = '' # текст для "вставки" (но ещё не вставлен) - буфер
    i = 0
    # цикл основной генерации текста.
    for letter in new_text:
        letters += letter
        if letter in ('', ' ', '\n', '\t'): # данные символы телеграмм может обрезать в 0 и будет ошибка
            continue
        if len(letters) > 4:
            i += 1 # играем с "ручкой" (анимация)
            text_in = text_in + letters
            await asyncio.sleep(0.1)
            await message.edit_text(text= text_old + teg_one +text_in+ teg_two + f'\n｡{'｡' * (i % 3)}🖋')
            letters = '' # вставленный буфер обновляем
    else:
        # в случае, когда дошли до конца, но НЕ добавили letters (он менее 5и)!
        text_in = text_in + letters
        await asyncio.sleep(0.1)
        await message.edit_text(text= text_old + teg_one +text_in+ teg_two)
        await asyncio.sleep(0.1)


    if keyboard is not None:
        await message.edit_reply_markup(reply_markup= keyboard)


async def output_text_error_bot(message : Message = None, new_text : str = 'Что-то пошло не так???',
                          keyboard = None, reset : bool = False, html_teg : str = None):
    '''Затычка для ошибки'''
    await asyncio.sleep(3.1) # защита от спама, хоть какая-то
    teg_one, teg_two = '', ''
    if html_teg is not None:
        teg_one, teg_two = f'<{html_teg}>', f'</{html_teg}>'
    text_old = message.text if not reset else ''
    await message.edit_text(text_old + teg_one +new_text+ teg_two)
    if keyboard is not None:
        await message.edit_reply_markup(reply_markup= keyboard)

async def reset_inline_kb(message : Message | CallbackQuery, keyboard = None, dell_msg = False):
    '''
    если не передать клаву - удалит текущую. Если передать - заменит
    Работает с колбеком (меняет давшее его сообщение) и самим смс

    keyboard :  если None - то обнулит, иначе вставит к сообщению. Ожидает ReplyMurkup
    dell_msg : True - удалит старый текст (полученный из объекта msg) иначе не трогает текст .

    '''
    if not isinstance(message, Message):
        message = message.message # если колбэк - достаем клаву
    try:
        if dell_msg is True:
            await message.edit_text(text=f'<tg-spoiler>{message.text}</tg-spoiler>')
            await asyncio.sleep(0.5)
            await message.delete()
    except:
        print(f"невозможно удаление сообщения! {message.message_id} : {message.text[:15]}")
    try:
        if keyboard is None:
            await message.edit_reply_markup(keyboard =  ReplyKeyboardRemove())
        else:
            await message.edit_reply_markup(reply_markup= keyboard)
    except:
        print(f"удаление клавиатуры невозможно для сообщения! {message.message_id} : {message.text[:15]}")

async def rewrite_last_txt(message : Message | CallbackQuery, reset : bool = False, new_text = 'Новые носки'):
    ''' меняет только текст у сообщения за один запрос'''
    if not isinstance(message, Message):
        message = message.message  # если колбэк - достаем msg
    await  asyncio.sleep(0.5)
    text = message.text if not reset else ''
    text += new_text
    await message.edit_text(text)

########################################################

def can_use_menu(user_tg_id : int):
    '''допускает к использованию меню'''
    res = bd.check_info(user_tg_id)
    if not res:
        return None # случай пустого ответа, нету Юзера
    else:
        return all(item is not None for item in res.values())

def get_user_data(user_tg_id : int) -> dict:
    res = bd.check_info(user_tg_id)
    if not res:
        return None
    else:
        return res
###########################