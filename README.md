# About

## Predictor
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

## Neural network trainer
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

