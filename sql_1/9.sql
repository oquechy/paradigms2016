/*
Вывести интервалы (начальный год, конечный год, название страны, 
среднегодовой прирост (уровень грамотности в конечный год -
 уровень грамотности в начальный год) / (конечный год - начальный год)) 
 в порядке убывания среднегодового прироста процента грамотных людей,
  интервалы с равным приростом выводить можно в любом порядке.
   Если для страны есть несколько показаний уровня грамотности,
    например, за 1990, 1991 и 2001 год, то для нее в выводе должно быть 2 интервала 
    1990-1991 и 1991-2001 (1,25 балла).

*/

select First.Year, Second.Year, Country.Name, ((Second.Rate - First.Rate) / (Second.Year - First.Year)) as Inc
from LiteracyRate First inner join LiteracyRate Second on First.CountryCode = Second.CountryCode
                        inner join Country on First.CountryCode = Country.Code
where (Second.Year - First.Year > 0)
group by First.CountryCode, First.Year
    having (Second.Year - First.Year = min(Second.Year - First.Year))
order by Inc desc;

