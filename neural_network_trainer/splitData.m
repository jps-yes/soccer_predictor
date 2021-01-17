function [X,Xcv,Xtest,y,yCV,yTest,Odds,OddsCV,OddsTest,order] = splitData(Xoriginal,Yoriginal,OddsOriginal)
%shuffles and splits data into training, cross-validation and test matrices

y = zeros(size(Yoriginal,1),1);
for i= 1:size(Yoriginal,2)
    y = y + (Yoriginal(:,i)==1)*i;
end

m = size(Xoriginal,1);
order = randperm(m);

X = Xoriginal(order,:);
y = y(order,:);
Odds = OddsOriginal(order,:);

m = round(size(X,1)*0.70/(2^10))*(2^10);
mTest = round((size(X,1) - m)/2);

Xcv = X(m+1:m+mTest,:);
yCV = y(m+1:m+mTest,:);
OddsCV = Odds(m+1:m+mTest,:);

Xtest = X(m+mTest+1:end,:);
yTest = y(m+mTest+1:end,:);
OddsTest = Odds(m+mTest+1:end,:);

X = X(1:m,:);
y = y(1:m,:);
Odds = Odds(1:m,:);
end