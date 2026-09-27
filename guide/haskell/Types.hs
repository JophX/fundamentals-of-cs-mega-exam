module Types where

-- @block shape
data Shape = Circle Double | Rect Double Double
  deriving (Show, Eq)

area :: Shape -> Double
area (Circle r) = pi * r * r
area (Rect w h) = w * h
-- @end

-- @block maybe
safeHead :: [a] -> Maybe a
safeHead []    = Nothing
safeHead (x:_) = Just x

safeDiv :: Int -> Int -> Maybe Int
safeDiv _ 0 = Nothing
safeDiv a b = Just (a `div` b)

lookupAge :: String -> [(String, Int)] -> Maybe Int
lookupAge _ [] = Nothing
lookupAge k ((name, age) : rest)
  | k == name = Just age
  | otherwise = lookupAge k rest
-- @end

-- @block list
data List a = Nil | Cons a (List a)
  deriving Show

lenL :: List a -> Int
lenL Nil         = 0
lenL (Cons _ xs) = 1 + lenL xs
-- @end

-- @block tree
data Tree a = Leaf | Node (Tree a) a (Tree a)
  deriving Show

insert :: Ord a => a -> Tree a -> Tree a
insert x Leaf = Node Leaf x Leaf
insert x t@(Node l v r)
  | x < v     = Node (insert x l) v r
  | x > v     = Node l v (insert x r)
  | otherwise = t

member :: Ord a => a -> Tree a -> Bool
member _ Leaf = False
member x (Node l v r)
  | x < v     = member x l
  | x > v     = member x r
  | otherwise = True

inorder :: Tree a -> [a]
inorder Leaf         = []
inorder (Node l v r) = inorder l ++ [v] ++ inorder r

fromList :: Ord a => [a] -> Tree a
fromList = foldr insert Leaf

size :: Tree a -> Int
size Leaf         = 0
size (Node l _ r) = size l + 1 + size r

depth :: Tree a -> Int
depth Leaf         = 0
depth (Node l _ r) = 1 + max (depth l) (depth r)
-- @end

-- @block expr
data Expr = Num Int
          | Add Expr Expr
          | Mul Expr Expr
          | Neg Expr
  deriving Show

eval :: Expr -> Int
eval (Num n)   = n
eval (Add a b) = eval a + eval b
eval (Mul a b) = eval a * eval b
eval (Neg e)   = negate (eval e)
-- @end

-- @block class
class Describable a where
  describe :: a -> String

instance Describable Bool where
  describe True  = "yes"
  describe False = "no"

instance Describable Shape where
  describe (Circle _) = "a round shape"
  describe (Rect _ _) = "a box"
-- @end

-- @block stack
newtype Stack a = Stack [a]

empty :: Stack a
empty = Stack []

push :: a -> Stack a -> Stack a
push x (Stack xs) = Stack (x : xs)

pop :: Stack a -> Maybe (Stack a)
pop (Stack [])     = Nothing
pop (Stack (_:xs)) = Just (Stack xs)

top :: Stack a -> Maybe a
top (Stack [])    = Nothing
top (Stack (x:_)) = Just x

isEmpty :: Stack a -> Bool
isEmpty (Stack xs) = null xs
-- @end

-- @block lazy
naturals :: [Integer]
naturals = [0 ..]

squares :: [Integer]
squares = [n * n | n <- naturals]

fibsLazy :: [Integer]
fibsLazy = 0 : 1 : zipWith (+) fibsLazy (tail fibsLazy)
-- @end
