function [NNparams,mu_avg,sigma_avg,alpha_opt] = trainNN(X, y,Xcv,yCV,lambda, nIter, initialNNparams,...
    inputLayerSize, hiddenLayersSize, numLabels,Odds,OddsCV,dropout_prob,lambda2,alpha_div)

m = size(X,1);
layers = [inputLayerSize hiddenLayersSize numLabels];

epoch = 0;
t = 1;
NNparams = initialNNparams;

% DIVIDE X, y and Odds in MINI-BATCHES (size=2^10)
batchIndex=0:(2^10):m;
for batch = 1:length(batchIndex)-1
    miniX{batch} = X(batchIndex(batch)+1:batchIndex(batch+1),:);
    miniY{batch} = y(batchIndex(batch)+1:batchIndex(batch+1));
    miniOdds{batch} = Odds(batchIndex(batch)+1:batchIndex(batch+1),:);
end

% Adams algorithm parameters
beta1 = 0.9;
beta2 = 0.999;
Vd = 0;
Sd = 0;
epsilon = 10^(-8);

Javg = 0;
best_J = Inf;
stop = 0;
f = figure();
movegui(f,'northwest');
alpha = 10^(-8);
alpha_opt = 10^(-9);
% FIND OPTIMAL ALPHA
while 1
    ylabel('Cost');
    xlabel('alpha');
    set(gca, 'XScale', 'log')
    xlim([alpha/20 2*alpha]);
    for i = 1:length(miniY)
        alpha = 10^(-8) * (10/10^(-8))^(t/max([min([(nIter*length(miniY)) 400]) 200]));
        [J,grad,~,~] = nnCostFunction(NNparams, inputLayerSize, hiddenLayersSize, numLabels, miniX{i}, miniY{i},lambda,miniOdds{i},dropout_prob,lambda2);
        Javg = Javg * 0.98 + J * (1-0.98);
        Jsmooth = Javg / (1-(0.98^t));
        if t == 100
            firstJ = Jsmooth;
        elseif t < 100
            firstJ = 100;
        end
        plot(alpha,Jsmooth,'ro')
        pause(0.0000001)
        if t > 1 && Jsmooth > (1.5+3*firstJ/100) * best_J
            stop = 1;
            break
        end
        if Jsmooth < best_J && t > 50
            best_J = min([best_J Jsmooth]);
            alpha_opt = alpha/alpha_div;
        end
        % ADAM OPTIMIZATION ALGORITHM
        Vd = beta1 * Vd + (1-beta1) * grad;
        Sd = beta2 * Sd + (1-beta2) * grad.^2;
        Vd_corrected = Vd / (1-(beta1^t));
        Sd_corrected = Sd / (1-(beta2^t));
        
        momentum = Vd_corrected./(sqrt(Sd_corrected)+epsilon);
        NNparams = NNparams - alpha * momentum ;
        t = t+1;
        epoch = epoch + 1/length(miniY);
        hold on
        if isnan(J) || alpha > 1000
            break
        end
    end
    if stop == 1
        break
    end
    if isnan(J) || alpha > 1000
        break
    end
end

if alpha_opt == 10^(-9)
    nIter = 1;
end
alpha = linspace(alpha_opt/10,alpha_opt,floor((nIter+1)*length(miniY)*0.45)-1);
alpha = [alpha linspace(alpha_opt,alpha_opt/10,floor((nIter+1)*length(miniY)*0.45)-1)];
alpha = [alpha linspace(alpha_opt/10,alpha_opt/10000,(nIter+1)*length(miniY)-length(alpha))];
close(f)
%% TRAINING MODEL

% Adams algorithm parameters
beta1 = 0.9;
beta2 = 0.999;
Vd = 0;
Sd = 0;
epsilon = 10^(-8);

t = 1;
epoch = 0;
NNparams = initialNNparams;

% GRADIENT DESCENT
f = figure();
movegui(f,'northwest');
ylabel('Cost');
xlabel('Epoch');
hold on

mu_avg = cell(length(layers),1);
sigma_avg = cell(length(layers),1);
mu_aux = cell(length(layers),1);
sigma_aux = cell(length(layers),1);
for l = 2:length(mu_avg)
    mu_avg{l} = zeros(1,layers(l));
    sigma_avg{l} = zeros(1,layers(l));
    mu_aux{l} = zeros(1,layers(l));
    sigma_aux{l} = zeros(1,layers(l));
end
while epoch <= nIter
    xlim([max([epoch-nIter/10 0]) epoch+1]);
    for i = 1:length(miniY)
        [J,grad,mu,sigma] = nnCostFunction(NNparams, inputLayerSize, hiddenLayersSize, numLabels, miniX{i}, miniY{i},lambda,miniOdds{i},dropout_prob,lambda2);
        for l = 2:length(mu_avg)
            mu_aux{l} = 0.9 * mu_avg{l} + 0.1 * mu{l};
            sigma_aux{l} = 0.9 * sigma_avg{l} + 0.1 * sigma{l};
            mu_avg{l} = mu_aux{l}/(1-(0.9^t));
            sigma_avg{l} = sigma_aux{l}/(1-(0.9^t));
        end
        % ADAM OPTIMIZATION ALGORITHM
        Vd = beta1 * Vd + (1-beta1) * grad;
        Sd = beta2 * Sd + (1-beta2) * grad.^2;
        Vd_corrected = Vd / (1-(beta1^t));
        Sd_corrected = Sd / (1-(beta2^t));
        momentum = Vd_corrected./(sqrt(Sd_corrected)+epsilon);
        NNparams = NNparams - alpha(t) * momentum ;
        t = t+1;
        epoch = epoch + 1/length(miniY);
        [Jcv,~,~,~] = nnCostFunction(NNparams, inputLayerSize, hiddenLayersSize, numLabels, Xcv, yCV,lambda,OddsCV,dropout_prob,lambda2);
        plot(epoch,Jcv,'g.')
        plot(epoch,J,'r.')
        pause(0.0000001)
        if isnan(J)
            break
        end
    end
    if isnan(J)
        break
    end
end
close(f)
end