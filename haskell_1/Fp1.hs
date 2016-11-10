module Main where

-- 1. head' возвращает первый элемент непустого списка (0,5 балла)
head' :: [a] -> a
head' (x:_) = x 
-- 2. tail' возвращает список без первого элемента, для пустого - пустой (0,5)
tail' :: [a] -> [a]
tail' [] = []
tail' (_:xs) = xs
-- 3. take' возвращает первые n >= 0 элементов исходного списка (0,5)
take' :: Int -> [a] -> [a]
take' 0 xs = []
take' n (x:xs) = x:take' (n - 1) xs 
-- 4. drop' возвращает список без первых n >= 0 элементов; если n больше длины -- списка, то пустой список. (0,5)
drop' :: Int -> [a] -> [a]
drop' n [] = []
drop' 0 xs = xs
drop' n (_:xs) = drop' (n - 1) xs
-- 5. filter' возвращает список из элементов, для которых f возвращает True (0,5)
filter' :: (a -> Bool) -> [a] -> [a]
filter' f [] = []
filter' f (x:xs) | f x = x:filter' f xs
                 | otherwise = filter' f xs
-- 6. foldl' последовательно применяет функцию f к элементу списка l и значению, полученному на предыдущем шаге, начальное значение z (0,5)
-- foldl' (+) 0 [1, 2, 3] == (((0 + 1) + 2) + 3)   
-- foldl' (*) 4 [] == 4
len' :: [a] -> Int
len' [] = 0
len' (_:xs) = 1 + len' xs

foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' _ z [] = z
foldl' f z (x:xs) = foldl' f (f z x) xs
-- 7. concat' принимает на вход два списка и возвращает их конкатенацию (0,5)
-- concat' [1,2] [3] == [1,2,3]
concat' :: [a] -> [a] -> [a]
concat' [] ys = ys
concat' (x:xs) ys = x:concat' xs ys

-- 8. quickSort' возвращает его отсортированный список (0,5)
quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' xs = concat' sortedle sortedg
                where x = head' xs
                      less = filter' (< x) xs
                      eq = filter' (== x) xs
                      greater = filter' (> x) xs
                      sortedl = quickSort' less
                      sortedle = concat' sortedl eq
                      sortedg = quickSort' greater
