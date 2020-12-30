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



if __name__ == "__main__":
    with con.cursor() as cur:
        cur.execute("SELECT * FROM accounts")
        a = cur.fetchall()
        print(a)
