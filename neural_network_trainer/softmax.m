function g = softmax(z)
% Compute softmax functoon
g = exp(z);
soma = sum(g,2);
g(:,1) = g(:,1)./soma;
g(:,2) = g(:,2)./soma;
g(:,3) = g(:,3)./soma;

end
