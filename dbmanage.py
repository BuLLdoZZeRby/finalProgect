import database


def data_select(room):
    """выбираем из таблицы 1, 2-ух или 3-х комнатные квартиры"""
    database.cur.execute(f"SELECT * FROM flat WHERE rum = '{room}';")


def get_data():
    """ выводим из выбранной таблицы квартиры по одной"""
    data = database.cur.fetchone()
    return data


def set_user(user_id, username):
    """Добавляем нового юзера в таблицу """
    database.cur.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}';")
    data = database.cur.fetchone()
    if data is None:
        database.cur.execute(f"INSERT INTO users (user_id, username) VALUES ('{user_id}', '{username}');")
        database.conn.commit()


def save_flat(id_flat, user_id):
    """Заполняем таблице users_to_flat"""
    database.cur2.execute(f"INSERT INTO users_to_flat (id_flat, user_id) VALUES ('{id_flat}','{user_id}');")
    database.conn.commit()


def select_save_flat(user_id):
    """выбираем из таблицы users_to_flat все квартиры, сохраненные юзером"""
    flat_user = []
    database.cur2.execute(f"SELECT id_flat  FROM users_to_flat WHERE user_id = '{user_id}' ;")
    flats = database.cur2.fetchall()
    for flat in flats:
        flat_user.append(flat[0])
    return flat_user

def get_save_flats_for_user(user_id):
    """Формируем сводную таблицу"""
    database.cur2.execute(f"SELECT "
                          f"flat.discription, flat.price, flat.phone, flat.url, flat.id_flat"
                          f" FROM users_to_flat"
                          f" JOIN flat ON users_to_flat.id_flat = flat.id_flat"
                          f" WHERE user_id = '{user_id}' ;")

    return database.cur2.fetchone()


def get_next_save_flats():
    return database.cur2.fetchone()


def delete_flat(user_id, id_flat):
    """Удаляем квартиры из сохраненных"""
    database.cur3.execute(f"DELETE FROM users_to_flat WHERE user_id = '{user_id}' and id_flat = '{id_flat}' ;")
    database.conn.commit()


def count_flats(room):
    """Подсчет квартир в таблице"""
    database.cur4.execute(f"SELECT COUNT(*)  FROM flat WHERE rum = {room} ;")
    count = database.cur4.fetchone()
    return count[0]


def count_save_flats(user_id):
    """Подсчет сохраненных квартир в таблице"""
    database.cur5.execute(f"SELECT COUNT(*)  FROM users_to_flat WHERE user_id = '{user_id}' ;")
    count = database.cur5.fetchone()
    return count[0]


def check_agency(phone):
    database.cur7.execute(f"SELECT COUNT(*)  FROM flat WHERE phone = '{phone}' ;")
    count_phone = database.cur7.fetchone()
    if count_phone[0] > 1:
        return f" Возможно, объявление от агенства!!! В базе {count_phone[0]} объявлений с этим номером телефона"
    else:
        return ' '



