import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from dictionaries import *

global bookmaker
from difflib import SequenceMatcher


def start_driver(visible=False):
    # STARTS CHROMEDRIVER
    options = Options()
    if not visible:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    return driver


def luckia_scraper():
    global bookmaker
    bookmaker = 'luckia'
    url_list, _ = get_todays_leagues()
    matches = {}
    driver = start_driver()
    for url in url_list:
        driver.get(url)
        while True:
            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            if not soup.find_all('div', {'class': 'rj-ev-list__ev-card__inner'}):
                continue
            for match in soup.find_all('div', {'class': 'rj-ev-list__ev-card__inner'}):
                if match.find_all('div', {'rj-ev-list__ev-card__section-item rj-ev-list__ev-card__scores'}):
                    continue  # in-play --> skip this match
                team1 = match.find_all('span', {'class': 'rj-ev-list__name-text'})[0].get_text()
                team2 = match.find_all('span', {'class': 'rj-ev-list__name-text'})[1].get_text()
                odds = match.find_all('span', {'class': 'rj-ev-list__bet-btn__content rj-ev-list__bet-btn__odd'})
                matches[team1 + ' - ' + team2] = [float(odds[0].get_text()),  # odd1
                                                  float(odds[2].get_text()),  # odd2
                                                  float(odds[1].get_text())]  # tie

            break
    driver.quit()
    return matches


def betano_scraper():
    global bookmaker
    bookmaker = 'betano'
    url_list, _ = get_todays_leagues()
    matches = {}
    driver = start_driver()
    for url in url_list:
        driver.get(url)
        while True:
            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            if not soup.find_all('tr', {'category': 'FOOT'}):
                continue
            for match in soup.find_all('tr', {'category': 'FOOT'}):
                team1 = match.find_all('span', {'class': 'events-list__grid__info__main__participants__name'})[0].get_text().strip()
                team2 = match.find_all('span', {'class': 'events-list__grid__info__main__participants__name'})[1].get_text().strip()
                odds = match.find_all('span', {'class': 'selections__selection__odd'})
                matches[team1 + ' - ' + team2] = [float(odds[0].get_text()),  # odd1
                                                  float(odds[2].get_text()),  # odd2
                                                  float(odds[1].get_text())]  # tie
            break
    return matches


def betpt_scraper():
    pass  # TODO


def placard_scraper():
    pass  # TODO


def solverde_scraper():
    pass  # TODO


def esc_scraper():
    pass  # TODO


def betclic_scraper():
    pass  # TODO


def moosh_scraper():
    pass  # TODO


def betway_scraper():
    pass  # TODO


def nossaaposta_scraper():
    pass  # TODO


def best_bookmaker():
    matches_luckia = luckia_scraper()
    odds_luckia = data_matcher(matches_luckia)
    matches_betano = betano_scraper()
    odds_betano = data_matcher(matches_betano)
    odds = np.maximum(odds_luckia, odds_betano)
    bookmakers = []
    for i in range(odds.shape[0]):
        bookmakers.append(['', '', ''])
        for j in range(odds.shape[1]):
            if odds[i][j] == 1:
                bookmakers[i][j] = ''
            elif odds[i][j] == odds_luckia[i][j]:
                bookmakers[i][j] = 'luckia'
            elif odds[i][j] == odds_betano[i][j]:
                bookmakers[i][j] = 'betano'
    odds[odds == 1] += .001
    return odds, bookmakers


def data_matcher(matches):
    _, include = get_todays_leagues()
    # IMPORTS TEAM NAMES FROM merged_data.xlsx
    wb = openpyxl.load_workbook(r'.\merged_data.xlsx')
    sheet = wb.active
    ordered_odds = []
    i = -1
    for row in sheet.iter_rows(2):
        i += 1
        if not include[i]:
            ordered_odds.append([1.00, 1.00, 1.00])
            continue
        score = 0
        match_actual = row[0].value + ' - ' + row[1].value
        # EXCEPTIONS
        match_actual = match_actual.replace('QPR', 'Queens Park Rangers')
        for match in matches.keys():
            if similar(match_actual, match) >= score:
                score = similar(match_actual, match)
                match_found = match
        print(str(score) + ': ' + match_actual + '-->' + match_found)
        if score >= 0.60:
            ordered_odds.append(matches[match_found])
        else:
            ordered_odds.append([1.00, 1.00, 1.00])
    return np.array(ordered_odds)


def get_todays_leagues():
    url_dict = league_to_url_dictionary(bookmaker)
    wb = openpyxl.load_workbook(r'.\merged_data.xlsx')
    sheet = wb.active
    url_list = []
    matches = []
    i = 0
    for row in sheet.iter_rows(min_row=1):
        if i == 0:  # gets league id order from "merged_data.xlsx"
            league_id_order = []
            for col in sheet.iter_cols(min_col=30):
                league_id_order.append(col[i].value)
        else:
            # identifies league id
            j = 0
            for col in sheet.iter_cols(min_col=30):
                if col[i].value == '1':
                    league_id = league_id_order[j]
                    if url_dict[league_id] is not None:
                        matches.append(True)
                        if url_dict[league_id] not in url_list:
                            url_list.append(url_dict[league_id])
                    else:
                        matches.append(False)
                    break
                j += 1
        i += 1
    return url_list, matches


def similar(a, b):
    return max([SequenceMatcher(None, a, b).ratio(), SequenceMatcher(None, b, a).ratio()])
