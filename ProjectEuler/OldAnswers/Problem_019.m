monthDays=[31 28 31 30 31 30 31 31 30 31 30 31];
% Jan 7, 1900 is the first Sunday.
year=1900;
month=1;
day=7;
firstSundays=0;
while year<2001
    day=day+7;
    if day>monthDays(month)
        day=day-monthDays(month);
        month=month+1;
        if month>12
            month=1;
            year=year+1;
            if (mod(year,4)==0&&mod(year,100)~=0)||mod(year,400)==0
                monthDays(2)=29;
            else
                monthDays(2)=28;
            end
        end
        if day==1&&year<2001&&year>1900
            firstSundays=firstSundays+1;
            sprintf('%d/%d/%d',year,month,day)
        end
    end
end
firstSundays