foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' _ z [] = z
foldl' f z (x:xs) = foldl' f (f z x) xs

foldr' :: (b -> a -> a) -> a -> [b] -> a
foldr' _ z []     = z
foldr' f z (x:xs) = f x (foldr' f z xs)

reverse' xs = foldl' (flip (:)) [] xs
foldl'' f z xs = foldr' (\x a acc -> a (f acc x)) id xs z

-- simple examples of foldr recursive patterns
sum'     = foldr' (+) 0
product' = foldr' (*) 1

and' :: [Bool] -> Bool
and'     = foldr' (&&) True

or' :: [Bool] -> Bool
or'      = foldr' (||) False

length' :: [a] -> Int
length'  = foldr' (\x y -> y + 1)  0

bin2int :: [Int] -> Int
bin2int  = foldl' (\x y -> x * 2 + y) 0

map' f   = foldr' (\x y -> (f x) : y) []

