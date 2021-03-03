from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flaskContacts'

mysql = MySQL(app)

app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data) 

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)",(fullname,phone,email))
        mysql.connection.commit()
        flash('Contact Added Successfully')
        return redirect(url_for('Index'))


@app.route('/edit/<id>', methods = ['POST','GET'])
def get_contact(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f'SELECT * FROM contacts WHERE id = {id}')
        data = cur.fetchall()
        cur.close()
        return render_template('edit.html', contact = data[0])
    except:
        flash("The contact doesn't exist in selected database")
        return redirect(url_for('Index'))


@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute(""" 
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))
    
@app.route('/delete')
@app.route('/delete/<id>')
def delete_contact(id=-1):
    if id != -1:
        cur = mysql.connection.cursor()
        cur.execute(f'DELETE FROM contacts WHERE id = {id}')
        mysql.connection.commit()
        flash('Contact Removed Successfully')
    else:
        flash("You can't get into the link")
    return redirect(url_for('Index'))

if __name__ == '__main__':

    app.run(port = 3000, debug = True)


