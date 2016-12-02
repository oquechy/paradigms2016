/*
Названия стран, у которых столица - не самый многочисленный город.
 Если для страны не задан ни один город, то выводить ее не нужно.
  Вывод должен быть отсортирован в порядке уменьшения плотности
   населения страны, при равной плотности в лексикографическом порядке 
   (вывод: название страны, население страны, площадь страны) (1,25 балла)
*/


select Country.Name, Country.Population, Country.SurfaceArea
from Country inner join Capital on Country.Code = Capital.CountryCode 
             inner join City on Country.Code = City.CountryCode
group by Country.Code
having (City.Population = max(City.Population)) and (City.Id <> Capital.CityId)
order by (Country.Population / 1.0 * Country.SurfaceArea) desc;


