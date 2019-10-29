import sys
import validators
import re
import csv
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# row_example = '"XXAAB33440","user1",1,255,0,0,5,1,0,1,1,5,2,TRUE,"7/29/2018 3:09:21 AM",1570527067947,1570527067963,TRUE,"sheet10",FALSE,FALSE,"DEFAULT","America/Chicago",0,0,"10/09/2019 0:00:00",FALSE,5,TRUE,TRUE,TRUE,"Oct 08, 2019 04:31","Jul 29, 2018 03:09","Oct 08, 2019 04:31",-1570527024183,0,"DO NOT RENAME OR REORDER *"'
example_data = '{"DID": "AABBCCDDEE00112233440", "USERID": "user1", "01": "1", "02": "255", "03": "0", "04": "", "15": "0", "16": "5", "17": "1", "18": "0", "19": "1", "20": "1", "21": "5", "22": "2", "CMD": "TRUE", "Last CMD": "7/29/2018 3:09:21 AM", "Last device call": "1570527067947", "Last reset": "1570527067963", "w2gs": "TRUE", "gsheet": "sheet10", "w2gbq": "FALSE", "w2wh": "FALSE", "HWREV": "", "location": "", "Name": "", "Description": "DEFAULT", "TZ": "America/Chicago", "T1": "0", "T2": "0", "NR": "10/09/2019 0:00:00", "alertsEnabled": "FALSE", "maxAlerts": "5", "DBG": "TRUE", "maxRows": "", "DEBUG": "TRUE", "enabled": "TRUE", "lat,lon": "", "Last Reset Time": "Oct 08, 2019 04:31", "Last CMD Date": "Jul 29, 2018 03:09", "Last Device Call Date": "Oct 08, 2019 04:31", "Last call timespan": "-1570527024180", "": "0", "notes": "DO NOT RENAME OR REORDER *"}'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
HEADERS = 'DID', 'USERID', '01', '02', '03', '04', '15', '16', '17', '18', '19', '20', '21', '22', 'CMD', 'Last CMD', 'Last device call', 'Last reset', 'w2gs', 'gsheet', 'w2gbq', 'w2wh', 'HWREV', 'location', 'Name', 'Description', 'TZ', 'T1', 'T2', 'NR', 'alertsEnabled', 'maxAlerts', 'DBG', 'maxRows', 'DEBUG', 'enabled', 'lat,lon', 'Last Reset Time', 'Last CMD Date', 'Last Device Call Date', 'Last call timespan', '', 'notes'


class InvalidParamsException(Exception):
    pass


class InvalidURLException(Exception):
    pass


class SheetIDNotFoundException(Exception):
    pass


class InvalidDataException(Exception):
    pass


class InvalidDataColumnException(Exception):
    pass


class InvalidInputDataStructure(Exception):
    pass


def build_sheet_service():
    """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)


def insert_row(spreadsheet_id, data):
    service = build_sheet_service()

    def modify_bool(item):
        if item.upper() == "TRUE":
            return True
        elif item.upper() == "FALSE":
            return False
        else:
            return item

    row_to_append = [modify_bool(data[i]) for i in HEADERS]
    body = {
        "values": [
            row_to_append
        ]
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range="DeviceConfig!A:AQ", valueInputOption="RAW", body=body).execute()
    print('{0} cells appended.'.format(result.get('updates').get('updatedCells')))


def validate_sheet_id(url):
    ss_id_regexp = r"\/d\/[0-9a-zA-Z-_]+"
    spreadsheet_id = re.search(ss_id_regexp, url)
    if spreadsheet_id is None:
        raise SheetIDNotFoundException("Sheet ID not found")
    return spreadsheet_id.group()[3:]


def validate_data(data):
    data = json.loads(data)
    if len(HEADERS) != len(data):
        raise InvalidDataColumnException("Columns mismatch. Expected {0}. Found {1}.".format(len(HEADERS), len(data)))
    if not all([h in data for h in HEADERS]):
        raise InvalidInputDataStructure("Invalid input data")
    return data


def main():
    if not len(sys.argv) == 3:
        raise InvalidParamsException("This is weird. Only sheet URL and data expected. Got {0} arguments".format(len(sys.argv)-1))
    spreadsheet_url = sys.argv[1]
    if not validators.url(spreadsheet_url):
        raise InvalidURLException("Invalid stylesheet URL")
    sheet_id = validate_sheet_id(spreadsheet_url)
    data = sys.argv[2]
    data = validate_data(data)
    insert_row(sheet_id, data)
    print("The row has been added")


if __name__ == "__main__":
    main()
