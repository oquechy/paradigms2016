/*
Названия стран в лексикографическом порядке, большинство населения 
которых не проживает в городах (имеются в виду города, информация
 о которых, есть в базе данных), если в базе данных для страны
 нет ни одного города, то ее городское население считается равным 0
  (будьте внимательны, при этом население страны тоже может быть равным 0
, в этом случае выводить такую страну не нужно). (0,5 баллов)

*/

select Country.Name, sum(City.Population), Country.Population
from Country
left outer join City on Country.Code = City.CountryCode
group by Country.Code
having (count(City.Name) = 0 and Country.Population > 0) or (2 * sum(City.Population) < Country.Population) 
order by Country.Name;

