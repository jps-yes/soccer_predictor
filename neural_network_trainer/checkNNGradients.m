function checkNNGradients(lambda,inputLayerSize,hiddenLayersSize,numLabels,Odds,dropout_prob,lambda2)
%CHECKNNGRADIENTS Creates a small neural network to check the
%backpropagation gradients
%   CHECKNNGRADIENTS(lambda) Creates a small neural network to check the
%   backpropagation gradients, it will output the analytical gradients
%   produced by your backprop code and the numerical gradients (computed
%   using computeNumericalGradient). These two gradient computations should
%   result in very similar values.
%

if ~exist('lambda', 'var') || isempty(lambda)
    lambda = 0;
end


m = 8;

% We generate some 'random' test data
[~,NNparams] =  randTheta(inputLayerSize,hiddenLayersSize,numLabels);

% Reusing debugInitializeWeights to generate X
X  = randInitializeWeights(inputLayerSize , m);
y  = 1 + mod(1:m, numLabels)';
Odds = Odds(1:m,:);

batch_g = 1;
batch_b = 0;
% Short hand for cost function
costFunc = @(p) nnCostFunction(p, inputLayerSize, hiddenLayersSize, ...
    numLabels, X, y, lambda, Odds, dropout_prob,lambda2);

[cost, grad] = costFunc(NNparams);
numgrad = computeNumericalGradient(costFunc, NNparams);

% Visually examine the two gradient computations.  The two columns
% you get should be very similar.
disp([numgrad grad]);
fprintf(['The above two columns you get should be very similar.\n' ...
    '(Left-Your Numerical Gradient, Right-Analytical Gradient)\n\n']);

% Evaluate the norm of the difference between two solutions.
% If you have a correct implementation, and assuming you used EPSILON = 0.0001
% in computeNumericalGradient.m, then diff below should be less than 1e-9
diff = norm(numgrad-grad)/norm(numgrad+grad);

fprintf(['If your backpropagation implementation is correct, then \n' ...
    'the relative difference will be small (less than 1e-9). \n' ...
    '\nRelative Difference: %g\n\n'], diff);


end
