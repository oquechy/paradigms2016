import Prelude hiding (lookup)

-- Реализовать двоичное дерево поиска без балансировки (4 балла)
data BinaryTree k v = Empty | Tree k v (BinaryTree k v) (BinaryTree k v) deriving Show
                                              
-- “Ord k =>” требует, чтобы элементы типа k можно было сравнивать 
lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup _ Empty = Nothing
lookup key (Tree k v l r)       | key == k = Just v
                                | key > k = lookup key r
                                | otherwise = lookup key l

insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v Empty = Tree k v Empty Empty 
insert key value (Tree k v l r) | key == k = Tree k value l r
                                | key > k = Tree k v l (insert key value r)
                                | otherwise = Tree k v (insert key value l) r

delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete _ Empty = Empty
delete key (Tree k v l r)       | key < k = (Tree k v (delete key l) r) 
                                | key > k = (Tree k v l (delete key r))
                                | otherwise = merge l r 

merge :: Ord k => BinaryTree k v -> BinaryTree k v -> BinaryTree k v
merge Empty t = t
merge (Tree k v l r) t = Tree k v l (merge r t)

