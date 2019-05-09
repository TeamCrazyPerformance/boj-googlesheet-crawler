from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import timeit

import parser

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

    # sheet 가져오기
    sheet = service.spreadsheets()

    # 테스트 스프레드 시트
    spreadsheet_id = '11jFC-jZa54KWcST_vdgn2ZcmzMhQ5TrpV1dWsYVboJA'
    range_name = 'cycle01!B2:Z'

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


if __name__ == '__main__':
    start = timeit.default_timer()

    crawled_data = parser.get_data_from_boj()
    main(crawled_data)

    end = timeit.default_timer()

    print("total: ", end - start)
