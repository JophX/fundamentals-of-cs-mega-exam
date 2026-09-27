module Pack where

import Prelude hiding (foldr, foldl, map, filter, sum, length, reverse)
import Data.Char (isDigit, digitToInt)

-- @block foldr
foldr :: (a -> b -> b) -> b -> [a] -> b
foldr f acc []     = acc
foldr f acc (x:xs) = f x (foldr f acc xs)
-- @end

-- @block foldl
foldl :: (b -> a -> b) -> b -> [a] -> b
foldl f acc []     = acc
foldl f acc (x:xs) = foldl f (f acc x) xs
-- @end

-- @block map
map :: (a -> b) -> [a] -> [b]
map f []     = []
map f (x:xs) = f x : map f xs
-- @end

-- @block filter
filter :: (a -> Bool) -> [a] -> [a]
filter p []     = []
filter p (x:xs)
  | p x       = x : filter p xs
  | otherwise = filter p xs
-- @end

-- @block sumlen
sum :: [Int] -> Int
sum xs = foldl (+) 0 xs

length :: [a] -> Int
length xs = foldr (\_ n -> n + 1) 0 xs
-- @end

-- @block myRev
myRev :: [a] -> [a]
myRev xs = go xs []
  where
    go []     acc = acc
    go (y:ys) acc = go ys (y : acc)
-- @end

-- @block myRevFold
myRevFold :: [a] -> [a]
myRevFold xs = foldl (\acc x -> x : acc) [] xs
-- @end

-- @block slowRev
slowRev :: [a] -> [a]
slowRev []     = []
slowRev (x:xs) = slowRev xs ++ [x]      -- correct, but O(n^2)!
-- @end

-- @block listToInt
listToInt :: [Int] -> Int
listToInt xs = go xs 0
  where
    go []     acc = acc
    go (d:ds) acc = go ds (acc * 10 + d)
-- @end

-- @block listToIntFold
listToIntFold :: [Int] -> Int
listToIntFold = foldl (\acc d -> acc * 10 + d) 0
-- @end

-- @block strToInt
strToInt :: String -> Int
strToInt s = listToInt (map digitToInt s)
-- @end

-- @block intToList
intToList :: Int -> [Int]
intToList n
  | n < 10    = [n]
  | otherwise = intToList (n `div` 10) ++ [n `mod` 10]
-- @end

-- @block compress
compress :: String -> [(Char, Int)]
compress []     = []
compress (c:cs) = (c, 1 + length same) : compress rest
  where
    same = takeWhile (== c) cs
    rest = dropWhile (== c) cs
-- @end

-- @block compressAcc
compress2 :: String -> [(Char, Int)]
compress2 []     = []
compress2 (c:cs) = go c 1 cs
  where
    go cur n []     = [(cur, n)]
    go cur n (x:xs)
      | x == cur  = go cur (n + 1) xs
      | otherwise = (cur, n) : go x 1 xs
-- @end

-- @block decompress
decompress :: [(Char, Int)] -> String
decompress []            = []
decompress ((c, n) : ps) = replicate n c ++ decompress ps
-- @end

-- @block decompressNoLib
decompress2 :: [(Char, Int)] -> String
decompress2 []            = []
decompress2 ((c, 0) : ps) = decompress2 ps
decompress2 ((c, n) : ps) = c : decompress2 ((c, n - 1) : ps)
-- @end

-- @block decompressStr
-- "a4b2c3"  ->  "aaaabbccc"   (counts may have several digits: "x12")
decompressStr :: String -> String
decompressStr []     = []
decompressStr (c:cs) = replicate (strToInt digits) c ++ decompressStr rest
  where
    digits = takeWhile isDigit cs
    rest   = dropWhile isDigit cs
-- @end

-- @block fib
fibs :: Int -> [Int]
fibs n = go n 0 1
  where
    go 0 _ _ = []
    go k a b = a : go (k - 1) b (a + b)

fibTail :: Int -> Int          -- the n-th Fibonacci number, tail recursive
fibTail n = go n 0 1
  where
    go 0 a _ = a
    go k a b = go (k - 1) b (a + b)
-- @end

-- @block foobar
foo x y = filter (\w -> x == w) y
bar x y = foldl (\w -> \q -> (if q /= x then w + 1 else w)) 0 y
-- @end
