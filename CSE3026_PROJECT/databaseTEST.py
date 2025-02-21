from flask import Flask, render_template
import pymysql

app = Flask(__name__)

# Database connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',  # Default XAMPP MySQL user
        password='',  # Default is empty
        database='university',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')  # Root route to display the table
def home():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM cse_classes;")
        classes = cursor.fetchall()
    connection.close()
    return render_template('index.html', classes=classes)

if __name__ == '__main__':
    app.run(debug=True)
