function [prob,pred] = predict(NNparams, X, inputLayerSize, hiddenLayersSize, numLabels,mu,sigma)
%PREDICT Predict the label of an input given a trained neural network
%   p = PREDICT(Theta1, Theta2, X) outputs the predicted label of X given the
%   trained weights of a neural network (Theta1, Theta2)

layers = [inputLayerSize hiddenLayersSize numLabels];
m = size(X, 1);
a = cell(length(layers),1);
z = cell(length(layers),1);
z_norm = cell(length(layers),1);
z_mu = cell(length(layers),1);

Theta = cell(length(layers)-1,1);
for i = 1:length(layers)-1
    Theta{i} = reshape(NNparams(1:layers(i+1) * (layers(i))), ...
        layers(i+1), (layers(i)));
    NNparams = NNparams(layers(i+1) * (layers(i))+1:end);
end
gamma = cell(length(layers),1);
for i = 1:length(layers)-1
    gamma{i+1} = NNparams(1:layers(i+1));
    NNparams = NNparams(layers(i+1)+1:end);
end
beta = cell(length(layers),1);
for i = 1:length(layers)-1
    beta{i+1} = NNparams(1:layers(i+1));
    NNparams = NNparams(layers(i+1)+1:end);
end

a{1} = X;
for i = 1:length(layers)-1
    % MULTIPLIES WEIGHTS (THETA)
    z{i+1} = a{i} * Theta{i}';
    
    % BATCH NORMALIZATION
    z_mu{i+1} = (z{i+1} - mu{i+1}); 
    z_norm{i+1} = z_mu{i+1}./sqrt(sigma{i+1} + 10^(-8)); % normalizes z
    z{i+1} =  gamma{i+1}' .* z_norm{i+1} + beta{i+1}';
    
    % ACTIVATION FUNCTION
    if i == length(layers)-1
        % If last layer, applies SOFTMAX
        a{i+1} = softmax(z{i+1});
    else
        % In other layers apply ReLu
        a{i+1} = max(0.01*z{i+1},z{i+1});
    end
end

prob = a{end};
[~, pred] = max(prob, [], 2);

end
