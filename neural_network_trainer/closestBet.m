function fraction = closestBet(fraction)
    %fraction(fraction>100) = 100;
    %fraction(fraction>75 & fraction<100) = 75;
    %fraction(fraction>50 & fraction<75) = 50;
    %fraction(fraction>20 & fraction<50) = 20;
    %fraction(fraction>10 & fraction<20) = 10;
    %fraction(fraction>5 & fraction<10) = 5;
    %fraction(fraction>2 & fraction<5) = 2;
    %fraction(fraction>1 & fraction<2) = 1;
    fraction(fraction<1) = 0;
    
    fraction = floor(fraction);
end

