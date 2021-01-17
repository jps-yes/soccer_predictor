from data_merger import *
from predict import *
from kelly_criterion import *
from bet_history import *

from bookmaker_scraper import *


def main():
    np.set_printoptions(formatter={'float_kind': '{:f}'.format})
    # Gets data from 538 and oddsportal, merges and saves it into "merged_data.json"
    data_merger()
    # Loads the model parameters from .mat file (neural network trained in Matlab) and predicts probability
    prob, _ = predict('model1x2_v1')
    if prob.size > 0:
        # Scrapes various bookmakers and returns best odds
        odds, bookmakers = best_bookmaker()
        # Saves match info and probability in to history file: "bet_history.xlsx"
        bet_history(prob, odds, bookmakers)
        # Applies kelly criterion to determine the percentage of bankroll to bet
        percentage = kelly_criterion(prob, odds)
    else:
        print('No more matches for today.')


if __name__ == "__main__":
    main()
