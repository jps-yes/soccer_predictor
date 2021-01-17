function [X,Y] = importExcelData(filename)
disp('Reading File...');
data = readtable(filename);


% READS STRING PARAMATERS
X = [data.spi1 data.spi2 data.prob1 data.prob2 data.probtie data.oddsW1 data.oddsW2 data.oddsTie data.proj_score1 data.proj_score2 data.importance1 data.importance2 data.capacity data.stadiumLat data.stadiumLon data.distance data.matchDay data.matchMonth data.matchYear data.date data.dayOfYear data.dayOfWeek data.numberBookmarkers data.matchTime data.league1 data.league2 data.league3 data.league4 data.league5 data.league6 data.league7 data.league8 data.league9 data.league10 data.league11 data.league12 data.league13 data.league14 data.league15 data.league16 data.league17 data.league18 data.league19 data.league20 data.league21 data.league22 data.league23 data.league24 data.league25 data.league26 data.league27 data.league28 data.league29 data.league30 data.league31 data.league32 data.league33 data.league34 data.league35 data.league36 data.league37 data.league38];
X = str2double(strrep(X,',','.')); % converts to double

% READS Y
Y = str2double([data.win1 data.win2 data.tie]);
disp('Data loaded successfully.');
end