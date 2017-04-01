import os
from flask import Flask,request,render_template,flash
from flaskext.mysql import MySQL
from flask_basicauth import BasicAuth
import pandas as pd

app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] =os.environ.get("MYSQL_HOST")
app.config["MYSQL_DATABASE_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_DATABASE_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DATABASE_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_DATABASE_PORT"] = 3306
mysql=MySQL(app)

app.config['BASIC_AUTH_USERNAME'] = os.environ.get("MYSQL_USER")
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get("PASSWORD_AUTH")
basic_auth = BasicAuth(app)

@app.route('/')
def start():
	return render_template('index.html')

@app.route('/soccent')
def soccent():
	conn=mysql.connect()
	# Querying Database
	query="""\
	    SELECT * from enterprise;
	    """
	df=pd.read_sql(query,conn)

	# Creating Table HTML
	data = ''
	for index, row in df.iterrows():
		temp = '<tr><td>'+row['Name']+'</td><td>'+row['Domain']+'</td><td>'+row['Email']+'</td><td>'+row['Phone']+'</td>'+'</td><td>'+row['Product']+'</td><td><a href="'+row['pdf']+'" target="_blank">PDF</a></td></tr>'
		data = data + temp
	conn.close()
	return render_template('soccent.html', data=data)

@app.route('/alumni')
def alumni():
	conn=mysql.connect()
	# Querying Database
	query2="""\
	    SELECT * from alumni;
	    """
	df2=pd.read_sql(query2,conn)

	# Creating Table HTML
	data2 = ''
	for index, row in df2.iterrows():
		temp = '<tr><td>'+row['first_name']+'</td><td>'+row['last_name']+'</td><td>'+row['email']+'</td><td>'+row['chapter_aff']+'</td><td>'+row['curr_city']+'</td><td>'+row['occupation']+'</td><td>'+row['institute_name']+'</td></tr>'
		data2 = data2 + temp
	conn.close()
	return render_template('alumni.html', data=data2)

if __name__=="__main__":
	app.run(debug=False)
