# api.py

# imports
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from copy import deepcopy
from datetime import date
import mysql.connector as mariadb
import sys

'''
Interact with the database using this API

'''

# setup & constants
database_host = "db"
send_names = ["title", "artist", "resource"]
send_names_log = ["access", "action", "resource"]

app = Flask(__name__)
api = Api(app)

mariadb_conn = mariadb.connect(user="root",
                               password="example_password",
                               database="example_db",
                               host=database_host,
                               port=3306)
mariadb_cursor = mariadb_conn.cursor()
mariadb_cursor.execute("SET FOREIGN_KEY_CHECKS=0")
mariadb_conn.commit()


# define API functions

# sys.exit() wrapper
def exit_critical():
    sys.exit("Critical error has occured, exiting...")


# convert sql.connector output to json for get
def return_to_dict(content):
    ret_dict = {}
    ret_dict_construct = {}

    #json names
    get_fields = ("id", "title", "artist", "resource")
    
    # convert content to dict, which gets turned to json
    for i in range(len(content)): #for each row
        for j in range(1, len(content[i])): #for each column
            ret_dict_construct[get_fields[j]] = content[i][j]
        ret_dict[content[i][0]] = deepcopy(ret_dict_construct)
        ret_dict_construct = {}
    return ret_dict


# log action
def log_action(action, del_id=0):
    send_arr = []
    proc_date = date.today()
    send_arr.append(proc_date.strftime("%Y-%m-%d"))
    send_arr.append(action)

    # get foreign key for log
    if action == 0:
        mariadb_cursor.execute("SELECT LAST_INSERT_ID()")
        send_arr.append(int(mariadb_cursor.fetchall()[0][0]))
    elif action == 1:
        send_arr.append(int(del_id))

    # post & delete statement
    if action != 2:
        statement = "INSERT INTO logs ("\
                    + send_names_log[0] + ", "\
                    + send_names_log[1] + ", "\
                    + send_names_log[2]\
                    + ") VALUES (%s, %s, %s)"
    # get statement
    elif action == 2: 
        statement = "INSERT INTO logs ("\
                    + send_names_log[0] + ", "\
                    + send_names_log[1]\
                    + ") VALUES (%s, %s)"

    # perform log
    mariadb_cursor.execute(statement, send_arr)
    mariadb_conn.commit()

    # no return since it shouldn't error. If it does, it
    # should crash.


# API post
def on_post():
    send_arr = []
    send_lens = [64, 64, 256]

    try:
        for i in range(len(send_names)):
            send_arr.append(request.headers.get(send_names[i]))
            if len(send_arr[i]) <= send_lens[i] and len(send_arr[i]) > 0:
                continue
            else:
                return {"status": 500}
    except:
        return {"status": 500}

    try:
        statement = "INSERT INTO resources (" \
                    + send_names[0] + ", "\
                    + send_names[1] + ", "\
                    + send_names[2]\
                    + ") VALUES (%s, %s, %s)"
    
        mariadb_cursor.execute(statement, send_arr)
        mariadb_conn.commit()
        log_action(0)
        return {"status": 201}
                
    except:
        print("Hit except")
        return {"status": 500}
     

# API delete
def on_delete():
    del_id = int(request.headers.get('id'))
    
    # check if entry exists
    check_statement = "SELECT * FROM resources WHERE id="+str(del_id)
    mariadb_cursor.execute(check_statement)
    ret = mariadb_cursor.fetchall()
   
    if not ret:
        return {"status": 500}

    # delete entry
    log_action(1, del_id=del_id)
    statement = "DELETE FROM resources WHERE id="+str(del_id)
    mariadb_cursor.execute(statement)
    mariadb_conn.commit()
    return {"status": 204}


# API get
def on_get():
    statement = "SELECT * FROM resources"
    mariadb_cursor.execute(statement)
    ret = mariadb_cursor.fetchall()
    ret = return_to_dict(ret)
    return ret

# define API
class MariaDB_RESTAPI(Resource):
    # add new song, 0
    def post(self):
        ret = on_post()
        return ret
    # delete existing song, 1
    def delete(self):
        ret = on_delete()
        return ret
    # get songs, 2
    def get(self):
        ret = on_get()
        return ret


# start API
api.add_resource(MariaDB_RESTAPI, '/')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
