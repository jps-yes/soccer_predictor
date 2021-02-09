from difflib import SequenceMatcher

import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from dictionaries import *

global bookmaker
import time

def start_driver(visible=False):
    # STARTS CHROMEDRIVER
    options = Options()
    options.add_argument("--log-level=3")
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
    url_found = {}
    driver = start_driver(visible=False)
    for url in url_list:
        driver.get(url)
        t0 = time.time()
        while True:
            t1 = time.time()
            total = t1 - t0
            if total > 3:
                driver.get(url)
                t0 = time.time()
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
                if len(odds) == 3:
                    matches[team1 + ' - ' + team2] = [float(odds[0].get_text()),  # odd1
                                                      float(odds[2].get_text()),  # odd2
                                                      float(odds[1].get_text())]  # tie
                    url_found[team1 + ' - ' + team2] = [url, url, url]
            break
    driver.quit()
    return matches, url_found


def betano_scraper():
    global bookmaker
    bookmaker = 'betano'
    url_list, _ = get_todays_leagues()
    matches = {}
    url_found = {}
    driver = start_driver(visible=False)
    for url in url_list:
        driver.get(url)
        while True:
            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            if not soup.find_all('tr', {'category': 'FOOT'}):
                continue
            for match in soup.find_all('tr', {'category': 'FOOT'}):
                team1 = match.find_all('span', {'class': 'events-list__grid__info__main__participants__name'})[
                    0].get_text().strip()
                team2 = match.find_all('span', {'class': 'events-list__grid__info__main__participants__name'})[
                    1].get_text().strip()
                sections = match.find_all('section')
                odds = []
                for section in sections:
                    if section.find('div', {'class', 'table__markets__market__title__text'}).get_text() == 'Resultado Final':
                        odds = section.find_all('span', {'class': 'selections__selection__odd'})
                if len(odds) == 3:
                    matches[team1 + ' - ' + team2] = [float(odds[0].get_text().replace('-', '1')),  # odd1
                                                      float(odds[2].get_text().replace('-', '1')),  # odd2
                                                      float(odds[1].get_text().replace('-', '1'))]  # tie
                    url_found[team1 + ' - ' + team2] = [url, url, url]

            break
    return matches, url_found


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
    matches_luckia, url_luckia = luckia_scraper()
    odds_luckia, url_luckia = data_matcher(matches_luckia, url_luckia)
    matches_betano, url_betano = betano_scraper()
    odds_betano, url_betano = data_matcher(matches_betano, url_betano)
    odds = np.maximum(odds_luckia, odds_betano)
    bookmakers = []
    urls = []
    for i in range(odds.shape[0]):
        bookmakers.append(['', '', ''])
        urls.append(['', '', ''])
        for j in range(odds.shape[1]):
            if odds[i][j] == 1:
                bookmakers[i][j] = ''
                urls[i][j] = ''
            elif odds[i][j] == odds_luckia[i][j]:
                bookmakers[i][j] = 'luckia'
                urls[i][j] = url_luckia[i][j]
            elif odds[i][j] == odds_betano[i][j]:
                bookmakers[i][j] = 'betano'
                urls[i][j] = url_betano[i][j]
    odds[odds == 1] += .001
    return odds, bookmakers, urls


def data_matcher(matches, url_found):
    _, include = get_todays_leagues()
    # IMPORTS TEAM NAMES FROM merged_data.xlsx
    wb = openpyxl.load_workbook(r'.\merged_data.xlsx')
    sheet = wb.active
    ordered_odds = []
    urls = []
    i = -1
    for row in sheet.iter_rows(2):
        i += 1
        if not include[i]:
            ordered_odds.append([1.00, 1.00, 1.00])
            urls.append(['', '', ''])
            continue
        score = 0
        match_actual = row[0].value + ' - ' + row[1].value
        # EXCEPTIONS ###################################################################################################
        #
        #
        match_actual = match_actual.replace('QPR', 'Queens Park Rangers')
        match_actual = match_actual.replace('Lecce', 'US Lecce')
        match_actual = match_actual.replace('Ferreira', 'Paços de Ferreira')
        match_actual = match_actual.replace('Atletico-MG', 'Atlético Mineiro')
        match_actual = match_actual.replace('Leuven', 'Oud Heverlee Leuven')
        match_actual = match_actual.replace('Sao Paulo', 'São Paulo')
        match_actual = match_actual.replace('Athletico-PR', 'Athletico PR Parana')
        match_actual = match_actual.replace('U.N.A.M.- Pumas', 'UNAM Pumas')
        match_actual = match_actual.replace('Nacional', 'CD Nacional')
        match_actual = match_actual.replace('Club Brugge KV', 'Club Brugge')
        match_actual = match_actual.replace('Beerschot VA', 'KFCO Beerschot VA')
        match_actual = match_actual.replace('Alaves', 'Alavés')
        match_actual = match_actual.replace('Aue', 'Aue Erzgebirge')
        match_actual = match_actual.replace('Tirol', 'WSG Swarovski Tirol')
        match_actual = match_actual.replace('Vasco', 'Vasco Da Gama')
        match_actual = match_actual.replace('Gijon', 'Sporting Gijón')
        match_actual = match_actual.replace('Brest', 'Stade Brestois')
        match_actual = match_actual.replace('Bordeaux', 'Bordéus')
        ###################
        if len(matches) > 0:
            for match in matches.keys():
                if similar(match_actual, match) >= score:
                    score = similar(match_actual, match)
                    match_found = match
            print(str(score) + ': ' + match_actual + '-->' + match_found)
        if score >= 0.65:
            ordered_odds.append(matches[match_found])
            urls.append(url_found[match_found])
        else:
            ordered_odds.append([1.00, 1.00, 1.00])
            urls.append(['', '', ''])
    return np.array(ordered_odds), urls


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
    a1, a2 = a.split(' - ')
    b1, b2 = b.split(' - ')
    score = [SequenceMatcher(None, a, b).ratio(), SequenceMatcher(None, b, a).ratio()]
    aux = max([SequenceMatcher(None, b1, a1).ratio(), SequenceMatcher(None, a1, b1).ratio()])/2
    aux = aux + max([SequenceMatcher(None, b2, a2).ratio(), SequenceMatcher(None, a2, b2).ratio()])/2
    score.append(aux)
    return max(score)
