import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from collections import OrderedDict

import time_util as tu


BASE_URL = "https://www.acmicpc.net"


def get_submission_links_from_user(boj_id: str) -> list:
    # 유저 프로필 '푼 문제'에 있는 제출 내역을 가져온다
    # 최근 100문제의 리스트를 가져온다
    req = requests.get(BASE_URL + "/status?user_id=" + boj_id + "&result_id=4")
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    data = ["/status?user_id=" + boj_id + "&result_id=4"]
    next_page = soup.select("#next_page")

    for i in range(4):
        if len(next_page) == 0:
            break

        link = next_page[0]['href']
        data.append(link)

        req = requests.get(BASE_URL + link)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        next_page = soup.select("#next_page")

    return data


def get_submissions(links: list) -> list:
    data = []

    for link in links:
        req = requests.get(BASE_URL + link)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.select("table#status-table > tbody > tr")
        for submit in table:
            row = submit.find_all('td')

            problem_id = row[2].text
            date = row[8].find('a')['title']

            submit_time = tu.convert_datetime(date)
            start_date, end_date = tu.get_start_and_end_of_this_week()

            if start_date <= submit_time <= end_date:
                data.append(problem_id)

    return list(OrderedDict.fromkeys(data))[::-1]   # 위(과거) -> 아래(최신)


def get_data_from_boj() -> list:
    boj_id_list = ['chsun0303', 'achaean', 'rm0576', 'joi0104', 'ooop0422', 'jjulia24', 'lkw4357', 'coxo9535',
                   'sabin5105']

    pool = Pool(processes=4)
    links = pool.map(get_submission_links_from_user, boj_id_list)
    data = pool.map(get_submissions, links)

    return data
