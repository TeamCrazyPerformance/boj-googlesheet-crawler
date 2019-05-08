from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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
    range_name = 'cycle01!A2:Z'

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


def get_data_from_boj() -> list:
    boj_id_list = ['chsun0303', 'achaean', 'rm0576', 'joi0104', 'ooop0422', 'jjulia24', 'lkw4357', 'coxo9535',
                   'sabin5105']

    data = []
    for boj_id in boj_id_list:
        links = parser.get_submission_links_from_user(boj_id)
        personal_data = parser.get_submissions(links)
        data.append(personal_data)

    return data


if __name__ == '__main__':
    crawled_data = get_data_from_boj()
    main(crawled_data)
