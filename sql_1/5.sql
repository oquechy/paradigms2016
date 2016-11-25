/*Вывести форму правления с максимальной суммарной площадью стран,
 которые ее придерживаются (вывод: форма правления и суммарная площадь).
  (0,25 баллов)
*/

select GovernmentForm, max(Surface) from 
    (select GovernmentForm, sum(SurfaceArea) as Surface
    from Country
    group by GovernmentForm);

