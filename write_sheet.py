from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import timeit
from datetime import date

import parser
import time_util as tu

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def main(crawled_data):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()

    # 테스트 스프레드 시트
    spreadsheet_id = '11jFC-jZa54KWcST_vdgn2ZcmzMhQ5TrpV1dWsYVboJA'
    range_name = get_range_name()

    body = {
        'values': crawled_data,
        'majorDimension': 'COLUMNS'
    }

    request = sheet.values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    )

    response = request.execute()


def get_range_name():
    sheet_range = '!B2:Z'
    base_start_date = date(2019, 5, 6)

    start_date, end_date = tu.get_start_and_end_of_this_week()
    week_idx = ((start_date - base_start_date)//7).days + 1
    week_range = "[{0:02}.{1:02} - {2:02}.{3:02}]".format(start_date.month, start_date.day, end_date.month, end_date.day)

    return "cycle {0:02} ".format(week_idx) + week_range + sheet_range


if __name__ == '__main__':
    start = timeit.default_timer()

    crawled_data = parser.get_data_from_boj()
    main(crawled_data)

    end = timeit.default_timer()

    print("total: ", end - start)
