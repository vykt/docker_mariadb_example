# api.py

# imports
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import mysql.connector as mariadb

'''
Interact with the database using this API

'''


# setup & constants
app = Flask(__name__)
api = Api(app)

mariadb_conn = mariadb.connect(user="root",
                               password="example_password",
                               database="example_db",
                               host="172.18.0.2",
                               port=3306)
mariadb_cursor = mariadb_conn.cursor()

database_host = "mariadb_container"


# define API
class MariaDB_RESTAPI(Resource):
    # add new song, 0
    def post(self):
        content = request.json
    # delete existing song, 1
    def delete(self):
        pass
    # get songs, 2
    def get(self):
        pass

api.add_resource(MariaDB_RESTAPI, '/')


# TODO DEBUG, REMOVE

mariadb_cursor.execute("SELECT * FROM resources")
result = mariadb_cursor.fetchall() #or fetchone()
print(result)

# TODO END DEBUG, REMOVE


# Start API
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000, debug=True)
