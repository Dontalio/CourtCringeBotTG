import asyncio
from create_bot import *
from aiogram.types import BotCommand, BotCommandScopeDefault
from all_handlers.main_menu import main_router
from all_handlers.start_menu import start_router
from FSM_dir.all_fsm import fsm_router


'''
Для запуска бота, его основного цикла с полингом. ПОдключение всего остального
'''

# court_bot = Bot(token=config('TOKEN'),
#                 default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]
# logger = logging.getLogger(__name__)
# dp = Dispatcher(storage=MemoryStorage())
# scheduler = AsyncIOScheduler(timezone='Europe/Moscow')


def include_routers():
    '''подключение всех роутеров'''
    dp.include_router(start_router)
    dp.include_router(fsm_router)
    dp.include_router(main_router)
    print(f'роутеры успешно подключены')


async def set_commands():
    '''принимает словарь с командами'''
    func_list = {
        'start': 'Первый и повторный запуск бота, регистрация',
        'menu': 'Основное меню бота',
        'help': 'Информационная справка о боте'
    }
    commands = []
    for command, descript in func_list.items():
        commands.append(BotCommand(command=command, description=descript))
    print("команды меню бота:", *commands, sep=' || ')
    await court_bot.set_my_commands(commands, BotCommandScopeDefault())
    print('SUCCES for SET COMMANDS')


async def main():
    '''основной асинхронный цикл бота'''
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start() # планировка и запуск задачи
    include_routers()  # запускаем все роутеры
    await court_bot.delete_webhook(
        drop_pending_updates=True)  # отключаем автообновление в окружении (skip_updates=True )
    await set_commands()  # сначала опеределим настройки бота (меню)
    await dp.start_polling(court_bot)  # запуск поллинга (опроса АПИ TG)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('бот выключен')
