index :: Int -> [Int] -> Int
index k [] = -1
index k k:_ = 1
index k x:xs = 1 + index k xs  
