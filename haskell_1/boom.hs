helper::Int -> Int -> [Int] -> Int
helper l k [] = -l -1 
helper l k (x:xs)
    | x == k = 0
    | otherwise = 1 + helper (l + 1) k xs

findK::Int -> [Int] -> Int
findK k xs = helper 0 k xs

numberOfDigits :: Integer -> Int
numberOfDigits x = length $ show x    

sumOfDigits :: Integer -> Integer
sumOfDigits 0 = 0
sumOfDigits x = (x `mod` 10) + sumOfDigits (x `div` 10)

isPal :: Eq x => [x] -> bool
isPal ([]) = True
isPal [a] = True
isPal ([a] ++ _	 ++ [b]) = True && (a == b) 
