import json
import re
import time
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from dictionaries import league_to_url_dictionary


def get_odds(url_league, data):
    # REGEX FOR SCRAPING
    team_regex = re.compile(r'(.+) - (.+)')
    time_regex = re.compile(r'([0-9]+):([0-9]+)')
    # ACCESSES URL AND GETS PAGE
    driver.get(url_league)
    time.sleep(1)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    identifier = len(data)
    for row in soup.table.tbody.find_all('tr'):
        try:
            attributes = row.attrs['class']
        except KeyError:
            attributes = ['odd']
        attributes.append('filler')
        # IF IT IS A DATE ROW
        if attributes[0] == 'center':
            match_date = row.select('span[class*="datet "]')[0].get_text()
            if 'Today' not in match_date:
                break
        # IF IT IS A MATCH ROW
        elif attributes[0] == 'odd':
            identifier += 1
            data[identifier] = {}
            # FILLS ATTRIBUTES FOR THIS MATCH
            if len(row.find_all('span', {'class': 'live-odds-ico-prev'})) == 0\
                    and len(row.find_all('td', {'class': 'center bold table-odds table-score'})) == 0\
                    and r"'" not in row.select('td[class*="table-time datet "]')[0].get_text():
                data[identifier]['matchTime'] = str(
                    float(time_regex.search(row.select('td[class*="table-time datet "]')[0].get_text()).group(1)) +
                    float(time_regex.search(row.select('td[class*="table-time datet "]')[0].get_text()).group(2)) / 60)
            else:
                # MATCH CURRENTLY HAPPENING
                del data[identifier]
                identifier -= 1
                continue

            data[identifier]['match_day'] = str(datetime.now().day)
            data[identifier]['match_month'] = str(datetime.now().month)
            data[identifier]['match_year'] = str(datetime.now().year)
            data[identifier]['numberBookmarkers'] = row.find_all('td', {'class': 'center info-value'})[0].get_text()
            data[identifier]['team1'] = team_regex.search(
                row.find_all('td', {'class': 'name table-participant'})[0].get_text()).group(1)
            data[identifier]['team2'] = team_regex.search(
                row.find_all('td', {'class': 'name table-participant'})[0].get_text()).group(2)
            data[identifier]['team1'] = data[identifier]['team1'].replace(u'\xa0', u'')
            data[identifier]['team2'] = data[identifier]['team2'].replace(u'\xa0', u'')
            try:
                data[identifier]['oddsW1'] = row.find_all('a', {'xparam': 'odds_text'})[0].get_text()
                data[identifier]['oddsTie'] = row.find_all('a', {'xparam': 'odds_text'})[1].get_text()
                data[identifier]['oddsW2'] = row.find_all('a', {'xparam': 'odds_text'})[2].get_text()
            except IndexError:  # match was postponed
                del data[identifier]
    return data


def get_results(url_league, data):
    # REGEX FOR SCRAPING
    team_regex = re.compile(r'(.+) - (.+)')
    # ACCESSES URL AND GETS PAGE
    driver.get(url_league)
    time.sleep(1)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    identifier = len(data)
    for row in soup.table.tbody.find_all('tr'):
        try:
            attributes = row.attrs['class']
        except KeyError:
            attributes = ['odd']
        attributes.append('filler')
        # IF IT IS A DATE ROW
        if attributes[0] == 'center':
            match_date = row.select('span[class*="datet "]')[0].get_text()
            if 'Yesterday' in match_date or 'Today' in match_date:
                pass
            else:
                match_date = datetime.strptime(match_date, '%d %b %Y')
                last_week = (datetime.now()-timedelta(8))
                if match_date < last_week:
                    break
        # IF IT IS A MATCH ROW
        elif attributes[0] == 'odd' or attributes[0] == 'deactivate':
            identifier += 1
            data[identifier] = {}
            # FILLS ATTRIBUTES FOR THIS MATCH
            data[identifier]['date'] = (datetime.now() - timedelta(1)).strftime('%d-%m-%Y')
            data[identifier]['team1'] = team_regex.search(
                row.find_all('td', {'class': 'name table-participant'})[0].get_text()).group(1)
            data[identifier]['team2'] = team_regex.search(
                row.find_all('td', {'class': 'name table-participant'})[0].get_text()).group(2)
            data[identifier]['team1'] = data[identifier]['team1'].replace(u'\xa0', u'')
            data[identifier]['team2'] = data[identifier]['team2'].replace(u'\xa0', u'')
            try:
                score_str = row.find_all('td', {'class': 'table-score'})[0].get_text()
                if ':' in score_str:
                    score = score_str.split(':')
                else:  # match was postponed
                    del data[identifier]
                    identifier -= 1
                    continue
            except IndexError:  # match in play
                del data[identifier]
                identifier -= 1
                continue
            if int(score[0]) > int(score[1]):
                data[identifier]['win1'] = 1
                data[identifier]['win2'] = 0
                data[identifier]['tie'] = 0
            elif int(score[0]) < int(score[1]):
                data[identifier]['win1'] = 0
                data[identifier]['win2'] = 1
                data[identifier]['tie'] = 0
            else:
                data[identifier]['win1'] = 0
                data[identifier]['win2'] = 0
                data[identifier]['tie'] = 1

    return data


def oddsportal_scraper(leagueid_list, scrape_results=False):
    # STARTS CHROMEDRIVER
    global driver
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    data_oddsportal = {}
    league_dict = league_to_url_dictionary('oddsportal')
    for leagueid in leagueid_list:
        if leagueid in league_dict.keys():
            url = league_dict[leagueid]
            if not scrape_results:
                data_oddsportal = get_odds(url, data_oddsportal)
            else:
                url = url + 'results/'
                data_oddsportal = get_results(url, data_oddsportal)

    json_odds = json.dumps(data_oddsportal)
    f = open("data_oddsportal.json", "w")
    f.write(json_odds)
    f.close()
    driver.quit()
