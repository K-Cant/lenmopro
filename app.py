from flask import Flask, render_template, request, redirect, url_for
import pymysql
import pymysql.cursors
from dbconfig import getDBConnection


app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    connection = getDBConnection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT id, nombre, genero FROM datos")
        datos = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        datos = []
    finally:
        cursor.close()
        connection.close()

    return render_template('form.html', contacts=datos)

@app.route('/', methods=['POST'])
def submit():
    nombre = request.form['nombre']
    genero = request.form['genero']

    connection = getDBConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO datos (nombre, genero) VALUES (%s,%s)", (nombre, genero))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)