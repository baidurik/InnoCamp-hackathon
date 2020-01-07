#=======================================================================================#
#Код, в котором определены реакции на запросы и запускается сервер
#=======================================================================================#

from flask import Flask, request, jsonify   #Модуль Flask используется для создания сервера, request для получения параметров запроса, jsonify для возвращения json
from db_config import *                 #Файл, содержащий функции для работы с ДБ

app = Flask(__name__)

@app.route('/catalog', methods=['GET'])             #При запросе на каталог возвращает json со всеми тортами, которые есть
def give_catalog_data():
    data = db.sql_get('cakes', '*')
    jsons = [{'name': i.name,
              'price': i.price,
              'baker': i.baker,
              'photos': i.photos,
              'desc': i.description} for i in Cake.select()]

    return jsonify({'List': jsons})

@app.route('/user/<nick>', methods=['GET'])         #При запросе на профиль пользователя возвращает json с его данными
def get_user_info(nick):
    usr = User.get_or_none(User.nickname == nick)
    if usr == None:
        return jsonify({'Error': 'No such user'})
    return jsonify({'nick': usr.nickname, 'fname': usr.firstname, 'lname': usr.lastname, 'bio': usr.bio, 'conn': usr.how_to_connect})

@app.route('/sign_in', methods=['POST'])            #При запросе на страницу входа берет данные из запроса
def sign_in_():                                     #Возвращает результат функции db.sign_in в виде json
    data = request.json
    print(data)
    result = sign_in(data['nick'], data['pass'])
    return jsonify({'resp': result})

@app.route('/sign_up', methods=['POST'])            #При запросе на страницу регистрации берет данные из запроса
def sign_up_():                                     #Возвращает результат функции db.sign_in в виде json
    data = request.json
    result = sign_up(data['nick'], data['pass'], data['fname'], data['lname'], data['bio'], data['conn'])
    return jsonify({'resp': result})

@app.route('/cakes/<cake_id>', methods=['GET'])     #При запросе на страницу определенного торта возвращает json с его параметрами
def get_cake_info(cake_id):
    data = Cake.get_by_id(cake_id)
    return jsonify({
        'name': data.name,
        'price': data.price,
        'baker': data.baker_id,
        'desc': data.description
    })

@app.route('/cakes', methods=['POST'])              #При POST-запросе на страницу тортов создает в БД новую строку
def upload_new_cake():                              #Её параметры берутся из запроса
    data = request.json
    Cake.create(name=data['name'],
                       price=data['price'],
                       baker_id=data['baker'],
                       photos=data['photos'],
                       description=data['desc'])
    return "OK"

app.run('127.0.0.1', 6000)                          #Запускает приложение
