/*
Для каждой страны вывести ее имя и количество городов-миллионников. 
Отсортировать вывод по убыванию числа городов-миллионников.
 Для стран с равным числом городов - порядок лексикографический.
  Учтите, что в базе данных могут быть страны без городов вообще
   (например, информации о городах нет, или кто-то посчитал Антарктиду страной),
    для таких стран нужно вывести 0 (0,75 баллов).
*/

select Country.Name, count(City.Name)
from Country
    left outer join (select * from City where City.Population >= 1000000) as City
        on Country.Code = City.CountryCode
group by Country.Code
order by count(City.Name) desc, Country.Name;  


