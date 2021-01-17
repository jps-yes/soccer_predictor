function [initialTheta,initialNNparams] = randTheta(inputLayerSize,hiddenLayersSize,numLabels)
% Randomize initial weights
layers = [inputLayerSize hiddenLayersSize numLabels];
initialNNparams = [];
initialTheta = cell(length(layers)-1,1);
for i = 1:length(layers)-1
    initialTheta{i} = randInitializeWeights(layers(i), layers(i+1));
    initialNNparams = [initialNNparams; initialTheta{i}(:)];% Unroll parameters
end
initialNNparams = [initialNNparams; ones(sum(layers(2:end)),1); zeros(sum(layers(2:end)),1)];
end