import time

from bet_history import *
from bookmaker_scraper import *
from data_merger import *
from github_updater import *  # --- !!! This file is private (contains credentials)
from kelly_criterion import *
from predict import *


def main():
    while True:
        np.set_printoptions(formatter={'float_kind': '{:f}'.format})
        # Gets data from 538 and oddsportal, merges and saves it into "merged_data.json"
        data_merger()
        # Loads the model parameters from .mat file (neural network trained in Matlab) and predicts probability
        model_list = ['modelA', 'modelB', 'modelC']
        # Scrapes various bookmakers and returns best odds
        odds, bookmakers, urls = best_bookmaker()
        for model_name in model_list:
            prob, _ = predict(model_name)
            if prob.size == 0:
                break
            # Saves match info and probability in to history file: "bet_history.xlsx"
            bet_history(prob, odds, bookmakers, model_name)
            # Applies kelly criterion to determine the percentage of bankroll to bet
            percentage = kelly_criterion(prob, odds, model_name)
            print(percentage)
        # Updates github README.md
        github_updater(model_list)  # --- !!! This file is private (contains credentials)
        if prob.size == 0:
            print('No more matches for today.')
            break
        time.sleep(60 * 90)


if __name__ == "__main__":
    main()
