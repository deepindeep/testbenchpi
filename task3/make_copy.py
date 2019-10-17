import sys
import re
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SAMPLE_SS_URL = "https://docs.google.com/spreadsheets/d/{0}"


def main(ss_id, s_id, new_name):
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

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=ss_id, range="A1:Z100").execute()
    values = result.get('values', [])
    print(values)

    spreadsheet = {
        'properties': {
            'title': new_name
        }
    }

    spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                fields='spreadsheetId').execute()
    print('New spreadsheet URL: {0}'.format(SAMPLE_SS_URL.format(spreadsheet.get('spreadsheetId'))))


if __name__ == '__main__':
    existed_doc_url = sys.argv[1]
    new_sheet_name = sys.argv[2]

    ss_id_regexp = r"\/d\/[0-9a-zA-Z-_]+"
    spreadsheet_id = re.search(ss_id_regexp, existed_doc_url).group()[3:]
    s_id_regexp = r"[#&]gid=([0-9]+)"
    sheet_id = re.search(s_id_regexp, existed_doc_url).group()[5:]
    print(sheet_id)

    print(existed_doc_url)
    print(new_sheet_name)
    main(spreadsheet_id, sheet_id, new_sheet_name)
