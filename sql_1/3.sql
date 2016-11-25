/*
 *  Вывести столицу Малайзии (Malaysia) (в выводе: только название города). (0,5 баллов)
 */

select City.Name
from Capital
    join Country
        on Capital.CountryCode = Country.Code
    join City
        on City.Id = Capital.CityId
where Country.Name = "Malaysia";
