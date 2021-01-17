import numpy as np
import xlwings as xw


# https://en.wikipedia.org/wiki/Kelly_criterion
def kelly_criterion(prob, odds):
    # REDUCES TOTAL PROBABILITY (margin of error)
    multi = 1.0
    expn = 1.2
    prob = (prob * multi) ** expn
    # CALCULATES KELLY CRITERION
    percentage = prob - (1-prob) / (odds-1)
    percentage[percentage < 0] = 0
    return np.floor(percentage * 1000)/10
