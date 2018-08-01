from __future__ import print_function
import httplib2
import os
import json
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

class Controller:
    def __init__(self):
        self.data = {}
        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
        self.SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.APPLICATION_NAME = 'Google Sheets API Python Quickstart'

    def get_sheet_data(self):
        """Shows basic usage of the Sheets API.

        Creates a Sheets API service object and prints the names and majors of
        students in a sample spreadsheet:
        https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheetId = '1Z_g1mqHpVWRo2pdJum_2Hp1J8G3b0R-yjhL5MSKjxLw'
        rangeName = 'Spolunteers'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName).execute()
        values = result.get('values', [])
        column_headers = values[0]
        if not values:
            print('No data found.')
        else:
            for row in values[1:]:
                self.data[str(values.index(row) +1 )] = dict()
                for header in column_headers:
                    try:
                        self.data[str(values.index(row) +1 )].update({header : row[column_headers.index(header)]})
                    except IndexError:
                        self.data[str(values.index(row) +1 )][header] = ""
            return self.data

    def get_spolunteer_data(self, query_params = {"First Name":"ben", "Surname": "boss"}):
        data = self.data
        returned_rows = []
        for row in data.keys():
            row_data = data[row]
            matched_params = 0
            for parameter in query_params.keys():
                if query_params[parameter].lower() == row_data[parameter].lower():
                    matched_params += 1
            if matched_params == len(query_params):
                returned_rows.append(row)
        return returned_rows



    def set_sheet_data(self):
        pass

    def get_table_data(self ):
        pass



    def set_table_data(self, table, value):
        pass

    def get_credentials(self):
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
                                       'sheets.googleapis.com-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

if __name__ == '__main__':

    check = Controller()
    check.get_sheet_data()
    check.get_spolunteer_data()
