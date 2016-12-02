/*Вывести форму правления с максимальной суммарной площадью стран,
 которые ее придерживаются (вывод: форма правления и суммарная площадь).
  (0,25 баллов)
*/

select GovernmentForm, sum(SurfaceArea)
from Country
group by GovernmentForm
order by sum(SurfaceArea) desc
limit 1;

