import os
from flask import Flask,request,render_template,flash
from flaskext.mysql import MySQL
from flask_basicauth import BasicAuth
import pandas as pd

app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = os.environ.get("HOST")
app.config["MYSQL_DATABASE_USER"] = os.environ.get("USER")
app.config["MYSQL_DATABASE_PASSWORD"] = os.environ.get("PASSWORD")
app.config["MYSQL_DATABASE_DB"] = os.environ.get("DB")
app.config["MYSQL_DATABASE_PORT"] = 3306
mysql=MySQL(app)
conn=mysql.connect()
cur= conn.cursor()

app.config['BASIC_AUTH_USERNAME'] = os.environ.get("USER")
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get("PASSWORD_AUTH")
basic_auth = BasicAuth(app)

@app.route('/')
@basic_auth.required
def start():

	# Querying Database
	query="""\
	    SELECT * from table1;
	    """
	df=pd.read_sql(query,conn)

	# Creating Table HTML
	data = ''
	for index, row in df.iterrows():
		temp = '<tr><td>'+row['Name']+'</td><td>'+row['Phone']+'</td><td>'+row['Sector']+'</td><td>'+row['Chapter']+'</td><td>'+row['Village']+'</td><td>'+row['Name']+'</td><td>'+row['Email']+'</td></tr>'
		data = data + temp
	
	return render_template('index.html', data=data)

if __name__=="__main__":
	app.run(debug=False,port=5000)

