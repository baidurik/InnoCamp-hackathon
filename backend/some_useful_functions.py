#=======================================================================================#
#Скрипт, в котором определено несколько полезных функций, нужных для сервера
#=======================================================================================#

import hashlib                                      #Библиотека для хеширования
import random, string                               #Библиотеки для генерации случайной строки

global_salt = 'DSw25P'

def randomstring(length):                           #Возвращает случайную строку длины length из латинских букв и цифр
    alpha = string.ascii_letters + string.digits
    return ''.join(random.choice(alpha) for i in range(length))

def take_md5(string, salt):                                 #Объединяет строки string, salt и global_salt
    temp = string + salt + global_salt                      #Возвращает md5 от склейки строк
    return hashlib.md5(temp.encode('utf-8')).hexdigest()    #Функция необходима для хеширования паролей
