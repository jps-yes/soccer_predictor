function [score] = betDiagnostic2(prob, probTest, OddsTest, yTest,red)
%red = 0; % comment this
probTest = probTest *  0.7;
prob = prob * red;
bankrollNN = 333;
bankrollTest = 333;
% Unroll Y
Y = [];
for i = 1:3
    Y = [Y yTest==i];
end
% split into subvectors of 32 length
probCell = cell(floor(length(prob)/16),1);
probTestCell = cell(floor(length(prob)/16),1);
oddsCell = cell(floor(length(prob)/16),1);
yCell = cell(floor(length(prob)/16),1);
j = 1;
for i = 1:16:length(prob)-16
    probCell{j} = [prob(i:i+15,1); prob(i:i+15,2); prob(i:i+15,3)];
    probTestCell{j} = [probTest(i:i+15,1); probTest(i:i+15,2);probTest(i:i+15,3)];
    oddsCell{j} = [OddsTest(i:i+15,1); OddsTest(i:i+15,2); OddsTest(i:i+15,3)];
    yCell{j} = [Y(i:i+15,1); Y(i:i+15,2); Y(i:i+15,3)];
    j = j+1;
end
fig=figure();
hold on;
for i = 1:length(probCell)-1
    pause(0.00000000001);
    plot(i,bankrollNN,'ro',i,bankrollTest,'go')
    fractionNN = probCell{i} - (1-probCell{i})./(oddsCell{i}-1);
    sumNN = closestBet(fractionNN * bankrollNN);
    if bankrollNN<1
        sumNN(sumNN>0) = 0;
    else
        while (sum(sumNN)>bankrollNN)
            sumNN(sumNN>bankrollNN) = bankrollNN;
            sumNN = closestBet(sumNN);
            sumNN(fractionNN==min(fractionNN(sumNN>0))) = 0;
        end
    end
    bankrollNN = bankrollNN - sum(sumNN);
    bankrollNN = bankrollNN + sum(sumNN.*oddsCell{i}.*yCell{i});
    
    fractionTest = probTestCell{i} - (1-probTestCell{i})./(oddsCell{i}-1);
    sumTest = closestBet(fractionTest * bankrollTest);
    if bankrollTest<1
        sumTest(sumTest>0) = 0;
    else
        while (sum(sumTest)>bankrollTest)
            sumTest(sumTest>bankrollTest) = bankrollTest;
            sumTest = closestBet(sumTest);
            sumTest(fractionTest==min(fractionTest(sumTest>0))) = 0;
        end
    end
    bankrollTest = bankrollTest - sum(sumTest);
    bankrollTest = bankrollTest + sum(sumTest.*oddsCell{i}.*yCell{i});
end
bankrollNN = bankrollNN + 1;
bankrollTest = bankrollTest + 1;
score =  1 - harmmean([bankrollNN/333, bankrollNN/bankrollTest]);
pause(0)
close(fig);
end