from distutils.command.config import config
from flask import Flask, redirect, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from json import dump
import mysql.connector
import _mysql_connector
import json
import config

app = Flask(__name__)

@app.route("/")
def login_page():
    return "This is home"

kya_ye_sahi_hai = False;

@app.route("/passwordapi", methods=['GET', 'POST'])
def password_checker():
    if(request.method == 'POST'):
        password = request.args.get('pwdd')
        with open('passwords.json') as saved_data:
            passwords = json.load(saved_data)
        
        if(password == passwords['pwd']):
            kya_ye_sahi_hai = True;
    else:
        return jsonify(kya_ye_sahi_hai)

@app.route('/home')
def home():
    conn=get_database_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("""SELECT room_no, balcony, ac, tv FROM rooms_info WHERE person_id IS NOT NULL""")
    result = {}
    result['available']= cursor.fetchall()
    cursor.execute("""SELECT room_no, balcony, ac, tv FROM rooms_info WHERE person_id IS NULL""")
    result['not_available']= cursor.fetchall()
    cursor.close()
    conn.close()
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response;

@app.route('/viewCurrentCustomers')
def currentCustomers():
    conn=get_database_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("""SELECT * FROM customers WHERE exit_date IS NOT NULL""")
    result = {}
    result['currentCustomers']= cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(result)


@app.route('/viewCurrentEmployees')
def currentEmployees():
    conn=get_database_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("""SELECT * FROM employees WHERE leftdate IS NOT NULL""")
    result = {}
    result['currentEmployees']= cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(result)    

@app.route('/viewAllCustomers')
def allCustomers():
    conn=get_database_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("""SELECT * FROM customers""")
    result = {}
    result['allCustomers']= cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(result)

@app.route('/viewAllEmployees')
def allEmployees():
    conn=get_database_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("""SELECT * FROM employees""")
    result = {}
    result['allEmployees']= cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(result)



def get_database_connection():
    conn = mysql.connector.connect(user=config.DATABASE_USER, password=config.DATABASE_PASSWORD, host=config.DATABASE_HOST, database=config.DATABASE_DB_NAME, use_pure=True)
    return conn

# to change password
# passwords = {'pwd': PASSWORD_HASH}
# with open('passwords.json', 'w') as password_json:
#     json.dump(passwords, password_json)

# # passwords = {'pwd': password}
    # with open('passwords.json', 'w') as password_json:
    #     json.dump(passwords, password_json)