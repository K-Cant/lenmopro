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

    return render_template('form.html', contacts=datos, data_to_edit=None)

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

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    connection = getDBConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM datos WHERE id=%s", (id))
        connection.commit()
    except pymysql.MySQLError as e: 
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('home'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    nombre = request.form['nombre']
    genero = request.form['genero']
    
    connection = getDBConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE datos SET nombre = %s, genero = %s WHERE id=%s ", (nombre, genero, id))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods =['GET'])
def edit(id):
    connection = getDBConnection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT id, nombre, genero FROM datos WHERE id=%s",(id))
        contact = cursor.fetchone()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        contact = None
    finally:
        cursor.close()
        connection.close()
    return render_template('edit_data.html',contacts=[], data_to_edit=contact)

if __name__ == "__main__":
    app.run(debug=True)