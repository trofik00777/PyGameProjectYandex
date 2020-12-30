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
    con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
    with con.cursor() as cur:
        cur.execute(f"INSERT INTO accounts(login, password) VALUES ('{login}', '{hash_password}')")
    con.commit()


def check_login_password(login, password):
    hash_password = md5(password)
    con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
    with con.cursor() as cur:
        cur.execute(f"SELECT * FROM accounts WHERE login='{login}' AND password='{hash_password}'")
        res = cur.fetchone()
    if res:
        return res
    return False


if __name__ == "__main__":
    with con.cursor() as cur:
        cur.execute("SELECT * FROM accounts")
        a = cur.fetchall()
        print(a)
