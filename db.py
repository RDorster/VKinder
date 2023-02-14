import psycopg2
from config import *

connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
connection.autocommit = True


# ===========================================================================
# ========================= оптимизация =====================================

def sql(sqltext):
    with connection.cursor() as cursor:
        cursor.execute(
            sqltext
        )


# ===========================================================================
# ========================= создание таблиц в базу ==========================
def create_table_users():  # таблица пользователей
    sql(
        """CREATE TABLE IF NOT EXISTS users
            (
                id serial,
                vk_id varchar(20) NOT NULL PRIMARY KEY,
                fname varchar(30) NOT NULL,
                lname varchar(30) NOT NULL,
                vk_link varchar(75)
            );"""
    )
    if debug == True:
        print("(SQL) Таблица USERS = ok")


def create_table_ch_users():  # таблица прочеканых пользователей
    sql(
        """CREATE TABLE IF NOT EXISTS ch_users
            (
            id serial,
            vk_id varchar(20) PRIMARY KEY
            );"""
    )
    if debug == True:
        print("(SQL) Таблица ch_users = ok")


# ===========================================================================
# ========================= создание таблицы в базу =========================
def creating_database():
    create_table_users()
    create_table_ch_users()


# ===========================================================================
# ========================= заполнение таблицы users ========================
def insert_data_users(vk_id, fname, lname, vk_link):
    sql(
        f"""INSERT INTO users (vk_id, fname, lname, vk_link) 
        VALUES ('{vk_id}', '{fname}', '{lname}', '{vk_link}');"""
    )
    if debug == True:
        print(f"(SQL) запись user: {fname}")


# ===========================================================================
# =================== заполнение таблицы про-веренных\смотренных users ======
def insert_data_ch_users(vk_id, offset):
    sql(
        f"""INSERT INTO ch_users (vk_id) 
            VALUES ('{vk_id}')
            OFFSET '{offset}';"""
    )
    if debug == True:
        print(f"(SQL) запись check userid: {vk_id}")


# ===========================================================================
# =================== выборка из не проверенных пользователей ===============

def select(offset):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT 
                users.vk_id,
                users.fname,
                users.lname,
                users.vk_link,
                ch_users.vk_id
                    FROM users 
                    LEFT JOIN ch_users
                    ON users.vk_id = ch_users.vk_id
                    WHERE ch_users.vk_id IS NULL
                    OFFSET '{offset}';"""
        )
        return cursor.fetchone()
