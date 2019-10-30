from utils import build_sheet_service, SheetIDNotFoundException, InvalidDataColumnException, \
    InvalidInputDataStructure, InvalidParamsException, InvalidURLException


SHEET = "https://docs.google.com/spreadsheets/d/1fsTbXKN-yUrlh4j433ndduyX8xyAdxJ-SlC8XkVw76A/edit#gid=0"

last_row = None


def main():
    global last_row
    service = build_sheet_service()


if __name__ == "__main__":
    main()
