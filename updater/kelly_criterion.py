import numpy as np
import xlwings as xw


# https://en.wikipedia.org/wiki/Kelly_criterion
def kelly_criterion(prob, odds):
    # REDUCES TOTAL PROBABILITY (margin of error)
    app = xw.App(visible=False)
    wb = xw.Book('bet_history.xlsx')
    sheet = wb.sheets.active
    multi = sheet['AC1'].value
    expn = sheet['AB1'].value
    prob = (prob * multi) ** expn
    wb.close()
    app.kill()
    # CALCULATES KELLY CRITERION
    percentage = prob - (1-prob) / (odds-1)
    percentage[percentage < 0] = 0
    return np.floor(percentage * 1000)/10
