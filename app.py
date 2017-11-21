import os
from flask import Flask,request,render_template,flash, Response
from flaskext.mysql import MySQL
from flask_basicauth import BasicAuth
import pandas as pd
import httplib2
from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage
from functools import wraps

app = Flask(__name__)
basic_auth = BasicAuth(app)

authSheet = '1iHPGcH4q5pcgG5A82z9hxSOhjNPHXvdcSI8BL9XkgWg'
authRange = 'Sheet1!A2:B'
soccentSheet = '18mY9pAnPhKs5uR0z5f1wjGgH7KqTsL9dUIzcEw3lbOc'
soccentRange = 'Sheet1!A2:F'
alumniSheet = '12mJnLcmnO2cM-9tj0pL1TUGYq__2dRuRyHfQaS1feLY'
alumniRange = 'Sheet1!B3:H'

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
    
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'LINK TO FILE GOES HERE'
APPLICATION_NAME = 'ATLAS'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-rishi-atlas.json')

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

def getValues(spreadsheetId, rangeName):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    print('About to read spreadsheet')
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    print('Got values')
    if not values:
        print('No data found.')
    return values

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    for elem  in getValues(authSheet, authRange):
        if len(elem) == 2:
            uname, pwd = elem
            if username == uname and password == pwd:
                return True
    return False

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/soccent')
@requires_auth
def soccent():
    data = ''
    for row in getValues(soccentSheet, soccentRange):
        data +=  '<tr><td>'+row[0]+'</td><td>'+row[1]+'</td><td>'+row[2]+'</td><td>'+row[3]+'</td><td>'+row[4]+'</td><td><a href="'+row[5]+'" target="_blank">PDF</a></td></tr>'
    return render_template('soccent.html', data=data)

@app.route('/alumni')
@requires_auth
def alumni():
    data = ''
    for row in getValues(alumniSheet, alumniRange):
        data += '<tr><td>'+row[0]+'</td><td>'+row[1]+'</td><td>'+row[2]+'</td><td>'+row[3]+'</td><td>'+row[4]+'</td><td>'+row[5]+'</td><td>'+row[6]+'</td></tr>'
    return render_template('alumni.html', data=data)

if __name__=="__main__":
    app.run(debug=False)
