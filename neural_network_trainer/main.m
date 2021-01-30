%% PROCESSING DATA
% !!!!!!! ADD training_data.xlsx to this directory
if exist('Yoriginal','var') == 0 && exist('Xoriginal','var') == 0
    [Xoriginal,Yoriginal] = importExcelData('training_data.xlsx');
end
X = Xoriginal;
mu = zeros(1,size(X,3));
sigma = zeros(1,size(X,2));
% spi score
X1 = X(:,1:2);
[X1, muTemp, sigmaTemp] = featureNormalize(X1(:));
mu(1:2) = muTemp; sigma(1:2) = sigmaTemp;
% 538 probs
X2 = X(:,3:5);
[X2, muTemp, sigmaTemp] = featureNormalize(X2(:));
mu(3:5) = muTemp; sigma(3:5) = sigmaTemp;
% Odds probs
X3 = 1./X(:,6:8);
Odds = X(:,6:8);
[X3, muTemp, sigmaTemp] = featureNormalize(X3(:));
mu(6:8) = muTemp; sigma(6:8) = sigmaTemp;
% proj scores
X4 = X(:,9:10);
[X4, muTemp, sigmaTemp] = featureNormalize(X4(:));
mu(9:10) = muTemp; sigma(9:10) = sigmaTemp;
% importance scores
X5 = X(:,11:12);
[X5, muTemp, sigmaTemp] = featureNormalize(X5(:));
mu(11:12) = muTemp; sigma(11:12) = sigmaTemp;
% Other data
X6 = X(:,13:24);
[X6, muTemp, sigmaTemp] = featureNormalize(X6);
mu(13:24) = muTemp; sigma(13:24) = sigmaTemp;

X7 = X(:,25:62);
% Merge pre-treated data
X = [X1(1:size(X1,1)/2), X1(size(X1,1)/2+1:end), ...
    X2(1:size(X2,1)/3), X2(size(X2,1)/3+1:size(X2,1)*2/3), X2(size(X2,1)*2/3+1:end),...
    X3(1:size(X3,1)/3), X3(size(X3,1)/3+1:size(X3,1)*2/3), X3(size(X3,1)*2/3+1:end),...
    X4(1:size(X4,1)/2), X4(size(X4,1)/2+1:end),...
    X5(1:size(X5,1)/2), X5(size(X5,1)/2+1:end),...
    X6];
%Categorical data
X7 = X7 * mean(std(X));
X = [X, X7];

% Split data in Training, validation and test
Xcopy = X;
OddsCopy = Odds;
desv = 100;
while desv > 9
    [X,Xcv,Xtest,y,yCV,yTest,Odds,OddsCV,OddsTest,order] = splitData(Xcopy,Yoriginal,OddsCopy); % splits data
    desv = sum(std(Xtest)<10^-1)+sum(std(X)<10^-1)+sum(std(Xcv)<10^-1)+ ...
        (sum(std(Xtest)<10^-2)+sum(std(X)<10^-2)+sum(std(Xcv)<10^-2))*2 + ...
        (sum(std(Xtest)<10^-3)+sum(std(X)<10^-3)+sum(std(Xcv)<10^-2))*4;
end

%% SETUP PARAMETERS
% you can edit this variables. Default values are good starting points
x.numLayers = 3; % number of hidden layers
x.nIter = 4; % number if epoch iterations
x.lambda = .1; % lambda for L2 regularization
x.dropout_prob = .0; % dropout probability for dropout regularization
x.layersShape = 1; % shape of network, 1: the number of elements in each layers decreases linearly
x.lambda2 = 100; % this value is summed to kelly criterion weight in the cost function
x.alpha_div = 10; % division constant in automatic alpha finder.
%%
inputLayerSize  = size(X,2);    % number of features
numLabels = size(Yoriginal,2);  % 3 labels, 1-team1 wins, 2-team2 wins, 3-tie
hiddenLayersSize = linspace(inputLayerSize, numLabels,x.numLayers+2).^x.layersShape;
hiddenLayersSize = ((hiddenLayersSize-min(hiddenLayersSize))/(max(hiddenLayersSize)-min(hiddenLayersSize))*(62-3)+3);
hiddenLayersSize = round(hiddenLayersSize);
hiddenLayersSize = hiddenLayersSize(2:end-1);
hiddenLayersSize(hiddenLayersSize<4) = 4;

m = size(X,1);                  % number of training examples
%% Randomize initial weights
[initialTheta,initialNNparams] = randTheta(inputLayerSize,hiddenLayersSize,numLabels);

%% CHECKS IMPLEMENTATION
% checks if backpropagation is correctly implemented
% !!! make sure your dropout probability is set to 0. Otherwise it wont work
checkNNGradients(x.lambda, inputLayerSize, hiddenLayersSize, numLabels, Odds, x.dropout_prob, x.lambda2);
% comment this out if not checking
%% TRAIN NEURAL NETWORK

[NNparams,mu_nn,sigma_nn,alpha_opt] = trainNN(X, y, Xcv, yCV, x.lambda, x.nIter, initialNNparams,...
    inputLayerSize, hiddenLayersSize, numLabels, Odds,OddsCV,x.dropout_prob, x.lambda2, x.alpha_div);
mu_nn{1} = mu;
sigma_nn{1} = sigma;

%% TEST MODEL

[prob, ~] = predict(NNparams, [Xtest; Xcv], inputLayerSize, hiddenLayersSize, numLabels,mu_nn,sigma_nn);

probTest1 = Xtest(:,3:5).* repmat(sigma_nn{1}(3:5),size(Xtest,1),1) + repmat(mu_nn{1}(3:5),size(Xtest,1),1);
probTest2 = Xcv(:,3:5).* repmat(sigma_nn{1}(3:5),size(Xcv,1),1) + repmat(mu_nn{1}(3:5),size(Xcv,1),1);
OddsT = [OddsTest; OddsCV];

yT = [yTest;yCV];
probTest = [probTest1; probTest2] + 1./OddsT;

soma = sum(probTest,2);
probTest(:,1) = probTest(:,1) ./ soma;
probTest(:,2) = probTest(:,2) ./ soma;
probTest(:,3) = probTest(:,3) ./ soma;
red = 1.2;
increment = 0.05;
score = [];
while red>=1
    score = [score betDiagnostic(prob, probTest, OddsT, yT, red)];
    red = red - increment;
    increment = increment/1.3;
end
score_exp = mean(score);

red = 0.8;
increment = 0.05;
score = [];
while red<=.95
    score = [score betDiagnostic2(prob, probTest, OddsT, yT, red)];
    red = red + increment;
    increment = increment/1.45;
end
score_div = mean(score);
score = score_div/4 + score_exp*3/4;
%%
if score < 0.4
    save(['modelnew' num2str(randi(10000))])
end
