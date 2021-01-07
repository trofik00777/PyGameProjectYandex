import pymysql
import hashlib
import ftplib
import os
import shutil


HOST = "f0478423.xsph.ru"
USER = "f0478423_pygame_wolf_and_eggs"
PASSWORD = "wolfandeggs"
DATABASE = "f0478423_pygame_wolf_and_eggs"

HOST_FTP = "141.8.193.236"
USER_FTP = "f0478423"

PATH_PHOTOS = "C:\\ProgramData\\UCSG"
SEPARATOR = "\\"


con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)


def md5(text):
    return hashlib.md5(text.encode()).hexdigest()


def registration(login, password):
    hash_password = md5(password)
    try:
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        with con.cursor() as cur:
            cur.execute(f"INSERT INTO accounts(login, password) "
                        f"VALUES ('{login}', '{hash_password}')")
        con.commit()
    except pymysql.err.IntegrityError:
        return f"Логин '{login}' уже существует"
    except Exception as e:
        print(e)
        return "Ошибка, повторите попытку позже"


def check_login_password(login, password):
    hash_password = md5(password)
    try:
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        with con.cursor() as cur:
            cur.execute(f"SELECT * "
                        f"FROM accounts "
                        f"WHERE login='{login}' AND password='{hash_password}'")
            res = cur.fetchone()
        if res:
            return res
        return False
    except Exception as e:
        print(e)
        return "Ошибка, повторите попытку позже"


def get_top10():
    try:
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        with con.cursor() as cur:
            cur.execute("SELECT accounts.login, rating.settings, rating.score "
                        "FROM accounts, rating "
                        "WHERE accounts.id=rating.id_player "
                        "ORDER BY rating.score "
                        "LIMIT 10")
            res = cur.fetchall()
            rating = []
            for rank, player in enumerate(res):
                settings = player[1].split(";")
                rating.append((rank + 1, player[0],
                               f"скорость яиц:{settings[0]}\n"
                               f"скорость волка:{settings[1]}\n"
                               f"скорость появления яиц:{settings[2]}",
                               player[2]))
        return rating
    except Exception as e:
        print(e)
        return "Ошибка, повторите попытку позже"


if __name__ == "__main__":
    print(get_top10())
