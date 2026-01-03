
class UserTable:
    def __init__(self, id_tg: int):
        self.id_tg = id_tg
        self.name = None
        self.adult = None
        self.gender = None
        self.last_set = None

    def get_user_info(self):
        return {'id_tg': self.id_tg, 'name': self.name,
                'adult': self.adult, 'gender': self.gender}

    def get_user_set(self):
        return self.last_set

    def set_user(self, adult: bool = None, gender: bool = None, name: str = None):
        '''Обновление данных  у экземплра на "непустышки"'''
        if adult is not None:
            self.adult = adult
        if gender is not None:
            self.gender = gender
        if name is not None:
            self.name = name

    def del_user(self):
        self.name = None
        self.adult = None
        self.gender = None
        self.last_set = None
        print(f'объект UserTable с {self.id_tg} обнулён до None')


class AllUsers:
    is_one = None
    all_users: dict = {'1' : 'None'}

    def __new__(cls, *args, **kwargs):
        raise IndentationError('объекты класса AllUsers нельзя создавать')

    @classmethod
    def register_id(cls, id_tg: int):
        cls.all_users[id_tg] = UserTable(id_tg)
        print(f"register_id : was remember new_id {id_tg}")

    @classmethod
    def check_info(cls, id_tg: int):
        res = cls.all_users.get(id_tg, None)
        if res:
            return res.get_user_info()
        else:
            print(f'{id_tg} такого пользователя нет в базе (не сработал register_id?)')
            return None

    @classmethod
    def insert_info(cls, id_tg: int, adult: bool = None, gender: bool = None, name: str = None):
        cls.all_users[id_tg].set_user(adult, gender, name)
        print(f"insert_info : update info for user_id : {id_tg} - with - adult : {adult}, gender : {gender} , name : {name}")
        print(f"after insert_info : {cls.check_info(id_tg)}\n")

    @classmethod
    def check_id(cls, id_tg):
        this_id = cls.all_users.get(id_tg, False)
        res =  True if cls.all_users.get(id_tg, False) else False
        print(f"check_id : for user with id {id_tg} and res {res} - for {this_id}")
        return res

    @classmethod
    def delete_info(cls, id_tg : int):
        if id_tg in cls.all_users:
            cls.all_users[id_tg].del_user()
            print(f'успешное удаление {id_tg} в БД')
        else:
            print(f'не найден пользователь {id_tg} в БД')



    ########################
    @classmethod
    def get_user(cls, id_tg: int):
        return cls.all_users.get(id_tg, False)
