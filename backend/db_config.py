
#=======================================================================================#
#Файл, в котором определены инструменты для работы с базой данных(далее - БД)
#=======================================================================================#

import some_useful_functions as funs    # Некоторые функции, необходимые для работы
from peewee import *                    # Модуль для высокоуровневой работы с SQL при помощи классов

db = PostgresqlDatabase('postgres', user='postgres', password='ghjcnjz[brrf', host='127.0.0.1', port=5432)  # Соединяется с базой данных

#=======================================================================================#
#Создание классов peewee для работы с таблицами в БД
#Поля класса - столбцы таблицы
#Класс Meta - метаданные
#В данных классах в метаданных определяется база данных, с которой работает класс

class User(Model):
    nickname = TextField()
    hashed_password = TextField()
    firstname = TextField()
    lastname = TextField()
    salt = TextField()
    bio = TextField(null=True)
    how_to_connect = TextField(null=True)
    products = ValuesList(TextField(null=True))

    class Meta:
        database = db

class Cake(Model):
    name = TextField()
    price = FloatField()
    baker = ForeignKeyField(User, related_name='products')
    photos = ValuesList(TextField())
    description = TextField()

    class Meta:
        database = db

class Image(Model):
    data = TextField()
    relation = ForeignKeyField(Cake, related_name='photos')

    class Meta:
        database = db
#=======================================================================================#

def sign_up(nick, password, firstname, lastname, bio, how_to_connect):  #Функция регистрации

    usr = User.get_or_none(User.nickname == nick) #Ищет пользователя по нику в ДБ
    if usr != None:                               #Если такой пользователь есть, выходит из функции и возвращает 0
        return 0

    salt = funs.randomstring(6)                         #Генерирует "соль" - подстроку, которая используется в хешировании пароля
    password = funs.take_md5(password, salt)            #Берет md5 от пароля и "соли"

    User.create(nickname=nick,                          #Создает объект класса User и строку в БД
                hashed_password=password,
                firstname=firstname,
                lastname=lastname,
                salt=salt,
                bio=bio,
                how_to_connect=how_to_connect
                )

def sign_in(nick, password):   #Функция входа

    usr = User.get_or_none(User.nickname == nick)       #Проверяет, есть ли такой пользователь
    if usr == None:                                     #Если есть, выходит из функции и возвращает 0
        return 0

    salt = usr.salt
    expected_password = funs.take_md5(password, salt)   #Берет индивидуальную "соль" пользователя, хранящуюся в ДБ и хеширует с её помощью введенный пароль

    if expected_password != usr.hashed_password:                 #Сравнивает полученный хеш с хешем, хранящимся в ДБ
        return -1                                   #Если они не одинаковы, возвращает ошибку
    return 1
