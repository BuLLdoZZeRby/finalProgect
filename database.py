import psycopg2
import temp
id = []
pr = []
conn = psycopg2.connect(host=temp.dbhost, dbname=temp.dbdbname, user=temp.dbuser, password=temp.dbpassword)

cur = conn.cursor()
cur2 = conn.cursor()
cur3 = conn.cursor()
cur4 = conn.cursor()
cur5 = conn.cursor()
cur6 = conn.cursor()
cur7 = conn.cursor()



def set_data(id_flat, rum, discription, price, phone, url, update=True, change=False):
    """запись новой строки в БД """
    cur.execute(f"INSERT INTO flat (id_flat, rum, discription, price, phone, url, update, change) "
            f"VALUES ('{id_flat}',{rum}, '{discription}', '{price}', '{phone}', '{url}', {update}, {change});")



def select_id():
    """Возрат всех id_flat"""
    cur.execute("SELECT id_flat FROM flat;")
    for i in cur:
        id.append(i[0])
    return id


def update_price(id_flat, price):
    """изменения цены"""
    cur.execute(f"UPDATE flat SET price = '{price}' WHERE id_flat = '{id_flat}';")


def update_flag(id_flat, flag, valeu):
    """Изменение флагов"""
    cur.execute(f"UPDATE flat SET {flag} = {valeu} WHERE id_flat = '{id_flat}';")


def select_price(id_flat):
    """Возвращает цену по id_flat"""
    cur.execute(f"SELECT price FROM flat WHERE id_flat = '{id_flat}';")
    return cur.fetchone()



def update_false():
    """Изменениe update"""
    cur.execute("UPDATE flat SET update = False;")


def change_false():
    """Изменениe update"""
    cur.execute("UPDATE flat SET change = False;")


def delete_update_false():
    """Удаляем из базы исчезнувшие квартиры. Сразу из таблицы users_to_flat, потом из flat"""
    flats = []
    try:
        cur6.execute(f"SELECT id_flat FROM flat WHERE update = False;")
        delflats = cur.fetchall()
        for flat in delflats:
            flats.append(flat[0])
        for flat in flats:
            cur6.execute(f"DELETE FROM flat WHERE id_flat = '{flat}';")

        cur6.execute("DELETE FROM users_to_flat WHERE update = False;")
    except:
        print('Нет объектов для удаления')







