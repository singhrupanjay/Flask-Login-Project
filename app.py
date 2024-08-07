from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re #re stands for “regular expressions.” It’s a built-in Python module that provides powerful tools for working with regular expressions.

app = Flask(__name__)

app.secret_key = 'secretKey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123Sql!@#'
app.config['MYSQL_DB'] = '1Flaskdb'

mysql = MySQL(app)
    # Let’s break it down:
    # MySQL is a class provided by the mysql-connector-python package.
    # app refers to your Flask application instance (created using Flask(__name__)).
    # By passing app to MySQL(app), you’re initializing an instance of the MySQL class that is associated with your Flask app.
    # This instance (mysql) will allow you to interact with the MySQL database throughout your application.

#------------------------------LOGIN-------------------------------------#
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])

def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # A cursor allows you to execute SQL queries, fetch data, and manage transactions within your Python code.

        # mysql.connection refers to the database connection object. This object represents the connection to your MySQL database.

        # .cursor() is a method provided by the connection object. It creates a new cursor.

        # MySQLdb.cursors.DictCursor specifies the type of cursor to create. In this case, it’s a dictionary cursor.

        #A dictionary cursor (specifically MySQLdb.cursors.DictCursor) returns query results as dictionaries.
        # Instead of accessing data by index (like a regular cursor), you can access columns by their names.
        # For example, if you fetch a row using a dictionary cursor, you can access the values like this: row['column_name'].


        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))

        account = cursor.fetchone() #to fetch the first matching account

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'logged in Successfully'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect Credentials'

    return render_template('login.html', msg=msg)

#------------------------------LOGOUT-------------------------------------#
@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

#------------------------------REGISTER-------------------------------------#

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()

        if account:
            msg = "Account already exists"
        # elif not re.match(r'[^@]+[^@]+\.[^@]',email):
        #     msg = 'Invalid email address !'
        # The expression within the re.match() function is a regular expression (regex).
        # Regular expressions are powerful tools for pattern matching and manipulation of strings.

        # Let’s break down the regex pattern: r'[^@]+[^@]+\.[^@]'
        # [^@]+: Matches one or more characters that are not the “@” symbol.
        # [^@]+\.: Matches one or more characters that are not “@” followed by a literal dot (.).
        # [^@]: Matches a single character that is not “@”.
        # The entire pattern ensures that the email contains at least one “@” symbol and one dot (for the domain).
        
        # elif not re.match(r'[A-Za-z0-9]+', username):
        #     msg = 'Username must only conatin characters and numbers'
        elif not username or not password or not email:
            msg = 'Please fill out form'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email,))
            mysql.connection.commit() # to commit and save changes
            msg = "registration Success"
    elif request.method == 'POST':
        msg = 'Fill out the form!'
    return render_template('register.html', msg=msg)





        


