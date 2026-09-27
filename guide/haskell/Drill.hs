module Drill where

-- @block d1
countOcc :: Eq a => a -> [a] -> Int
countOcc _ [] = 0
countOcc y (x:xs)
  | x == y    = 1 + countOcc y xs
  | otherwise = countOcc y xs
-- @end

-- @block d2
myLength :: [a] -> Int
myLength xs = go xs 0
  where
    go []     acc = acc
    go (_:ys) acc = go ys (acc + 1)
-- @end

-- @block d3
mapF :: (a -> b) -> [a] -> [b]
mapF f xs = foldr (\x acc -> f x : acc) [] xs

filterF :: (a -> Bool) -> [a] -> [a]
filterF p xs = foldr (\x acc -> if p x then x : acc else acc) [] xs
-- @end

-- @block d4
sumSqOdd :: [Int] -> Int
sumSqOdd xs = foldl (+) 0 (map (\x -> x * x) (filter odd xs))
-- @end

-- @block d5
myLast :: [a] -> a
myLast [x]    = x
myLast (_:xs) = myLast xs

myMaximum :: [Int] -> Int
myMaximum [x]    = x
myMaximum (x:xs) = max x (myMaximum xs)

elemAt :: [a] -> Int -> a
elemAt (x:_)  0 = x
elemAt (_:xs) n = elemAt xs (n - 1)
-- @end

-- @block d6
isPal :: Eq a => [a] -> Bool
isPal xs = xs == rev xs []
  where
    rev []     acc = acc
    rev (y:ys) acc = rev ys (y : acc)
-- @end

-- @block d7
dedup :: Eq a => [a] -> [a]
dedup (x:y:rest)
  | x == y    = dedup (y : rest)
  | otherwise = x : dedup (y : rest)
dedup xs = xs           -- 0 or 1 element left
-- @end

-- @block d8
myZip :: [a] -> [b] -> [(a, b)]
myZip (x:xs) (y:ys) = (x, y) : myZip xs ys
myZip _      _      = []

myAppend :: [a] -> [a] -> [a]
myAppend []     ys = ys
myAppend (x:xs) ys = x : myAppend xs ys
-- @end

-- @block d9
myReplicate :: Int -> a -> [a]
myReplicate 0 _ = []
myReplicate n x = x : myReplicate (n - 1) x
-- @end
