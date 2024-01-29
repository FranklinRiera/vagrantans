from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

db_config = {
    'database': 'DB',
    'user': 'root',
    'password': 'root',
    'port': '5432',
    'host': '192.168.56.11'
}

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

#post all users
@app.route("/insert", methods=["POST"])
def insert_data():
    try:
        con = psycopg2.connect(**db_config)
        cursor = con.cursor()

        data = request.get_json()
        name = data.get('name')
        lastname = data.get('lastname')

       # cursor.execute("INSERT INTO form (name, lastname) VALUES (%s, %s)", (name,lastname))
        postgres_insert_query = 'INSERT INTO form (name, lastname) VALUES (%s, %s);'
        record_to_insert = (name, lastname)
        cursor.execute(postgres_insert_query, record_to_insert)

        con.commit()

        return jsonify({'mensaje': 'Datos insertados correctamente'}), 201
       

    except Exception as err:
        print ("Error:", str(err))
        print ("Error:", type(err).__name__)
        print ("Error:", err.with_traceback)
        return jsonify({"message": "error insert in form"}, 500)

    finally:
        if con:
           con.close()

#get all users
@app.route("/get", methods=["GET"])
def get_data():
    try:
        con = psycopg2.connect(**db_config)
        cursor = con.cursor()

        cursor.execute("SELECT * FROM form;")
        resultados = cursor.fetchall()

        data_json = [{"name": row[1], "lastename": row[2]} for row in resultados]
        #datos_json = [{'nombre': row[0], 'edad': row[1]} for row in resultados]
        return jsonify({"data": data_json})

    except Exception as e:
        print ("Error:", str(err))
        print ("Error:", type(err).__name__)
        print ("Error:", err.with_traceback)
        return jsonify({'message': "error select in form"}, 500)

    finally:
        if con:
           con.close()


if __name__ == "__main__":
    app.run(debug=true, port=5000, host='0.0.0.0')

