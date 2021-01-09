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

PATH_PHOTOS = "data"
SEPARATOR = "\\"


con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
if os.name != "nt":
    PATH_PHOTOS = "data"
    SEPARATOR = "/"


def upload_images_menu_to_pc():
    def upload(ftp, name):
        with open(f"{PATH_PHOTOS}/{name}", "wb") as f:
            ftp.retrbinary('RETR ' + name, f.write)

    ftp = ftplib.FTP(host=HOST_FTP, user=USER_FTP, passwd="trofikpsswrd")
    ftp.cwd("wolf_and_eggs")
    list_dir = ftp.nlst()[2:]
    pos_skins = list_dir.index("skins")
    del list_dir[pos_skins]
    print(list_dir)

    if os.path.exists(PATH_PHOTOS):
        pass
    else:
        os.mkdir(PATH_PHOTOS)

    for file in list_dir:
        if os.path.exists(f"{PATH_PHOTOS}/{file}"):
            print(f"{file} is exist")
        else:
            upload(ftp, file)

    # if os.path.exists(PATH_PHOTOS):
    #     if os.path.exists(f"{PATH_PHOTOS}{SEPARATOR}{path_in_filemanager}"):
    #         print("exist")
    #     else:
    #         upload()
    # else:
    #     os.mkdir(PATH_PHOTOS)
    #
    #     upload()


def upload_skins():
    def upload(ftp, name, dir):
        with open(f"{PATH_PHOTOS}/skins/{dir}/{name}", "wb") as f:
            ftp.retrbinary('RETR ' + name, f.write)

    ftp = ftplib.FTP(host=HOST_FTP, user=USER_FTP, passwd="trofikpsswrd")
    ftp.cwd("wolf_and_eggs/skins")
    list_dir = ftp.nlst()[2:]
    print(list_dir)

    if os.path.exists(f"{PATH_PHOTOS}/skins"):
        pass
    else:
        os.mkdir(f"{PATH_PHOTOS}/skins")

    for directory in list_dir:
        if os.path.exists(f"{PATH_PHOTOS}/skins/{directory}"):
            pass
        else:
            os.mkdir(f"{PATH_PHOTOS}/skins/{directory}")

        ftp.cwd(f"{directory}")
        list_skins = ftp.nlst()[2:]
        print(list_skins)

        for file in list_skins:
            if os.path.exists(f"{PATH_PHOTOS}/skins/{directory}/{file}"):
                print(f"{file} is exist")
            else:
                upload(ftp, file, directory)

        ftp.cwd("..")


def download_images_icons_to_ftp(path_os):
    ftp = ftplib.FTP(host=HOST_FTP, user=USER_FTP, passwd="trofikpsswrd")
    ftp.cwd("images")
    with open(f"{path_os}", "rb") as f:
        ftp.storbinary('STOR ' + path_os.split(f"{SEPARATOR}")[-1], f)


def del_files_from_pc():
    if os.path.exists(PATH_PHOTOS):
        shutil.rmtree(PATH_PHOTOS)


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


def get_top10(level):
    try:
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        with con.cursor() as cur:
            cur.execute(f"SELECT accounts.login, rating.score "
                        f"FROM accounts, rating "
                        f"WHERE accounts.id=rating.id_player "
                        f"AND rating.level='{level}' "
                        f"ORDER BY rating.score DESC "
                        f"LIMIT 10")
            res = cur.fetchall()
            rating = []
            for rank, player in enumerate(res):
                rating.append((rank + 1, player[0], player[1]))
            # rating = []
            # for rank, player in enumerate(res):
            #     settings = player[1].split(";")
            #     rating.append((rank + 1, player[0],
            #                    f"скорость яиц:{settings[0]}\n"
            #                    f"скорость волка:{settings[1]}\n"
            #                    f"скорость появления яиц:{settings[2]}",
            #                    player[2]))
        return rating
        # return res
    except Exception as e:
        print(e)
        return "Ошибка, повторите попытку позже"


def get_rank_player(player_login: str, level):
    try:
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        with con.cursor() as cur:
            cur.execute(f"SELECT accounts.login, rating.score "
                        f"FROM accounts, rating "
                        f"WHERE accounts.id=rating.id_player "
                        f"AND rating.level='{level}' "
                        f"ORDER BY rating.score DESC")
            res = cur.fetchall()
            print(res)
        ranks = None
        # for rank, player in enumerate(res):
        #     if player[0] == player_login:
        #         settings = player[1].split(";")
        #
        #         ranks.append((rank + 1, player[0],
        #                        f"скорость яиц:{settings[0]}\n"
        #                        f"скорость волка:{settings[1]}\n"
        #                        f"скорость появления яиц:{settings[2]}",
        #                        player[2]))
        for rank, player in enumerate(res):
            if player[0] == player_login:
                ranks = (rank + 1, player[0], player[1])
                break

        if ranks:
            return ranks
        else:
            return "Информация о результатах отсутствует"
    except Exception as e:
        print(e)
        return "Ошибка, повторите попытку позже"


def update_rating(login: str, level, score):
    try:
        con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        with con.cursor() as cur:
            cur.execute(f"SELECT rating.id, rating.score "
                        f"FROM rating, accounts "
                        f"WHERE accounts.login='{login}' "
                        f"AND rating.id_player=accounts.id "
                        f"AND rating.level='{level}'")
            res = cur.fetchone()
            if res:
                id, pred_score = res
                if pred_score < score:
                    cur.execute(f"UPDATE rating "
                                f"SET score='{score}' "
                                f"WHERE id='{id}'")
            else:
                cur.execute(f"SELECT id "
                            f"FROM accounts "
                            f"WHERE login='{login}'")
                id_login = cur.fetchone()[0]
                cur.execute(f"INSERT INTO rating (id_player, score, level) "
                            f"VALUES ('{id_login}', '{score}', '{level}')")
        con.commit()
    except Exception as e:
        print(e)
        return "Ошибка, повторите попытку позже"


def upload():
    ftp = ftplib.FTP(host=HOST_FTP, user=USER_FTP, passwd="trofikpsswrd")
    ftp.cwd("wolf_and_eggs/skins")
    list_dir = ftp.nlst()
    dot1 = list_dir.index(".")
    if dot1 >= 0:
        del list_dir[dot1]
    dot2 = list_dir.index("..")
    if dot2 >= 0:
        del list_dir[dot2]
    print(list_dir)


if __name__ == "__main__":
    # print(get_top10(2))
    # print(get_rank_player("log", 1))
    # update_rating("Gleb", 2, 21)
    upload_skins()
