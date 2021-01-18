# Soccer Predictor
<sub>__Disclaimer__: This project is solely an exercise on web scraping and machine learning.
I do not use it to place bets myself, but if you are willing to proceed anyway, first consider that past performance
does not guarantee further performance. The further to the future we get, the more the conditions the matches are
played change and the more we are extrapolating from the training dataset. Concretely, new rules might be
introduced to the game, for instance the introduction of the video assistant referee (VAR). External factors can also
negatively influence the performance of the model, for example COVID-19 increases the chances of players missing a game.
Furthermore, the longer before the game begins, the less accurate the prediction will be.</sub>

## Predictions
__Model__: full time result v1.0</br>
__ROI__: sample size too small 


### Today's matches
|match|bet|p(bet)|odd|best bookmaker|% of bankroll|
|---  |---|---        |---|---           |---|
|Cagliari - AC Milan|team 2|68.2%|1.62|[betano](https://www.betano.pt/sport/futebol/italia/serie-a/1635r/)|9.8%|
|Palmeiras - Corinthians|team 1|58.2%|2.05|[betano](https://www.betano.pt/sport/futebol/brasil/brasileirao-serie-a/10016r/)|9.9%|


&nbsp;&nbsp;<sup>_automatically updated at 09:03h GMT - 18 Jan, 2021_</sup>

### Last week's matches
|match|bet|p(bet)|odd|best bookmaker|% of bankroll|
|---  |---|---        |---|---           |---|
|:heavy_check_mark: Fluminense - Sport Recife|team 1|59.6%|1.88|betano|4.8%|
|:x: Nantes - Lens|team 2|36.3%|3.9|luckia|5.8%|
|:x: Wolfsberger AC - Sturm Graz|team 2|50.6%|2.6|luckia|11.0%|
|:heavy_check_mark: U.N.A.M.- Pumas - Mazatlan FC|team 1|51.8%|2.15|luckia|0.2%|
|:heavy_check_mark: Manchester City - Crystal Palace|team 1|82.2%|1.25|luckia|13.0%|

    
## About

### Predictor
* Collects and preprocesses input data for the neural network;
* Deploys neural network obtaining the probability of each match outcome;
* Collects odds from legal portuguese bookmakers, compares and determines best odd;</br>
Currently implemented:
    * __luckia__:heavy_check_mark:
    * __betano__:heavy_check_mark:
    * bet.pt:x:
    * placard:x:
    * solverde:x:
    * esc:x:
    * betclick:x:
    * moosh:x:
    * betway:x:
    * nossaaposta:x:

- Calculates the [Kelly criterion](https://en.wikipedia.org/wiki/Kelly_criterion) to determine the bankroll percentage 
to wager.

### Neural network trainer
The neural network was implemented mostly from scratch in Matlab, although some code snippets were used as provided by 
[Andrew Ng's machine learning course](https://www.coursera.org/learn/machine-learning).

Very briefly, the current implementation includes:
* Data preprocessing (feature normalization, _etc._);
* Batch normalization;
* Dropout regularization;
* L2 regularization;
* Adam optimization algorithm;
* A protocol for finding the learning rate based on [this paper by Leslie Smith](https://arxiv.org/abs/1708.07120);
* Leaky ReLu for input and hidden layers, and softmax for output layer activation functions;
* A custom cost function consisting of the typical 
[cross entropy loss function](https://en.wikipedia.org/wiki/Cross_entropy#Cross-entropy_loss_function_and_logistic_regression)
, but each match's outcome is weighted differently by multiplying the Kelly criterion for that outcome.
* A diagnostic protocol to evaluate the model.

<sup>A lot of these features are overkill for this application, where a medium sized dataset was used.
Again, this was made for the sake of learning, not necessarily to save time or have the best performance ever.</sup>

