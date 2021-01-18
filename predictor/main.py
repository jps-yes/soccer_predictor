import time

from bet_history import *
from bookmaker_scraper import *
from data_merger import *
from kelly_criterion import *
from predict import *


def main():
    while True:
        np.set_printoptions(formatter={'float_kind': '{:f}'.format})
        # Gets data from 538 and oddsportal, merges and saves it into "merged_data.json"
        data_merger()
        # Loads the model parameters from .mat file (neural network trained in Matlab) and predicts probability
        prob, _ = predict('model1x2_v1')
        if prob.size > 0:
            # Scrapes various bookmakers and returns best odds
            odds, bookmakers, urls = best_bookmaker()
            # Saves match info and probability in to history file: "bet_history.xlsx"
            bet_history(prob, odds, bookmakers)
            # Applies kelly criterion to determine the percentage of bankroll to bet
            percentage = kelly_criterion(prob, odds)
            # Updates github README.md --> private
            # github_updater(percentage, prob, odds, bookmakers, urls)
        else:
            print('No more matches for today.')
            percentage = np.array
            odds = np.array([])
            bookmakers = []
            # Updates github README.md --> private
            # github_updater(percentage, prob, odds, bookmakers, urls)
            break
        time.sleep(60 * 30)


if __name__ == "__main__":
    main()
