/*
Вывести названия 20 городов с самым большим процентом от населения 
страны в порядке убывания процента. В случае равенства процентов,
отсортировать города в порядке обратном лексикографическому 
(вывод: название города, его население, население страны).
 (0,5 баллов)
*/

select City.Name, City.Population, Country.Population
from City left outer join Country on City.CountryCode = Country.Code
order by (100.0 * City.Population / Country.Population) desc, City.Name desc
limit 20;
