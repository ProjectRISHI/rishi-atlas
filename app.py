import os
from flask import Flask,request,render_template,flash
from flaskext.mysql import MySQL
from flask_basicauth import BasicAuth
import pandas as pd
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get("MYSQL_USER")
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get("PASSWORD_AUTH")
basic_auth = BasicAuth(app)

soccentSheet = '18mY9pAnPhKs5uR0z5f1wjGgH7KqTsL9dUIzcEw3lbOc'
soccentRange = 'Sheet1!A2:F'
alumniSheet = '12mJnLcmnO2cM-9tj0pL1TUGYq__2dRuRyHfQaS1feLY'
alumniRange = 'Sheet1!B3:H'

def get_credentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""

	# If modifying these scopes, delete your previously saved credentials
	# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
	CLIENT_SECRET_FILE = 'client_secret.json'
	APPLICATION_NAME = 'Google Sheets API Python Quickstart'

	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,
								   'sheets.googleapis.com-python-quickstart.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials


@app.route('/')
def start():
	return render_template('index.html')

@app.route('/soccent')
def soccent():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
					'version=v4')
	service = discovery.build('sheets', 'v4', http=http,
							  discoveryServiceUrl=discoveryUrl)
	print('About to read spreadsheet')
	spreadsheetId = soccentSheet
	rangeName = soccentRange
	result = service.spreadsheets().values().get(
		spreadsheetId=spreadsheetId, range=rangeName).execute()
	values = result.get('values', [])
	print('Got values')
	if not values:
		print('No data found.')
		
	# Creating Table HTML
	data2 = ''
	for row in values:
		temp = '<tr><td>'+row[0]+'</td><td>'+row[1]+'</td><td>'+row[2]+'</td><td>'+row[3]+'</td><td>'+row[4]+'</td><td><a href="'+row[5]+'" target="_blank">PDF</a></td></tr>'
		data2 = data2 + temp
	return render_template('soccent.html', data=data2)

@app.route('/alumni')
def alumni():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
					'version=v4')
	service = discovery.build('sheets', 'v4', http=http,
							  discoveryServiceUrl=discoveryUrl)
	print('About to read spreadsheet')
	spreadsheetId = alumniSheet
	rangeName = alumniRange
	result = service.spreadsheets().values().get(
		spreadsheetId=spreadsheetId, range=rangeName).execute()
	values = result.get('values', [])
	print('Got values')
	if not values:
		print('No data found.')
		
	# Creating Table HTML
	data2 = ''
	for row in values:
		temp = '<tr><td>'+row[0]+'</td><td>'+row[1]+'</td><td>'+row[2]+'</td><td>'+row[3]+'</td><td>'+row[4]+'</td><td>'+row[5]+'</td><td>'+row[6]+'</td></tr>'
		data2 = data2 + temp
	# conn.close()
	return render_template('alumni.html', data=data2)

if __name__=="__main__":
	app.run(debug=False)
