import os
import psycopg2
from flask import request
import json
from datetime import datetime

class Database:
    def connect(self):
        print ("db_name:", os.environ.get('DB_NAME'))
        return psycopg2.connect(
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
        )
    
    def readall(self)
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("SELECT * FROM form")
            return cursor.fetchall()
        except Exception as err:
            print ("Error:", str(err))
            print ("Error:", type(err).__name__)
            print ("Error:", err.with_traceback)
            return()
        finally:
            con.close()

    def insert(self, request):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if request.headers.getlist("X-Forward-For"):
                ipaddress=request.headers.getlist("X-Forward-For")[0]
            else:
                 ipaddress=request.remote_addr

            requestcontent=request.json

            cursor.execute("INSERT INTO form(tstamp, name, lastname) VALUES(%s, %s, %s)",
                           (datetime.now(), ipaddress, json.dumps(requestcontent)))
            con.commit()

            return True
        except Exception as err:
            print ("Error:", str(err))
            print ("Error:", type(err).__name__)
            print ("Error:", err.with_traceback)
            con.rollback()
            
            return False

