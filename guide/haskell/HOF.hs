module HOF where

-- @block apply
applyTwice :: (a -> a) -> a -> a
applyTwice f x = f (f x)
-- @end

-- @block curry
add3 :: Int -> Int -> Int -> Int
add3 x y z = x + y + z

addFive :: Int -> Int
addFive = (+ 5)
-- @end

-- @block zipWith
myZipWith :: (a -> b -> c) -> [a] -> [b] -> [c]
myZipWith f (x:xs) (y:ys) = f x y : myZipWith f xs ys
myZipWith _ _      _      = []

myTakeWhile :: (a -> Bool) -> [a] -> [a]
myTakeWhile _ [] = []
myTakeWhile p (x:xs)
  | p x       = x : myTakeWhile p xs
  | otherwise = []
-- @end

-- @block compose
countLongWords :: String -> Int
countLongWords = length . filter (\w -> length w > 3) . words
-- @end

-- @block pipeline
sumOfSquaresOfEvens :: [Int] -> Int
sumOfSquaresOfEvens xs = sum (map (^ 2) (filter even xs))
-- @end
