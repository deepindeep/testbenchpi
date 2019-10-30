from utils import build_sheet_service, validate_sheet_id
import pytz
import datetime

SHEET = "https://docs.google.com/spreadsheets/d/1fsTbXKN-yUrlh4j433ndduyX8xyAdxJ-SlC8XkVw76A/edit#gid=0"


def utc_time_stamp_to_utc_datetime(ts):
    return datetime.datetime.utcfromtimestamp(int(int(ts) / 1000))


def local_time_zone_to_utc_datetime(local_time, time_zone):
    format_str = '%m/%d/%Y %I:%M:%S %p' if "PM" in local_time or "AM" in local_time else '%m/%d/%Y %H:%M:%S'
    local = pytz.timezone(time_zone)
    naive = datetime.datetime.strptime(local_time, format_str)
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    utc_dt = utc_dt.replace(tzinfo=None)
    return utc_dt


def compare_times(utc_dt, utc_dt2):
    return datetime.timedelta(minutes=-6) < utc_dt2 - utc_dt < datetime.timedelta(minutes=6)


def get_data():
    service = build_sheet_service()
    sheet_id = validate_sheet_id(SHEET)
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range="DATA!A:R").execute()
    data = dict()
    for i in range(len(result["values"][0])):
        data[result["values"][0][i].strip()] = result["values"][-1][i]
    return data


def main():
    data = get_data()
    time_zone = data["TimeZone"]
    lt = data["Localtime"]
    utc_ts = data["UTC"]
    utc_dt = utc_time_stamp_to_utc_datetime(utc_ts)
    utc_dt2 = local_time_zone_to_utc_datetime(lt, time_zone)
    check = compare_times(utc_dt, utc_dt2)
    return data


if __name__ == "__main__":
    main()
    print("Bye!")
