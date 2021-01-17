import csv
import unidecode
from datetime import datetime

import requests

from dictionaries import team_exists


def save_file_538():
    response = requests.get('https://projects.fivethirtyeight.com/soccer-api/club/spi_matches_latest.csv')
    if response.status_code == 200:
        with open('spi_matches_latest.csv', 'w+', newline='') as file:
            writer = csv.writer(file)
            for line in response.iter_lines():
                writer.writerow(line.decode('utf8').split(','))
            file.close()


def get_today_matches():
    with open(r'.\spi_matches_latest.csv') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        csv_data = {}
        today = datetime.today().strftime('%Y-%m-%d')
        i = 0
        for row in reader:
            if i == 0:
                headers = list(row)
                i += 1
                continue
            elif row[1] != today or row[15] != '':   # Skips if date is not today OR match already has a score
                continue
            if row[13] == '' or row[14] == '':  # Skips if importance coefficient doesn't exist
                continue
            j = 0
            csv_data[i] = {}
            for header in headers:
                csv_data[i][header] = unidecode.unidecode(list(row)[j])
                j = j + 1
            i += 1
        teams = []
        for match in csv_data:
            teams.append(csv_data[match]['team1'])
            teams.append(csv_data[match]['team2'])
        team_exists(teams)
        return csv_data
