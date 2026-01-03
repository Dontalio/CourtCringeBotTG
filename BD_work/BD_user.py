from BD_work.BD_USER_TABLE import AllUsers


def decor_bd(func):
    def wrapper_bd(*args, **kwargs):
        func_wrapper = {
            'check_id': AllUsers.check_id,
            'register_id': AllUsers.register_id,
            'check_info': AllUsers.check_info,
            'insert_info': AllUsers.insert_info,
            'delete_info' : AllUsers.delete_info,
        }
        wrapper_bd.__name__ = func.__name__
        wrapper_bd.__doc__ = func.__doc__
        res = func(*args, **kwargs)
        func_name = func.__name__
        if res is None:
            try:
                res_func = func_wrapper.get(func_name, f'None function for {func_name}')
                res =  res_func(*args, **kwargs)
                return res
            except Exception as ex:
                print(f'Error {ex} in wrapper for: {func_name}')

        else:
            return res


    return wrapper_bd


@decor_bd
def check_id(id: int):
    return None


@decor_bd
def register_id(id: int):
    return None


@decor_bd
def check_info(id: int):
    return None


@decor_bd
def insert_info(user_tg_id : int, adult: bool = None, gender: bool = None, name: str = None):
    return None

@decor_bd
def delete_info(id : int):
    return None