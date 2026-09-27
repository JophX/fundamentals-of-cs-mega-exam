module Basics where

-- @block first
double :: Int -> Int
double x = x * 2

add :: Int -> Int -> Int
add x y = x + y

isTeen :: Int -> Bool
isTeen age = age >= 13 && age <= 19
-- @end

-- @block guards
grade :: Int -> Char
grade points
  | points >= 90 = 'A'
  | points >= 70 = 'B'
  | points >= 50 = 'C'
  | otherwise    = 'F'
-- @end

-- @block patterns
describe :: [Int] -> String
describe []      = "empty"
describe [x]     = "one element: " ++ show x
describe (x:y:_) = "starts with " ++ show x ++ " and " ++ show y
-- @end

-- @block wherelet
bmi :: Double -> Double -> String
bmi weight height
  | v < 18.5  = "under"
  | v < 25.0  = "normal"
  | otherwise = "over"
  where
    v = weight / (height * height)

cylinder :: Double -> Double -> Double
cylinder r h =
  let side = 2 * pi * r * h
      top  = pi * r * r
  in  side + 2 * top
-- @end

-- @block caseof
sign :: Int -> String
sign n = case compare n 0 of
  LT -> "negative"
  EQ -> "zero"
  GT -> "positive"
-- @end

-- @block tuples
swapPair :: (a, b) -> (b, a)
swapPair (x, y) = (y, x)

minMax :: [Int] -> (Int, Int)
minMax xs = (minimum xs, maximum xs)
-- @end

-- @block recursion
mySum :: [Int] -> Int
mySum []     = 0
mySum (x:xs) = x + mySum xs

myProduct :: [Int] -> Int
myProduct []     = 1
myProduct (x:xs) = x * myProduct xs

myElem :: Eq a => a -> [a] -> Bool
myElem _ []     = False
myElem y (x:xs) = x == y || myElem y xs

myTake :: Int -> [a] -> [a]
myTake 0 _      = []
myTake _ []     = []
myTake n (x:xs) = x : myTake (n - 1) xs

myDrop :: Int -> [a] -> [a]
myDrop 0 xs     = xs
myDrop _ []     = []
myDrop n (_:xs) = myDrop (n - 1) xs

factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)
-- @end

-- @block sorts
insertSorted :: Int -> [Int] -> [Int]
insertSorted x [] = [x]
insertSorted x (y:ys)
  | x <= y    = x : y : ys
  | otherwise = y : insertSorted x ys

insertionSort :: [Int] -> [Int]
insertionSort []     = []
insertionSort (x:xs) = insertSorted x (insertionSort xs)

quicksort :: [Int] -> [Int]
quicksort []     = []
quicksort (p:xs) = quicksort [x | x <- xs, x < p] ++ [p] ++ quicksort [x | x <- xs, x >= p]

merge :: [Int] -> [Int] -> [Int]
merge [] ys = ys
merge xs [] = xs
merge (x:xs) (y:ys)
  | x <= y    = x : merge xs (y:ys)
  | otherwise = y : merge (x:xs) ys

mergeSort :: [Int] -> [Int]
mergeSort []  = []
mergeSort [x] = [x]
mergeSort xs  = merge (mergeSort l) (mergeSort r)
  where (l, r) = splitAt (length xs `div` 2) xs
-- @end
