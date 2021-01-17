function W = randInitializeWeights(L_in, L_out)
%RANDINITIALIZEWEIGHTS Randomly initialize the weights of a layer with L_in
%incoming connections and L_out outgoing connections
%   W = RANDINITIALIZEWEIGHTS(L_in, L_out) randomly initializes the weights
%   of a layer with L_in incoming connections and L_out outgoing
%   connections.

%epsilon = sqrt(2)/sqrt(L_out+L_in);
epsilon = sqrt(2/L_in);
W = normrnd(0,1,L_out, L_in)  ;

while length(unique(round(W,7)))~=L_in*L_out
    W = normrnd(0,1,L_out, L_in);
end
W = W .* epsilon;

end
