function [J, grad, mu, sigma] = nnCostFunction(NNparams, ...
    inputLayerSize, hiddenLayersSize, numLabels, ...
    X, y, lambda, Odds, dropout_prob,lambda2)

% Reshape nn_params back into the parameters Theta matrices
layers = [inputLayerSize hiddenLayersSize numLabels];
Theta = cell(length(layers)-1,1);
for i = 1:length(layers)-1
    Theta{i} = reshape(NNparams(1:layers(i+1) * (layers(i))), ...
        layers(i+1), (layers(i)));
    NNparams = NNparams(layers(i+1) * (layers(i))+1:end);
end

gamma = cell(length(layers)-1,1);
for i = 1:length(layers)-1
    gamma{i+1} = NNparams(1:layers(i+1));
    NNparams = NNparams(layers(i+1)+1:end);
end
beta = cell(length(layers)-1,1);
for i = 1:length(layers)-1
    beta{i+1} = NNparams(1:layers(i+1));
    NNparams = NNparams(layers(i+1)+1:end);
end
% Setup some useful variables
m = size(X, 1);

Y = [];
for i = 1:numLabels
    Y = [Y y==i];
end

%% FORWARD PROP
% Step 1 - feedforward
a = cell(length(layers),1);
z = cell(length(layers),1);
z_norm = cell(length(layers),1);
z_mu = cell(length(layers),1);
mu = cell(length(layers),1);
sigma = cell(length(layers),1);
a{1} = X;
for i = 1:length(layers)-1 
    % APPLIES DROPOUT
    if i ~= 1 && i ~= length(layers)-1
        drop_vector{i} = rand(size(a{i})) > dropout_prob*(layers(i)-3)/(layers(1)-3);
        a{i} = drop_vector{i} .* a{i};
        a{i} = a{i}./(1-dropout_prob*(layers(i)-3)/(layers(1)-3));
    else
        drop_vector{i} = ones(size(a{i}));
    end
    % MULTIPLIES WEIGHTS (THETA)
    z{i+1} = a{i} * Theta{i}';
    
    % BATCH NORMALIZATION
    mu{i+1} = mean(z{i+1}); % calculates mean
    sigma{i+1} = sum((z{i+1}- mu{i+1}).^2)/m; % calculates variance
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

%% COST FUNCTION
%J = 1/m *sum(-sum(   Y .* log(a{end})   ));
f = a{end} - (1-a{end})./(Odds-1) + lambda2;
f = (f>0).*f;
J = 1/m *sum(-sum(   Y.*log(a{end}) .* f   ));

for i = 1:length(layers)-1
    J = J + lambda/2/m * (sum(sum(Theta{i}.^2)));
end

%% BACKPROPAGATION
% Step 2 - calculate lambda

aux_term1 = sum(     (f.*Y)   ,2);
aux_term2 = sum(     (f>0).*(Y.*log(a{end}).*(Odds)./(Odds-1).*a{end})   ,2);
dz_norm{length(layers)} =   (aux_term1.*a{end}-(f.*Y)) - ((f>0).*(Y.*log(a{end}).*(Odds)./(Odds-1).*a{end}) - a{end}.*aux_term2);
%dz_norm{length(layers)} = a{end}-Y;

% batch norm
divar{length(layers)} = sum(z_mu{length(layers)} .* dz_norm{length(layers)});
dz_mu1{length(layers)} = dz_norm{length(layers)} ./ sqrt(sigma{length(layers)}+10^(-8));
dsqrtivar{length(layers)} = divar{length(layers)} * (-1) ./ sqrt(sigma{length(layers)}+10^(-8)).^2;
dvar{length(layers)} = dsqrtivar{length(layers)} * 0.5 ./ sqrt(sigma{length(layers)}+10^(-8));
dsqdiff{length(layers)} = dvar{length(layers)}/m .* ones(m,length(dvar{length(layers)}));
dz_mu2{length(layers)} = dsqdiff{length(layers)} .* 2 .* z_mu{length(layers)};
dz1{length(layers)} = dz_mu1{length(layers)} + dz_mu2{length(layers)};
dmu{length(layers)} = sum(-(dz_mu1{length(layers)} + dz_mu2{length(layers)}));
dz2{length(layers)} = dmu{length(layers)} ./m .* ones(m,length(dmu{length(layers)}));
dz{length(layers)} = dz1{length(layers)} + dz2{length(layers)};
dgamma{length(layers)} = sum(dz_norm{length(layers)} .* z_norm{length(layers)})/m;
dbeta{length(layers)} = sum(dz_norm{length(layers)})/m;

% Step 3 - propagate error
for i = 1:length(layers)-2
    dz_norm{end-i} = (dz{end+1-i} * Theta{end+1-i}) .* ((z{end-i}<=0)*0.01 + (z{end-i}>0));
    %dropout
    dz_norm{end-i} = dz_norm{end-i} .* drop_vector{end-i+1}; 
    % batch norm
    divar{end-i} = sum(z_mu{end-i} .* dz_norm{end-i});
    dz_mu1{end-i} = dz_norm{end-i} ./ sqrt(sigma{end-i}+10^(-8));
    dsqrtivar{end-i} = divar{end-i} * (-1) ./ sqrt(sigma{end-i}+10^(-8)).^2;
    dvar{end-i} = dsqrtivar{end-i} * 0.5 ./ sqrt(sigma{end-i}+10^(-8));
    dsqdiff{end-i} = dvar{end-i}/m .* ones(m,length(dvar{end-i}));
    dz_mu2{end-i} = dsqdiff{end-i} .* 2 .* z_mu{end-i};
    dz1{end-i} = dz_mu1{end-i} + dz_mu2{end-i};
    dmu{end-i} = sum(-(dz_mu1{end-i} + dz_mu2{end-i}));
    dz2{end-i} = dmu{end-i} ./m .* ones(m,length(dmu{end-i}));
    dz{end-i} = dz1{end-i} + dz2{end-i};
    dgamma{end-i} = sum(dz_norm{end-i} .* z_norm{end-i})/m;
    dbeta{end-i} = sum(dz_norm{end-i})/m;
end
% Step 4 - accumulate
Delta = cell(length(layers)-1,1);
for i = 1:length(layers)-1
    Delta{i} = dz{i+1}'*a{i};
end
% Step 5 - scaling
grad = [];
ThetaGrad = cell(length(layers)-1,1);
for i = 1:length(layers)-1
    ThetaGrad{i} = Delta{i}./m;
    ThetaGrad{i} = ThetaGrad{i} + lambda/m * Theta{i};
    grad = [grad ; ThetaGrad{i}(:)]; % Unroll gradients
end
for i = 1:length(layers)-1
    grad = [grad; dgamma{i+1}'];
end
for i = 1:length(layers)-1
    grad = [grad; dbeta{i+1}'];
end
end