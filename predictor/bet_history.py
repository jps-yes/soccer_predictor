import openpyxl, os, json
from oddsportal_scraper import *
from datetime import datetime, timedelta


def bet_history(prob, odds, bookmakers):
    # Creates file "bet_history.xlsx" is it doesn't exist
    if not os.path.isfile(r'.\bet_history.xlsx'):
        wb_history = openpyxl.Workbook()
        sheet_history = wb_history.active
        header = ['date', 'team1', 'team2', 'league_id', 'prob1', 'prob2', 'probTie', 'odd1', 'odd2', 'oddTie',
                  'bookmaker1', 'bookmaker2', 'bookmakerTie', 'outcome1', 'outcome2', 'outcomeTie']
        sheet_history.append(header)
        wb_history.save('bet_history.xlsx')

    wb_today = openpyxl.load_workbook(r'.\merged_data.xlsx')
    sheet_today = wb_today.active
    wb_history = openpyxl.load_workbook(r'.\bet_history.xlsx')
    sheet_history = wb_history.active

    id_history = []
    id_history_without_result = []
    league_without_result = []
    for row in sheet_history.iter_rows(min_row=2):
        id_history.append([row[0].value, row[1].value, row[2].value])
        if row[15].value is None and row[0].value == (datetime.now() - timedelta(1)).strftime('%d-%m-%Y'):
            id_history_without_result.append([row[0].value, row[1].value, row[2].value])
            if str(row[3].value) not in league_without_result:
                league_without_result.append(str(row[3].value))
    # ADDS RESULTS FROM YESTERDAY
    # scrapes result data and saves into "data_oddsportal.json"
    oddsportal_scraper(league_without_result, scrape_results=True)
    with open(r'.\data_oddsportal.json') as jsonFile:
        data_oddsportal = json.load(jsonFile)
        for match in data_oddsportal:
            match_id = [data_oddsportal[match]['date'], data_oddsportal[match]['team1'],
                        data_oddsportal[match]['team2']]
            if match_id in id_history_without_result:
                sheet_history.cell(id_history.index(match_id) + 2, 14).value = data_oddsportal[match]['win1']
                sheet_history.cell(id_history.index(match_id) + 2, 15).value = data_oddsportal[match]['win2']
                sheet_history.cell(id_history.index(match_id) + 2, 16).value = data_oddsportal[match]['tie']
    # ADDS OR UPDATES TODAY'S MATCHES
    i = 0
    for row in sheet_today.iter_rows(min_row=1):
        if i == 0:  # gets league id order from "merged_data.xlsx"
            league_id_order = []
            for col in sheet_today.iter_cols(min_col=30):
                league_id_order.append(col[i].value)
        else:
            # identifies league id
            j = 0
            league_id = 0
            for col in sheet_today.iter_cols(min_col=30):
                if col[i].value == '1':
                    league_id = league_id_order[j]
                    break
                j += 1
            id_today = [row[18].value + '-' + row[19].value + '-' + row[20].value, row[0].value, row[1].value]
            if id_today not in id_history:  # appends data if item does not exist
                sheet_history.append(id_today + [league_id] + prob[i - 1].tolist() + odds[i - 1].tolist())
            else:  # updates data if item already exists
                index = id_history.index(id_today)
                sheet_history.cell(index + 2, 5).value = prob[i-1][0]
                sheet_history.cell(index + 2, 6).value = prob[i-1][1]
                sheet_history.cell(index + 2, 7).value = prob[i-1][2]
                sheet_history.cell(index + 2, 8).value = odds[i-1][0]
                sheet_history.cell(index + 2, 9).value = odds[i-1][1]
                sheet_history.cell(index + 2, 10).value = odds[i-1][2]
                sheet_history.cell(index + 2, 11).value = bookmakers[i-1][0]
                sheet_history.cell(index + 2, 12).value = bookmakers[i-1][1]
                sheet_history.cell(index + 2, 13).value = bookmakers[i-1][2]
        i += 1
    wb_history.save('bet_history.xlsx')
