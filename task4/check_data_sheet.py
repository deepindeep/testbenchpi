from utils import build_sheet_service, validate_sheet_id
import sys
import pytz
import time
import datetime

SHEET = "https://docs.google.com/spreadsheets/d/1fsTbXKN-yUrlh4j433ndduyX8xyAdxJ-SlC8XkVw76A/edit#gid=0"
FAILED = 0


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


def test_data(data):
    data = [int(i) for i in data[5:]]
    print(data)
    return all([5 < data[0] < 100,
                0 < data[1] < 10,
                0 < data[2] < 10,
                5 < data[3] < 10,
                -10 < data[4] < 60,
                -10 < data[5] < 60,
                5 < data[6] < 100,
                data[7] == 0,
                data[8] == 0,
                6 < data[9] < 15])


def main():
    global FAILED
    print("Test has been started.")
    while True:
        data = get_data()
        time_zone = data["TimeZone"]
        lt = data["Localtime"]
        utc_dt = local_time_zone_to_utc_datetime(lt, time_zone)
        check = compare_times(datetime.datetime.utcnow(), utc_dt)
        if not check:
            print("Time check failed. No new row.")
            if FAILED > 0:
                print("TEST FAILED")
                sys.exit(1)
            print("Waiting 6 minutes...")
            time.sleep(360)
            FAILED += 1
        FAILED = 0
        result = test_data(list(data.values()))
        if result:
            print("TEST COMPLETE")
            print("Waiting 5 minutes...")
            time.sleep(300)
        else:
            print("TEST FAILED")
            sys.exit(1)


if __name__ == "__main__":
    main()
    print("Bye!")
