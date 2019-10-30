import sys
import validators
import re
import json
from utils import build_sheet_service, SheetIDNotFoundException, InvalidDataColumnException, \
    InvalidInputDataStructure, InvalidParamsException, InvalidURLException, validate_sheet_id


HEADERS = 'DID', 'USERID', '01', '02', '03', '04', '15', '16', '17', '18', '19', '20', '21', '22', 'CMD', 'Last CMD', 'Last device call', 'Last reset', 'w2gs', 'gsheet', 'w2gbq', 'w2wh', 'HWREV', 'location', 'Name', 'Description', 'TZ', 'T1', 'T2', 'NR', 'alertsEnabled', 'maxAlerts', 'DBG', 'maxRows', 'DEBUG', 'enabled', 'lat,lon', 'Last Reset Time', 'Last CMD Date', 'Last Device Call Date', 'Last call timespan', '', 'notes'


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
