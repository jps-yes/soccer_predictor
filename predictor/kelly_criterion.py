import numpy as np


# https://en.wikipedia.org/wiki/Kelly_criterion
def kelly_criterion(prob, odds):
    # REDUCES TOTAL PROBABILITY (margin of error)
    prob = (prob * 1.0) ** 1.2
    # CALCULATES KELLY CRITERION
    percentage = prob - (1-prob) / (odds-1)
    percentage[percentage < 0] = 0
    return np.floor(percentage * 1000)/10
